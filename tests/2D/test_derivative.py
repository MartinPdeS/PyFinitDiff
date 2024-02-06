#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import math
import pytest

from PyFinitDiff.finite_difference_2D import FiniteDifference
from PyFinitDiff.finite_difference_2D import Boundaries


def foo(power: int, size: int = 20):
    x_array = numpy.arange(0, size) ** power

    y_array = numpy.ones(size)

    x_array, y_array = numpy.meshgrid(x_array, y_array)

    return x_array, y_array


derivatives = [1, 2, 3]
derivatives_ids = [
    f'derivative: {d}' for d in derivatives
]

accuracies = [2, 4, 6]
accuracies_ids = [
    f'accuracy: {a}' for a in accuracies
]


@pytest.mark.parametrize('derivative', derivatives, ids=derivatives_ids)
@pytest.mark.parametrize('accuracy', accuracies, ids=accuracies_ids)
def test_derivative(accuracy, derivative):
    size = 20
    x_array, y_array = foo(power=derivative, size=size)

    boundaries = Boundaries(
        top='symmetric',
        bottom='symmetric',
        right='symmetric',
        left='symmetric'
    )

    finit_difference = FiniteDifference(
        n_x=size,
        n_y=size,
        dx=1,
        dy=1,
        derivative=derivative,
        accuracy=accuracy,
        boundaries=boundaries
    )

    sparse_matrix = finit_difference.triplet.to_scipy_sparse()

    y_gradient = sparse_matrix * x_array.ravel()

    y_gradient = y_gradient.reshape([size, size])

    theoretical = math.factorial(derivative)
    evaluation = y_gradient[size // 2, size // 2]

    discrepency = numpy.isclose(evaluation, theoretical, atol=1e-5)

    assert discrepency, 'Deviation from theoretical value for derivative'

# -
