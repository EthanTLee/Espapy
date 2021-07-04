from . import splitting_indexes


def split_into_spectral_orders(data):
    split_data = []

    indexes_to_split_at = splitting_indexes.get_splitting_indexes(data['wavelength'])

    for i in range(indexes_to_split_at.size - 1):
        split_data.append(data[indexes_to_split_at[i]:indexes_to_split_at[i+1]])

    return split_data
