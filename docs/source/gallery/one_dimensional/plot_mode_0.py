"""
Example: 1D eigenmodes 0
========================

"""

# %%
# .. list-table:: 1D Finit-difference parameters
#    :widths: 25
#    :header-rows: 1
#
#    * - boundaries: {left: symmetric, right: symmetric}
#    * - derivative: 2
#    * - accuracy: 6


import numpy
import matplotlib.pyplot as plt
from scipy.sparse import linalg

from PyFinitDiff.Sparse1D import FiniteDifference1D
from PyFinitDiff.Utils import get_1D_circular_mesh_triplet


n_x = 100
sparse_instance = FiniteDifference1D(n_x=n_x,
                                     dx=1,
                                     derivative=2,
                                     accuracy=6,
                                     boundaries={'left': 'zero',
                                                 'right': 'zero'})


mesh_triplet = get_1D_circular_mesh_triplet(n_x=n_x, radius=60, value0=1, value1=1.4444, x_offset=0)

dynamic_triplet = sparse_instance.triplet + mesh_triplet

eigen_values, eigen_vectors = linalg.eigs(dynamic_triplet.to_dense(), k=4, which='LM', sigma=1.4444)

fig, axes = plt.subplots(1, eigen_values.size, figsize=(14, 3))

shape = [sparse_instance.n_x]

for i, ax in enumerate(axes[:]):
    Vector = eigen_vectors.T[i].real.reshape(shape).T
    Vector = numpy.flip(Vector, -1)
    ax.plot(Vector.T)
    ax.set_title(f'eigenvalues: \n{eigen_values[i]:.1f}')

plt.tight_layout()

plt.show()

# -
