from . import splitting_indexes
from . import spectral_order


def split_into_spectral_orders(whole_data):
    spectral_orders = []

    indexes_to_split_at = splitting_indexes.get_splitting_indexes(whole_data['wavelength'])

    for i in range(indexes_to_split_at.size - 1):
        order = spectral_order.SpectralOrder(whole_data[indexes_to_split_at[i]:indexes_to_split_at[i + 1]])
        spectral_orders.append(order)

    return spectral_orders
