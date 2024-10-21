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
    Class representing a boundary with a specific name, value, and mesh information.

    Parameters
    ----------
    name : str
        The name of the boundary.
    value : Optional[str]
        The value associated with the boundary, such as 'symmetric', 'anti-symmetric', 'zero', or 'none'.
    mesh_info : object
        The mesh information object containing information about the mesh size and structure.
    """

    name: str
    value: Optional[str]
    mesh_info: object

    def get_factor(self) -> float:
        """
        Get the factor associated with the boundary value.

        Returns
        -------
        float
            The factor corresponding to the boundary value.

        Raises
        ------
        ValueError
            If the boundary value is unexpected.
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
            case _:
                raise ValueError(f"Unexpected boundary value: {self.value}")

    def get_shift_vector(self, offset: int) -> Optional[numpy.ndarray]:
        """
        Calculate the shift vector based on the boundary name and offset.

        Parameters
        ----------
        offset : int
            The offset value to be used in the shift vector calculation.

        Returns
        -------
        Optional[numpy.ndarray]
            The shift vector as a numpy array, or None if the boundary name is 'center'.

        Raises
        ------
        ValueError
            If the boundary name is unexpected.
        """
        offset = abs(offset)

        match self.name.lower():
            case 'center':
                return None
            case 'left':
                shift_vector = numpy.zeros(self.mesh_info.size)
                shift_vector[:offset] = numpy.arange(offset)[::-1] + 1
                return shift_vector
            case 'right':
                shift_vector = numpy.zeros(self.mesh_info.size)
                shift_vector[-offset - 1:] = -numpy.arange(offset + 1)
                return shift_vector
            case _:
                raise ValueError(f"Unexpected boundary name: {self.name}")


@dataclass(config=config_dict)
class Boundaries:
    """
    Class representing the boundaries with left and right values.

    Parameters
    ----------
    left : Optional[str]
        Value of the left boundary. Defaults to 'zero'. Must be either 'zero', 'symmetric', or 'anti-symmetric'.
    right : Optional[str]
        Value of the right boundary. Defaults to 'zero'. Must be either 'zero', 'symmetric', or 'anti-symmetric'.
    acceptable_boundary : List[str]
        List of acceptable boundary values.
    all_boundaries : List[str]
        List of all boundary names.
    """
    left: Optional[str] = 'zero'
    right: Optional[str] = 'zero'

    acceptable_boundary = ['zero', 'symmetric', 'anti-symmetric', 'none']
    all_boundaries = ['left', 'right']

    def __post_init__(self) -> None:
        """
        Post-initialization method to assert acceptable boundary values.
        """
        for boundary in self.all_boundaries:
            self.assert_boundary_acceptable(boundary_string=boundary)

    def assert_both_boundaries_not_same(self, boundary_0: str, boundary_1: str) -> None:
        """
        Assert that both boundaries are not the same axis symmetries if they are not 'zero'.

        Parameters
        ----------
        boundary_0 : str
            The first boundary value.
        boundary_1 : str
            The second boundary value.

        Raises
        ------
        ValueError
            If both boundaries are set to the same axis symmetries.
        """
        if boundary_0 != 'zero' and boundary_1 != 'zero':
            raise ValueError("Same-axis symmetries shouldn't be set on both ends")

    def assert_boundary_acceptable(self, boundary_string: str) -> None:
        """
        Assert that a given boundary value is acceptable.

        Parameters
        ----------
        boundary_string : str
            The name of the boundary to check.

        Raises
        ------
        AssertionError
            If the boundary value is not acceptable.
        """
        boundary_value = getattr(self, boundary_string)
        assert boundary_value in self.acceptable_boundary, (
            f"Error: {boundary_string} boundary: {boundary_value} argument not accepted. "
            f"Input must be in: {self.acceptable_boundary}"
        )

    def get_boundary_pairs(self) -> List[Tuple[str, str]]:
        """
        Get the pairs of boundaries.

        Returns
        -------
        List[Tuple[str, str]]
            A list of tuples containing boundary pairs.
        """
        return [(self.left, self.right)]

    def get_boundary(self, name: str) -> Boundary:
        """
        Return a specific instance of the boundary.

        Parameters
        ----------
        name : str
            The name of the boundary.

        Returns
        -------
        Boundary
            The boundary instance.

        Raises
        ------
        AttributeError
            If the boundary name is not an attribute of the instance.
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

    def offset_to_boundary(self, offset: int) -> str:
        """
        Determine the boundary based on the offset.

        Parameters
        ----------
        offset : int
            The offset value.

        Returns
        -------
        str
            The name of the boundary corresponding to the offset.

        Raises
        ------
        ValueError
            If the offset does not correspond to a valid boundary.
        """
        if offset == 0:
            return self.get_boundary('center')

        if offset > 0:
            if offset < self.mesh_info.n_x:
                return self.get_boundary('right')

        if offset < 0:
            if offset > -self.mesh_info.n_x:
                return self.get_boundary('left')

        raise ValueError("Offset does not correspond to a valid boundary.")
