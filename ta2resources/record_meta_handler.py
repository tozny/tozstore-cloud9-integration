from e3db.types import Record, Search
from psycopg2 import connect
from json import dumps


def run(conn: connect):
    with conn:
        with conn.cursor() as curs:
            curs.execute("insert into fetched_records")

    with conn:
        with conn.cursor() as curs:
            a = curs.execute("select * from fetched_records")

    print(a)


def truncate(conn: connect):
    with conn:
        with conn.cursor() as curs:
            curs.execute("truncate fetched_records")


def insert_record(record: Record, query: Search, conn: connect, s3_bucket: str, s3_location: str):
    # this needs to use e3db fetched records
    with conn:
        with conn.cursor() as curs:
            curs.execute((
                "INSERT INTO fetched_records"
                "   (query_string, record_meta, file_data, record_id, record_id_updated_at, file_name,"
                "   s3_bucket, s3_location)"
                "VALUES "
                "   (%(query_string)s, %(record_meta)s, %(file_data)s, %(record_id)s,"
                "    %(record_id_updated_at)s, %(file_name)s, %(s3_bucket)s, %(s3_location)s)"),
                {'query_string': dumps(query.to_json()), 'record_meta': dumps(record.meta.plain),
                 'file_data': dumps(record.meta.file_meta.to_json()), 'record_id': record.meta.record_id,
                 'record_id_updated_at': record.meta.last_modified, 'file_name': record.meta.file_meta._file_name,
                 's3_bucket': s3_bucket, 's3_location': s3_location})


def fetch_local_s3_url(record: Record, query: Search, conn: connect):
    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT s3_bucket, s3_location FROM fetched_records where record_id = %(record_id)s limit 1",
                         {'record_id': record.meta.record_id})
            response = curs.fetchone()
    if response is not None:
        return True, response
    else:
        return False,


def record_exists(record: Record, conn: connect):
    with conn:
        with conn.cursor() as curs:
            curs.execute((
                "SELECT record_id_updated_at FROM fetched_records WHERE record_id = %(record_id)s"
            ), {'record_id': record.meta.record_id})
            response = curs.fetchone()
    return not (response is None or len(response) == 0)


if __name__ == '__main__':
    context = connect(dbname='ta2', user='postgres', password='postgres', host='localhost')

    truncate(context)
