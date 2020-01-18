import datetime

import pandas as pd
import numpy as np
from sklearn import preprocessing
from pathlib import Path


data_dir = Path("data")
csv_file = data_dir / "clear_nyc_taxi_data.csv"
chunk_size = 100

# Read one chunks to initialize the scale
data = pd.read_csv(csv_file, nrows=chunk_size)
data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'], format='%Y-%m-%d %H:%M:%S').astype(int)
data['dropoff_datetime'] = pd.to_datetime(data['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S').astype(int)

min_max_scalar = preprocessing.MinMaxScaler()
norm_data = min_max_scalar.fit_transform(data)


def data_in_chunks(norm=False):
    i = 0
    while True:
        tmp = pd.read_csv(csv_file, skiprows=i, nrows=chunk_size)
        if tmp.empty:
            break

        tmp['pickup_datetime'] = pd.to_datetime(tmp['pickup_datetime'], format='%Y-%m-%d %H:%M:%S').astype(int)
        tmp['dropoff_datetime'] = pd.to_datetime(tmp['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S').astype(int)
        if norm:
            tmp = min_max_scalar.fit_transform(tmp.values)

        i += chunk_size
        yield tmp


def sliding_window(norm=False):
    """
    Usage example:

    for i, item in enumerate(sliding_window()):
    print(item)
    if i == 3:
        break
    """
    i = chunk_size
    ret = data_in_chunks(norm=norm).__next__()
    while True:
        tmp = pd.read_csv(csv_file, names=ret.columns, skiprows=i+1, nrows=1)
        if tmp.empty:
            break

        tmp['pickup_datetime'] = pd.to_datetime(tmp['pickup_datetime'], format='%Y-%m-%d %H:%M:%S').astype(int)
        tmp['dropoff_datetime'] = pd.to_datetime(tmp['dropoff_datetime'], format='%Y-%m-%d %H:%M:%S').astype(int)
        if norm:
            tmp = min_max_scalar.fit_transform(tmp.values)

        ret = pd.concat([ret, tmp], ignore_index=True)
        i += 1
        yield ret
        ret = ret.drop([0])


def reformat(item):
    # Not working
    item['pickup_datetime'] = datetime.datetime.fromtimestamp(item['pickup_datetime'] // 1000)
    item['dropoff_datetime'] = datetime.datetime.fromtimestamp(item['dropoff_datetime'] // 1000)
    return item
