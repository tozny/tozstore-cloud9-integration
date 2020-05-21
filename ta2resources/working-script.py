from e3db.types import Search

from compliance import get_most_recent_check
from client_creator import ClientSupport
import e3db


def run():

    # DO NOT SHARE THIS WORKSPACE WITH OTHERS IF YOUR CONFIG IS PRESENT
    # DO NOT ADD YOUR CONFIG INTO SOURCE CONTROL

    support = ClientSupport.from_config(
        "/home/ec2-user/environment/tozstore-cloud9-integration/ta2resources/config.json")

    # Construct search query here (The sample query retrieves all records your client can read with the replaced record type)
    # For full examples on the search query see https://github.com/tozny/e3db-python
    q = Search(count=50, include_data=True, include_all_writers=True).match(
        record_type=["<Replace with a record type>"])

    # The simplest approach is to use support.search_and_store(q)
    support.search_and_store(q)

    # If intermediary actions are needed on the records one can also do
    # records = support.search(q)
    # support.store(records)


if __name__ == '__main__':
    # By removing the compliance check you may be violating the law.
    get_most_recent_check()
    run()
