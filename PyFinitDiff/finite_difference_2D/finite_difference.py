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
    frozen=False
)


@dataclass(config=config_dict)
class FiniteDifference:
    """
    Represents a specific finite difference configuration, defined by the discretization
    of the mesh, derivative order, accuracy, and boundary conditions.

    Parameters
    ----------
    n_x : int
        Number of points in the x direction.
    n_y : int
        Number of points in the y direction.
    dx : float, optional
        Infinitesimal displacement in the x direction (default is 1).
    dy : float, optional
        Infinitesimal displacement in the y direction (default is 1).
    derivative : int, optional
        Order of the derivative to convert into a finite-difference matrix (default is 1).
    accuracy : int, optional
        Accuracy of the derivative approximation (error is inversely proportional to the power of this value, default is 2).
    boundaries : PyFinitDiff.finite_difference_2D.boundaries.Boundary, optional
        Values of the four possible boundaries of the system (default is an empty Boundaries object).
    x_derivative : bool, optional
        Whether to add the x derivative (default is True).
    y_derivative : bool, optional
        Whether to add the y derivative (default is True).

    Attributes
    ----------
    mesh_info : MeshInfo
        Contains information about the mesh, such as the number of points and spacing.
    boundaries : PyFinitDiff.finite_difference_2D.boundaries.Boundary
        Boundary conditions applied to the system.
    finite_coefficient : FiniteCoefficients
        Coefficients used for finite difference calculations.
    _triplet : Triplet or None
        The triplet representation of the finite-difference matrix, initialized to None.
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
        """
        Post-initialization to set up mesh info and finite coefficients.
        """
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
        """
        Returns the shape of the mesh as a tuple.

        Returns
        -------
        tuple
            The shape of the system, represented by the number of points in the x and y directions.
        """
        return (self.n_x, self.n_y)

    @property
    def triplet(self):
        """
        Returns the triplet representation of the non-null values of the finite-difference configuration.
        Constructs the triplet if it has not been initialized.

        Returns
        -------
        Triplet
            The Triplet instance containing the array and shape.
        """
        if not self._triplet:
            self.construct_triplet()
        return self._triplet

    @property
    def _dx(self) -> float:
        """
        Returns the scaled infinitesimal displacement for the x direction.

        Returns
        -------
        float
            The displacement scaled by the derivative order.
        """
        return self.dx ** self.derivative

    @property
    def _dy(self) -> float:
        """
        Returns the scaled infinitesimal displacement for the y direction.

        Returns
        -------
        float
            The displacement scaled by the derivative order.
        """
        return self.dy ** self.derivative

    def iterate_central_coefficient(self, coefficients: str, offset_multiplier: int):
        """
        Iterates through the given type of coefficients to provide the offset, value, and boundary type.

        Parameters
        ----------
        coefficients : str
            The type of coefficients to iterate over.
        offset_multiplier : int
            Multiplier applied to the coefficient offset.

        Yields
        ------
        tuple
            A tuple containing the offset, value, and corresponding boundary type.
        """
        for offset, value in coefficients:
            offset *= offset_multiplier
            boundary = self.boundaries.offset_to_boundary(offset=offset)
            yield offset, value, boundary

    def _add_diagonal_coefficient(self, coefficient_type: str, offset_multiplier: int, delta: float) -> 'DiagonalSet':
        """
        Adds a diagonal coefficient to the list of diagonals.

        Parameters
        ----------
        coefficient_type : str
            The type of coefficients to add (e.g., 'central', 'forward', 'backward').
        offset_multiplier : int
            Multiplier applied to the offset for each coefficient.
        delta : float
            Scaling factor for the coefficient values.

        Returns
        -------
        DiagonalSet
            A set of diagonals representing the finite-difference configuration.
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
        Constructs and returns a complete set of diagonals, including central, forward, and backward coefficients.

        Parameters
        ----------
        offset_multiplier : int
            Multiplier applied to the coefficient offset.
        delta : float
            Scaling factor for the coefficient values.

        Returns
        -------
        DiagonalSet
            A set of diagonals representing the finite-difference configuration, including adjustments for boundaries.
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
        """
        Constructs the Triplet instance for the finite-difference configuration.
        """
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
