import numpy as np
import numpy
import matplotlib.pyplot as plt
from scipy import sparse
from dataclasses import dataclass, field
from typing import Dict

from PyFinitDiff.utils import NameSpace
from PyFinitDiff.coefficients import FinitCoefficients


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

    @property
    def size(self):
        return self.n_y * self.n_x

    @property
    def shape(self):
        return [self.size, self.size]

    def _set_right_boundary_(self, symmetry, mesh):
        if symmetry in ['symmetric', 1]:
            for idx, value in self.finit_coefficient.Central().items():
                mesh[self.Index.i == self.Index.j + idx] = (value if idx == 0 else 2 * value if idx > 0 else 0)

        elif symmetry in ['anti_symmetric', -1]:
            for idx, value in self.finit_coefficient.Central().items():
                mesh[self.Index.i == self.Index.j + idx] = (value if idx == 0 else 0 if idx > 0 else 0)

        elif symmetry in ['zero', 0]:
            for idx, value in {0: -2, 1: 1}.items():
                mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        elif symmetry == 'none':
            for idx, value in self.finit_coefficient.Forward().items():
                mesh[self.Index.i == self.Index.j + idx] = value

        return mesh

    def _set_left_boundary_(self, symmetry, mesh):
        if symmetry in ['symmetric', 1]:
            for idx, value in self.finit_coefficient.Central().items():
                mesh[self.Index.i == self.Index.j + idx] = (value if idx == 0 else 2 * value if idx < 0 else 0)

        elif symmetry in ['anti_symmetric', -1]:
            for idx, value in self.finit_coefficient.Central().items():
                mesh[self.Index.i == self.Index.j + idx] = (value if idx == 0 else 0 if idx < 0 else 0)

        elif symmetry in ['zero', 0]:
            for idx, value in {0: -2, -1: 1}.items():
                mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        elif symmetry == 'none':
            for idx, value in self.finit_coefficient.Backward().items():
                mesh[self.Index.i == self.Index.j + idx] = value

        return mesh

    def _set_top_boundary_(self, symmetry, mesh):
        if symmetry in ['symmetric', 1]:
            for idx, value in self.finit_coefficient.Central().items():
                mesh[self.Index.i == self.Index.j + idx * self.n_y] = (value if idx == 0 else 2 * value if idx > 0 else 0)

        elif symmetry in ['anti_symmetric', -1]:
            for idx, value in self.finit_coefficient.Central().items():
                mesh[self.Index.i == self.Index.j + idx * self.n_y] = (value if idx == 0 else 0 if idx > 0 else 0)

        elif symmetry in ['zero', 0]:
            for idx, value in {0: -2, 1: 1}.items():
                mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        elif symmetry == 'none':
            for idx, value in self.finit_coefficient.Forward().items():
                mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        return mesh

    def _set_bottom_boundary_(self, symmetry, mesh):
        if symmetry in ['symmetric', 1]:
            for idx, value in self.finit_coefficient.Central().items():
                mesh[self.Index.i == self.Index.j + idx * self.n_y] = (value if idx == 0 else 2 * value if idx < 0 else 0)

        elif symmetry in ['anti_symmetric', -1]:
            for idx, value in self.finit_coefficient.Central().items():
                mesh[self.Index.i == self.Index.j + idx * self.n_y] = (value if idx == 0 else 0 if idx > 0 else 0)

        elif symmetry in ['zero', 0]:
            for idx, value in {0: -2, -1: 1}.items():
                mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        elif symmetry == 'none':
            for idx, value in self.finit_coefficient.Backward().items():
                mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        return mesh

    def _compute_slices_(self):
        self.slice_right, self.slice_left, self.slice_bottom, self.slice_top = self._get_zeros_(n=4, Type=bool)

        for offset in range(1, self.finit_coefficient.offset_index + 1):
            self.slice_right[self.n_y - offset::self.n_y, :] = True

        for offset in range(0, self.finit_coefficient.offset_index):
            self.slice_left[offset::self.n_y, :] = True

        for offset in range(1, self.finit_coefficient.offset_index + 1):
            self.slice_top[self.size - offset * self.n_y:, :] = True

        for offset in range(1, self.finit_coefficient.offset_index + 1):
            self.slice_bottom[:offset * self.n_y, :] = True

    def _get_x_diagonal_(self):
        for idx, value in self.finit_coefficient.Central().items():
            self.x_meshes.center[self.Index.i == self.Index.j + idx] = value

        self.x_meshes.right = self._set_right_boundary_(self.symmetries['right'], self.x_meshes.right)
        self.x_meshes.left = self._set_left_boundary_(self.symmetries['left'], self.x_meshes.left)

    def _get_zeros_(self, n, Type=float):
        return [np.zeros(self.shape).astype(Type) for i in range(n)]

    def _get_ones_(self, n, Type=float):
        return [np.ones(self.shape).astype(Type) for i in range(n)]

    def _compute_meshes_(self):
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

    def _get_y_diagonal_(self):
        for idx, value in self.finit_coefficient.Central().items():
            self.y_meshes.center[self.Index.i == self.Index.j - idx * self.n_y] = value

        self.y_meshes.top = self._set_top_boundary_(self.symmetries['top'], self.y_meshes.top)
        self.y_meshes.bottom = self._set_bottom_boundary_(self.symmetries['bottom'], self.y_meshes.bottom)

    def Plot(self, Text=False):
        from pylab import cm
        cmap = cm.get_cmap('viridis', 101)

        Figure, Axes = plt.subplots(1, 1, figsize=(10, 9))
        Axes.set_title('Finite-difference coefficients.')
        Data = self.M.todense()

        Axes.grid(True)
        im0 = Axes.imshow(Data, cmap=cmap)
        plt.colorbar(im0, ax=Axes)
        if Text:
            for (i, j), z in np.ndenumerate(Data.astype(float)):
                Axes.text(j, i, '{:.0e}'.format(z), ha='center', va='center', size=8)

        plt.show()

    def construct_matrix(self, Addmesh: numpy.ndarray = None):
        i, j = np.indices(self.shape)

        self.Index = NameSpace(i=i, j=j)

        self._compute_slices_()

        self._compute_meshes_()

        self._get_y_diagonal_()

        self._get_x_diagonal_()

        self._slices_meshes_()

        self._add_meshes_()

        # if Addmesh is not None:
            # np.fill_diagonal(self.M, self.M.diagonal() + Addmesh.flatten())

    @property
    def Dense(self):
        return self.M

    @property
    def Sparse(self):
        return sparse.csr_matrix(self.M)

    def _to_triplet_(self):
        Coordinate = self.Sparse.tocoo()
        return numpy.array([Coordinate.col, Coordinate.row, Coordinate.data])

