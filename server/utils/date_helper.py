import datetime


def get_utc_timestamp():
    return datetime.datetime.now(datetime.UTC).timestamp()
