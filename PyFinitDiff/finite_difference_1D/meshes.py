#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy

from PyFinitDiff.triplet import DiagonalTriplet


def get_circular_mesh_triplet(
        n_x: int,
        radius: float,
        x_offset: float = 0,
        value_out: float = 0,
        value_in: float = 1) -> DiagonalTriplet:
    """
    Gets a Triplet corresponding to a 1d mesh with
    circular structure of value_in inside and value_out outside.

    :param      n_x:        The number of point in the x-axis
    :type       n_x:        int
    :param      radius:     The radius of the structure
    :type       radius:     float
    :param      x_offset:   The x offset of the circular structure
    :type       x_offset:   float
    :param      value_out:  The value inside
    :type       value_out:  float
    :param      value_in:   The value outside
    :type       value_in:   float

    :returns:   The 1d circular mesh triplet.
    :rtype:     DiagonalTriplet
    """
    x = numpy.linspace(-100, 100, n_x)

    r = numpy.sqrt((x - x_offset)**2)
    mesh = numpy.ones(x.shape) * value_out
    mesh[r < radius] = value_in

    return DiagonalTriplet(mesh, shape=(n_x,))

# -
