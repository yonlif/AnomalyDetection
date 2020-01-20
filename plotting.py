import matplotlib.pyplot as plt
from pathlib import Path
from load_data import data


# box = ((df.longitude.min(),   df.longitude.max(), df.latitude.min(), df.latitude.max())
large_box = (-74.3294, -73.6578, 40.9182, 40.5681)
small_box = (-74.0191, -73.9981, 40.7162, 40.7053)

image_path = Path('images') / 'new_york_large.png'
image_large = plt.imread(str(image_path))

image_path = Path('images') / 'new_york_small.png'
image_small = plt.imread(str(image_path))


def plot_df(df, large=False):
    print("Plotting")
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.scatter(df.dropoff_longitude, df.dropoff_latitude, zorder=1, alpha=1, c='b', s=10, label='drop')
    ax.scatter(df.pickup_longitude, df.pickup_latitude, zorder=1, alpha=1, c='r', s=10, label='pick')
    ax.legend()
    ax.set_title('Plotting Spatial Data on New York Map')
    if large:
        ax.set_xlim(large_box[0], large_box[1])
        ax.set_ylim(large_box[2], large_box[3])
        ax.imshow(image_large, zorder=0, extent=large_box, aspect='equal')
    else:
        ax.set_xlim(small_box[0], small_box[1])
        ax.set_ylim(small_box[2], small_box[3])
        ax.imshow(image_small, zorder=0, extent=small_box, aspect='equal')


if __name__ == '__main__':
    plot_df(data)
    plt.show()
