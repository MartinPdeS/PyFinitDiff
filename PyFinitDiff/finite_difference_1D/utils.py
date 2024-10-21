#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import numpy
from PyFinitDiff.triplet import DiagonalTriplet


@dataclass
class MeshInfo:
    """
    Represents the mesh information for a 1D finite-difference grid.

    Attributes
    ----------
    n_x : int
        Number of points in the x direction.
    dx : float, optional
        Infinitesimal displacement in the x direction. Defaults to 1.
    size : int
        Total number of points in the mesh.
    shape : Tuple[int]
        Shape of the mesh as a tuple.
    """
    n_x: int
    dx: float = 1

    def __post_init__(self) -> None:
        """
        Post-initialization to calculate mesh size and shape.
        """
        self.size = self.n_x
        self.shape = (self.n_x,)


def get_circular_mesh_triplet(
        n_x: int,
        radius: float,
        x_offset: float = 0,
        value_out: float = 0,
        value_in: float = 1) -> DiagonalTriplet:
    """
    Generates a DiagonalTriplet representing a 1D mesh with a circular structure.

    The mesh is represented with `value_in` inside a circle of a given `radius`,
    and `value_out` outside the circle. The circular structure is centered with an
    optional x-offset.

    Parameters
    ----------
    n_x : int
        The number of points in the x-axis.
    radius : float
        The radius of the circular structure.
    x_offset : float, optional
        The x-offset of the circular structure. Defaults to 0.
    value_out : float, optional
        The value outside the circular structure. Defaults to 0.
    value_in : float, optional
        The value inside the circular structure. Defaults to 1.

    Returns
    -------
    DiagonalTriplet
        The 1D circular mesh triplet.
    """
    x = numpy.linspace(-100, 100, n_x)
    r = numpy.abs(x - x_offset)
    mesh = numpy.ones(x.shape) * value_out
    mesh[r < radius] = value_in

    return DiagonalTriplet(mesh, shape=(n_x,))
