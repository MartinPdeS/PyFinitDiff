"""
Example: 1D eigenmodes 2
========================

"""

# %%
# .. list-table:: 1D Finit-difference parameters
#    :widths: 25
#    :header-rows: 1
#
#    * - boundaries: {left: anti-symmetric, right: anti-symmetric}
#    * - derivative: 2
#    * - accuracy: 6

from scipy.sparse import linalg

from MPSPlots.render2D import SceneList

from PyFinitDiff.finite_difference_1D import FiniteDifference
from PyFinitDiff.finite_difference_1D import get_circular_mesh_triplet
from PyFinitDiff.finite_difference_1D import Boundaries


n_x = 200
sparse_instance = FiniteDifference(
    n_x=n_x,
    dx=1,
    derivative=2,
    accuracy=6,
    boundaries=Boundaries()
)

mesh_triplet = get_circular_mesh_triplet(
    n_x=n_x,
    radius=60,
    value_out=1,
    value_in=1.4444,
    x_offset=+100
)

dynamic_triplet = sparse_instance.triplet + mesh_triplet

eigen_values, eigen_vectors = linalg.eigs(
    dynamic_triplet.to_dense(),
    k=4,
    which='LM',
    sigma=1.4444
)

figure = SceneList(unit_size=(3, 3), tight_layout=True, ax_orientation='horizontal')

for i in range(4):
    Vector = eigen_vectors[:, i].real.reshape([sparse_instance.n_x])
    ax = figure.append_ax(title=f'eigenvalues: \n{eigen_values[i]:.3f}')
    _ = ax.add_line(y=Vector)

figure.show()


# -
