#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import math
import pytest
from PyFinitDiff.finite_difference_2D import FiniteDifference, Boundaries


def foo(power: int, size: int = 20):
    """
    Generates 2D arrays for testing finite difference calculations.

    Args:
        power (int): The power to which elements in the x_array are raised.
        size (int, optional): The size of the generated arrays. Default is 20.

    Returns:
        tuple: A tuple containing the x_array and y_array.
    """
    x_array = np.arange(0, size) ** power
    y_array = np.ones(size)
    x_array, y_array = np.meshgrid(x_array, y_array)
    return x_array, y_array


# Define derivatives and accuracies to be tested
derivatives = [1, 2, 3]
derivatives_ids = [f'derivative: {d}' for d in derivatives]
accuracies = [2, 4, 6]
accuracies_ids = [f'accuracy: {a}' for a in accuracies]


@pytest.mark.parametrize('derivative', derivatives, ids=derivatives_ids)
@pytest.mark.parametrize('accuracy', accuracies, ids=accuracies_ids)
def test_derivative(accuracy, derivative):
    """
    Tests the finite difference derivative calculations with various accuracies and derivatives.

    Args:
        accuracy (int): Accuracy level of the finite difference calculation.
        derivative (int): Order of the derivative for the finite difference calculation.
    """
    size = 20
    x_array, y_array = foo(power=derivative, size=size)

    boundaries = Boundaries(
        top='symmetric',
        bottom='symmetric',
        right='symmetric',
        left='symmetric'
    )

    finite_difference = FiniteDifference(
        n_x=size,
        n_y=size,
        dx=1,
        dy=1,
        derivative=derivative,
        accuracy=accuracy,
        boundaries=boundaries
    )

    sparse_matrix = finite_difference.triplet.to_scipy_sparse()
    y_gradient = sparse_matrix * x_array.ravel()
    y_gradient = y_gradient.reshape([size, size])

    theoretical = math.factorial(derivative)
    evaluation = y_gradient[size // 2, size // 2]

    discrepancy = np.isclose(evaluation, theoretical, atol=1e-5)

    assert discrepancy, (
        f'Deviation from theoretical value for derivative. '
        f'Evaluation: {evaluation}, Theoretical: {theoretical}'
    )


if __name__ == "__main__":
    pytest.main(["-W error", __file__])
