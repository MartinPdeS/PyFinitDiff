"""
Example: triplets 0
===================
"""

# %%
# .. list-table:: Finit-difference parameters
#    :widths: 25
#    :header-rows: 1
#
#    * - boundaries: {left: 0, right: 0, top: 0, bottom: 0}
#    * - derivative: 2
#    * - accuracy: 4

from PyFinitDiff.sparse2D import FiniteDifference2D
from PyFinitDiff.boundaries import Boundaries2D

sparse_instance = FiniteDifference2D(
    n_x=20,
    n_y=20,
    dx=1,
    dy=1,
    derivative=2,
    accuracy=2,
    boundaries=Boundaries2D()
)

sparse_instance.triplet.plot()

# -
