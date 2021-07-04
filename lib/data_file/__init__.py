from astropy.io import ascii
from . import header_access
from . import column_names
from . import order_splitting


class DataFile:

    def __init__(self, file_path, file_line_num_of_first_data=3):
        self.header_info = header_access.get_header_info(file_path)

        total_num_columns = self.header_info["num_additional_columns"] + 1
        data_column_names = column_names.generate_column_names(total_num_columns)

        self.whole_data = ascii.read(
            file_path,
            format='basic',
            data_start=file_line_num_of_first_data - 1,
            names=data_column_names
        )

        self.split_data = order_splitting.split_into_spectral_orders(self.whole_data)

    def wavelength_data(self, order_num=None):
        if order_num is None:
            return self.whole_data["wavelength"]
        return self.split_data[order_num]["wavelength"]

    def intensity_data(self, order_num=None):
        if order_num is None:
            return self.whole_data["intensity"]
        return self.split_data[order_num]["intensity"]
