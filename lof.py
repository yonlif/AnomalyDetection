from load_data import data, norm_data, reformat
from utils import euclidean_distance_metric
from sklearn.neighbors import LocalOutlierFactor
from heapq import nsmallest

# Define hyper parameters
K = 5
print(data.head())

# Define detector
clf = LocalOutlierFactor(n_neighbors=20, metric=euclidean_distance_metric)

# Predict outliers
res = clf.fit_predict(norm_data)
# Res is a binary vector (1 or -1) where -1 is an outlier
print(res)
print(f"Number of outliers: {len([_ for _ in res if _ < 0])}, out of: {len(res)}")

# Outlier score: smaller - more outlier
print(clf.negative_outlier_factor_)

# Print all outliers

# for i, cls in enumerate(res):
#     if cls == -1:
#         print(data.iloc[i])

# Print the n most out
n = 5
z = [(x, y[1]) for x, y in zip(clf.negative_outlier_factor_, data.iterrows())]
smallest = nsmallest(n, z, key=lambda x: x[0])
for item in smallest:
    print()
    print(f"Score: {item[0]}")
    print(item[1])
