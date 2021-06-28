# containing preprocessing logic
import pandas as pd

from utils import get_binary_columns
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def add_noise(value, binary_noise):
    if value < 0:
        return value + np.random.uniform(0, binary_noise)
    if value > 0:
        return value - np.random.uniform(0, binary_noise)


def scale(x):
    if x < 0:
        return -1
    else:
        return 1


class DataProcessor:
    def __init__(self, dataset):
        self.pandas_dataset = dataset
        self.binary_columns = get_binary_columns(self.pandas_dataset)
        self.sc = None

    def preprocess(self, binary_noise=0.2):
        np_data = self.pandas_dataset.to_numpy()
        self.sc = MinMaxScaler((-1, 1))
        self.sc = self.sc.fit(np_data)
        scaled_data = self.sc.fit_transform(np_data)

        for i in self.binary_columns:
            scaled_data[:, i] = np.array([add_noise(x, binary_noise) for x in scaled_data[:, i]])

        # todo: do data augumentation by adding noise somewhere here
        return scaled_data

    def postprocess(self, data):
        # reverse binary
        for i in self.binary_columns:
            data[:, i] = np.array([scale(x) for x in data[:, i]])

        # reverse min max scaling
        data = pd.DataFrame(self.sc.inverse_transform(data))

        data.columns = self.pandas_dataset.columns
        data.astype(self.pandas_dataset.dtypes)
        return data