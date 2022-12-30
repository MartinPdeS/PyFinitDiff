"""
Example: triplets 0
===================
"""

# %%
# .. list-table:: Finit-difference parameters
#    :widths: 25
#    :header-rows: 1
#
#    * - symmetries: {left: 0, right: 0, top: 0, bottom: 0}
#    * - derivative: 2
#    * - accuracy: 4

from PyFinitDiff.Sparse import FiniteDifference2D as SparseFD

sparse_instance = SparseFD(n_x=6,
                           n_y=6,
                           dx=1,
                           dy=1,
                           derivative=2,
                           accuracy=2,
                           symmetries={'left': 'none',
                                       'right': 'none',
                                       'top': 'none',
                                       'bottom': 'none'})

sparse_instance.triplet.plot()

# -
