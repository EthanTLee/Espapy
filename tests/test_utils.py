import espapy.utils as utils
from lib.set_attributes import Domain
from lib.data_file import DataFile
import numpy as np


if __name__ == '__main__':

    target_domain = Domain(1900, 2000)

    data_file = DataFile('/Users/peepeepoopoo/Desktop/espapy/tests/1834099in.s')

    print(utils.get_max_intensity_in_domain(data_file.spectral_orders[0], target_domain))



