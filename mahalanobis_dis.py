import numpy as np
from sklearn.covariance import MinCovDet
from heapq import nlargest

from load_data import data, norm_data, reformat


NUMBER_OF_ANOMALIES = 10

robust_cov = MinCovDet().fit(norm_data)
mahal_robust_cov = enumerate(robust_cov.mahalanobis(norm_data))
anomalies = nlargest(NUMBER_OF_ANOMALIES, mahal_robust_cov, key=lambda _: _[1])
print(anomalies)
