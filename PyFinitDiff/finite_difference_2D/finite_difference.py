#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Self

import numpy
from dataclasses import dataclass, field
import PyFinitDiff.finite_difference_2D as module
from PyFinitDiff.coefficients import FiniteCoefficients
from PyFinitDiff.triplet import Triplet


@dataclass
class DiagonalSet():
    n_x: int
    n_y: int
    diagonals: list = field(default_factory=list)

    def append(self, diagonal):
        self.diagonals.append(diagonal)

    def concatenate(self, other_diagonal_set: Self) -> Self:
        self.diagonals += other_diagonal_set.diagonals

        return self

    def remove_nan_rows(self):
        nan_index = self.get_nan_values()
        self.triplet.array = self.triplet.array[~nan_index]

    def initialize_triplet(self) -> Triplet:
        shape = [self.n_x, self.n_y]

        triplet = Triplet(array=[0, 0, 0], shape=shape)

        for diagonal in self.diagonals:
            diagonal.compute_triplet()
            triplet += diagonal.triplet

        self.triplet = triplet

    def get_nan_values(self) -> numpy.ndarray:
        return numpy.isnan(self.triplet.values)

    def get_lowest_nan(self) -> int:
        nan_index = self.get_nan_values()

        rows = self.triplet[nan_index]

        return rows.min()

    def get_highest_nan(self) -> int:
        nan_index = self.get_nan_values()

        rows = self.triplet[nan_index]

        return rows.max()

    def __add__(self, other) -> Self:
        self.diagonals += other.diagonals

        return self

    def plot(self):
        return self.triplet.plot()


@dataclass
class FiniteDifference():
    """
    This class represent a specific finit difference configuration, which is defined with the descretization of the mesh, the derivative order,
    accuracy and the boundary condition that are defined. More information is providided at the following link: 'math.toronto.edu/mpugh/Teaching/Mat1062/notes2.pdf'
    """
    n_x: int
    """ Number of point in the x direction """
    n_y: int
    """ Number of point in the y direction """
    dx: float = 1
    """ Infinetisemal displacement in x direction """
    dy: float = 1
    """ Infinetisemal displacement in y direction """
    derivative: int = 1
    """ Derivative order to convert into finit-difference matrix. """
    accuracy: int = 2
    """ Accuracy of the derivative approximation [error is inversly proportional to the power of that value]. """
    boundaries: module.Boundaries = field(default_factory=module.Boundaries())
    """ Values of the four possible boundaries of the system. """
    x_derivative: bool = True
    """ Add the x derivative """
    y_derivative: bool = True
    """ Add the y derivative """

    def __post_init__(self):
        self.finit_coefficient = FiniteCoefficients(
            derivative=self.derivative,
            accuracy=self.accuracy
        )
        self._triplet = None

    @property
    def triplet(self):
        """
        Triplet representing the non-nul values of the specific
        finit-difference configuration.

        """
        if not self._triplet:
            self.construct_triplet()
        return self._triplet

    @property
    def size(self) -> int:
        return self.n_y * self.n_x

    @property
    def shape(self) -> tuple:
        return (self.n_y, self.n_x)

    @property
    def _dx(self) -> float:
        return self.dx ** self.derivative

    @property
    def _dy(self) -> float:
        return self.dy ** self.derivative

    def offset_to_boundary_name(self, offset: int) -> str:
        if offset == 0:
            return 'center'

        if offset > 0:
            if offset < self.n_x:
                return 'right'
            else:
                return 'top'

        if offset < 0:
            if offset > -self.n_x:
                return 'left'
            else:
                return 'bottom'

    def iterate_central_coefficient(
            self,
            coefficients: str,
            offset_multiplier: int) -> tuple:
        """
        Iterate throught the given type coefficients

        :param      coefficient_type:   The coefficient type
        :type       coefficient_type:   str
        :param      offset_multiplier:  The offset multiplier
        :type       offset_multiplier:  int

        :returns:   The offset, value, coefficient and boundary type
        :rtype:     tuple
        """
        for offset, value in coefficients:
            offset *= offset_multiplier
            boundary_name = self.offset_to_boundary_name(offset=offset)
            boundary = self.boundaries.get_boundary(boundary_name)
            yield offset, value, boundary

    def _add_diagonal_coefficient(
            self,
            coefficient_type: str,
            offset_multiplier: int,
            delta: float) -> None:
        """
        Adds a diagonal coefficient to the list of diagonals.

        :param      coefficient_type:   The coefficient type
        :type       coefficient_type:   str
        :param      diagonals:          The diagonals
        :type       diagonals:          list
        :param      offset_multiplier:  The offset multiplier
        :type       offset_multiplier:  int
        :param      delta:              The delta
        :type       delta:              float

        :returns:   No return
        :rtype:     None
        """
        diagonal_set = DiagonalSet(n_x=self.n_x, n_y=self.n_y)

        coefficients = getattr(self.finit_coefficient, coefficient_type)

        iterator = self.iterate_central_coefficient(
            coefficients=coefficients,
            offset_multiplier=offset_multiplier
        )

        for offset, value, boundary in iterator:
            diagonal = module.ConstantDiagonal(
                shape=self.shape,
                offset=offset,
                boundary=boundary,
                value=value * (1 / delta),
            )

            diagonal_set.append(diagonal)

        diagonal_set.initialize_triplet()

        return diagonal_set

    def add_central_coeffients(self, diagonal_set: list) -> None:
        x_diagonal_set = self._add_diagonal_coefficient(
            coefficient_type='central',
            offset_multiplier=1,
            delta=self._dx
        )
        # x_diagonal_set.remove_nan_rows()
        # x_diagonal_set.plot().show()

        diagonal_set.concatenate(x_diagonal_set)

        y_diagonal_set = self._add_diagonal_coefficient(
            coefficient_type='central',
            offset_multiplier=self.n_x,
            delta=self._dy
        )
        # y_diagonal_set.remove_nan_rows()
        # y_diagonal_set.plot().show()

        diagonal_set.concatenate(y_diagonal_set)

    def construct_triplet(self) -> None:
        diagonal_set = DiagonalSet(n_x=self.n_x, n_y=self.n_y)

        self.add_central_coeffients(diagonal_set)

        diagonal_set.initialize_triplet()

        diagonal_set.remove_nan_rows()

        # diagonal_set.triplet.plot().show()

        self._triplet = diagonal_set.triplet

# -
