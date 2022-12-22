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
    def __init__(self, array: numpy.ndarray):
        self._array = numpy.asarray(array)

    @property
    def index(self):
        return self._array[:2]

    @property
    def values(self):
        return self._array[2]

    def __iter__(self):
        for i, j, value in self._array:
            yield (int(i), int(j)), value


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

    def _set_boundary_(self, symmetry: int, coefficient_none: dict, coefficient_0: dict, offset: int, sign: int):
        triplet = []
        match symmetry:
            case 1:
                triplet = self._get_diagonal_triplet_(coefficients=self.finit_coefficient.Central(), offset=offset, symmetry=symmetry, sign=sign)

            case -1:
                triplet = self._get_diagonal_triplet_(coefficients=self.finit_coefficient.Central(), offset=offset, symmetry=symmetry, sign=sign)

            case 0:
                triplet = self._get_diagonal_triplet_(coefficients=coefficient_0, offset=offset, symmetry=symmetry, sign=sign)

            case None:
                triplet = self._get_diagonal_triplet_(coefficients=coefficient_none, offset=offset, symmetry=symmetry, sign=sign)

        return triplet

    def _set_top_boundary_(self):
        return self._set_boundary_(symmetry=self.symmetries['top'],
                                   coefficient_none=self.finit_coefficient.Backward(),
                                   coefficient_0={0: -2, 1: 1},
                                   offset=self.n_y,
                                   sign=+1)

    def _set_bottom_boundary_(self):
        return self._set_boundary_(symmetry=self.symmetries['bottom'],
                                   coefficient_none=self.finit_coefficient.Forward(),
                                   coefficient_0={0: -2, -1: 1},
                                   offset=self.n_y,
                                   sign=-1)

    def _set_right_boundary_(self):
        return self._set_boundary_(symmetry=self.symmetries['right'],
                                   coefficient_none=self.finit_coefficient.Backward(),
                                   coefficient_0={0: -2, 1: 1},
                                   offset=1,
                                   sign=+1)

    def _set_left_boundary_(self):
        return self._set_boundary_(symmetry=self.symmetries['left'],
                                   coefficient_none=self.finit_coefficient.Forward(),
                                   coefficient_0={0: -2, -1: 1},
                                   offset=1,
                                   sign=-1)

    def _compute_slices_idx_(self):
        for offset in range(1, self.finit_coefficient.offset_index + 1):
            x_idx, y_idx = numpy.mgrid[self.n_y - offset:self.size:self.n_y, 0:self.size]
            right_idx = (x_idx.ravel(), y_idx.ravel())

        for offset in range(0, self.finit_coefficient.offset_index):
            x_idx, y_idx = numpy.mgrid[offset:self.size:self.n_y, 0:self.size]
            left_idx = (x_idx.ravel(), y_idx.ravel())

        for offset in range(1, self.finit_coefficient.offset_index + 1):
            x_idx, y_idx = numpy.mgrid[self.size - offset * self.n_y:self.size, 0:self.size]
            top_idx = (x_idx.ravel(), y_idx.ravel())

        for offset in range(1, self.finit_coefficient.offset_index + 1):
            x_idx, y_idx = numpy.mgrid[0:offset * self.n_y, 0:self.size]
            bottom_idx = (x_idx.ravel(), y_idx.ravel())

        return right_idx, left_idx, top_idx, bottom_idx

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

    def apply_idx_to_submeshes(self, right_idx, left_idx, top_idx, bottom_idx):
        self.slice_right[right_idx] = True
        self.slice_left[left_idx] = True
        self.slice_top[top_idx] = True
        self.slice_bottom[bottom_idx] = True

    def construct_matrix(self, Addmesh: numpy.ndarray = None):
        i, j = numpy.indices(self.shape)

        self.Index = NameSpace(i=i, j=j)
        self.slice_right, self.slice_left, self.slice_bottom, self.slice_top = self._get_zeros_(n=4, type=bool)

        indices = self._compute_slices_idx_()

        self.apply_idx_to_submeshes(*indices)

        self._generate_empty_meshes_()

        x_central_triplet = self._get_x_diagonal_triplet_()
        y_central_triplet = self._get_y_diagonal_triplet_()

        bottom_triplet = self._set_bottom_boundary_()
        top_triplet = self._set_top_boundary_()
        left_triplet = self._set_left_boundary_()
        right_triplet = self._set_right_boundary_()

        # self._not_coincide_indices_(x_central_index_values, x_central_index_values)
        self._coincide_indices_(right_triplet, x_central_triplet)

        for index, value in y_central_triplet:
            self.y_meshes.center[index] = value

        for index, value in x_central_triplet:
            self.x_meshes.center[index] = value

        for index, value in right_triplet:
            self.x_meshes.right[index] = value

        for index, value in left_triplet:
            self.x_meshes.left[index] = value

        for index, value in top_triplet:
            self.y_meshes.top[index] = value

        for index, value in bottom_triplet:
            self.y_meshes.bottom[index] = value

        # plot_mesh(self.y_meshes.top,
        #           self.y_meshes.bottom,
        #           self.x_meshes.right,
        #           self.x_meshes.left)

        self._slices_meshes_()

        self._add_meshes_()

    def _coincide_indices_(self, triplet_0, triplet_1):
        new_indices = []
        for idx_0 in triplet_0.index:
            if idx_0 in triplet_1.index:
                print('coincidence spotted', idx_0)
                new_indices.append(idx_0)

        return numpy.asarray(new_indices)

    def _not_coincide_indices_(self, indices_values_0, indices_values_1):
        new_indices = []
        for idx_0 in indices_values_0:
            if idx_0[0:2] not in indices_values_1[:, 0:2]:
                print('anti-coincidence spotted', idx_0)
                new_indices.append(idx_0)

        return numpy.asarray(new_indices)

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
