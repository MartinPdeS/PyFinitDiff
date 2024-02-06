"""
Generating Whittle-Matérn field
===============================

"""

import numpy
from scipy import linalg
from MPSPlots.render2D import SceneList

from PyFinitDiff.finite_difference_2D import FiniteDifference
from PyFinitDiff.finite_difference_2D import get_circular_mesh_triplet
from PyFinitDiff.finite_difference_2D import Boundaries


n_x = n_y = 80

sparse_instance = FiniteDifference(
    n_x=n_x,
    n_y=n_y,
    dx=1000 / n_x,
    dy=1000 / n_y,
    derivative=2,
    accuracy=2,
    boundaries=Boundaries(top='symmetric')
)


laplacian = sparse_instance.triplet.to_dense()


def get_field(D: float, lc: float, Nc: float, shape: list):
    n_x, n_y = shape
    eta = numpy.random.rand(n_x * n_y)

    left_hand_side = (- laplacian + lc**2)**(3 / 2)

    right_hand_side = eta

    field = linalg.solve(left_hand_side, right_hand_side)

    return Nc * field


figure = SceneList(
    unit_size=(4, 4),
    tight_layout=True,
    ax_orientation='horizontal'
)

field = get_field(
    D := 3,
    lc := 1,
    Nc := 1,
    shape=[n_x, n_y]
)

ax = figure.append_ax(title=f'Correlation length: {lc}')

artist = ax.add_mesh(scalar=field.reshape([n_x, n_y]))

ax.add_colorbar(artist=artist)

# ---------------

field = get_field(
    D := 3,
    lc := 2,
    Nc := 1,
    shape=[n_x, n_y]
)

ax = figure.append_ax(title=f'Correlation length: {lc}')

artist = ax.add_mesh(scalar=field.reshape([n_x, n_y]))

ax.add_colorbar(artist=artist)


# ---------------

field = get_field(
    D := 3,
    lc := 4,
    Nc := 1,
    shape=[n_x, n_y]
)

ax = figure.append_ax(title=f'Correlation length: {lc}')

artist = ax.add_mesh(scalar=field.reshape([n_x, n_y]))

ax.add_colorbar(artist=artist)

figure.show()


# -
