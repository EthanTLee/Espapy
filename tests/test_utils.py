import espapy.utils as utils
from lib.set_attributes import Domain

domain1 = Domain(2, 4)
domain2 = Domain(3, 5)

print(utils.overlaps(domain2, domain1))

