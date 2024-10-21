#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from typing import Optional, List, Tuple
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict

config_dict = ConfigDict(
    extra='forbid',
    strict=True,
    arbitrary_types_allowed=True,
    kw_only=True,
    frozen=False
)


@dataclass(config=config_dict)
class Boundary:
    """
    Represents a boundary with a specific name, value, and mesh information.

    Parameters
    ----------
    name : str
        The name of the boundary.
    value : Optional[str]
        The value associated with the boundary (e.g., 'symmetric', 'anti-symmetric').
    mesh_info : object
        Mesh information object, used to determine mesh-related properties.
    """
    name: str
    value: Optional[str]
    mesh_info: object

    def get_factor(self) -> float:
        """
        Gets the factor associated with the boundary value.

        Returns
        -------
        float
            The factor corresponding to the boundary value. Possible values are:
            - 1.0 for 'symmetric'
            - -1.0 for 'anti-symmetric'
            - 0.0 for 'zero'
            - numpy.nan for 'none'
        """
        match self.value:
            case 'symmetric':
                return 1.0
            case 'anti-symmetric':
                return -1.0
            case 'zero':
                return 0.0
            case 'none':
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
    left : str
        Value of the left boundary. Must be one of ['zero', 'symmetric', 'anti-symmetric', 'none'].
    right : str
        Value of the right boundary. Must be one of ['zero', 'symmetric', 'anti-symmetric', 'none'].
    top : str
        Value of the top boundary. Must be one of ['zero', 'symmetric', 'anti-symmetric', 'none'].
    bottom : str
        Value of the bottom boundary. Must be one of ['zero', 'symmetric', 'anti-symmetric', 'none'].
    acceptable_boundary : List[str]
        List of acceptable boundary values.
    all_boundaries : List[str]
        List of all boundary names.
    """
    left: str = 'zero'
    right: str = 'zero'
    top: str = 'zero'
    bottom: str = 'zero'

    acceptable_boundary = ['zero', 'symmetric', 'anti-symmetric', 'none']
    all_boundaries = ['left', 'right', 'top', 'bottom']

    def __post_init__(self) -> None:
        """
        Validates boundary values after initialization to ensure they are acceptable.
        """
        for boundary in self.all_boundaries:
            self.assert_boundary_acceptable(boundary_string=boundary)

    def assert_both_boundaries_not_same(self, boundary_0: str, boundary_1: str) -> None:
        """
        Ensures that two boundaries on the same axis are not set to identical symmetry conditions unless they are 'zero'.

        Parameters
        ----------
        boundary_0 : str
            The first boundary value.
        boundary_1 : str
            The second boundary value.

        Raises
        ------
        ValueError
            If both boundaries are set to the same symmetry condition and are not 'zero'.
        """
        if boundary_0 != 'zero' and boundary_1 != 'zero':
            raise ValueError("Same-axis symmetries shouldn't be set on both ends")

    def assert_boundary_acceptable(self, boundary_string: str) -> None:
        """
        Checks whether the boundary value is acceptable.

        Parameters
        ----------
        boundary_string : str
            The name of the boundary to validate.

        Raises
        ------
        AssertionError
            If the boundary value is not within the list of acceptable values.
        """
        boundary_value = getattr(self, boundary_string)
        assert boundary_value in self.acceptable_boundary, (
            f"Error: {boundary_string} boundary: {boundary_value} argument not accepted. "
            f"Input must be in: {self.acceptable_boundary}"
        )

    def get_boundary_pairs(self) -> List[Tuple[str, str]]:
        """
        Retrieves pairs of boundaries.

        Returns
        -------
        List[Tuple[str, str]]
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
        if self.left == 'symmetric' or self.right == 'symmetric':
            return 'symmetric'
        elif self.left == 'anti-symmetric' or self.right == 'anti-symmetric':
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
        if self.top == 'symmetric' or self.bottom == 'symmetric':
            return 'symmetric'
        elif self.top == 'anti-symmetric' or self.bottom == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'
