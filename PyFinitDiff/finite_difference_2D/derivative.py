#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy

import PyFinitDiff.finite_difference_2D as module


def get_array_derivative(
        array: numpy.ndarray,
        derivative: int,
        accuracy: int = 4,
        coefficient_type: str = 'central',
        dx: float = 1,
        dy: float = 1,
        x_derivative: bool = True,
        y_derivative: bool = True,
        boundaries: module.Boundaries = module.Boundaries()) -> float:
    """
    Gets the 2D gradient of an array array.

    :param      array:             The array of which to compute the nth derivative
    :type       array:             object
    :param      derivative:        The order of the derivative
    :type       derivative:        int
    :param      accuracy:          The accuracy for the derivative
    :type       accuracy:          int
    :param      coefficient_type:  The coefficient type
    :type       coefficient_type:  str
    :param      dx:                The delta value in x direction
    :type       dx:                float
    :param      dy:                The delta value in y direction
    :type       dy:                float
    :param      x_derivative:      Compute the x derivative
    :type       x_derivative:      bool
    :param      y_derivative:      Compute the y derivative
    :type       y_derivative:      bool
    :param      boundaries:        The boundaries conditions
    :type       boundaries:        Boundaries

    :returns:   The 2D gradient array.
    :rtype:     float
    """
    n_x, n_y = array.shape

    sparse_instance = module.FiniteDifference(
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

    triplet = sparse_instance.triplet

    gradient = triplet.to_scipy_sparse() * array.ravel()

    return gradient.reshape([n_x, n_y])

# -
