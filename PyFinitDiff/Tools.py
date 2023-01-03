import numpy

from MPSPlots.Render2D import Scene2D, Axis, Mesh, ColorBar


class Triplet():
    def __init__(self, array: numpy.ndarray = None, add_extra_column: bool = False):
        if array is None:
            array = [[0, 0, 0]]

        self._array = numpy.asarray(array)
        self._array = numpy.atleast_2d(self._array)

        if add_extra_column:
            self._array = numpy.c_[self._array, numpy.ones(self._array.shape[0])]

        assert self._array.shape[1] == 3, 'Array shape error'

    @property
    def index(self) -> numpy.ndarray:
        return self._array[:, 0:2].astype(int)

    @property
    def index_with_label(self) -> numpy.ndarray:
        return numpy.c_[self.label, self.index].astype(int)

    @property
    def i(self) -> numpy.ndarray:
        return self._array[:, 0].astype(int)

    @property
    def j(self) -> numpy.ndarray:
        return self._array[:, 1].astype(int)

    @property
    def values(self) -> numpy.ndarray:
        return self._array[:, 2]

    @property
    def size(self):
        return self.i.size

    @values.setter
    def values(self, value) -> numpy.ndarray:
        self._array[:, 2] = value

    def delete(self, index):
        self._array = numpy.delete(self._array, index.astype(int), axis=0)

    def append(self, other):
        self._array = numpy.r_[self._array, other._array]

    def __add__(self, other) -> 'Triplet':
        """
        The methode concatenate the two triplet array and
        reduce if any coinciding index values.
        """

        new_array = numpy.r_[self._array, other._array]

        new_triplet = Triplet(new_array)

        return new_triplet.remove_duplicate()

    def add_triplet(self, *others) -> 'Triplet':
        others_array = (other._array for other in others)

        self._array = numpy.r_[(self._array, *others_array)]

        self.merge_duplicate()

    def remove_duplicate(self) -> 'Triplet':
        new_array = self._array
        index_to_delete = []
        duplicate = self.get_duplicate_index()

        if duplicate.size == 0:
            return Triplet(self._array)

        for duplicate in duplicate:
            index_to_keep = duplicate[0]
            for index_to_merge in duplicate[1:]:
                index_to_delete.append(index_to_merge)
                new_array[index_to_keep, 2] += new_array[index_to_merge, 2]

        triplet_array = numpy.delete(new_array, index_to_delete, axis=0)

        return Triplet(triplet_array)

    def coincide_i(self, mask) -> 'Triplet':
        """
        The methode removing all index i which do not coincide with the
        other triplet
        """
        mask_i = numpy.unique(mask.i[mask.values != 0])

        temp = (self._array[self.i == i] for i in mask_i)

        self._array = numpy.r_[tuple(temp)]

    def __sub__(self, other) -> 'Triplet':
        """
        The methode removing index[i] (rows) value corresponding between the two triplets.
        It doesn't change the other triplet, only the instance that called the method.
        """
        index_duplicate = numpy.isin(self.i, other.i)
        index_duplicate = numpy.arange(self.size)[index_duplicate]

        triplet_array = numpy.delete(self._array, index_duplicate, axis=0)

        return Triplet(triplet_array)

    def __iter__(self):
        for i, j, value in self._array:
            yield (int(i), int(j)), value

    def enumerate(self, start=None, stop=None):
        for n, (i, j, value) in enumerate(self._array[start:stop, :]):
            yield n, (int(i), int(j), value)

    def get_duplicate_index(self) -> numpy.ndarray:

        _, inverse, count = numpy.unique(self.index, axis=0, return_inverse=True, return_counts=True)

        index_duplicate = numpy.where(count > 1)[0]

        rows, cols = numpy.where(inverse == index_duplicate[:, numpy.newaxis])

        _, inverse_rows = numpy.unique(rows, return_index=True)

        return numpy.asarray(numpy.split(cols, inverse_rows[1:]), dtype=object)

    def merge_duplicate(self):
        duplicates = self.get_duplicate_index()

        if numpy.size(duplicates) == 0:
            return self._array

        for duplicate in duplicates:  # merge values
            self._array[int(duplicate[0]), 2] = self._array[duplicate.astype(int)][:, 2].sum()

        duplicates = [d[1:] for d in duplicates]

        self._array = numpy.delete(self._array, numpy.concatenate(duplicates).astype(int), axis=0)

    @property
    def max_i(self) -> int:
        """
        Return max i value, which is the first element of the index format.
        """
        return self.i.max()

    @property
    def max_j(self) -> int:
        """
        Return max j value, which is the second element of the index format.
        """
        return self.j.max()

    @property
    def min_i(self) -> float:
        """
        Return min i value, which is the first element of the index format.
        """
        return self.i.min()

    @property
    def min_j(self) -> float:
        """
        Return max j value, which is the second element of the index format.
        """
        return self.j.min()

    def to_dense(self, max_i: int = None, max_j: int = None) -> numpy.ndarray:
        """
        Return dense representation of the triplet, if none of max_i and max_j is provided
        it assumes the max_i and max_j is the shape of the dense matrix.
        """
        max_i = self.max_i + 1 if max_i is None else max_i
        max_j = self.max_j + 1 if max_j is None else max_j

        matrix = numpy.zeros([max_i, max_j])
        for index, value in self:
            matrix[index] = value

        return matrix

    def plot(self, max_i: int = None, max_j: int = None) -> None:
        """
        Plot the dense matrix representation of the triplet.
        """
        max_i = self.max_i + 1 if max_i is None else max_i
        max_j = self.max_j + 1 if max_j is None else max_j

        figure = Scene2D(unit_size=(6, 6), tight_layout=True)
        colorbar = ColorBar(discreet=False, position='right', numeric_format='%.4f')

        ax = Axis(row=0,
                  col=0,
                  title='Finite-difference coefficients structure',
                  show_legend=False,
                  show_grid=True,
                  colorbar=colorbar)

        artist = Mesh(scalar=numpy.flip(self.to_dense(max_i, max_j), axis=[0]), colormap='Blues')

        ax.AddArtist(artist)

        figure.AddAxes(ax)

        figure.Show()





class DiagonalTriplet(Triplet):
    def __init__(self, mesh: numpy.ndarray):
        size = mesh.size
        triplet_array = numpy.zeros([size, 3])
        triplet_array[:, 0] = numpy.arange(size)
        triplet_array[:, 1] = numpy.arange(size)
        triplet_array[:, 2] = mesh.ravel()

        super().__init__(triplet_array)

# -
