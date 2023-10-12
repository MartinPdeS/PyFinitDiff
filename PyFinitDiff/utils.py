import matplotlib.pyplot as plt
from collections.abc import Iterable
import numpy
import scipy

from PyFinitDiff.triplet import DiagonalTriplet


class NameSpace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class BoundaryClass:

    _acceptedValues = ['symmetric', 'anti_symmetric', 'zero', 'none', 1, -1, 0]

    def __init__(self, left='None', right='None', top='None', bottom='None'):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

    def __repr__(self):
        return f"symmetries \n{'-'*50} \n{self.top = }\n{self.bottom = }\n{self.left = }\n{self.right = }"

    def AssertValues(self, value):
        assert value in self.symmetries, f"Error unexpected symmetry value {value}. Accepted are {self.symmetries}"

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        assert value in self._acceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self._acceptedValues}"

        self._top = value

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        assert value in self._acceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self._acceptedValues}"

        self._bottom = value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        assert value in self._acceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self._acceptedValues}"

        self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        assert value in self._acceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self._acceptedValues}"

        self._right = value


def plot_mesh(*meshes, text=False, title=''):
    from pylab import cm
    cmap = cm.get_cmap('viridis', 101)

    figure, axes = plt.subplots(1, len(meshes), figsize=(5 * len(meshes), 5))

    if not isinstance(axes, Iterable):
        axes = [axes]

    for ax, mesh in zip(axes, meshes):

        if isinstance(mesh, scipy.sparse._csr.csr_matrix):
            mesh = mesh.todense()

        im0 = ax.imshow(mesh, cmap=cmap)
        plt.colorbar(im0, ax=ax)
        ax.set_title(f'FD:  {title}')
        ax.grid(True)

        if text:
            for (i, j), z in numpy.ndenumerate(mesh.astype(float)):
                ax.text(j, i, '{:.0f}'.format(z), ha='center', va='center', size=8)

    plt.show()


def get_2D_circular_mesh_triplet(n_x: int,
                                 n_y: int,
                                 radius: float,
                                 x_offset: float = 0,
                                 y_offset: float = 0,
                                 value0: float = 0,
                                 value1: float = 1):

    y, x = numpy.mgrid[-100:100:complex(n_y),
                       -100:100:complex(n_x)]

    r = numpy.sqrt((x - x_offset)**2 + (y - y_offset)**2)
    mesh = numpy.ones(x.shape) * value0
    mesh[r < radius] = value1

    return DiagonalTriplet(mesh)


def get_1D_circular_mesh_triplet(n_x: int,
                                 radius: float,
                                 x_offset: float = 0,
                                 value0: float = 0,
                                 value1: float = 1):

    x = numpy.linspace(-100, 100, n_x)

    r = numpy.sqrt((x - x_offset)**2)
    mesh = numpy.ones(x.shape) * value0
    mesh[r < radius] = value1

    return DiagonalTriplet(mesh)

# -
