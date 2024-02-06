#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict

from PyFinitDiff.triplet import Triplet
from PyFinitDiff.coefficients import FiniteCoefficients
import PyFinitDiff.finite_difference_1D as module


@dataclass
class FiniteDifference():
    """
    This class represent a specific finit difference configuration,
        which is defined with the descretization of the mesh, the derivative order,
        accuracy and the boundary condition that are defined.
        More information is providided at the following link:
        'math.toronto.edu/mpugh/Teaching/Mat1062/notes2.pdf'
    """
    n_x: int
    """ Number of point in the x direction """
    dx: float = 1
    """ Infinetisemal displacement in x direction """
    derivative: int = 1
    """ Derivative order to convert into finit-difference matrix. """
    accuracy: int = 2
    """ Accuracy of the derivative approximation [error is inversly proportional to the power of that value]. """
    boundaries: Dict[str, str] = field(default_factory=lambda: ({'left': 'zero', 'right': 'zero'}))
    """ Values of the four possible boundaries of the system. """

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
        return self.n_x

    @property
    def shape(self) -> list:
        return [self.size, self.size]

    @property
    def _dx(self) -> float:
        return self.dx ** self.derivative

    def offset_to_boundary_name(self, offset: int) -> str:
        if offset == 0:
            return 'center'
        elif offset < 0:
            return 'left'
        elif offset > 0:
            return 'right'

    def boundary_name_to_boundary_type(self, boundary_name: str) -> int:
        match boundary_name:
            case 'center':
                return 0
            case 'left':
                return 1
            case 'right':
                return 2

    def construct_central_triplet(self):
        diagonals = []
        for offset, value in self.finit_coefficient.central:
            boundary_name = self.offset_to_boundary_name(offset=offset)
            boundary_type = self.boundary_name_to_boundary_type(boundary_name=boundary_name)

            diagonal = module.ConstantDiagonal(
                value=value,
                size=self.n_x,
                offset=offset,
                boundary=self.boundaries.dictionary.get(boundary_name),
                boundary_type=boundary_type
            )

            diagonals.append(diagonal.triplet)

        triplet = diagonals[0]

        for diagonal in diagonals[1:]:
            triplet += diagonal

        return triplet

    def construct_triplet(self):
        self._triplet = self.construct_central_triplet()

# -
