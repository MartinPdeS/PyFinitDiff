#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import PyFinitDiff.finite_difference_2D as module
from PyFinitDiff.coefficients import FiniteCoefficients


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
        self.mesh_info = module.MeshInfo(
            n_x=self.n_x,
            n_y=self.n_y,
            dx=self.dx,
            dy=self.dy
        )
        self.boundaries.mesh_info = self.mesh_info

        self.finit_coefficient = FiniteCoefficients(
            derivative=self.derivative,
            accuracy=self.accuracy
        )
        self._triplet = None

    @property
    def shape(self):
        return (self.n_x, self.n_y)

    @property
    def triplet(self):
        """
        Triplet representing the non-nul values of the specific
        finite-difference configuration.

        """
        if not self._triplet:
            self.construct_triplet()
        return self._triplet

    @property
    def _dx(self) -> float:
        return self.dx ** self.derivative

    @property
    def _dy(self) -> float:
        return self.dy ** self.derivative

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

            boundary = self.boundaries.offset_to_boundary(offset=offset)

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
        diagonal_set = module.DiagonalSet(mesh_info=self.mesh_info)

        coefficients = getattr(self.finit_coefficient, coefficient_type)

        iterator = self.iterate_central_coefficient(
            coefficients=coefficients,
            offset_multiplier=offset_multiplier
        )

        for offset, value, boundary in iterator:
            diagonal = module.ConstantDiagonal(
                mesh_info=self.mesh_info,
                offset=offset,
                boundary=boundary,
                value=value / delta,
            )

            diagonal_set.append(diagonal)

        diagonal_set.initialize_triplet()

        return diagonal_set

    def get_diagonal_set_full(self, offset_multiplier: int, delta: float) -> None:
        """
        Constructs and returns the central coefficents diagonals which is completed with
        forward and backward coefficients if some 'nan' values are left.

        :param      offset_multiplier:  The offset multiplier
        :type       offset_multiplier:  int
        :param      delta:              The delta
        :type       delta:              float

        :returns:   No return
        :rtype:     None
        """
        central_diagonal = self._add_diagonal_coefficient(
            coefficient_type='central',
            offset_multiplier=offset_multiplier,
            delta=delta
        )

        forward_diagonal = self._add_diagonal_coefficient(
            coefficient_type='forward',
            offset_multiplier=offset_multiplier,
            delta=delta
        )

        backward_diagonal = self._add_diagonal_coefficient(
            coefficient_type='backward',
            offset_multiplier=offset_multiplier,
            delta=delta
        )

        central_diagonal.replace_nan_rows_with(forward_diagonal)

        central_diagonal.replace_nan_rows_with(backward_diagonal)

        return central_diagonal

    def construct_triplet(self) -> None:
        x_diagonals = self.get_diagonal_set_full(
            offset_multiplier=1,
            delta=self._dx
        )

        y_diagonals = self.get_diagonal_set_full(
            offset_multiplier=self.n_x,
            delta=self._dy
        )

        self._triplet = x_diagonals.triplet + y_diagonals.triplet


# -
