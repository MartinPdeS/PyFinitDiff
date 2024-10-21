#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import field
from typing import Optional, List
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict

import numpy
from PyFinitDiff.triplet import Triplet
from PyFinitDiff.finite_difference_2D.utils import MeshInfo
from PyFinitDiff.finite_difference_2D.boundaries import Boundary

config_dict = ConfigDict(
    extra='forbid',
    strict=True,
    kw_only=True,
    frozen=False,
    arbitrary_types_allowed=True
)


@dataclass(config=config_dict)
class Diagonal:
    """
    Represents the diagonal elements of the finite-difference method.

    This class can be initialized with parameters such as its offset or boundary condition.

    Parameters
    ----------
    mesh_info : MeshInfo
        Instance describing the meta information on the mesh to be considered.
    offset : int
        Offset of the column index for the diagonal.
    values : numpy.ndarray
        Values associated with the diagonal.
    boundary : Optional[PyFinitDiff.finite_difference_2D.boundaries.Boundary]
        Instance of the boundary used for that diagonal.
    """
    mesh_info: MeshInfo
    offset: int
    values: numpy.ndarray
    boundary: Optional[Boundary] = None

    @property
    def triplet(self) -> Triplet:
        """
        Returns the Triplet instance of the diagonal.

        Returns
        -------
        Triplet
            The Triplet instance containing the array and shape.
        """
        self.array: numpy.ndarray = numpy.c_[self.rows, self.columns, self.values]

        triplet = Triplet(
            array=self.array,
            shape=self.mesh_info.shape
        )

        return triplet

    def compute_triplet(self) -> None:
        """
        Computes the diagonal indices and generates a Triplet instance out of it.

        The value of the third triplet column depends on the boundary condition.
        """
        self.rows: numpy.ndarray = numpy.arange(0, self.mesh_info.size)
        self.columns: numpy.ndarray = self.rows + self.offset
        self.apply_symmetry()
        self.array: numpy.ndarray = numpy.c_[self.rows, self.columns, self.values]

    def apply_symmetry(self) -> None:
        """
        Adjusts the values of the diagonal indices as defined by the boundary condition.

        If the boundary is symmetric, the value stays the same. If anti-symmetric, a minus sign is added.
        If zero, it returns zero.
        """
        shift_array = self.boundary.get_shift_vector(self.offset)

        if shift_array is None:
            return

        self.columns = self.columns + 2 * shift_array
        self.values[shift_array != 0] *= self.boundary.get_factor()

    def validate_index(self) -> None:
        """
        Removes all negative indices from the diagonal.
        """
        valid_index = self.columns >= 0
        self.columns = self.columns[valid_index]
        self.rows = self.rows[valid_index]
        self.values = self.values[valid_index]

    def plot(self) -> None:
        """
        Plots the Triplet instance representing the diagonal.
        """
        return self.triplet.plot()


class ConstantDiagonal(Diagonal):
    """
    Represents a diagonal with constant values for the finite-difference method.

    This subclass of Diagonal is initialized with constant values for the entire diagonal.
    """
    def __init__(self, offset: int, value: float, mesh_info: list, boundary: Boundary):
        super().__init__(
            offset=offset,
            mesh_info=mesh_info,
            values=numpy.ones(mesh_info.size) * value,
            boundary=boundary,
        )


@dataclass(config=config_dict)
class DiagonalSet:
    """
    Represents a set of diagonals for the finite-difference method.

    This class provides various utilities for manipulating and analyzing the set of diagonals.

    Parameters
    ----------
    mesh_info : MeshInfo
        Meta information about the mesh.
    diagonals : List[Diagonal]
        List of Diagonal objects.
    """
    mesh_info: MeshInfo
    diagonals: List[Diagonal] = field(default_factory=list)

    def append(self, diagonal: Diagonal) -> DiagonalSet:
        """
        Appends a Diagonal to the set.

        Parameters
        ----------
        diagonal : Diagonal
            The diagonal to append.

        Returns
        -------
        DiagonalSet
            The updated DiagonalSet.
        """
        self.diagonals.append(diagonal)
        return self

    def concatenate(self, other_diagonal_set: DiagonalSet) -> DiagonalSet:
        """
        Concatenates another DiagonalSet to this one.

        Parameters
        ----------
        other_diagonal_set : DiagonalSet
            The other DiagonalSet to concatenate.

        Returns
        -------
        DiagonalSet
            The updated DiagonalSet.
        """
        self.diagonals += other_diagonal_set.diagonals
        return self

    def get_row_nan_bool(self) -> numpy.ndarray:
        """
        Returns a boolean array with True where the associated rows have a NaN value.

        Returns
        -------
        numpy.ndarray
            Boolean array indicating NaN rows.
        """
        nan_index = self.get_nan_index()
        nan_rows = self.triplet.rows[nan_index]
        nan_index = numpy.isin(self.triplet.rows, nan_rows)
        return nan_index

    def get_list_of_nan_rows(self) -> numpy.ndarray:
        """
        Gets a list of rows containing NaN values.

        Returns
        -------
        numpy.ndarray
            Array of rows with NaN values.
        """
        nan_index = numpy.isnan(self.triplet.values)
        nan_rows = self.triplet.rows[nan_index]
        return numpy.unique(nan_rows)

    def get_list_of_not_nan_rows(self) -> numpy.ndarray:
        """
        Gets a list of rows without NaN values.

        Returns
        -------
        numpy.ndarray
            Array of rows without NaN values.
        """
        nan_rows = self.get_list_of_nan_rows()
        non_nan_index = ~numpy.isin(self.triplet.rows, nan_rows)
        non_nan_rows = self.triplet.rows[non_nan_index]
        return non_nan_rows

    def get_nan_index(self) -> numpy.ndarray:
        """
        Gets a boolean array indicating the indices of NaN values in the triplet.

        Returns
        -------
        numpy.ndarray
            Boolean array indicating NaN indices.
        """
        return numpy.isnan(self.triplet.values)

    def get_array_from_rows(self, rows: numpy.ndarray) -> numpy.ndarray:
        """
        Returns the array elements for the specified rows.

        Parameters
        ----------
        rows : numpy.ndarray
            The rows to search for.

        Returns
        -------
        numpy.ndarray
            The array elements corresponding to the specified rows.
        """
        rows_index = numpy.isin(self.triplet.rows, rows)
        return self.triplet.array[rows_index]

    def remove_nan_rows(self) -> DiagonalSet:
        """
        Removes rows containing NaN values from the triplet.

        Returns
        -------
        DiagonalSet
            The updated DiagonalSet with NaN rows removed.
        """
        nan_rows = self.get_row_nan_bool()
        return self.remove_rows(rows=nan_rows)

    def remove_rows(self, rows: numpy.ndarray) -> DiagonalSet:
        """
        Removes the specified rows from the triplet.

        Parameters
        ----------
        rows : numpy.ndarray
            The rows to remove.

        Returns
        -------
        DiagonalSet
            The updated DiagonalSet with the specified rows removed.
        """
        index_to_remove = numpy.isin(self.triplet.rows, rows)
        self.triplet.array = numpy.delete(self.triplet.array, index_to_remove, axis=0)
        return self

    def replace_nan_rows_with(self, other: DiagonalSet) -> DiagonalSet:
        """
        Replaces NaN rows in this DiagonalSet with the equivalent rows from another DiagonalSet.

        Parameters
        ----------
        other : DiagonalSet
            The other DiagonalSet to source non-NaN rows from.

        Returns
        -------
        DiagonalSet
            The updated DiagonalSet with NaN rows replaced.
        """
        self_nan_rows = self.get_list_of_nan_rows()
        other_not_nan_rows = other.get_list_of_not_nan_rows()
        replace_rows = numpy.intersect1d(self_nan_rows, other_not_nan_rows)
        self.remove_rows(replace_rows)
        add_array = other.get_array_from_rows(self_nan_rows)
        self.triplet.append_array(add_array)
        return self

    def initialize_triplet(self) -> DiagonalSet:
        """
        Initializes the triplet by combining all diagonals in the set.

        Returns
        -------
        DiagonalSet
            The initialized DiagonalSet.
        """
        triplet = Triplet(
            array=numpy.array([0, 0, 0]),
            shape=self.mesh_info.shape
        )
        for diagonal in self.diagonals:
            diagonal.compute_triplet()
            triplet += diagonal.triplet
        self.triplet = triplet
        return self

    def get_lowest_nan(self) -> int:
        """
        Gets the lowest row index containing a NaN value.

        Returns
        -------
        int
            The lowest row index with a NaN value.
        """
        nan_index = self.get_nan_index()
        rows = self.triplet.rows[nan_index]
        return rows.min()

    def get_highest_nan(self) -> int:
        """
        Gets the highest row index containing a NaN value.

        Returns
        -------
        int
            The highest row index with a NaN value.
        """
        nan_index = self.get_nan_index()
        rows = self.triplet.rows[nan_index]
        return rows.max()

    def __add__(self, other: DiagonalSet) -> DiagonalSet:
        """
        Adds another DiagonalSet to this one.

        Parameters
        ----------
        other : DiagonalSet
            The other DiagonalSet to add.

        Returns
        -------
        DiagonalSet
            The updated DiagonalSet.
        """
        self.diagonals += other.diagonals
        return self

    def plot(self) -> None:
        """
        Plots the Triplet instance representing the entire DiagonalSet.
        """
        return self.triplet.plot()
