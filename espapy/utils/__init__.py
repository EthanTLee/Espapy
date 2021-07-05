from lib import set_attributes


def get_orders_in_domain(datafile, target_domain):
    orders_in_domain = []

    for order in datafile.spectral_orders:
        if overlaps(order.wavelength_domain(), target_domain):
            orders_in_domain.append(order)

    return orders_in_domain


def overlaps(domain1, domain2):
    return domain1.minimum <= domain2.maximum and domain2.minimum <= domain1.maximum
