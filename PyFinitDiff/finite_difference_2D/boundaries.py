#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass


@dataclass(frozen=True)
class Boundary():
    name: str
    value: str
    mesh_info: object

    def get_factor(self) -> float:
        match self.value:
            case 'symmetric':
                return +1
            case 'anti-symmetric':
                return -1
            case 'zero':
                return 0
            case 'none':
                return numpy.nan

    def get_shift_vector(self, offset: int) -> numpy.ndarray:
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


@dataclass()
class Boundaries():
    left: str = 'zero'
    """ Value of the left boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    right: str = 'zero'
    """ Value of the right boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    top: str = 'zero'
    """ Value of the top boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    bottom: str = 'zero'
    """ Value of the bottom boundary, either ['zero', 'symmetric', 'anti-symmetric'] """

    acceptable_boundary = ['zero', 'symmetric', 'anti-symmetric', 'none']

    all_boundaries = ['left', 'right', 'top', 'bottom']

    def __post_init__(self) -> None:
        for boundary in self.all_boundaries:
            self.assert_boundary_acceptable(boundary_string=boundary)

    def assert_both_boundaries_not_same(self, boundary_0: str, boundary_1: str) -> None:
        if boundary_0 != 'zero' and boundary_1 != 'zero':
            raise ValueError("Same-axis symmetries shouldn't be set on both end")

    def assert_boundary_acceptable(self, boundary_string: str) -> None:
        boundary_value = getattr(self, boundary_string)
        assert boundary_value in self.acceptable_boundary, f"Error: {boundary_string} boundary: {boundary_value} argument not accepted. Input must be in: {self.acceptable_boundary}"

    def get_boundary_pairs(self) -> list:
        return [(self.left, self.right), (self.top, self.bottom)]

    def get_boundary(self, name: str) -> Boundary:
        """
        Return a specific instance of the boundary

        :param      name:  The name
        :type       name:  str

        :returns:   The boundary.
        :rtype:     Boundary
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
        if self.left == 'symmetric' or self.right == 'symmetric':
            return 'symmetric'
        elif self.left == 'anti-symmetric' or self.right == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'

    def get_y_parity(self) -> str:
        if self.top == 'symmetric' or self.bottom == 'symmetric':
            return 'symmetric'
        elif self.top == 'anti-symmetric' or self.bottom == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'

# -
