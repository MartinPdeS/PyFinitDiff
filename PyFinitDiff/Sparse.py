import numpy
import scipy
import matplotlib.pyplot as plt
from scipy import sparse
from dataclasses import dataclass, field
from typing import Dict

from PyFinitDiff.Utils import NameSpace
from PyFinitDiff.Coefficients import FinitCoefficients
from PyFinitDiff.Utils import plot_mesh


class Triplet():
    def __init__(self, array: numpy.ndarray, add_extra_column=None):
        self._array = numpy.asarray(array)
        self._array = numpy.atleast_2d(self._array)
        if add_extra_column:
            self._array = numpy.c_[self._array, numpy.ones(self._array.shape[0])]

    @property
    def index(self) -> numpy.ndarray:
        return self._array[:, :2].astype(int)

    @property
    def i(self) -> numpy.ndarray:
        return self._array[:, 0].astype(int)

    @property
    def j(self) -> numpy.ndarray:
        return self._array[:, 1].astype(int)

    @property
    def values(self) -> numpy.ndarray:
        return self._array[:, 2]

    def delete(self, index):
        self._array = numpy.delete(self._array, index.astype(int), axis=0)

    def append(self, other):
        self._array = numpy.r_[self._array, other._array]

    def __add__(self, other):
        """
        The methode concatenate the two triplet array and
        reduce if any coinciding index values.
        """
        self.append(other)

        self.remove_duplicate()

        return self

    def remove_duplicate(self):
        duplicate = self.get_duplicate_index()

        for (d0, i0, j0, v0), (d1, i1, j1, v1) in duplicate:
            self._array[int(d0), 2] = v0 + v1

        self.delete(index=duplicate[:, 1, 0])

    def __sub__(self, other):
        """
        The methode removing index[i] (rows) value corresponding between the two triplets.
        It doesn't change the other triplet, only the instance that called the method.
        """
        new_triplet = self._array
        index_to_remove = []
        for n_0, tri_0 in enumerate(self.i):
            if tri_0 in other.i:
                index_to_remove.append(n_0)

        new_triplet = numpy.delete(new_triplet, index_to_remove, axis=0)

        return Triplet(new_triplet)

    def __iter__(self):
        for i, j, value in self._array:
            yield (int(i), int(j)), value

    def enumerate(self, start=None, stop=None):
        for n, (i, j, value) in enumerate(self._array[start:stop, :]):
            yield n, (int(i), int(j), value)

    def get_duplicate_index(self):
        duplicate = []
        for n_0, tri_0 in self.enumerate():
            for n_1, tri_1 in self.enumerate(stop=n_0):
                if numpy.all(tri_0[0:2] == tri_1[0:2]):
                    duplicate.append(((n_0, *tri_0), (n_1, *tri_1)))

        return numpy.asarray(duplicate)

    def reduce(self):
        """
        Remove identical triplet with identical index. Warning this means
        this method doesn't care about the value of the triplet
        """
        new_triplet = numpy.asarray([[None, None, None]])

        for tri in self._array:
            if not numpy.any(numpy.all(tri == new_triplet, axis=1)):
                new_triplet = numpy.r_[new_triplet, [tri]]

        return Triplet(numpy.asarray(new_triplet)[1:])

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

        from pylab import cm
        cmap = cm.get_cmap('viridis', 101)

        figure, ax = plt.subplots(1, 1, figsize=(5, 5))

        mesh = self.to_dense(max_i, max_j)

        i_list = numpy.arange(0, max_i)
        j_list = numpy.arange(0, max_j)

        im0 = ax.pcolormesh(j_list, i_list, mesh, cmap=cmap)
        plt.gca().invert_yaxis()
        ax.set_aspect('equal')
        plt.colorbar(im0, ax=ax)
        ax.grid(True)

        plt.show()


@dataclass
class FiniteDifference2D():
    """
    Reference : ['math.toronto.edu/mpugh/Teaching/Mat1062/notes2.pdf']
    """
    n_x: int
    n_y: int
    dx: float = 1
    dy: float = 1
    derivative: int = 1
    accuracy: int = 2
    naive: bool = False
    symmetries: Dict[str, str] = field(default_factory=lambda: ({'left': 0, 'right': 0, 'top': 0, 'bottom': 0}))

    def __post_init__(self):
        self.finit_coefficient = FinitCoefficients(derivative=self.derivative, accuracy=self.accuracy)
        self.triplet = []
        self.debug = False

    @property
    def size(self):
        return self.n_y * self.n_x

    @property
    def shape(self):
        return [self.size, self.size]

    def _get_diagonal_triplet_(self, coefficients: dict, offset: int, symmetry, sign: int):
        triplet = []
        for idx, value in coefficients.items():
            if symmetry == 1:
                value = (value if idx == 0 else 2 * value if sign * idx > 0 else 0)
            if symmetry == -1:
                value = (value if idx == 0 else 0 if sign * idx < 0 else 0)
            if symmetry in [0, None]:
                value = value

            if idx < 0:
                for i in range(0, self.size + idx * offset):
                    triplet.append((i, i - idx * offset, value))
            if idx > 0:
                for i in range(0, self.size - idx * offset):
                    triplet.append((i + idx * offset, i, value))
            if idx == 0:
                for i in range(0, self.size):
                    triplet.append((i, i, value))

        return Triplet(triplet)

    def _set_boundary_(self, symmetry: int, offset: int, sign: int, coefficients: dict = None):
        triplet = []
        match symmetry:
            case 1:
                triplet = self._get_diagonal_triplet_(coefficients=coefficients, offset=offset, symmetry=symmetry, sign=sign)

            case -1:
                triplet = self._get_diagonal_triplet_(coefficients=coefficients, offset=offset, symmetry=symmetry, sign=sign)

            case 0:
                triplet = self._get_diagonal_triplet_(coefficients=coefficients, offset=offset, symmetry=symmetry, sign=sign)

            case None:
                triplet = self._get_diagonal_triplet_(coefficients=coefficients, offset=offset, symmetry=symmetry, sign=sign)

        return triplet

    def _set_top_boundary_(self):
        return self._set_boundary_(symmetry=self.symmetries['top'],
                                   coefficients=self.finit_coefficient.Forward(),
                                   offset=self.n_y,
                                   sign=+1)

    def _set_bottom_boundary_(self):
        return self._set_boundary_(symmetry=self.symmetries['bottom'],
                                  coefficients=self.finit_coefficient.Backward(),
                                  offset=self.n_y,
                                  sign=-1)

    def _set_right_boundary_(self):
        return self._set_boundary_(symmetry=self.symmetries['right'],
                                   coefficients=self.finit_coefficient.Backward(),
                                   offset=1,
                                   sign=+1)

    def _set_left_boundary_(self):
        return self._set_boundary_(symmetry=self.symmetries['left'],
                                   coefficients=self.finit_coefficient.Forward(),
                                   offset=1,
                                   sign=-1)

    def _compute_slices_idx_(self):
        for offset in range(1, self.finit_coefficient.offset_index + 1):
            x_idx, y_idx = numpy.mgrid[self.n_y - offset:self.size:self.n_y, 0:self.size]
            array = numpy.asarray([x_idx.ravel(), y_idx.ravel()]).T
            right_slice_triplet = Triplet(array, add_extra_column=True)

        for offset in range(0, self.finit_coefficient.offset_index):
            x_idx, y_idx = numpy.mgrid[offset:self.size:self.n_y, 0:self.size]
            array = numpy.asarray([x_idx.ravel(), y_idx.ravel()]).T
            left_slice_triplet = Triplet(array, add_extra_column=True)

        for offset in range(1, self.finit_coefficient.offset_index + 1):
            x_idx, y_idx = numpy.mgrid[self.size - offset * self.n_y:self.size, 0:self.size]
            array = numpy.asarray([x_idx.ravel(), y_idx.ravel()]).T
            top_slice_triplet = Triplet(array, add_extra_column=True)

        for offset in range(1, self.finit_coefficient.offset_index + 1):
            x_idx, y_idx = numpy.mgrid[0:offset * self.n_y, 0:self.size]
            array = numpy.asarray([x_idx.ravel(), y_idx.ravel()]).T
            bottom_slice_triplet = Triplet(array, add_extra_column=True)

        return right_slice_triplet, left_slice_triplet, top_slice_triplet, bottom_slice_triplet

    def _get_zeros_(self, n, type=float):
        return [numpy.zeros(self.shape).astype(type) for i in range(n)]

    def _generate_empty_meshes_(self):
        self.x_meshes = NameSpace(right=self._get_zeros_(1)[0],
                                  left=self._get_zeros_(1)[0],
                                  center=self._get_zeros_(1)[0])

        self.y_meshes = NameSpace(top=self._get_zeros_(1)[0],
                                  bottom=self._get_zeros_(1)[0],
                                  center=self._get_zeros_(1)[0])

    def _slices_meshes_(self):
        if self.naive:
            self.y_meshes.bottom = 0
            self.y_meshes.top = 0

            self.x_meshes.right = 0
            self.x_meshes.left = 0

        else:
            self.y_meshes.bottom[~self.slice_bottom] = 0
            self.y_meshes.top[~self.slice_top] = 0
            self.y_meshes.center[self.slice_bottom + self.slice_top] = 0

            self.x_meshes.right[~self.slice_right] = 0
            self.x_meshes.left[~self.slice_left] = 0
            self.x_meshes.center[self.slice_right + self.slice_left] = 0

    def _add_meshes_(self):
        self.M = (self.y_meshes.top + self.y_meshes.bottom + self.y_meshes.center) / (self.dx**self.finit_coefficient.derivative)  # Y derivative

        self.M += (self.x_meshes.left + self.x_meshes.right + self.x_meshes.center) / (self.dy**self.finit_coefficient.derivative)  # X derivative

        self.M = sparse.csr_matrix(self.M)

    def _get_y_diagonal_triplet_(self):
        return self._get_diagonal_triplet_(coefficients=self.finit_coefficient.Central(), offset=self.n_y, symmetry=None, sign=1)

    def _get_x_diagonal_triplet_(self):
        return self._get_diagonal_triplet_(coefficients=self.finit_coefficient.Central(), offset=1, symmetry=None, sign=1)

    def _construct_triplet_(self, Addmesh: numpy.ndarray = None):
        right_slice_triplet, left_slice_triplet, top_slice_triplet, bottom_slice_triplet = self._compute_slices_idx_()

        x_triplet = self._get_x_diagonal_triplet_()
        y_triplet = self._get_y_diagonal_triplet_()

        bottom_triplet = self._set_bottom_boundary_()
        top_triplet = self._set_top_boundary_()
        left_triplet = self._set_left_boundary_()
        right_triplet = self._set_right_boundary_()

        y_triplet = y_triplet - top_slice_triplet - bottom_slice_triplet

        x_triplet = x_triplet - left_slice_triplet - right_slice_triplet

        top_triplet -= y_triplet
        bottom_triplet -= y_triplet
        left_triplet -= x_triplet
        right_triplet -= x_triplet

        top_triplet = self._coincide_indices_(top_triplet, top_slice_triplet)
        bottom_triplet = self._coincide_indices_(bottom_triplet, bottom_slice_triplet)
        left_triplet = self._coincide_indices_(left_triplet, left_slice_triplet)
        right_triplet = self._coincide_indices_(right_triplet, right_slice_triplet)

        total_triplet = y_triplet + x_triplet + top_triplet + bottom_triplet + left_triplet + right_triplet
        # total_triplet.plot(max_i=self.size, max_j=self.size)
        return total_triplet

    def get_triplet(self):
        return self._construct_triplet_()

    def _coincide_indices_(self, triplet_0: Triplet, *triplets):
        new_triplet = []
        for triplet_1 in triplets:
            for idx_0, value in triplet_0:
                if idx_0[0] in triplet_1.i:
                    new_triplet.append([*idx_0, value])

        return Triplet(new_triplet)

    def _not_coincide_indices_(self, triplet_0: Triplet, *triplets):
        new_triplet = []
        for triplet_1 in triplets:
            for idx_0, value in triplet_0:
                if idx_0[0] not in triplet_1.i:
                    new_triplet.append([*idx_0, value])

            return Triplet(new_triplet)

    @property
    def Dense(self):
        return self.M

    @property
    def Sparse(self):
        return sparse.csr_matrix(self.M)

    def _to_triplet_(self):
        Coordinate = self.Sparse.tocoo()
        return numpy.array([Coordinate.col, Coordinate.row, Coordinate.data])

    def Plot(self, Text=False):
        from pylab import cm
        cmap = cm.get_cmap('viridis', 101)

        Figure, Axes = plt.subplots(1, 1, figsize=(10, 9))
        Axes.set_title('Finite-difference coefficients.')
        Data = self.M

        if isinstance(Data, scipy.sparse._csr.csr_matrix):
            Data = Data.todense()

        Axes.grid(True)
        im0 = Axes.imshow(Data, cmap=cmap)
        plt.colorbar(im0, ax=Axes)
        if Text:
            for (i, j), z in numpy.ndenumerate(Data.astype(float)):
                Axes.text(j, i, '{:.0e}'.format(z), ha='center', va='center', size=8)

        plt.show()

# -
