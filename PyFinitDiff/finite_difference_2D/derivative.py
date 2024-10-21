#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import PyFinitDiff.finite_difference_2D as module


def get_array_derivative(
        array: np.ndarray,
        derivative: int,
        accuracy: int = 4,
        dx: float = 1,
        dy: float = 1,
        x_derivative: bool = True,
        y_derivative: bool = True,
        boundaries: module.Boundaries = module.Boundaries()) -> np.ndarray:
    """
    Compute the 2D gradient of a given array using finite differences.

    Parameters
    ----------
    array : np.ndarray
        The array for which to compute the nth derivative.
    derivative : int
        The order of the derivative.
    accuracy : int, optional
        The accuracy for the derivative approximation (default is 4).
    dx : float, optional
        The spacing in the x direction (default is 1).
    dy : float, optional
        The spacing in the y direction (default is 1).
    x_derivative : bool, optional
        Whether to compute the derivative in the x direction (default is True).
    y_derivative : bool, optional
        Whether to compute the derivative in the y direction (default is True).
    boundaries : module.Boundaries, optional
        The boundary conditions for the finite difference (default is module.Boundaries()).

    Returns
    -------
    np.ndarray
        The 2D gradient array computed using finite differences.

    Examples
    --------
    >>> array = np.array([[1, 2], [3, 4]])
    >>> get_array_derivative(array, derivative=1, dx=0.1, dy=0.1)
    array([[ ... ], [ ... ]])
    """
    n_x, n_y = array.shape

    finite_difference = module.FiniteDifference(
        n_x=n_x,
        n_y=n_y,
        dx=dx,
        dy=dy,
        derivative=derivative,
        accuracy=accuracy,
        boundaries=boundaries,
        x_derivative=x_derivative,
        y_derivative=y_derivative
    )

    triplet = finite_difference.triplet

    gradient = triplet.to_scipy_sparse() * array.ravel()

    return gradient.reshape([n_x, n_y])
