class ComplianceError(Exception):
    def __init__(self):
        print("You must accept the terms of use before using this script and every 24 hours following")
        Exception.__init__(self, "You must accept the terms of use before using this script and every 24 hours following")
