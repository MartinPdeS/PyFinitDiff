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

from PyFinitDiff.finite_difference_2D import FiniteDifference
from PyFinitDiff.finite_difference_2D import Boundaries


sparse_instance = FiniteDifference(
    n_x=12,
    n_y=12,
    dx=1,
    dy=1,
    derivative=2,
    accuracy=4,
    boundaries=Boundaries()
)

figure = sparse_instance.triplet.plot()

_ = figure.show()

# -
