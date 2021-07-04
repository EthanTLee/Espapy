import numpy as np


def get_indexes_of_decrease(array):
    indexes = np.where(np.diff(array) <= 0)[0] + 1

    return indexes
