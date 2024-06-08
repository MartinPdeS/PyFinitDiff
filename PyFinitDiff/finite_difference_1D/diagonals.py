#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


# Local imports
import numpy
from PyFinitDiff.triplet import Triplet
from PyFinitDiff.finite_difference_1D.utils import MeshInfo
from PyFinitDiff.finite_difference_1D.boundaries import Boundary


@dataclass
class Diagonal():
    """
    This class is a construction of diagonals element of the finit-difference method.
    The class can be initialized with different parameters suchs as it's offset or
    boundary condition.

    """
    mesh_info: object
    """ Instance describing the meta info on the mesh to be considered. """
    offset: int
    """ Offset of the column index for the diagonal. """
    values: float
    """ Value associated with the diagonal. """
    boundary: Boundary
    """ Instance of the boundary used for that diagonal. """

    @property
    def triplet(self) -> Triplet:
        """
        Return the Triplet instance of the diagonal.

        """
        self.array: numpy.ndarray = numpy.c_[self.rows, self.columns, self.values]

        triplet = Triplet(
            array=self.array,
            shape=self.mesh_info.shape
        )

        return triplet

    def compute_triplet(self) -> None:
        """
        Compute the diagonal index and generate a Triplet instance out of it.
        The value of the third triplet column depends on the boundary condition.

        :returns:   No return
        :rtype:     None
        """
        self.rows: numpy.ndarray = numpy.arange(0, self.mesh_info.size)

        self.columns: numpy.ndarray = self.rows + self.offset

        self.apply_symmetry()

        self.array: numpy.ndarray = numpy.c_[self.rows, self.columns, self.values]

    def apply_symmetry(self) -> None:
        """
        Return the value of the diabonal index as defined by the boundary condition.
        If boundary is symmetric the value stays the same, if anti-symmetric a minus sign
        is added, if zero it returns zero.

        :param      values:       The values
        :type       values:       The initial value
        :param      shift_array:  The shift array
        :type       shift_array:  numpy.ndarray

        :returns:   The symmetrized value
        :rtype:     float
        """
        shift_array = self.boundary.get_shift_vector(self.offset)

        if shift_array is None:
            return

        self.columns = self.columns + 2 * shift_array

        self.values[shift_array != 0] *= self.boundary.get_factor()

    def validate_index(self) -> None:
        """
        Removes all negative index

        :returns:   No return
        :rtype:     None
        """
        valid_index = self.columns >= 0

        self.columns = self.columns[valid_index]

        self.rows = self.rows[valid_index]

        self.values = self.values[valid_index]

    def plot(self) -> None:
        """
        Plots the Triplet instance.

        """
        return self.triplet.plot()


class ConstantDiagonal(Diagonal):
    def __init__(self, offset: int, value: float, mesh_info: list, boundary: Boundary):
        super().__init__(
            offset=offset,
            mesh_info=mesh_info,
            values=numpy.ones(mesh_info.size) * value,
            boundary=boundary,
        )


@dataclass
class DiagonalSet():
    mesh_info: object
    diagonals: list = field(default_factory=list)

    def append(self, diagonal: Diagonal) -> 'DiagonalSet':
        self.diagonals.append(diagonal)
        return self

    def concatenate(self, other_diagonal_set: 'DiagonalSet') -> 'DiagonalSet':
        self.diagonals += other_diagonal_set.diagonals

        return self

    def get_row_nan_bool(self) -> numpy.ndarray:
        """
        Returns a bool array with True where the associated rows has a numpy.nan value.

        :returns:   The nan index.
        :rtype:     numpy.ndarray
        """
        nan_index = self.get_nan_index()

        nan_rows = self.triplet.rows[nan_index]
        nan_index = numpy.isin(self.triplet.rows, nan_rows)

        return nan_index

    def get_list_of_nan_rows(self) -> numpy.ndarray:
        nan_index = numpy.isnan(self.triplet.values)

        nan_rows = self.triplet.rows[nan_index]

        return numpy.unique(nan_rows)

    def get_list_of_not_nan_rows(self) -> numpy.ndarray:
        """
        Gets the row list where no nan value is associated.

        :returns:   The list of not nan rows.
        :rtype:     numpy.ndarray
        """
        nan_rows = self.get_list_of_nan_rows()

        non_nan_index = ~numpy.isin(self.triplet.rows, nan_rows)

        non_nan_rows = self.triplet.rows[non_nan_index]

        return non_nan_rows

    def get_nan_index(self) -> numpy.ndarray:
        """
        Return a boolean list of True/False depending of the values of the triplet

        :returns:   The nan index.
        :rtype:     numpy.ndarray
        """
        return numpy.isnan(self.triplet.values)

    def get_array_from_rows(self, rows: numpy.ndarray) -> numpy.ndarray:
        """
        Returns the array element which for which the rows is in the given rows input

        :param      rows:  The rows to search for
        :type       rows:  numpy.ndarray

        :returns:   The array from rows.
        :rtype:     numpy.ndarray
        """
        rows_index = numpy.isin(self.triplet.rows, rows)

        return self.triplet.array[rows_index]

    def remove_nan_rows(self) -> 'DiagonalSet':
        nan_rows = self.get_row_nan_bool()

        return self.remove_rows(rows=nan_rows)

    def remove_rows(self, rows: numpy.ndarray) -> 'DiagonalSet':
        index_to_remove = numpy.isin(self.triplet.rows, rows)

        self.triplet.array = numpy.delete(
            arr=self.triplet.array,
            obj=index_to_remove,
            axis=0
        )

        return self

    def replace_nan_rows_with(self, other: 'DiagonalSet') -> 'DiagonalSet':
        """
        Replace the nan rows in self for the equivalent rows in the other_diagonal_set if any.

        :param      other_diagonal_set:  The other diagonal set
        :type       other_diagonal_set:  'DiagonalSet'

        :returns:   The self instance
        :rtype:     'DiagonalSet'
        """
        self_nan_rows = self.get_list_of_nan_rows()

        other_not_nan_rows = other.get_list_of_not_nan_rows()

        replace_rows = numpy.intersect1d(self_nan_rows, other_not_nan_rows)

        self.remove_rows(replace_rows)

        add_array = other.get_array_from_rows(self_nan_rows)

        self.triplet.append_array(add_array)

    def initialize_triplet(self) -> 'DiagonalSet':
        triplet = Triplet(
            array=[0, 0, 0],
            shape=self.mesh_info.shape
        )

        for diagonal in self.diagonals:
            diagonal.compute_triplet()
            triplet += diagonal.triplet

        self.triplet = triplet

        return self

    def __add__(self, other: 'DiagonalSet') -> 'DiagonalSet':
        self.diagonals += other.diagonals

        return self

    def plot(self):
        return self.triplet.plot()
# -
