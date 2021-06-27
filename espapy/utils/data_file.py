from astropy.io import ascii


class DataFile:

    def __init__(self, file_path, file_line_num_of_first_data):

        self.data = ascii.read(
            file_path,
            format='basic',
            data_start=file_line_num_of_first_data - 1,
            names=['Wavelength', 'Intensity', 'Error']
        )

    def wavelength_data(self):
        return self.data["Wavelength"]

    def intensity_data(self):
        return self.data["Intensity"]
