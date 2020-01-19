import datetime

import pandas as pd
import numpy as np
import datetime as dt
from sklearn import preprocessing
from sklearn.utils.validation import _assert_all_finite
from pathlib import Path


data_dir = Path("data")
csv_file = data_dir / "clear_nyc_taxi_data.csv"
chunk_size = 100


def data_in_chunks(norm=False):
    i = 0
    while True:
        tmp = pd.read_csv(csv_file, skiprows=i, nrows=chunk_size)
        if tmp.empty:
            break

        tmp = format_data(tmp, norm=norm)

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
    ret = next(data_in_chunks(norm=norm))
    while True:
        tmp = pd.read_csv(csv_file, names=ret.columns, skiprows=i+1, nrows=1)
        if tmp.empty:
            break
        tmp = format_data(tmp, norm=norm)

        ret = pd.concat([ret, tmp], ignore_index=True)
        i += 1
        yield ret
        ret = ret.drop([0])


def data_generator(start_from=0, norm=False):
    i = start_from + 1
    ret = format_data(pd.read_csv(csv_file,names=data.columns, skiprows=i, nrows=1), norm=norm)
    while True:
        if not np.isnan(ret).any():
            yield ret
        else:
            print(f"falied to read line: {i}")
        tmp = pd.read_csv(csv_file, names=data.columns, skiprows=i+1, nrows=1)
        if tmp.empty:
            break
        ret = format_data(tmp, norm=norm)
        i += 1


def format_data(items, norm=False):
    # Adding 2 hours to date for some reason
    items.drop(['Unnamed: 0'], axis=1, inplace=True, errors='ignore')
    items['pickup_datetime'] = pd.to_datetime(items['pickup_datetime']).map(lambda x: x.timestamp())
    items['dropoff_datetime'] = pd.to_datetime(items['dropoff_datetime']).map(lambda x: x.timestamp())
    if norm:
        items = min_max_scalar.transform(items.values)
    return items


def reformat(item):
    item['pickup_datetime'] = item['pickup_datetime'].map(lambda x: dt.datetime.fromtimestamp(x))
    item['dropoff_datetime'] = item['dropoff_datetime'].map(lambda x: dt.datetime.fromtimestamp(x))
    return item


# Read one chunks to initialize the scale
data = pd.read_csv(csv_file, nrows=chunk_size)
data = format_data(data)
min_max_scalar = preprocessing.MinMaxScaler()
norm_data = min_max_scalar.fit_transform(data)
