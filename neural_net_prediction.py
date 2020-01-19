from load_data import data, norm_data, reformat, data_generator
from sklearn.neural_network import MLPRegressor
from tqdm import tqdm
from pathlib import Path
from datetime import datetime


NUMBER_OF_ANOMALIES = 100

x = norm_data[:, :-1]
y = norm_data[:, -1]
print("fare amount distribution over first window:")
print(data.iloc[:, -1].describe())


regressor = MLPRegressor()

# Initial training
regressor.fit(x, y)
predictions = regressor.predict(x)
print(len(predictions))
smallest = [(i, -abs(a[0] - a[1])) for i, a in enumerate(zip(predictions, y))]

# Next: use partial_fit in order to iterate over all the data and update the model as we go

for index, item in tqdm(enumerate(data_generator(start_from=100, norm=True))):
    prediction = regressor.predict(item[:, :-1])
    regressor.partial_fit(item[:, :-1], item[:, -1])
    score = -abs(prediction - item[:, -1])
    if score < smallest[-1][1]:
        smallest.append((index + 1024, score))
        smallest = sorted(smallest, key=lambda _: _[1])[:NUMBER_OF_ANOMALIES]
    if index == 10000:
        break


log_path = Path("run_log") / f"{datetime.now().strftime('%d.%m.%Y_%H:%M:%S')}"
print(log_path)
with open(log_path, 'w') as f:
    for item in smallest:
        f.write(str(item[0]))
        f.write('\n')
