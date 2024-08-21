#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from dataclasses import field

from PyFinitDiff.coefficients import FiniteCoefficients
from PyFinitDiff.triplet import Triplet
from PyFinitDiff.finite_difference_2D.boundaries import Boundaries
from PyFinitDiff.finite_difference_2D.utils import MeshInfo
from PyFinitDiff.finite_difference_2D.diagonals import DiagonalSet, ConstantDiagonal


config_dict = ConfigDict(
    extra='forbid',
    strict=True,
    arbitrary_types_allowed=True,
    kw_only=True,
    frozen=True
)


@dataclass(config=config_dict)
class FiniteDifference():
    """
    This class represents a specific finite difference configuration, which is defined
    with the discretization of the mesh, the derivative order, accuracy, and the boundary
    conditions that are defined. More information is provided at the following link:
    'math.toronto.edu/mpugh/Teaching/Mat1062/notes2.pdf'

    Attributes:
        n_x (int): Number of points in the x direction.
        n_y (int): Number of points in the y direction.
        dx (float): Infinitesimal displacement in the x direction. Defaults to 1.
        dy (float): Infinitesimal displacement in the y direction. Defaults to 1.
        derivative (int): Derivative order to convert into finite-difference matrix. Defaults to 1.
        accuracy (int): Accuracy of the derivative approximation (error is inversely proportional to the power of this value). Defaults to 2.
        boundaries (Boundaries): Values of the four possible boundaries of the system.
        x_derivative (bool): Add the x derivative. Defaults to True.
        y_derivative (bool): Add the y derivative. Defaults to True.
    """
    n_x: int
    n_y: int
    dx: float = 1
    dy: float = 1
    derivative: int = 1
    accuracy: int = 2
    boundaries: Boundaries = field(default_factory=Boundaries)
    x_derivative: bool = True
    y_derivative: bool = True

    def __post_init__(self):
        """Post-initialization to set up mesh info and finite coefficients."""
        self.mesh_info = MeshInfo(
            n_x=self.n_x,
            n_y=self.n_y,
            dx=self.dx,
            dy=self.dy
        )
        self.boundaries.mesh_info = self.mesh_info

        self.finite_coefficient = FiniteCoefficients(
            derivative=self.derivative,
            accuracy=self.accuracy
        )
        self._triplet = None

    @property
    def shape(self):
        """Returns the shape of the mesh as a tuple."""
        return (self.n_x, self.n_y)

    @property
    def triplet(self):
        """
        Triplet representing the non-null values of the specific
        finite-difference configuration.

        Returns:
            Triplet: The Triplet instance containing the array and shape.
        """
        if not self._triplet:
            self.construct_triplet()
        return self._triplet

    @property
    def _dx(self) -> float:
        """Returns the dx value raised to the power of the derivative order."""
        return self.dx ** self.derivative

    @property
    def _dy(self) -> float:
        """Returns the dy value raised to the power of the derivative order."""
        return self.dy ** self.derivative

    def iterate_central_coefficient(
            self,
            coefficients: str,
            offset_multiplier: int) -> tuple:
        """
        Iterate through the given type coefficients.

        Args:
            coefficients (str): The coefficient type.
            offset_multiplier (int): The offset multiplier.

        Yields:
            tuple: The offset, value, and boundary.
        """
        for offset, value in coefficients:
            offset *= offset_multiplier
            boundary = self.boundaries.offset_to_boundary(offset=offset)
            yield offset, value, boundary

    def _add_diagonal_coefficient(
            self,
            coefficient_type: str,
            offset_multiplier: int,
            delta: float) -> 'DiagonalSet':
        """
        Adds a diagonal coefficient to the list of diagonals.

        Args:
            coefficient_type (str): The coefficient type.
            offset_multiplier (int): The offset multiplier.
            delta (float): The delta value.

        Returns:
            DiagonalSet: The diagonal set with added coefficients.
        """
        diagonal_set = DiagonalSet(mesh_info=self.mesh_info)
        coefficients = getattr(self.finite_coefficient, coefficient_type)

        iterator = self.iterate_central_coefficient(
            coefficients=coefficients,
            offset_multiplier=offset_multiplier
        )

        for offset, value, boundary in iterator:
            diagonal = ConstantDiagonal(
                mesh_info=self.mesh_info,
                offset=offset,
                boundary=boundary,
                value=value / delta,
            )
            diagonal_set.append(diagonal)

        diagonal_set.initialize_triplet()
        return diagonal_set

    def get_diagonal_set_full(self, offset_multiplier: int, delta: float) -> 'DiagonalSet':
        """
        Constructs and returns the central coefficients diagonals which is completed with
        forward and backward coefficients if some 'nan' values are left.

        Args:
            offset_multiplier (int): The offset multiplier.
            delta (float): The delta value.

        Returns:
            DiagonalSet: The full set of diagonal coefficients.
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
        """Constructs the Triplet instance for the finite-difference configuration."""
        self._triplet = Triplet(array=[[0, 0, 0]], shape=self.mesh_info.shape)

        if self.x_derivative:
            x_diagonals = self.get_diagonal_set_full(
                offset_multiplier=1,
                delta=self._dx
            )
            self._triplet += x_diagonals.triplet

        if self.y_derivative:
            y_diagonals = self.get_diagonal_set_full(
                offset_multiplier=self.n_x,
                delta=self._dy
            )
            self._triplet += y_diagonals.triplet


# -
