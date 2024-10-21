#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import NoReturn, Tuple, Union
import numpy
from scipy.sparse import coo_matrix
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class Triplet:
    """
    A class representing a sparse matrix in triplet (COO) format, useful for finite-difference operations.

    Parameters
    ----------
    shape : tuple of int
        Shape of the matrix (rows, columns).
    array : numpy.ndarray
        A 2D array with three columns representing row indices, column indices, and values.
    add_extra_column : bool, optional
        If True, adds an extra column of ones to the array (default is False).

    """
    shape: Tuple[int, int]
    array: numpy.ndarray
    add_extra_column: bool = False

    def __post_init__(self):
        """
        Post-initialization to ensure the correct shape of the input array and to handle optional
        addition of an extra column to the array.
        """
        self.array = numpy.atleast_2d(self.array)
        self.shape = numpy.asarray(self.shape)

        if self.add_extra_column:
            self.array = numpy.c_[self.array, numpy.ones(self.array.shape[0])]

        if self.array.shape[1] != 3:
            raise ValueError("Array must have exactly 3 columns.")

    @property
    def index(self) -> numpy.ndarray:
        """
        Return the first two columns of the array, representing the indices.

        Returns
        -------
        numpy.ndarray
            Array of row and column indices.
        """
        return self.array[:, :2].astype(int)

    @property
    def rows(self) -> numpy.ndarray:
        """
        Return the row indices (first column).

        Returns
        -------
        numpy.ndarray
            Array of row indices.
        """
        return self.array[:, 0].astype(int)

    @property
    def columns(self) -> numpy.ndarray:
        """
        Return the column indices (second column).

        Returns
        -------
        numpy.ndarray
            Array of column indices.
        """
        return self.array[:, 1].astype(int)

    @property
    def values(self) -> numpy.ndarray:
        """
        Return the values (third column).

        Returns
        -------
        numpy.ndarray
            Array of values.
        """
        return self.array[:, 2]

    @values.setter
    def values(self, value: Union[float, numpy.ndarray]) -> None:
        """
        Set the values in the array.

        Parameters
        ----------
        value : float or numpy.ndarray
            The new value(s) to set in the third column of the array.
        """
        self.array[:, 2] = value

    @property
    def size(self) -> int:
        """
        Return the number of entries in the triplet.

        Returns
        -------
        int
            Number of entries.
        """
        return self.array.shape[0]

    def remove_below_i(self, i_value: int) -> 'Triplet':
        """
        Remove all entries with row indices below a specified value.

        Parameters
        ----------
        i_value : int
            Threshold for row indices. Entries with row indices below this value are removed.

        Returns
        -------
        Triplet
            The modified Triplet instance.
        """
        self.array = self.array[self.rows > i_value]
        return self

    def remove_above_i(self, i_value: int) -> 'Triplet':
        """
        Remove all entries with row indices above a specified value.

        Parameters
        ----------
        i_value : int
            Threshold for row indices. Entries with row indices above this value are removed.

        Returns
        -------
        Triplet
            The modified Triplet instance.
        """
        self.array = self.array[self.rows < i_value]
        return self

    def remove_below_j(self, j_value: int) -> 'Triplet':
        """
        Remove all entries with column indices below a specified value.

        Parameters
        ----------
        j_value : int
            Threshold for column indices. Entries with column indices below this value are removed.

        Returns
        -------
        Triplet
            The modified Triplet instance.
        """
        self.array = self.array[self.columns > j_value]
        return self

    def remove_above_j(self, j_value: int) -> 'Triplet':
        """
        Remove all entries with column indices above a specified value.

        Parameters
        ----------
        j_value : int
            Threshold for column indices. Entries with column indices above this value are removed.

        Returns
        -------
        Triplet
            The modified Triplet instance.
        """
        self.array = self.array[self.columns < j_value]
        return self

    def delete(self, index: numpy.ndarray) -> None:
        """
        Delete entries at the given indices.

        Parameters
        ----------
        index : numpy.ndarray
            Indices of entries to delete.
        """
        self.array = numpy.delete(self.array, index.astype(int), axis=0)

    def append(self, other: 'Triplet') -> None:
        """
        Append another triplet to this one.

        Parameters
        ----------
        other : Triplet
            Another Triplet instance to append.
        """
        self.array = numpy.r_[self.array, other.array]

    def append_array(self, array: numpy.ndarray) -> None:
        """
        Append a NumPy array to this triplet.

        Parameters
        ----------
        array : numpy.ndarray
            The array to append to the triplet.
        """
        self.array = numpy.r_[self.array, array]

    def __add__(self, other: 'Triplet') -> 'Triplet':
        """
        Concatenate two triplets and merge any duplicate indices.

        Parameters
        ----------
        other : Triplet
            Another Triplet instance to concatenate with this one.

        Returns
        -------
        Triplet
            A new Triplet instance with merged values for duplicate indices.
        """
        combined_array = numpy.r_[self.array, other.array]
        return Triplet(array=combined_array, shape=self.shape).remove_duplicate()

    def __mul__(self, factor: float) -> 'Triplet':
        """
        Multiply all values in the triplet by a factor.

        Parameters
        ----------
        factor : float
            The factor to multiply all values by.

        Returns
        -------
        Triplet
            A new Triplet instance with values scaled by the factor.
        """
        return Triplet(array=self.array * [1, 1, factor], shape=self.shape)

    __rmul__ = __mul__

    def remove_duplicate(self) -> 'Triplet':
        """
        Remove duplicate entries by summing their values.

        Returns
        -------
        Triplet
            A new Triplet instance with duplicate entries removed.
        """
        new_array = self.array
        index_to_delete = []
        duplicate = self.get_duplicate_index()

        if duplicate.size == 0:
            return Triplet(array=self.array, shape=self.shape)

        for duplicate in duplicate:
            index_to_keep = duplicate[0]
            for index_to_merge in duplicate[1:]:
                index_to_delete.append(index_to_merge)
                new_array[index_to_keep, 2] += new_array[index_to_merge, 2]

        triplet_array = numpy.delete(new_array, index_to_delete, axis=0)

        return Triplet(array=triplet_array, shape=self.shape)

    def coincide_i(self, mask: 'Triplet') -> None:
        """
        Remove entries whose row indices do not coincide with those in the mask.

        Parameters
        ----------
        mask : Triplet
            The mask triplet used to filter rows.
        """
        mask_i_unique = numpy.unique(mask.rows[mask.values != 0])
        self.array = numpy.vstack([self.array[self.rows == i] for i in mask_i_unique])

    def __sub__(self, other: 'Triplet') -> 'Triplet':
        """
        Subtract another triplet by removing matching row indices.

        Parameters
        ----------
        other : Triplet
            Another Triplet instance to subtract.

        Returns
        -------
        Triplet
            A new Triplet instance with non-matching rows.
        """
        non_matching_indices = ~numpy.isin(self.rows, other.rows)
        return Triplet(array=self.array[non_matching_indices], shape=self.shape)

    def __iter__(self):
        """
        Iterator to yield the indices and values as tuples.

        Yields
        ------
        tuple
            A tuple containing row index, column index, and value.
        """
        return iter((int(i), int(j), value) for i, j, value in self.array)

    def enumerate(self, start: int = 0, stop: int = None):
        """
        Enumerate over the entries, yielding an index and the entry values.

        Parameters
        ----------
        start : int, optional
            Starting index for enumeration (default is 0).
        stop : int, optional
            Stopping index for enumeration (default is None).

        Yields
        ------
        tuple
            Index and a tuple of row index, column index, and value.
        """
        for idx, (i, j, value) in enumerate(self.array[start:stop], start=start):
            yield idx, (int(i), int(j), value)

    def merge_duplicate(self) -> None:
        """
        Merge duplicate entries by summing their values.
        """
        duplicates = self.get_duplicate_index()
        if duplicates.size == 0:
            return
        for duplicate in duplicates:
            first_idx = duplicate[0]
            self.array[first_idx, 2] = self.array[duplicate, 2].sum()
            self.delete(duplicate[1:])

    def get_duplicate_index(self) -> numpy.ndarray:
        """
        Get indices of duplicate entries.

        Returns
        -------
        numpy.ndarray
            Array of duplicate indices.
        """
        unique_indices, inverse_indices, counts = numpy.unique(self.index, axis=0, return_inverse=True, return_counts=True)
        duplicate_indices = numpy.where(counts > 1)[0]
        return numpy.array([numpy.where(inverse_indices == idx)[0] for idx in duplicate_indices], dtype=object)

    @property
    def max_i(self) -> int:
        """
        Return the maximum row index.

        Returns
        -------
        int
            Maximum row index.
        """
        return self.rows.max()

    @property
    def max_j(self) -> int:
        """
        Return the maximum column index.

        Returns
        -------
        int
            Maximum column index.
        """
        return self.columns.max()

    @property
    def min_i(self) -> int:
        """
        Return the minimum row index.

        Returns
        -------
        int
            Minimum row index.
        """
        return self.rows.min()

    @property
    def min_j(self) -> int:
        """
        Return the minimum column index.

        Returns
        -------
        int
            Minimum column index.
        """
        return self.columns.min()

    @property
    def diagonal(self) -> numpy.ndarray:
        """
        Return the diagonal elements of the triplet.

        Returns
        -------
        numpy.ndarray
            Diagonal elements.
        """
        return self.array[self.rows == self.columns]

    def shift_diagonal(self, value: float) -> 'Triplet':
        """
        Shift the diagonal elements by a specified value.

        Parameters
        ----------
        value : float
            Value to add to the diagonal elements.

        Returns
        -------
        Triplet
            A new Triplet instance with the shifted diagonal.
        """
        diagonal_triplet = DiagonalTriplet(numpy.ones(min(self.max_i, self.max_j)) * value, shape=self.shape)
        return self + diagonal_triplet

    def update_elements(self, other_triplet: 'Triplet', i_range: slice) -> 'Triplet':
        """
        Update elements within a specified range.

        Parameters
        ----------
        other_triplet : Triplet
            The Triplet instance whose elements will be used for updating.
        i_range : slice
            Range of rows to update.

        Returns
        -------
        Triplet
            The updated Triplet instance.
        """
        self.array[i_range, :] = other_triplet.array[i_range, :]
        return self

    def to_dense(self) -> numpy.ndarray:
        """
        Convert the triplet to a dense matrix representation.

        Returns
        -------
        numpy.ndarray
            Dense matrix representation of the triplet.
        """
        return self.to_scipy_sparse().toarray()

    def plot(self) -> NoReturn:
        """
        Plot the dense matrix representation of the triplet.
        """
        plt.figure()
        plt.title('Finite-difference coefficients structure')
        plt.xlabel('Columns')
        plt.ylabel('Rows')

        dense_matrix = numpy.flip(self.to_dense(), axis=0)
        plt.pcolormesh(dense_matrix, cmap='Blues')
        plt.gca().set_aspect('equal')
        plt.grid(True)
        plt.colorbar()
        plt.show()

    def to_scipy_sparse(self) -> coo_matrix:
        """
        Convert the triplet to a SciPy sparse matrix.

        Returns
        -------
            coo_matrix: The scipy sparse matrix representation.
        """
        return coo_matrix((self.values, (self.rows, self.columns)), shape=(numpy.prod(self.shape),) * 2)


class DiagonalTriplet(Triplet):
    def __init__(self, mesh: numpy.ndarray, shape: Tuple[int, int]):
        size = mesh.size
        triplet_array = numpy.column_stack((numpy.arange(size), numpy.arange(size), mesh.ravel()))
        super().__init__(array=triplet_array, shape=shape)
