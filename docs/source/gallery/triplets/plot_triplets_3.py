"""
Example: triplets 3
===================
"""

# %%
# .. list-table:: Finit-difference parameters
#    :widths: 25
#    :header-rows: 1
#
#    * - boundaries: {left: -1, right: 0, top: 0, bottom: 0}
#    * - derivative: 2
#    * - accuracy: 4

from PyFinitDiff.sparse2D import FiniteDifference2D as SparseFD
from PyFinitDiff.boundaries import Boundaries2D


sparse_instance = SparseFD(
    n_x=12,
    n_y=12,
    dx=1,
    dy=1,
    derivative=2,
    accuracy=4,
    boundaries=Boundaries2D()
)

sparse_instance.triplet.plot()

# -
