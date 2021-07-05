import numpy as np


def get_indexes_in_domain(array, domain):
    indexes = np.where((array < domain.maximum) & (array > domain.minimum))[0]
    return indexes
