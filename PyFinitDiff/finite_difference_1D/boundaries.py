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
    Class representing a boundary with a specific name, value, and mesh information.

    Parameters
    ----------
    name : str
        The name of the boundary.
    value : Optional[BoundaryValue]
        The value associated with the boundary, such as BoundaryValue.SYMMETRIC, BoundaryValue.ANTI_SYMMETRIC, BoundaryValue.ZERO, or BoundaryValue.NONE.
    mesh_info : object
        The mesh information object containing information about the mesh size and structure.
    """

    def __init__(self, name: str, value: Optional[BoundaryValue], mesh_info: object) -> None:
        self.name = name
        self.value = value
        self.mesh_info = mesh_info

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
            case BoundaryValue.SYMMETRIC:
                return 1.0
            case BoundaryValue.ANTI_SYMMETRIC:
                return -1.0
            case BoundaryValue.ZERO:
                return 0.0
            case BoundaryValue.NONE:
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
    left : Optional[BoundaryValue]
        Value of the left boundary. Defaults to BoundaryValue.ZERO.
    right : Optional[BoundaryValue]
        Value of the right boundary. Defaults to BoundaryValue.ZERO.

    all_boundaries : List[str]
        List of all boundary names.
    """
    left: Optional[BoundaryValue] = BoundaryValue.ZERO
    right: Optional[BoundaryValue] = BoundaryValue.ZERO

    all_boundaries = ['left', 'right']

    def assert_both_boundaries_not_same(self, boundary_0: BoundaryValue, boundary_1: BoundaryValue) -> None:
        """
        Assert that both boundaries are not the same axis symmetries if they are not BoundaryValue.ZERO.

        Parameters
        ----------
        boundary_0 : BoundaryValue
            The first boundary value.
        boundary_1 : BoundaryValue
            The second boundary value.

        Raises
        ------
        ValueError
            If both boundaries are set to the same axis symmetries.
        """
        if boundary_0 != BoundaryValue.ZERO and boundary_1 != BoundaryValue.ZERO:
            raise ValueError("Same-axis symmetries shouldn't be set on both ends")

    def get_boundary_pairs(self) -> List[Tuple[BoundaryValue, BoundaryValue]]:
        """
        Get the pairs of boundaries.

        Returns
        -------
        List[Tuple[BoundaryValue, BoundaryValue]]
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
