from lib import set_attributes


class SpectralOrder:
    def __init__(self, order_data):
        self.data = order_data

    def wavelength_data(self):
        return self.data["wavelength"]

    def intensity_data(self):
        return self.data["intensity"]

    def wavelength_domain(self):
        wavelength_min = self.wavelength_data()[0]
        wavelength_max = self.wavelength_data()[-1]
        domain = set_attributes.Domain(wavelength_min, wavelength_max)
        return domain
