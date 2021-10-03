from datetime import datetime


def iso_timestamp_to_days(timestamp):
    #    print(timestamp)
    return (datetime.now() - datetime.fromisoformat(timestamp)).days
