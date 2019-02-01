from concurrent.futures import ThreadPoolExecutor, as_completed
from json import loads, load
from os import remove
from typing import List

from boto3 import resource
from e3db import Client
from e3db.types import Search, Record
from psycopg2 import connect, extras

from record_meta_handler import insert_record, record_exists, fetch_local_s3_url


class ClientSupport(object):

    def __init__(
            self, json: dict, s3_bucket: str, db_host: str, db_user: str, db_name: str, db_password: str, threads: int):
        self.client = Client(json)
        self.s3 = resource('s3', endpoint_url=None, aws_access_key_id=None,
                           aws_secret_access_key=None)
        self.bucket_name = s3_bucket
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.host = db_host;
        self.db_user = db_user
        self.db_name = db_name
        self.db_password = db_password
        self.threads = threads
        extras.register_uuid()

    @classmethod
    def from_config(cls, file_location: str):
        with open(file_location, 'r') as f:
            config = load(f)
        keys = {"CLIENT", "S3", "DB_HOST", "DB_PASSWORD", "DB_NAME", "DB_USER", "DOWNLOAD_THREADS"}
        verify_keys(config, keys)
        return cls(
            config["CLIENT"], config["S3"], config["DB_HOST"], config["DB_USER"], config["DB_NAME"],
            config["DB_PASSWORD"], config["DOWNLOAD_THREADS"])

    def search_and_store(self, query: Search, all_results: bool = False, records: List[Record] = None,
                         previous_after: int = 0):
        records = self.search(query, all_results=all_results, records=records, previous_after=previous_after)
        self.store_all_records(query, records)

    def search(
            self,
            query: Search,
            all_results: bool = False,
            records: List[Record] = None,
            previous_after: int = 0) -> List[Record]:

        if records is None:
            records = []
        response = self.client.search(query)
        after = response.after_index
        records.extend(response.records)
        if after:
            if all_results is False:
                user_input = input(('There were more records than configured batch count, current record count is'
                                    ' {record_count}.\n\n'
                                    'To retrieve another batch before storing type: "next"\n'
                                    'To retrieve all batches before storing (this can cause very long load times) '
                                    'type: "all"\n'
                                    'To store all retrieved batches type: "store" (or any other response)\n'
                                    'Current after index is {after_index}\n').format(after_index=after,
                                                                                     record_count=len(records)))
                if user_input.lower() == "next":
                    print("get next")
                    query.after_index = after
                    self.search(query, records=records, previous_after=after, all_results=False)
                elif user_input.lower() == "all":
                    query.after_index = after
                    self.search(query, records=records, previous_after=after, all_results=True)
            else:
                query.after_index = after
                self.search(query, records=records, previous_after=after, all_results=True)
                print("get all")
        return records

    def store_all_records(self, query: Search, records: List[Record]) -> bool:
        # loop through all records
        context = connect(dbname=self.db_name, user=self.db_user, password=self.db_password, host=self.host)
        records_left = len(records)
        mbsleft = sum([i.meta.file_meta._size for i in records if is_file_record(i)])

        print("Fetching {} records, with a total of {} of data".format(records_left, to_data_size(mbsleft)))
        confirm = input("Do you want to fetch files [Y/n]?\n")

        if not confirm.lower().startswith('y'):
            raise KeyboardInterrupt("Downloaded cancelled by user input")

        with ThreadPoolExecutor(self.threads) as executor:
            f = [
                executor.submit(self.fetch_and_increment_record, context, mbsleft, query, r, records_left - e)
                for (e, r) in enumerate(records)]

            for future in as_completed(f):
                future.result()

        print("Successfully fetched all records ")
        context.close()

    def fetch_and_increment_record(self, context, mbsleft, query, r, records_left):
        self.store_record(query, r, context)
        if is_file_record(r):
            mbsleft -= r.meta.file_meta._size
        records_left -= 1
        if records_left != 0:
            print("{} records remaining".format(records_left))

    def store_record(self, query: Search, record: Record, conn):
        record_id = record.meta.record_id
        if not is_file_record(record):
            # This means that the record is not a file and therefore should not be included
            print("Not fetching, record {} it is not a file record and is not supported at this time".format(record_id))
            return
        # determine if they are in postgres, with a matching timestamp
        exists = record_exists(record, conn)
        # if they are not add a new row to postgres
        local_s3 = None
        if exists:
            local_s3 = fetch_local_s3_url(record, query, conn)
            print("Record exists in s3 no need to re-fetch")
        # retrieve file from e3db
        if not exists or not local_s3:
            temp_file = "{}-temp".format(record_id)
            self.client.read_file(record_id, temp_file)
            object_location = "{}-s3".format(record_id)
            self.bucket.upload_file(temp_file, object_location)
            remove(temp_file)
            bucket_name = self.bucket_name
        else:
            bucket_name = local_s3[1][0]
            object_location = local_s3[1][1]

        insert_record(record, query, conn, bucket_name, object_location)


def verify_keys(config, keys):
    missing = keys.difference(config.keys())
    if missing:
        raise KeyError("{} must be present in the config".format(missing))


def to_data_size(bytes: float):
    size = [(0, 1000, 'bytes'),
            (1000, 1000000, 'Kbs'),
            (1000000, 1000000000, 'Mbs'),
            (1000000000, 1000000000000, 'Gbs')]
    for i in size:
        if i[0] < bytes < i[1]:
            return "{} {}".format(bytes / i[0], i[2])


def is_file_record(record: Record):
    return record.meta.file_meta is not None
