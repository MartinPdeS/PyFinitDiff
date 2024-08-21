#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import PyFinitDiff.finite_difference_2D as module


def get_array_derivative(
        array: np.ndarray,
        derivative: int,
        accuracy: int = 4,
        coefficient_type: str = 'central',
        dx: float = 1,
        dy: float = 1,
        x_derivative: bool = True,
        y_derivative: bool = True,
        boundaries: module.Boundaries = module.Boundaries()) -> np.ndarray:
    """
    Computes the 2D gradient of a given array using finite differences.

    Args:
        array (np.ndarray): The array for which to compute the nth derivative.
        derivative (int): The order of the derivative.
        accuracy (int, optional): The accuracy for the derivative. Defaults to 4.
        coefficient_type (str, optional): The coefficient type. Defaults to 'central'.
        dx (float, optional): The delta value in the x direction. Defaults to 1.
        dy (float, optional): The delta value in the y direction. Defaults to 1.
        x_derivative (bool, optional): Whether to compute the x derivative. Defaults to True.
        y_derivative (bool, optional): Whether to compute the y derivative. Defaults to True.
        boundaries (module.Boundaries, optional): The boundary conditions. Defaults to module.Boundaries().

    Returns:
        np.ndarray: The 2D gradient array.
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
