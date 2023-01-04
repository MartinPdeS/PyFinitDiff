"""
Example: eigenmodes 7
=====================

"""

# %%
# +-------------+------------+--------------+------------+------------+
# | Boundaries  |    left    |     right    |    top     |   bottom   |
# +=============+============+==============+============+============+
# |             |    zero    |   anti-sym   |   zero     |   zero     |
# +-------------+------------+--------------+------------+------------+

import numpy
import matplotlib.pyplot as plt
from scipy.sparse import linalg


from PyFinitDiff.Sparse2D import FiniteDifference2D
from PyFinitDiff.Utils import get_2D_circular_mesh_triplet

n_y = n_x = 60


sparse_instance = FiniteDifference2D(n_x=n_x,
                                     n_y=n_y,
                                     dx=1,
                                     dy=1,
                                     derivative=2,
                                     accuracy=4,
                                     boundaries={'left': 'zero',
                                                 'right': 'anti-symmetric',
                                                 'top': 'zero',
                                                 'bottom': 'zero'})

mesh_triplet = get_2D_circular_mesh_triplet(n_x=n_x,
                                            n_y=n_y,
                                            value0=1.0,
                                            value1=1.4444,
                                            x_offset=+100,
                                            y_offset=0,
                                            radius=70)

dynamic_triplet = sparse_instance.triplet + mesh_triplet

eigen_values, eigen_vectors = linalg.eigs(dynamic_triplet.to_dense(), k=5, which='LM', sigma=1.4444)

fig, axes = plt.subplots(1, eigen_values.size, figsize=(10, 3))

shape = [sparse_instance.n_x, sparse_instance.n_y]

for i, ax in enumerate(axes[:]):
    Vector = eigen_vectors.T[i].real.reshape(shape).T
    Vector = numpy.flip(Vector, -1)
    ax.imshow(Vector.T)
    ax.set_title(f'eigenvalues: \n{eigen_values[i]:.1f}')

plt.tight_layout()

plt.show()


# -
