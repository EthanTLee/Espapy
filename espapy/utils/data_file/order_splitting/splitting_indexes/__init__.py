import numpy as np
from . import indexes_of_decrease


def get_splitting_indexes(array):
    splitting_indexes = indexes_of_decrease.get_indexes_of_decrease(array)
    splitting_indexes = np.insert(splitting_indexes, 0, 0)
    splitting_indexes = np.append(splitting_indexes, array.size)

    return splitting_indexes
