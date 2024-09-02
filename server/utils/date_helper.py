import datetime


def get_utc_timestamp_in_seconds():
    return datetime.datetime.now(datetime.UTC).timestamp()


def get_utc_timestamp():
    return int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
