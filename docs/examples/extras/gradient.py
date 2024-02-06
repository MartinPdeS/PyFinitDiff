"""
Gradient of array
=================

"""
from PyFinitDiff.finite_difference_2D import get_array_gradient
from PyFinitDiff.finite_difference_2D import Boundaries

import numpy
import matplotlib.pyplot as plt


idx = numpy.linspace(-5, 5, 7)
# x_array = numpy.exp(-idx**2)
# y_array = numpy.exp(-idx**2)


x_array = y_array = numpy.arange(7)

y_array, x_array = numpy.meshgrid(x_array, y_array)

mesh = x_array

condition = 'none'
boundaries = Boundaries(
    top=condition,
    bottom=condition,
    left=condition,
    right=condition,
)

gradient = get_array_gradient(
    array=mesh,
    accuracy=2,
    order=1,
    x_derivative=True,
    y_derivative=True,
    boundaries=boundaries
)


figure, ax = plt.subplots(1, 2)

image = ax[0].imshow(mesh)
image = ax[1].imshow(gradient)

plt.show()


# -
