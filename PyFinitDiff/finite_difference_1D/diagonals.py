#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

# Local imports
import numpy
from PyFinitDiff.triplet import Triplet
from PyFinitDiff.finite_difference_1D.boundaries import Boundary


@dataclass
class Diagonal:
    """
    Represents a diagonal element of the finite-difference method.

    This class constructs a diagonal with parameters such as its offset and boundary condition.

    Parameters
    ----------
    mesh_info : object
        Instance describing the meta information on the mesh to be considered.
    offset : int
        Offset of the column index for the diagonal.
    values : float
        Value associated with the diagonal.
    boundary : PyFinitDiff.finite_difference_1D.boundaries.Boundary
        Instance of the boundary used for the diagonal.
    """
    mesh_info: object
    offset: int
    values: float
    boundary: Boundary

    @property
    def triplet(self) -> Triplet:
        """
        Return the Triplet instance of the diagonal.

        Returns
        -------
        Triplet
            A Triplet instance representing the non-zero values in the diagonal.
        """
        self.array: numpy.ndarray = numpy.c_[self.rows, self.columns, self.values]

        triplet = Triplet(
            array=self.array,
            shape=self.mesh_info.shape
        )

        return triplet

    def compute_triplet(self) -> None:
        """
        Compute the diagonal indices and generate a Triplet instance out of it.

        The value of the third column in the triplet depends on the boundary condition.
        """
        self.rows: numpy.ndarray = numpy.arange(0, self.mesh_info.size)
        self.columns: numpy.ndarray = self.rows + self.offset
        self.apply_symmetry()
        self.array: numpy.ndarray = numpy.c_[self.rows, self.columns, self.values]

    def apply_symmetry(self) -> None:
        """
        Apply boundary symmetry conditions to the diagonal.

        If the boundary is symmetric, the value stays the same. If it is anti-symmetric,
        a negative sign is added. If it is zero, the value becomes zero.
        """
        shift_array = self.boundary.get_shift_vector(self.offset)

        if shift_array is None:
            return

        self.columns = self.columns + 2 * shift_array
        self.values[shift_array != 0] *= self.boundary.get_factor()

    def validate_index(self) -> None:
        """
        Remove all negative indices from the diagonal.
        """
        valid_index = self.columns >= 0
        self.columns = self.columns[valid_index]
        self.rows = self.rows[valid_index]
        self.values = self.values[valid_index]

    def plot(self) -> None:
        """
        Plot the Triplet instance representing the diagonal.
        """
        return self.triplet.plot()


class ConstantDiagonal(Diagonal):
    """
    Represents a diagonal with constant values.

    This subclass of Diagonal is initialized with constant values for the entire diagonal.
    """
    def __init__(self, offset: int, value: float, mesh_info: list, boundary: Boundary):
        super().__init__(
            offset=offset,
            mesh_info=mesh_info,
            values=numpy.ones(mesh_info.size) * value,
            boundary=boundary,
        )


@dataclass
class DiagonalSet:
    """
    Represents a set of diagonals for the finite-difference matrix.

    Parameters
    ----------
    mesh_info : object
        Instance describing the meta information on the mesh.
    diagonals : list of Diagonal
        List containing diagonal elements.
    """
    mesh_info: object
    diagonals: list = field(default_factory=list)

    def append(self, diagonal: Diagonal) -> 'DiagonalSet':
        """
        Append a diagonal to the set.

        Parameters
        ----------
        diagonal : Diagonal
            The diagonal to be added to the set.

        Returns
        -------
        DiagonalSet
            The modified DiagonalSet instance.
        """
        self.diagonals.append(diagonal)
        return self

    def concatenate(self, other_diagonal_set: 'DiagonalSet') -> 'DiagonalSet':
        """
        Concatenate another DiagonalSet to this one.

        Parameters
        ----------
        other_diagonal_set : DiagonalSet
            The other DiagonalSet to concatenate.

        Returns
        -------
        DiagonalSet
            The modified DiagonalSet instance.
        """
        self.diagonals += other_diagonal_set.diagonals
        return self

    def get_row_nan_bool(self) -> numpy.ndarray:
        """
        Get a boolean array indicating which rows have NaN values.

        Returns
        -------
        numpy.ndarray
            Boolean array with True where rows have NaN values.
        """
        nan_index = self.get_nan_index()
        nan_rows = self.triplet.rows[nan_index]
        nan_index = numpy.isin(self.triplet.rows, nan_rows)
        return nan_index

    def get_list_of_nan_rows(self) -> numpy.ndarray:
        """
        Get a list of rows containing NaN values.

        Returns
        -------
        numpy.ndarray
            Unique list of rows with NaN values.
        """
        nan_index = numpy.isnan(self.triplet.values)
        nan_rows = self.triplet.rows[nan_index]
        return numpy.unique(nan_rows)

    def get_list_of_not_nan_rows(self) -> numpy.ndarray:
        """
        Get a list of rows without NaN values.

        Returns
        -------
        numpy.ndarray
            List of rows that do not have NaN values.
        """
        nan_rows = self.get_list_of_nan_rows()
        non_nan_index = ~numpy.isin(self.triplet.rows, nan_rows)
        non_nan_rows = self.triplet.rows[non_nan_index]
        return non_nan_rows

    def get_nan_index(self) -> numpy.ndarray:
        """
        Get a boolean array indicating which entries have NaN values.

        Returns
        -------
        numpy.ndarray
            Boolean array indicating which entries in the triplet have NaN values.
        """
        return numpy.isnan(self.triplet.values)

    def get_array_from_rows(self, rows: numpy.ndarray) -> numpy.ndarray:
        """
        Get the array elements for the specified rows.

        Parameters
        ----------
        rows : numpy.ndarray
            Rows to search for in the triplet.

        Returns
        -------
        numpy.ndarray
            Array elements corresponding to the specified rows.
        """
        rows_index = numpy.isin(self.triplet.rows, rows)
        return self.triplet.array[rows_index]

    def remove_nan_rows(self) -> 'DiagonalSet':
        """
        Remove rows with NaN values from the DiagonalSet.

        Returns
        -------
        DiagonalSet
            The modified DiagonalSet instance with NaN rows removed.
        """
        nan_rows = self.get_row_nan_bool()
        return self.remove_rows(rows=nan_rows)

    def remove_rows(self, rows: numpy.ndarray) -> 'DiagonalSet':
        """
        Remove specified rows from the DiagonalSet.

        Parameters
        ----------
        rows : numpy.ndarray
            Rows to be removed.

        Returns
        -------
        DiagonalSet
            The modified DiagonalSet instance with specified rows removed.
        """
        index_to_remove = numpy.isin(self.triplet.rows, rows)
        self.triplet.array = numpy.delete(
            arr=self.triplet.array,
            obj=index_to_remove,
            axis=0
        )
        return self

    def replace_nan_rows_with(self, other: 'DiagonalSet') -> 'DiagonalSet':
        """
        Replace NaN rows in this DiagonalSet with corresponding rows from another DiagonalSet.

        Parameters
        ----------
        other : DiagonalSet
            The other DiagonalSet whose non-NaN rows will replace NaN rows in this set.

        Returns
        -------
        DiagonalSet
            The modified DiagonalSet instance with replaced rows.
        """
        self_nan_rows = self.get_list_of_nan_rows()
        other_not_nan_rows = other.get_list_of_not_nan_rows()
        replace_rows = numpy.intersect1d(self_nan_rows, other_not_nan_rows)
        self.remove_rows(replace_rows)
        add_array = other.get_array_from_rows(self_nan_rows)
        self.triplet.append_array(add_array)

    def initialize_triplet(self) -> 'DiagonalSet':
        """
        Initialize the Triplet instance by concatenating all diagonal triplets.

        Returns
        -------
        DiagonalSet
            The modified DiagonalSet instance with initialized Triplet.
        """
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
        """
        Add another DiagonalSet to this one.

        Parameters
        ----------
        other : DiagonalSet
            The other DiagonalSet to add.

        Returns
        -------
        DiagonalSet
            The combined DiagonalSet instance.
        """
        self.diagonals += other.diagonals
        return self

    def plot(self):
        """
        Plot the Triplet instance representing the entire DiagonalSet.
        """
        return self.triplet.plot()
