"""
Example: triplets 0
===================

Derivative = 2
Accuracy = 2
Symmetry = {left: 0, right: 0, top: 0, bottom: 0}
"""


from PyFinitDiff.Sparse import FiniteDifference2D as SparseFD
from PyFinitDiff.Utils import get_circular_mesh_triplet

n_y = n_x = 6
sparse_instance = SparseFD(n_x=n_x,
                           n_y=n_y,
                           dx=1,
                           dy=1,
                           derivative=2,
                           accuracy=2,
                           symmetries={'left': 0, 'right': 0, 'top': 0, 'bottom': 0})

mesh_triplet = get_circular_mesh_triplet(n_x=n_x,
                                         n_y=n_y,
                                         value0=1.0,
                                         value1=1.4444,
                                         x_offset=0,
                                         y_offset=0,
                                         radius=70)

dynamic_triplet = sparse_instance.triplet + mesh_triplet

dynamic_triplet.plot()

# -
