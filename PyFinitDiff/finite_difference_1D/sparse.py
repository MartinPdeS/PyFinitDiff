#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass
from PyFinitDiff.triplet import Triplet


@dataclass
class VariableDiagonal():
    """
    This class is a construction of diagonals element of the finit-difference method.
    The class can be initialized with different parameters suchs as it's offset or
    boundary condition.

    """
    offset: int
    """Offset of the column index for the diagonal."""
    values: numpy.ndarray
    """Value associated with the diagonal."""
    boundary: str = 'none'
    """Boundary condition. ['symmetric', 'anti-symmetric', 'zero']"""
    boundary_type: int = 0
    """Define the boundary position. [0, 1, 2, 3]"""

    def __post_init__(self):
        self.size = len(self.values.ravel())
        self._triplet: numpy.ndarray = None

    @property
    def triplet(self) -> Triplet:
        """
        Return the Triplet instance of the diagonal.

        """
        if self._triplet is None:
            self.compute_triplet()
        return self._triplet

    def symmetrize_values(self, values: numpy.ndarray, shift_array: numpy.ndarray) -> float:
        """
        Return the value of the diabonal index as defined by the boundary condition.
        If boundary is symmetric the value stays the same, if anti-symmetric a minus sign
        is added, if zero it returns zero.

        """
        match self.boundary:
            case 'symmetric':
                values[shift_array != 0] *= +1
            case 'anti-symmetric':
                values[shift_array != 0] *= -1
            case 'zero':
                values[shift_array != 0] *= 0
            case 'none':
                pass

        return values

    def _get_shift_vector_(self) -> numpy.ndarray:
        """


        """
        match self.boundary_type:
            case 0:
                shift_vector = numpy.zeros(self.size)
            case 1:
                shift_vector = numpy.zeros(self.size)
                shift_vector[:abs(self.offset)] = numpy.arange(abs(self.offset))[::-1] + 1
            case 2:
                shift_vector = numpy.zeros(self.size)
                shift_vector[-abs(self.offset) - 1:] = - numpy.arange(abs(self.offset) + 1)

        return shift_vector

    def get_boundary_row(self) -> numpy.ndarray:
        return self._get_shift_vector_().astype(bool)

    def compute_triplet(self) -> None:
        """
        Compute the diagonal index and generate a Triplet instance out of it.
        The value of the third triplet column depends on the boundary condition.

        """
        row = numpy.arange(0, self.size)

        shift = self._get_shift_vector_()

        col = row + self.offset + 2 * shift

        values = self.symmetrize_values(self.values, shift)

        self._triplet = Triplet(
            array=numpy.c_[row, col, values],
            shape=[self.size]
        )

    def remove_out_of_bound(self, array: numpy.ndarray) -> numpy.ndarray:
        """
        Remove entries of the diagonal that are out of boundary and then return the array.
        The boundary is defined by [size, size].

        """
        i: numpy.ndarray = array[:, ]
        j: numpy.ndarray = array[:, 1]

        return array[(0 <= i) & (i <= self.size - 1) & (0 <= j) & (j <= self.size - 1)]

    def plot(self) -> None:
        """
        Plots the Triplet instance.

        """
        self.triplet.plot()


class ConstantDiagonal(VariableDiagonal):
    def __init__(self, offset: int, value: float, size: int, boundary: str = 'none', boundary_type: int = 0):
        super().__init__(
            offset=offset,
            values=numpy.ones(size) * value,
            boundary=boundary,
            boundary_type=boundary_type
        )
# -
