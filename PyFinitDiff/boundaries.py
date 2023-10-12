#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import dataclasses


class BoundariesBase:
    acceptable_boundary = ['zero', 'symmetric', 'anti-symmetric']

    def __post_init__(self) -> None:
        for boundary in self.all_boundaries:
            self.assert_boundary_acceptable(boundary_string=boundary)

        for boundary_pair in self.get_boundary_pairs():
            self.assert_both_boundaries_not_same(*boundary_pair)

    def assert_both_boundaries_not_same(self, boundary_0: str, boundary_1: str) -> None:
        if boundary_0 != 'zero' and boundary_1 != 'zero':
            raise ValueError("Same-axis symmetries shouldn't be set on both end")

    def assert_boundary_acceptable(self, boundary_string: str) -> None:
        boundary = getattr(self, boundary_string)
        if boundary not in self.acceptable_boundary:
            raise ValueError(
                f"Error: {boundary_string} boundary: {boundary} argument not accepted."
                f"{self.acceptable_boundary}"
            )

    @property
    def dictionary(self) -> dict:
        return {
            field.name: getattr(self, field.name) for field in dataclasses.fields(self.__class__)
        }


@dataclass
class Boundaries2D(BoundariesBase):
    left: str = 'zero'
    """ Value of the left boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    right: str = 'zero'
    """ Value of the right boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    top: str = 'zero'
    """ Value of the top boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    bottom: str = 'zero'
    """ Value of the bottom boundary, either ['zero', 'symmetric', 'anti-symmetric'] """

    all_boundaries = ['left', 'right', 'top', 'bottom']

    def get_boundary_pairs(self):
        return [(self.left, self.right), (self.top, self.bottom)]

    @property
    def x_symmetry(self) -> str:
        if self.left == 'symmetric' or self.right == 'symmetric':
            return 'symmetric'
        elif self.left == 'anti-symmetric' or self.right == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'

    @property
    def y_symmetry(self) -> str:
        if self.top == 'symmetric' or self.bottom == 'symmetric':
            return 'symmetric'
        elif self.top == 'anti-symmetric' or self.bottom == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'


@dataclass()
class Boundaries1D(BoundariesBase):
    left: str = 'zero'
    """ Value of the left boundary, either ['zero', 'symmetric', 'anti-symmetric'] """
    right: str = 'zero'
    """ Value of the right boundary, either ['zero', 'symmetric', 'anti-symmetric'] """

    all_boundaries = ['left', 'right']

    def get_boundary_pairs(self):
        return [(self.left, self.right)]

    @property
    def x_symmetry(self) -> str:
        if self.left == 'symmetric' or self.right == 'symmetric':
            return 'symmetric'
        elif self.left == 'anti-symmetric' or self.right == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'


# -
