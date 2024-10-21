#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from PyFinitDiff.triplet import DiagonalTriplet
from dataclasses import dataclass


@dataclass
class MeshInfo:
    """
    Represents the mesh information for a finite-difference grid.

    Attributes
    ----------
    n_x : int
        Number of points in the x direction.
    n_y : int
        Number of points in the y direction.
    dx : float, optional
        Infinitesimal displacement in the x direction. Defaults to 1.
    dy : float, optional
        Infinitesimal displacement in the y direction. Defaults to 1.
    size : int
        Total number of points in the mesh.
    shape : Tuple[int, int]
        Shape of the mesh as a tuple.
    """
    n_x: int
    n_y: int
    dx: float = 1
    dy: float = 1

    def __post_init__(self) -> None:
        """
        Post-initialization to calculate mesh size and shape.
        """
        self.size = self.n_x * self.n_y
        self.shape = (self.n_x, self.n_y)


def get_circular_mesh_triplet(
        n_x: int,
        n_y: int,
        radius: float,
        x_offset: float = 0,
        y_offset: float = 0,
        value_out: float = 0,
        value_in: float = 1) -> DiagonalTriplet:
    """
    Generates a DiagonalTriplet representing a 2D mesh with a circular structure.

    The mesh is represented with `value_in` inside a circle of a given `radius`,
    and `value_out` outside the circle. The circular structure is centered at
    a specific (x, y) offset.

    Parameters
    ----------
    n_x : int
        The number of points in the x-axis.
    n_y : int
        The number of points in the y-axis.
    radius : float
        The radius of the circular structure.
    x_offset : float, optional
        The x offset of the circular structure. Defaults to 0.
    y_offset : float, optional
        The y offset of the circular structure. Defaults to 0.
    value_out : float, optional
        The value outside the circular structure. Defaults to 0.
    value_in : float, optional
        The value inside the circular structure. Defaults to 1.

    Returns
    -------
    DiagonalTriplet
        The 2D circular mesh triplet.
    """
    y, x = numpy.mgrid[
        -100:100:complex(n_y),
        -100:100:complex(n_x)
    ]

    r = numpy.sqrt((x - x_offset)**2 + (y - y_offset)**2)
    mesh = numpy.ones(x.shape) * value_out
    mesh[r < radius] = value_in

    return DiagonalTriplet(mesh, shape=(n_x, n_y))
