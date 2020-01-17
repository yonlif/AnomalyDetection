import pandas as pd
from pathlib import Path


data_dir = Path("data")
csv_file = data_dir / "nyc_taxi_data.csv"
output_file = data_dir / "new_nyc_taxi_data.csv"

print(pd.read_csv(csv_file, nrows=1).columns)

cleared_data_frame = pd.read_csv(csv_file,
                                 usecols=['pickup_datetime', 'dropoff_datetime', 'trip_distance', 'pickup_longitude',
                                          'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude',
                                          'fare_amount', 'rate_code'])
print(cleared_data_frame.head())

cleared_data_frame.to_csv(output_file)
