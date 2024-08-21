#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import numpy
from PyFinitDiff.triplet import DiagonalTriplet


@dataclass
class MeshInfo:
    """
    This class represents the mesh information for a 1D finite-difference grid.

    Attributes:
        n_x (int): Number of points in the x direction.
        dx (float): Infinitesimal displacement in the x direction. Defaults to 1.
        size (int): Total number of points in the mesh.
        shape (Tuple[int]): Shape of the mesh as a tuple.
    """
    n_x: int
    dx: float = 1

    def __post_init__(self):
        """Post-initialization to calculate mesh size and shape."""
        self.size = self.n_x
        self.shape = (self.n_x,)


def get_circular_mesh_triplet(
        n_x: int,
        radius: float,
        x_offset: float = 0,
        value_out: float = 0,
        value_in: float = 1) -> DiagonalTriplet:
    """
    Gets a Triplet corresponding to a 1D mesh with a circular structure of value_in inside and value_out outside.

    Args:
        n_x (int): The number of points in the x-axis.
        radius (float): The radius of the circular structure.
        x_offset (float, optional): The x offset of the circular structure. Defaults to 0.
        value_out (float, optional): The value outside the circular structure. Defaults to 0.
        value_in (float, optional): The value inside the circular structure. Defaults to 1.

    Returns:
        DiagonalTriplet: The 1D circular mesh triplet.
    """
    x = numpy.linspace(-100, 100, n_x)

    r = numpy.abs(x - x_offset)
    mesh = numpy.ones(x.shape) * value_out
    mesh[r < radius] = value_in

    return DiagonalTriplet(mesh, shape=(n_x,))
