import numpy as np
import numpy
import matplotlib.pyplot as plt
from scipy import sparse
from dataclasses import dataclass, field
from typing import Dict

from PyFinitDiff.Utils import NameSpace
from PyFinitDiff.Coefficients import FinitCoefficients


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
    symmetries: Dict[str, str] = field(default_factory=lambda: ({'left': None, 'right': None, 'top': None, 'bottom': None}))

    def __post_init__(self):
        self.FinitCoefficients = FinitCoefficients(derivative=self.derivative, accuracy=self.accuracy)

    @property
    def Size(self):
        return self.n_y * self.n_x

    @property
    def Shape(self):
        return [self.Size, self.Size]

    def _set_right_boundary_(self, Value, Mesh):
        if Value in ['Symmetric', 1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j + idx] = (value if idx == 0 else 2 * value if idx > 0 else 0)

        elif Value in ['AntiSymmetric', -1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j + idx] = (value if idx == 0 else 0 if idx > 0 else 0)

        elif Value in ['Zero', 0]:
            for idx, value in {0: -2, 1: 1}.items():
                Mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        elif Value == 'None':
            for idx, value in self.FinitCoefficients.Forward().items():
                Mesh[self.Index.i == self.Index.j + idx] = value

        return Mesh

    def _set_left_boundary_(self, Value, Mesh):
        if Value in ['Symmetric', 1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j + idx] = (value if idx == 0 else 2 * value if idx < 0 else 0)

        elif Value in ['AntiSymmetric', -1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j + idx] = (value if idx == 0 else 0 if idx < 0 else 0)

        elif Value in ['Zero', 0]:
            for idx, value in {0: -2, -1: 1}.items():
                Mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        elif Value == 'None':
            for idx, value in self.FinitCoefficients.Backward().items():
                Mesh[self.Index.i == self.Index.j + idx] = value

        return Mesh

    def _set_top_boundary_(self, Value, Mesh):
        if Value in ['Symmetric', 1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j + idx * self.n_y] = (value if idx == 0 else 2 * value if idx > 0 else 0)

        elif Value in ['AntiSymmetric', -1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j + idx * self.n_y] = (value if idx == 0 else 0 if idx > 0 else 0)

        elif Value in ['Zero', 0]:
            for idx, value in {0: -2, 1: 1}.items():
                Mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        elif Value == 'None':
            for idx, value in self.FinitCoefficients.Forward().items():
                Mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        return Mesh

    def _set_bottom_boundary_(self, Value, Mesh):
        if Value in ['Symmetric', 1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j + idx * self.n_y] = (value if idx == 0 else 2 * value if idx < 0 else 0)

        elif Value in ['AntiSymmetric', -1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j + idx * self.n_y] = (value if idx == 0 else 0 if idx > 0 else 0)

        elif Value in ['Zero', 0]:
            for idx, value in {0: -2, -1: 1}.items():
                Mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        elif Value == 'None':
            for idx, value in self.FinitCoefficients.Backward().items():
                Mesh[self.Index.i == self.Index.j + idx * self.n_y] = value

        return Mesh

    def _compute_slices_(self):
        self.Sliceright, self.Sliceleft, self.Slicebottom, self.Slicetop = self._get_zeros_(n=4, Type=bool)

        for Offset in range(1, self.FinitCoefficients.OffsetIndex + 1):
            self.Sliceright[self.n_y - Offset::self.n_y, :] = True

        for Offset in range(0, self.FinitCoefficients.OffsetIndex):
            self.Sliceleft[Offset::self.n_y, :] = True

        for Offset in range(1, self.FinitCoefficients.OffsetIndex + 1):
            self.Slicetop[self.Size - Offset * self.n_y:, :] = True

        for Offset in range(1, self.FinitCoefficients.OffsetIndex + 1):
            self.Slicebottom[:Offset * self.n_y, :] = True

    def _get_x_diagonal_(self):
        for idx, value in self.FinitCoefficients.Central().items():
            self.XMeshes.Center[self.Index.i == self.Index.j + idx] = value

        self.XMeshes.right = self._set_right_boundary_(self.symmetries['right'], self.XMeshes.right)
        self.XMeshes.left = self._set_left_boundary_(self.symmetries['left'], self.XMeshes.left)

    def _get_zeros_(self, n, Type=float):
        return [np.zeros(self.Shape).astype(Type) for i in range(n)]

    def _get_ones_(self, n, Type=float):
        return [np.ones(self.Shape).astype(Type) for i in range(n)]

    def _compute_meshes_(self):
        self.XMeshes = NameSpace(right=self._get_zeros_(1)[0],
                                 left=self._get_zeros_(1)[0],
                                 Center=self._get_zeros_(1)[0])

        self.YMeshes = NameSpace(top=self._get_zeros_(1)[0],
                                 bottom=self._get_zeros_(1)[0],
                                 Center=self._get_zeros_(1)[0])

    def _slices_meshes_(self):
        if self.naive:
            self.YMeshes.bottom = 0
            self.YMeshes.top = 0

            self.XMeshes.right = 0
            self.XMeshes.left = 0

        else:
            self.YMeshes.bottom[~self.Slicebottom] = 0
            self.YMeshes.top[~self.Slicetop] = 0
            self.YMeshes.Center[self.Slicebottom + self.Slicetop] = 0

            self.XMeshes.right[~self.Sliceright] = 0
            self.XMeshes.left[~self.Sliceleft] = 0
            self.XMeshes.Center[self.Sliceright + self.Sliceleft] = 0

    def _add_meshes_(self):
        self.M = (self.YMeshes.top + self.YMeshes.bottom + self.YMeshes.Center) / (self.dx**self.FinitCoefficients.derivative)  # Y derivative

        self.M += (self.XMeshes.left + self.XMeshes.right + self.XMeshes.Center) / (self.dy**self.FinitCoefficients.derivative)  # X derivative

    def _get_y_diagonal_(self):
        for idx, value in self.FinitCoefficients.Central().items():
            self.YMeshes.Center[self.Index.i == self.Index.j - idx * self.n_y] = value

        self.YMeshes.top = self._set_top_boundary_(self.symmetries['top'], self.YMeshes.top)
        self.YMeshes.bottom = self._set_bottom_boundary_(self.symmetries['bottom'], self.YMeshes.bottom)

    def Plot(self, Text=False):
        from pylab import cm
        cmap = cm.get_cmap('viridis', 101)

        Figure, Axes = plt.subplots(1, 1, figsize=(10, 9))
        Axes.set_title('Finite-difference coefficients.')
        Data = self.M

        Axes.grid(True)
        im0 = Axes.imshow(Data, cmap=cmap)
        plt.colorbar(im0, ax=Axes)
        if Text:
            for (i, j), z in np.ndenumerate(Data.astype(float)):
                Axes.text(j, i, '{:.0e}'.format(z), ha='center', va='center', size=8)

        plt.show()

    def Compute(self, AddMesh: numpy.ndarray = None):
        i, j = np.indices(self.Shape)

        self.Index = NameSpace(i=i, j=j)

        self._compute_slices_()

        self._compute_meshes_()

        self._get_y_diagonal_()

        self._get_x_diagonal_()

        self._slices_meshes_()

        self._add_meshes_()

        # if AddMesh is not None:
            # np.fill_diagonal(self.M, self.M.diagonal() + AddMesh.flatten())

    @property
    def Dense(self):
        return self.M

    @property
    def Sparse(self):
        return sparse.csr_matrix(self.M) 

    def _to_triplet_(self):
        Coordinate = self.Sparse.tocoo()
        return numpy.array([Coordinate.col, Coordinate.row, Coordinate.data])
