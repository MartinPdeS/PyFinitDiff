from PyFinitDiff.tools.derivatives import get_gradient_2D_array
from PyFinitDiff.finite_difference_2D import Boundaries
from PyFinitDiff.finite_difference_2D import FiniteDifference
from PyFinitDiff.coefficients import FiniteCoefficients

import numpy
import matplotlib.pyplot as plt


def get_gradient_2D_array_v0(
        array: numpy.ndarray,
        order: int,
        accuracy: int = 4,
        coefficient_type: str = 'central',
        dx: float = 1,
        dy: float = 1,
        x_derivative: bool = True,
        y_derivative: bool = True,
        boundaries: Boundaries = Boundaries()) -> float:

    n_x, n_y = array.shape

    coefficients = FiniteCoefficients(
        derivative=order,
        accuracy=accuracy,
        coefficient_type=coefficient_type
    )

    coefficients.coefficient_type = 'central'

    coefficients.print()

    print(coefficients.values)

    x_gradient = numpy.apply_along_axis(
        lambda m: numpy.convolve(m, coefficients.values, mode='same'),
        axis=0,
        arr=array
    )

    print(x_gradient)

    return x_gradient


def get_gradient_2D_array_v1(
        array: numpy.ndarray,
        order: int,
        accuracy: int = 4,
        coefficient_type: str = 'central',
        dx: float = 1,
        dy: float = 1,
        x_derivative: bool = True,
        y_derivative: bool = True,
        boundaries: Boundaries = Boundaries()) -> float:

    n_x, n_y = array.shape

    sparse_instance = FiniteDifference(
        n_x=n_x,
        n_y=n_y,
        dx=dx,
        dy=dy,
        derivative=order,
        accuracy=accuracy,
        boundaries=boundaries,
        x_derivative=x_derivative,
        y_derivative=y_derivative
    )

    triplet = sparse_instance.triplet

    gradient = triplet.to_scipy_sparse() * array.ravel()

    return gradient.reshape([n_x, n_y])


idx = numpy.linspace(-1, 1, 10)
x_array = numpy.exp(-idx**2)
y_array = numpy.exp(-idx**2)

y_array, x_array = numpy.meshgrid(x_array, y_array)

array = y_array * x_array

boundaries = Boundaries(
    top='symmetric',
    bottom='symmetric',
    left='symmetric',
    right='symmetric'
)

gradient = get_gradient_2D_array_v1(
    array=array,
    accuracy=2,
    order=1,
    x_derivative=False,
    y_derivative=False,
    boundaries=boundaries
)


figure, ax = plt.subplots(1, 2)

image = ax[0].pcolormesh(array)
plt.colorbar(mappable=image)
image = ax[1].pcolormesh(gradient)
plt.colorbar(mappable=image)
plt.show()