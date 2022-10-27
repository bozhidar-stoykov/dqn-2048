import pandas as pd
import numpy as np

df = pd.read_csv("highest_tile.txt", header=None)
values = df.values[0][1:-1]
values_int = [int(x) for x in values]
print(f"Mean: {np.mean(values_int)}")
print(f"Number of values: {len(values_int)}")

# print the number of unique values per value
for i in np.unique(values_int):
    print(f"{i}: {np.count_nonzero(values_int == i)}")