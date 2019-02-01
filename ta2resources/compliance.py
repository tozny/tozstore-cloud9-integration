# MAKE A NOTE HERE THAT BY MODIFYING THIS FILE TO NOT DISPLAY THE WANRING YOU MAY BE BREAKING THE LAW

import os
import time
from compliance_error import ComplianceError
from constants import compliance_message

HOURS = 24
MINUTES = 60
SECONDS = 60
file = 'wash-compliance-timestamp.txt'
COMPLIANCE_MESSAGE = compliance_message


def get_most_recent_check():
    # Verifies that the compliance check has been completed in the past 24
    home = os.path.expanduser('~')
    directory = os.path.join(home, '.compliance')
    if not os.path.exists(directory):
        os.makedirs(directory)

    timestamp_file = "{}/{}".format(directory, file)
    if os.path.isfile(timestamp_file):
        with open(timestamp_file, 'r') as f:
            val = f.readline()
        try:
            last = float(val.strip())
            current = time.time()
            if last > current or (current - last) > SECONDS * MINUTES * HOURS:
                do_compliance_check()
        except ValueError:
            do_compliance_check()
    else:
        do_compliance_check()


def do_compliance_check():
    response = input(COMPLIANCE_MESSAGE)
    if response.lower() != "yes":
        raise ComplianceError()
    home = os.path.expanduser('~')
    directory = os.path.join(home, '.compliance')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open("{}/{}".format(directory, file), 'w') as r:
        r.write(str(time.time()))
    print("Thank you for verifying")
    return True

