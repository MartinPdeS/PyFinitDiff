#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyFinitDiff.coefficients import FiniteCoefficients


def get_function_derivative(
        function: callable,
        x_eval: float,
        derivative: int,
        delta: float,
        function_kwargs: dict,
        accuracy: int = 4,
        coefficient_type: str = 'central') -> float:
    """
    Compute the derivative of a given function at a specified point using finite differences.

    Parameters
    ----------
    function : callable
        The function to differentiate.
    x_eval : float
        The point at which to evaluate the derivative.
    derivative : int
        The order of the derivative.
    delta : float
        The distance between points used in the finite difference.
    function_kwargs : dict
        Additional keyword arguments to pass to the function.
    accuracy : int, optional
        The accuracy of the finite difference approximation (default is 4).
    coefficient_type : str, optional
        The type of finite difference coefficients to use ('central', 'forward', 'backward'). Defaults to 'central'.

    Returns
    -------
    float
        The value of the derivative at the specified point.

    Examples
    --------
    >>> def func(x):
    >>>     return x**2
    >>> get_function_derivative(func, 1.0, 1, 0.01, {})
    2.0
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
