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

from PyFinitDiff.Sparse2D import FiniteDifference2D as SparseFD

sparse_instance = SparseFD(n_x=6,
                           n_y=6,
                           dx=1,
                           dy=1,
                           derivative=2,
                           accuracy=4,
                           boundaries={'left': 'anti-symmetric',
                                       'right': 'none',
                                       'top': 'none',
                                       'bottom': 'none'})

sparse_instance.triplet.plot()

# -
