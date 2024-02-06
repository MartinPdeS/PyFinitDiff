"""
Gradient of array
=================

"""
from PyFinitDiff.finite_difference_2D import get_array_derivative
from PyFinitDiff.finite_difference_2D import Boundaries

import numpy
from MPSPlots.render2D import SceneList

idx = numpy.linspace(-5, 5, 100)
x_array = numpy.exp(-idx**2)
y_array = numpy.exp(-idx**2)

y_array, x_array = numpy.meshgrid(x_array, y_array)

mesh = x_array * y_array

condition = 'none'
boundaries = Boundaries(
    top=condition,
    bottom=condition,
    left=condition,
    right=condition,
)

scene = SceneList(
    unit_size=(3, 3),
    ax_orientation='horizontal'
)

ax = scene.append_ax(title='Initial mesh')
ax.add_mesh(scalar=mesh)

for derivative in [1, 2, 3]:
    gradient = get_array_derivative(
        array=mesh,
        accuracy=6,
        derivative=derivative,
        x_derivative=True,
        y_derivative=True,
        boundaries=boundaries
    )

    ax = scene.append_ax(title=f'derivative: {derivative}')

    ax.add_mesh(scalar=gradient)

scene.show()


# -
