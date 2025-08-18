#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy

from typing import Optional, List, Tuple
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from PyFinitDiff.boundary_values import BoundaryValue

config_dict = ConfigDict(
    extra='forbid',
    strict=True,
    arbitrary_types_allowed=True,
    kw_only=True,
    frozen=False
)


class Boundary:
    """
    Represents a boundary with a specific name, value, and mesh information.

    Parameters
    ----------
    name : str
        The name of the boundary.
    value : Optional[BoundaryValue]
        The value associated with the boundary (e.g., BoundaryValue.SYMMETRIC, BoundaryValue.ANTI_SYMMETRIC).
    mesh_info : object
        Mesh information object, used to determine mesh-related properties.
    """

    def __init__(self, name: str, value: Optional[BoundaryValue], mesh_info: object) -> None:
        self.name = name
        self.value = value
        self.mesh_info = mesh_info

    def get_factor(self) -> float:
        """
        Gets the factor associated with the boundary value.

        Returns
        -------
        float
            The factor corresponding to the boundary value. Possible values are:
            - 1.0 for BoundaryValue.SYMMETRIC
            - -1.0 for BoundaryValue.ANTI_SYMMETRIC
            - 0.0 for BoundaryValue.ZERO
            - numpy.nan for BoundaryValue.NONE
        """
        match self.value:
            case BoundaryValue.SYMMETRIC:
                return 1.0
            case BoundaryValue.ANTI_SYMMETRIC:
                return -1.0
            case BoundaryValue.ZERO:
                return 0.0
            case BoundaryValue.NONE:
                return numpy.nan

    def get_shift_vector(self, offset: int) -> Optional[numpy.ndarray]:
        """
        Calculates the shift vector based on the boundary name and offset.

        Parameters
        ----------
        offset : int
            The offset value to be used in the shift vector calculation.

        Returns
        -------
        Optional[numpy.ndarray]
            The shift vector as a numpy array, or None if the boundary is 'center'.
        """
        offset = abs(offset)

        match self.name.lower():
            case 'center':
                shift_vector = None
            case 'bottom':
                shift_vector = numpy.zeros(self.mesh_info.size)
                shift_vector[:offset] += offset
            case 'top':
                shift_vector = numpy.zeros(self.mesh_info.size)
                shift_vector[-offset:] -= offset
            case 'right':
                shift_vector = numpy.zeros(self.mesh_info.n_x)
                shift_vector[-offset:] = - numpy.arange(1, offset + 1)
                shift_vector = numpy.tile(shift_vector, self.mesh_info.n_y)
            case 'left':
                shift_vector = numpy.zeros(self.mesh_info.n_x)
                shift_vector[:offset] = numpy.arange(1, offset + 1)[::-1]
                shift_vector = numpy.tile(shift_vector, self.mesh_info.n_y)

        return shift_vector


@dataclass(config=config_dict)
class Boundaries:
    """
    Represents the boundary conditions for a 2D finite-difference mesh.

    Parameters
    ----------
    left : Union[str, BoundaryValue]
        Value of the left boundary.
    right : Union[str, BoundaryValue]
        Value of the right boundary.
    top : Union[str, BoundaryValue]
        Value of the top boundary.
    bottom : Union[str, BoundaryValue]
        Value of the bottom boundary.
    all_boundaries : List[str]
        List of all boundary names.
    """
    left: Optional[BoundaryValue] = BoundaryValue.ZERO
    right: Optional[BoundaryValue] = BoundaryValue.ZERO
    top: Optional[BoundaryValue] = BoundaryValue.ZERO
    bottom: Optional[BoundaryValue] = BoundaryValue.ZERO

    all_boundaries = ['left', 'right', 'top', 'bottom']

    def assert_both_boundaries_not_same(self, boundary_0: BoundaryValue, boundary_1: BoundaryValue) -> None:
        """
        Ensures that two boundaries on the same axis are not set to identical symmetry conditions unless they are BoundaryValue.ZERO.

        Parameters
        ----------
        boundary_0 : BoundaryValue
            The first boundary value.
        boundary_1 : BoundaryValue
            The second boundary value.

        Raises
        ------
        ValueError
            If both boundaries are set to the same symmetry condition and are not BoundaryValue.ZERO.
        """
        if boundary_0 != BoundaryValue.ZERO and boundary_1 != BoundaryValue.ZERO:
            raise ValueError("Same-axis symmetries shouldn't be set on both ends")

    def get_boundary_pairs(self) -> List[Tuple[BoundaryValue, BoundaryValue]]:
        """
        Retrieves pairs of boundaries.

        Returns
        -------
        List[Tuple[BoundaryValue, BoundaryValue]]
            A list of tuples containing the pairs of boundaries.
        """
        return [(self.left, self.right), (self.top, self.bottom)]

    def get_boundary(self, name: str) -> Boundary:
        """
        Retrieves a Boundary instance by name.

        Parameters
        ----------
        name : str
            The name of the boundary to retrieve.

        Returns
        -------
        Boundary
            An instance of the Boundary class for the given boundary name.
        """
        if not hasattr(self, name):
            value = None
        else:
            value = getattr(self, name)

        boundary = Boundary(
            name=name,
            value=value,
            mesh_info=self.mesh_info
        )

        return boundary

    def offset_to_boundary(self, offset: int) -> Boundary:
        """
        Determines the boundary corresponding to the given offset.

        Parameters
        ----------
        offset : int
            The offset value.

        Returns
        -------
        Boundary
            The boundary instance corresponding to the offset.
        """
        if offset == 0:
            return self.get_boundary('center')

        if offset > 0:
            if offset < self.mesh_info.n_x:
                return self.get_boundary('right')
            else:
                return self.get_boundary('top')

        if offset < 0:
            if offset > -self.mesh_info.n_x:
                return self.get_boundary('left')
            else:
                return self.get_boundary('bottom')

    def get_x_parity(self) -> str:
        """
        Determines the parity in the x direction based on the left and right boundaries.

        Returns
        -------
        str
            The parity in the x direction ('symmetric', 'anti-symmetric', or 'zero').
        """
        if self.left == BoundaryValue.SYMMETRIC or self.right == BoundaryValue.SYMMETRIC:
            return 'symmetric'
        elif self.left == BoundaryValue.ANTI_SYMMETRIC or self.right == BoundaryValue.ANTI_SYMMETRIC:
            return 'anti-symmetric'
        else:
            return 'zero'

    def get_y_parity(self) -> str:
        """
        Determines the parity in the y direction based on the top and bottom boundaries.

        Returns
        -------
        str
            The parity in the y direction ('symmetric', 'anti-symmetric', or 'zero').
        """
        if self.top == BoundaryValue.SYMMETRIC or self.bottom == BoundaryValue.SYMMETRIC:
            return 'symmetric'
        elif self.top == BoundaryValue.ANTI_SYMMETRIC or self.bottom == BoundaryValue.ANTI_SYMMETRIC:
            return 'anti-symmetric'
        else:
            return 'zero'
