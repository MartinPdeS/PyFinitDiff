"""
Example: eigenmodes 7
=====================

"""

# %%
# +-------------+------------+--------------+------------+------------+
# | Boundaries  |    left    |     right    |    top     |   bottom   |
# +=============+============+==============+============+============+
# |      -      |    zero    |   anti-sym   |   zero     |   zero     |
# +-------------+------------+--------------+------------+------------+

from scipy.sparse import linalg
from MPSPlots.render2D import SceneList

from PyFinitDiff.sparse2D import FiniteDifference2D
from PyFinitDiff.utils import get_2D_circular_mesh_triplet
from PyFinitDiff.boundaries import Boundaries2D

n_y = n_x = 80


sparse_instance = FiniteDifference2D(
    n_x=n_x,
    n_y=n_y,
    dx=1,
    dy=1,
    derivative=2,
    accuracy=4,
    boundaries=Boundaries2D(right='anti-symmetric')
)

mesh_triplet = get_2D_circular_mesh_triplet(
    n_x=n_x,
    n_y=n_y,
    value0=1.0,
    value1=1.4444,
    x_offset=0,
    y_offset=+100,
    radius=70
)

dynamic_triplet = sparse_instance.triplet + mesh_triplet

eigen_values, eigen_vectors = linalg.eigs(
    dynamic_triplet.to_scipy_sparse(),
    k=4,
    which='LM',
    sigma=1.4444
)

shape = [sparse_instance.n_y, sparse_instance.n_x]

figure = SceneList(unit_size=(3, 3), tight_layout=True, ax_orientation='horizontal')

for i in range(4):
    Vector = eigen_vectors[:, i].real.reshape(shape)
    ax = figure.append_ax(title=f'eigenvalues: \n{eigen_values[i]:.3f}')
    ax.add_mesh(scalar=Vector)

figure.show()


# -
