from math import sqrt
from datetime import datetime

import pandas as pd


def euclidean_distance_metric(x, y) -> float:
    """
    Returns the euclidean distance between two data instances
    """
    ret = 0.0
    for x_i, y_i in zip(x, y):
        if type(x_i) == pd.Timestamp and type(y_i) == pd.Timestamp:
            ret += abs(x_i - y_i).total_seconds()
        else:
            ret += (x_i - y_i) ** 2

    return sqrt(ret)

