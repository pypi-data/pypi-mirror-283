import os
from datetime import datetime, timedelta


def filter_by_type(directory, file_type):
    return [f for f in os.listdir(directory) if f.endswith(file_type)]


def filter_by_size(directory, min_size, max_size):
    return [
        f
        for f in os.listdir(directory)
        if min_size <= os.path.getsize(os.path.join(directory, f)) <= max_size
    ]


def filter_by_date_modified(directory, days):
    cutoff = datetime.now() - timedelta(days=days)
    return [
        f
        for f in os.listdir(directory)
        if datetime.fromtimestamp(os.path.getmtime(os.path.join(directory, f))) > cutoff
    ]
