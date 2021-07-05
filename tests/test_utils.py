import espapy.utils as utils
from lib.set_attributes import Domain
from lib.data_file import DataFile
import numpy as np


if __name__ == '__main__':

    target_domain = Domain(0, 2000)

    data_file = DataFile('/Users/peepeepoopoo/Desktop/espapy/tests/1834099in.s')

    max_intensity_point = utils.get_max_intensity_point_in_spectral_order_in_domain(
        data_file.spectral_orders[0],
        target_domain
    )

    print("d")



