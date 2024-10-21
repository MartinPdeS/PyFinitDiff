#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy as np
import math
from PyFinitDiff.finite_difference_1D import get_function_derivative


def foo(x, power: int):
    """
    A simple function to return x raised to the power specified.

    Args:
        x (float): The input value.
        power (int): The power to which x is raised.

    Returns:
        float: x raised to the specified power.
    """
    return x**power


# List of coefficient types to be tested
coefficient_type_list = ['central', 'backward', 'forward']


@pytest.mark.parametrize("coefficient_type", coefficient_type_list)
@pytest.mark.parametrize("accuracy", [2, 4, 6], ids=['accuracy_2', 'accuracy_4', 'accuracy_6'])
@pytest.mark.parametrize("derivative", [1, 2, 3], ids=['derivative_1', 'derivative_2', 'derivative_3'])
def test_central_derivative(accuracy: int, coefficient_type: str, derivative: int):
    """
    Tests the get_function_derivative function with various accuracy levels, coefficient types, and derivatives.

    Args:
        accuracy (int): Accuracy level of the finite difference calculation.
        coefficient_type (str): Type of finite difference coefficients ('central', 'backward', 'forward').
        derivative (int): Order of the derivative for the finite difference calculation.
    """
    # Evaluate the derivative of the function using finite differences
    evaluation = get_function_derivative(
        function=foo,
        x_eval=3,
        derivative=derivative,
        accuracy=accuracy,
        delta=1,
        function_kwargs=dict(power=derivative),
        coefficient_type=coefficient_type
    )

    # Compute the theoretical value of the derivative
    theoretical = math.factorial(derivative)

    # Check if the evaluated derivative is close to the theoretical value
    discrepancy = np.isclose(evaluation, theoretical, atol=1e-5)

    assert discrepancy, (
        f"[derivative = {derivative} | accuracy = {accuracy}] "
        f"Evaluation output is unexpected. evaluation = {evaluation:.7f} | theoretical = {theoretical:.7f}"
    )


if __name__ == "__main__":
    pytest.main(["-W error", __file__])
