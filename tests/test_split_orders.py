from astropy.io import ascii
from espapy.utils.data_file import order_splitting
import matplotlib.pyplot as plt


def split_array(big_array, indicies_to_split_at):
    component_arrays = []

    for i in range(indicies_to_split_at.size - 1):
        component_arrays.append(big_array[indicies_to_split_at[i]:indicies_to_split_at[i+1]])

    return component_arrays


if __name__ == '__main__':
#    arr = np.array([1, 2, 3, 5, 7, 4, 5, 6, 8])
#    arr_diff = np.diff(arr)
#
#    arr_split_indicies = np.where(arr_diff <= 0)[0] + 1
#    arr_split_indicies = np.insert(arr_split_indicies, 0, 0)
#    arr_split_indicies = np.append(arr_split_indicies, arr.size)
#
#    components = split_array(arr, arr_split_indicies)

    my_data = ascii.read(
        '/Users/peepeepoopoo/Desktop/espapy/tests/1834099in.s',
        format='basic',
        data_start=3 - 1,
        names=["wavelength", "intensity", "error"]
    )

    split_stuff = order_splitting.split_into_spectral_orders(my_data)

    for order in split_stuff:
        plt.plot(order["wavelength"], order["intensity"])
    plt.show()

    print("done")


