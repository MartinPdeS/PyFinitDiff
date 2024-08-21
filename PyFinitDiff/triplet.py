import numpy

from MPSPlots.render2D import SceneList
from scipy.sparse import coo_matrix
from dataclasses import dataclass


@dataclass
class Triplet():
    shape: list
    array: numpy.ndarray
    add_extra_column: bool = False

    def __post_init__(self):
        self.array = numpy.atleast_2d(self.array)
        self.shape = numpy.asarray(self.shape)

        if self.add_extra_column:
            self.array = numpy.c_[self.array, numpy.ones(self.array.shape[0])]

        assert self.array.shape[1] == 3, 'Array shape error'

    @property
    def index(self) -> numpy.ndarray:
        return self.array[:, 0:2].astype(int)

    @property
    def index_with_label(self) -> numpy.ndarray:
        return numpy.c_[self.label, self.index].astype(int)

    @property
    def rows(self) -> numpy.ndarray:
        """
        Returns the first index i of the Triplet

        :returns:   The values associated to the Triplet
        :rtype:     numpy.ndarray
        """
        return self.array[:, 0].astype(int)

    @property
    def columns(self) -> numpy.ndarray:
        """
        Returns the second index j of the Triplet

        :returns:   The values associated to the Triplet
        :rtype:     numpy.ndarray
        """
        return self.array[:, 1].astype(int)

    @property
    def i(self) -> numpy.ndarray:
        """
        Returns the first index i of the Triplet

        :returns:   The values associated to the Triplet
        :rtype:     numpy.ndarray
        """
        return self.array[:, 0].astype(int)

    @property
    def j(self) -> numpy.ndarray:
        """
        Returns the second index j of the Triplet

        :returns:   The values associated to the Triplet
        :rtype:     numpy.ndarray
        """
        return self.array[:, 1].astype(int)

    @property
    def values(self) -> numpy.ndarray:
        """
        Returns the values of the Triplet

        :returns:   The values associated to the Triplet
        :rtype:     numpy.ndarray
        """
        return self.array[:, 2]

    @property
    def size(self) -> int:
        """
        Return the size of the Triplet, which means the number of values.

        :returns:   Size of the triplet
        :rtype:     int
        """
        return self.i.size

    def remove_below_i(self, i_value: int) -> 'Triplet':
        idx = self.i > i_value
        self.array = self.array[idx, :]
        return self

    def remove_above_i(self, i_value: int) -> 'Triplet':
        idx = self.i < i_value
        self.array = self.array[idx, :]
        return self

    def remove_below_j(self, j_value: int) -> 'Triplet':
        idx = self.j > j_value
        self.array = self.array[idx, :]
        return self

    def remove_above_j(self, j_value: int) -> 'Triplet':
        idx = self.j < j_value
        self.array = self.array[idx, :]
        return self

    @values.setter
    def values(self, value: float) -> None:
        self.array[:, 2] = value

    def delete(self, index) -> None:
        self.array = numpy.delete(self.array, index.astype(int), axis=0)

    def append(self, other: object) -> None:
        self.array = numpy.r_[self.array, other.array]

    def append_array(self, array: object) -> None:
        self.array = numpy.r_[self.array, array]

    def __add__(self, other: object) -> 'Triplet':
        """
        The methode concatenate the two triplet array and
        reduce if any coinciding index values.

        """
        new_array = numpy.r_[self.array, other.array]

        new_triplet = Triplet(array=new_array, shape=self.shape)

        return new_triplet.remove_duplicate()

    def __mul__(self, factor: float) -> 'Triplet':
        """
        The method output a new triplet where the values
        are left-multiplied by the factor

        :param      factor:  The factor
        :type       factor:  float

        :returns:   The triplet after multiplication
        :rtype:     Triplet
        """
        new_triplet = Triplet(array=self.array, shape=self.shape)

        new_triplet.values *= factor

        return new_triplet

    def __rmul__(self, factor: float) -> 'Triplet':
        """
        The method output a new triplet where the values
        are right-multiplied by the factor

        :param      factor:  The factor
        :type       factor:  float

        :returns:   The triplet after multiplication
        :rtype:     Triplet
        """
        return self.__mul__(factor)

    def __div__(self, factor) -> 'Triplet':
        """
        The method output a new triplet where the values
        are left-divided by the factor

        :param      factor:  The factor
        :type       factor:  float

        :returns:   The triplet after division
        :rtype:     Triplet
        """
        new_triplet = Triplet(array=self.array, shape=self.shape)

        new_triplet /= factor

        return new_triplet

    def __rdiv__(self, factor: float) -> 'Triplet':
        """
        The method output a new triplet where the values
        are right-divided by the factor

        :param      factor:  The factor
        :type       factor:  float

        :returns:   The triplet after division
        :rtype:     Triplet
        """
        new_triplet = Triplet(array=self.array, shape=self.shape)

        new_triplet /= factor

        return new_triplet

    def add_triplet(self, *others) -> 'Triplet':
        others_array = (other.array for other in others)

        self.array = numpy.r_[(self.array, *others_array)]

        self.merge_duplicate()

    def remove_duplicate(self) -> 'Triplet':
        """
        Removes the duplicate values of the Triplet.

        :returns:   The triplet with removed duplicate values
        :rtype:     Triplet
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

    def coincide_i(self, mask) -> 'Triplet':
        """
        The methode removing all index i which do not coincide with the
        other triplet
        """
        mask_i = numpy.unique(mask.i[mask.values != 0])

        temp = (self.array[self.i == i] for i in mask_i)

        self.array = numpy.r_[tuple(temp)]

    def __sub__(self, other: object) -> 'Triplet':
        """
        The methode removing index[i] (rows) value corresponding between the two triplets.
        It doesn't change the other triplet, only the instance that called the method.

        :param      other:  The other
        :type       other:  object

        :returns:   The substracted triplet
        :rtype:     Triplet
        """
        index_duplicate = numpy.isin(self.i, other.i)
        index_duplicate = numpy.arange(self.size)[index_duplicate]

        triplet_array = numpy.delete(self.array, index_duplicate, axis=0)

        return Triplet(array=triplet_array, shape=self.shape)

    def __iter__(self) -> tuple:
        """
        Creates an iterator for this container yielding the
        indexes i, j and value.

        :returns:   The iterator.
        :rtype:     tuple
        """
        for i, j, value in self.array:
            yield (int(i), int(j)), value

    def enumerate(self, start: int = None, stop: int = None) -> tuple:
        """
        Does the same as __iter__ but adds an overall single index n.

        :param      start:  The start
        :type       start:  int
        :param      stop:   The stop
        :type       stop:   int

        :returns:   The enumerator
        :rtype:     tuple
        """
        for n, (i, j, value) in enumerate(self.array[start:stop, :]):
            yield n, (int(i), int(j), value)

    def get_duplicate_index(self) -> numpy.ndarray:
        """
        Gets the duplicate index.

        :returns:   The duplicate index.
        :rtype:     numpy.ndarray
        """
        _, inverse, count = numpy.unique(self.index, axis=0, return_inverse=True, return_counts=True)

        index_duplicate = numpy.where(count > 1)[0]

        rows, cols = numpy.where(inverse == index_duplicate[:, numpy.newaxis])

        _, inverse_rows = numpy.unique(rows, return_index=True)

        return numpy.asarray(numpy.split(cols, inverse_rows[1:]), dtype=object)

    def merge_duplicate(self):
        duplicates = self.get_duplicate_index()

        if numpy.size(duplicates) == 0:
            return self.array

        for duplicate in duplicates:  # merge values
            self.array[int(duplicate[0]), 2] = self.array[duplicate.astype(int)][:, 2].sum()

        duplicates = [d[1:] for d in duplicates]

        self.array = numpy.delete(self.array, numpy.concatenate(duplicates).astype(int), axis=0)

    @property
    def max_i(self) -> int:
        """
        Return max i value, which is the first element of the index format.

        :returns:   The maximum index value i
        :rtype:     int
        """
        return self.i.max()

    @property
    def max_j(self) -> int:
        """
        Return max j value, which is the second element of the index format.

        :returns:   The maximum index value j
        :rtype:     int
        """
        return self.j.max()

    @property
    def min_i(self) -> float:
        """
        Return min i value, which is the first element of the index format.

        :returns:   The minimum index value i
        :rtype:     float
        """
        return self.i.min()

    @property
    def min_j(self) -> float:
        """
        Return max j value, which is the second element of the index format.

        :returns:   The minimum index value j
        :rtype:     float
        """
        return self.j.min()

    @property
    def diagonal(self) -> numpy.ndarray:
        """
        Return the diagonal element of the Triplet values.

        :returns:   The diagonal elements
        :rtype:     numpy.ndarray
        """
        return self.array[self.i == self.j]

    def shift_diagonal(self, value: float) -> None:
        """
        Shift the diagonal element of a certain value.

        :param      value:  The value to shift
        :type       value:  float
        """
        size = min(self.max_j, self.max_i)
        vector = numpy.ones(size) * value
        shift_triplet = DiagonalTriplet(vector)

        return self + shift_triplet

    def update_elements(self, other_triplet: 'Triplet', i_range: slice) -> 'Triplet':
        self.array[i_range, :] = other_triplet.array[i_range, :]

        return self

    def to_dense(self) -> numpy.ndarray:
        """
        Returns a dense representation of the object.

        :returns:   Dense representation of the object.
        :rtype:     numpy.ndarray:
        """
        dense_matrix = self.to_scipy_sparse().todense()

        dense_matrix = numpy.asarray(dense_matrix)

        return dense_matrix

    def plot(self) -> SceneList:
        """
        Plot the dense matrix representation of the triplet.

        :returns:   The figure
        :rtype:     SceneList
        """
        figure = SceneList(unit_size=(6, 6), tight_layout=True)

        ax = figure.append_ax(
            title='Finite-difference coefficients structure',
            show_legend=False,
            show_grid=True,
        )

        dense_matrix = numpy.flip(self.to_dense(), axis=[0])

        artist = ax.add_mesh(
            scalar=dense_matrix,
        )

        ax.add_colorbar(artist=artist, colormap='Blues')

        return figure

    def to_scipy_sparse(self) -> coo_matrix:
        """
        Returns a scipy sparse representation of the object.

        :returns:   Scipy sparse representation of the object.
        :rtype:     coo_matrix
        """
        size = numpy.prod(self.shape)

        output_shape = [size, size]

        sparse_matrix = coo_matrix((self.values, (self.i, self.j)), shape=output_shape)

        return sparse_matrix


class DiagonalTriplet(Triplet):
    def __init__(self, mesh: numpy.ndarray, shape: list):
        size = mesh.size
        triplet_array = numpy.zeros([size, 3])
        triplet_array[:, 0] = numpy.arange(size)
        triplet_array[:, 1] = numpy.arange(size)
        triplet_array[:, 2] = mesh.ravel()

        super().__init__(array=triplet_array, shape=shape)


# -
