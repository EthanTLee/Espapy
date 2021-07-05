import numpy as np
from lib import set_attributes


def get_max_intensity_in_domain(spectral_order, domain):

    def get_intensities_in_domain(spectral_order, domain):

        def get_indexes_in_domain(array, domain):
            indexes = np.where((array < domain.maximum) & (array > domain.minimum))[0]
            return indexes

        intensity_indexes_in_domain = get_indexes_in_domain(spectral_order.intensity_data(), domain)
        intensities = spectral_order.intensity_data()[intensity_indexes_in_domain]

        return intensities

    intensities_in_domain = get_intensities_in_domain(spectral_order, domain)
    max_intensity_in_domain = np.amax(intensities_in_domain)

    return max_intensity_in_domain


def get_spectral_orders_in_domain(datafile, domain):
    orders_in_domain = []

    for order in datafile.spectral_orders:
        if overlaps(order.wavelength_domain(), domain):
            orders_in_domain.append(order)

    return orders_in_domain


def overlaps(domain1, domain2):
    return domain1.minimum <= domain2.maximum and domain2.minimum <= domain1.maximum
