#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyFinitDiff.coefficients import FiniteCoefficients

import numpy


def get_function_derivative(
        function: numpy.ndarray,
        x_eval: float,
        derivative: int,
        delta: float,
        function_kwargs: dict,
        accuracy: int = 4,
        coefficient_type: str = 'central') -> float:
    """
    Returns the derivative a the given function

    :param      function:       The function
    :type       function:       function
    :param      x_eval:         parameter to derive
    :type       x_eval:         float
    :param      order:          Differentiation order (1 to 5)
    :type       order:          int
    :param      n_point:        Number of points (3 to 6)
    :type       n_point:        int
    :param      delta:          Distance between points
    :type       delta:          float
    :param      args:           The arguments
    :type       args:           list

    :returns:   The value of the derivative
    :rtype:     float
    """
    coefficients = FiniteCoefficients(
        derivative=derivative,
        accuracy=accuracy,
        coefficient_type=coefficient_type
    )

    summation = 0
    for index, value in coefficients:

        x = x_eval + index * delta

        y = function(x, **function_kwargs)

        summation += value * y

    return summation / delta ** derivative

# -
