import numpy as np
import numpy.ma as ma
import colorsys
import matplotlib.pyplot as plt
from astropy.io import ascii
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.signal import find_peaks, peak_prominences


def extract_renamed_orders(file_path):
    def extract_full_renamed_data(file_path: str):
        def extract_full_raw_data(file_path: str):
            full_raw_data = ascii.read(
                file_path,
                format='no_header',
                data_start=2
            )
            return full_raw_data

        def change_col_names(raw_data):
            name_changed_data = raw_data['col1', 'col2']
            name_changed_data['col1'].name = 'wavelength'
            name_changed_data['col2'].name = 'intensity'
            return name_changed_data

        raw_data = extract_full_raw_data(file_path)
        full_renamed_data = change_col_names(raw_data)
        return full_renamed_data

    def split_full_data_into_orders(full_data):
        def split_data_at_wavelength_decrease(full_data):
            def find_indices_of_decrease(array):
                indices = np.where(np.diff(array) <= 0)[0] + 1
                return indices

            def split_data_at_indices(indices, data):
                split_data = [data[0:indices[0]]]
                for i in range(indices.size - 1):
                    order = data[indices[i]:indices[i + 1]]
                    split_data.append(order)
                split_data.append(data[indices[-1]:])
                return split_data

            indices_of_decrease = find_indices_of_decrease(full_data['wavelength'])
            split_data = split_data_at_indices(indices_of_decrease, full_data)
            return split_data

        orders = split_data_at_wavelength_decrease(full_data)
        return orders

    full_renamed_data = extract_full_renamed_data(file_path)
    orders = split_full_data_into_orders(full_renamed_data)
    return orders


def extract_header_info(file_path):

    def get_first_two_lines(file_path):
        file = open(file_path)
        line0 = file.readline()
        line1 = file.readline()
        return line0, line1

    def extract_header_info_from_first_two_lines(first_two_lines):
        class HeaderInfo:
            def __init__(self, title, num_lines, num_dep_cols):
                self.title = title
                self.num_lines = num_lines
                self.num_dep_cols = num_dep_cols

        title = first_two_lines[0].split('\'')[1]
        num_lines = int(first_two_lines[1].split(' ')[1])
        num_dep_cols = int(first_two_lines[1].split(' ')[2])
        header_info = HeaderInfo(title, num_lines, num_dep_cols)
        return header_info

    first_two_lines = get_first_two_lines(file_path)
    header_info = extract_header_info_from_first_two_lines(first_two_lines)
    return header_info


def find_max_in_view_domain(order_datas, view_domain):
    def get_orders_in_view_domain(order_datas, view_domain):
        def check_order_in_view_domain(order):
            def get_order_domain(order):
                order_domain = (np.amin(order['wavelength']), np.amax(order['wavelength']))
                return order_domain

            order_domain = get_order_domain(order)
            return view_domain[0] < order_domain[1] and order_domain[0] < view_domain[1]

        orders_in_view_domain = list(filter(check_order_in_view_domain, order_datas))
        return orders_in_view_domain

    def find_max_per_order_in_view_domain(orders_in_view_domain, view_domain):
        def max_in_view_domain(order):
            def find_max(order, indices_to_search):
                index_of_max = np.argmax(order['intensity'][indices_to_search])
                max_coord_x = order['wavelength'][indices_to_search][index_of_max]
                max_coord_y = order['intensity'][indices_to_search][index_of_max]
                return max_coord_x, max_coord_y

            def get_indices_in_view_domain(order, view_domain):
                return np.where((order['wavelength'] < view_domain[1]) & (order['wavelength'] > view_domain[0]))
            return find_max(order, get_indices_in_view_domain(order, view_domain))
        return list(map(max_in_view_domain, orders_in_view_domain))

    orders_in_view_domain = get_orders_in_view_domain(order_datas, view_domain)
    max_per_order_in_view_domain = find_max_per_order_in_view_domain(orders_in_view_domain, view_domain)
    return max(max_per_order_in_view_domain, key=lambda n: n[1])


def find_min_in_view_domain(order_datas, view_domain):
    def get_orders_in_view_domain(order_datas, view_domain):
        def check_order_in_view_domain(order):
            def get_order_domain(order):
                order_domain = (np.amin(order['wavelength']), np.amax(order['wavelength']))
                return order_domain

            order_domain = get_order_domain(order)
            return view_domain[0] < order_domain[1] and order_domain[0] < view_domain[1]

        orders_in_view_domain = list(filter(check_order_in_view_domain, order_datas))
        return orders_in_view_domain

    def find_min_per_order_in_view_domain(orders_in_view_domain, view_domain):
        def min_in_view_domain(order):
            def find_min(order, indices_to_search):
                index_of_min = np.argmin(order['intensity'][indices_to_search])
                min_coord_x = order['wavelength'][indices_to_search][index_of_min]
                min_coord_y = order['intensity'][indices_to_search][index_of_min]
                return min_coord_x, min_coord_y

            def get_indices_in_view_domain(order, view_domain):
                return np.where((order['wavelength'] < view_domain[1]) & (order['wavelength'] > view_domain[0]))
            return find_min(order, get_indices_in_view_domain(order, view_domain))
        return list(map(min_in_view_domain, orders_in_view_domain))

    orders_in_view_domain = get_orders_in_view_domain(order_datas, view_domain)
    min_per_order_in_view_domain = find_min_per_order_in_view_domain(orders_in_view_domain, view_domain)
    return min(min_per_order_in_view_domain, key=lambda n: n[1])


def find_intersections_with_half_max_of_local_max(order_datas, view_domain, baseline_value):

    def find_order_with_max_in_view_domain(order_datas, view_domain):
        def get_orders_in_view_domain(order_datas, view_domain):
            def check_order_in_view_domain(order):
                def get_order_domain(order):
                    order_domain = (np.amin(order['wavelength']), np.amax(order['wavelength']))
                    return order_domain

                order_domain = get_order_domain(order)
                return view_domain[0] < order_domain[1] and order_domain[0] < view_domain[1]

            orders_in_view_domain = list(filter(check_order_in_view_domain, order_datas))
            return orders_in_view_domain

        def find_max_per_order_in_view_domain(orders_in_view_domain, view_domain):
            def max_in_view_domain(order):
                def find_max(order, indices_to_search):
                    index_of_max = np.argmax(order['intensity'][indices_to_search])
                    max_coord_x = order['wavelength'][indices_to_search][index_of_max]
                    max_coord_y = order['intensity'][indices_to_search][index_of_max]
                    return max_coord_x, max_coord_y

                def get_indices_in_view_domain(order, view_domain):
                    return np.where((order['wavelength'] < view_domain[1]) & (order['wavelength'] > view_domain[0]))

                return find_max(order, get_indices_in_view_domain(order, view_domain))

            return list(map(max_in_view_domain, orders_in_view_domain))

        orders_in_view_domain = get_orders_in_view_domain(order_datas, view_domain)
        max_per_order_in_view_domain = find_max_per_order_in_view_domain(orders_in_view_domain, view_domain)
        index_of_order_containing_max = np.argmax(np.array(max_per_order_in_view_domain), axis=0)[0]
        return orders_in_view_domain[index_of_order_containing_max]

    def find_index_of_max_in_view_domain(order, view_domain):
        data_masked_to_view = ma.masked_where(~((order['wavelength'] < view_domain[1]) & (order['wavelength'] > view_domain[0])), order['intensity'])
        return data_masked_to_view.argmax()

    def find_num_samples_in_view_domain(order, view_domain):
        indices_in_view_domain = np.where((order['wavelength'] < view_domain[1]) & (order['wavelength'] > view_domain[0]))
        return indices_in_view_domain[0].size

    def find_left_and_right_peak_bound_indices(y_data, peak_index, wlen):
        prominences = peak_prominences(y_data, np.array([peak_index]), wlen=wlen)
        return prominences[1][0], prominences[2][0]

    def find_samples_indices_in_view_domain(view_domain, x_data):
        return np.where((x_data < view_domain[1]) & (x_data > view_domain[0]))

    def find_interpolated_function(x_data, y_data):
        return InterpolatedUnivariateSpline(x_data, y_data)

    def find_baseline(y_data, peak_index):
        return y_data[peak_index] - peak_prominences(y_data, np.array([peak_index]))[0][0]

    def find_half_max_value(y_data, baseline_value):
        y_max = np.amax(y_data)
        return (y_max + baseline_value) / 2

    def find_roots_at_half_max(x_data, y_data, half_max_value):
        interpolated_shifted_peak_function = InterpolatedUnivariateSpline(x_data, y_data - half_max_value)
        return interpolated_shifted_peak_function.roots()

    order_with_max_in_view_domain = find_order_with_max_in_view_domain(order_datas, view_domain)
    index_of_max_in_view_domain = find_index_of_max_in_view_domain(order_with_max_in_view_domain, view_domain)
    max_x_pos = order_with_max_in_view_domain['wavelength'][index_of_max_in_view_domain]
    max_y_pos = order_with_max_in_view_domain['intensity'][index_of_max_in_view_domain]
    samples_in_view_domain = find_samples_indices_in_view_domain(view_domain, order_with_max_in_view_domain['wavelength'])
    baseline = baseline_value
    half_max_value = find_half_max_value(order_with_max_in_view_domain['intensity'][samples_in_view_domain], baseline)
    roots_at_half_max = find_roots_at_half_max(order_with_max_in_view_domain['wavelength'][samples_in_view_domain], order_with_max_in_view_domain['intensity'][samples_in_view_domain], half_max_value)
    interpolated_function = find_interpolated_function(order_with_max_in_view_domain['wavelength'][samples_in_view_domain], order_with_max_in_view_domain['intensity'][samples_in_view_domain])
    return np.array([roots_at_half_max[0], interpolated_function(roots_at_half_max[0])]), np.array([roots_at_half_max[-1], interpolated_function(roots_at_half_max[-1])])



def find_intersections_with_half_min_of_local_min(order_datas, view_domain, baseline_value):

    def find_order_with_max_in_view_domain(order_datas, view_domain):
        def get_orders_in_view_domain(order_datas, view_domain):
            def check_order_in_view_domain(order):
                def get_order_domain(order):
                    order_domain = (np.amin(order['wavelength']), np.amax(order['wavelength']))
                    return order_domain

                order_domain = get_order_domain(order)
                return view_domain[0] < order_domain[1] and order_domain[0] < view_domain[1]

            orders_in_view_domain = list(filter(check_order_in_view_domain, order_datas))
            return orders_in_view_domain

        def find_max_per_order_in_view_domain(orders_in_view_domain, view_domain):
            def max_in_view_domain(order):
                def find_max(order, indices_to_search):
                    index_of_max = np.argmin(order['intensity'][indices_to_search])
                    max_coord_x = order['wavelength'][indices_to_search][index_of_max]
                    max_coord_y = order['intensity'][indices_to_search][index_of_max]
                    return max_coord_x, max_coord_y

                def get_indices_in_view_domain(order, view_domain):
                    return np.where((order['wavelength'] < view_domain[1]) & (order['wavelength'] > view_domain[0]))

                return find_max(order, get_indices_in_view_domain(order, view_domain))

            return list(map(max_in_view_domain, orders_in_view_domain))

        orders_in_view_domain = get_orders_in_view_domain(order_datas, view_domain)
        max_per_order_in_view_domain = find_max_per_order_in_view_domain(orders_in_view_domain, view_domain)
        index_of_order_containing_max = np.argmin(np.array(max_per_order_in_view_domain), axis=0)[0]
        return orders_in_view_domain[index_of_order_containing_max]

    def find_index_of_max_in_view_domain(order, view_domain):
        data_masked_to_view = ma.masked_where(~((order['wavelength'] < view_domain[1]) & (order['wavelength'] > view_domain[0])), order['intensity'])
        return data_masked_to_view.argmin()

    def find_num_samples_in_view_domain(order, view_domain):
        indices_in_view_domain = np.where((order['wavelength'] < view_domain[1]) & (order['wavelength'] > view_domain[0]))
        return indices_in_view_domain[0].size

    def find_left_and_right_peak_bound_indices(y_data, peak_index, wlen):
        prominences = peak_prominences(y_data, np.array([peak_index]), wlen=wlen)
        return prominences[1][0], prominences[2][0]

    def find_samples_indices_in_view_domain(view_domain, x_data):
        return np.where((x_data < view_domain[1]) & (x_data > view_domain[0]))

    def find_interpolated_function(x_data, y_data):
        return InterpolatedUnivariateSpline(x_data, y_data)

    def find_baseline(y_data, peak_index):
        return y_data[peak_index] - peak_prominences(y_data, np.array([peak_index]))[0][0]

    def find_half_max_value(y_data, baseline_value):
        y_max = np.amin(y_data)
        return (y_max + baseline_value) / 2

    def find_roots_at_half_max(x_data, y_data, half_max_value):
        interpolated_shifted_peak_function = InterpolatedUnivariateSpline(x_data, y_data - half_max_value)
        return interpolated_shifted_peak_function.roots()

    order_with_max_in_view_domain = find_order_with_max_in_view_domain(order_datas, view_domain)
    index_of_max_in_view_domain = find_index_of_max_in_view_domain(order_with_max_in_view_domain, view_domain)
    max_x_pos = order_with_max_in_view_domain['wavelength'][index_of_max_in_view_domain]
    max_y_pos = order_with_max_in_view_domain['intensity'][index_of_max_in_view_domain]
    samples_in_view_domain = find_samples_indices_in_view_domain(view_domain, order_with_max_in_view_domain['wavelength'])
    baseline = baseline_value
    half_max_value = find_half_max_value(order_with_max_in_view_domain['intensity'][samples_in_view_domain], baseline)
    roots_at_half_max = find_roots_at_half_max(order_with_max_in_view_domain['wavelength'][samples_in_view_domain], order_with_max_in_view_domain['intensity'][samples_in_view_domain], half_max_value)
    interpolated_function = find_interpolated_function(order_with_max_in_view_domain['wavelength'][samples_in_view_domain], order_with_max_in_view_domain['intensity'][samples_in_view_domain])
    return np.array([roots_at_half_max[0], interpolated_function(roots_at_half_max[0])]), np.array([roots_at_half_max[-1], interpolated_function(roots_at_half_max[-1])])





def test_peak_prominences():

    x = np.array([4,1,2,3,4,6,4,2,1,3,2])
    print(x - 1)
    print(x)
    peaks = np.array([5])
    prominences = peak_prominences(x, peaks)
    print(prominences)
    plt.plot(x)
    plt.show()


if __name__ == '__main__':
    test_peak_prominences()





