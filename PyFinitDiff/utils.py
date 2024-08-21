import matplotlib.pyplot as plt
from collections.abc import Iterable
import numpy
import scipy

from PyFinitDiff.triplet import DiagonalTriplet


def plot_mesh(*meshes, text=False, title=''):
    figure, axes = plt.subplots(1, len(meshes), figsize=(5 * len(meshes), 5))

    if not isinstance(axes, Iterable):
        axes = [axes]

    for ax, mesh in zip(axes, meshes):

        if isinstance(mesh, scipy.sparse._csr.csr_matrix):
            mesh = mesh.todense()

        im0 = ax.imshow(mesh, cmap='viridis')
        plt.colorbar(im0, ax=ax)
        ax.set_title(f'FD:  {title}')
        ax.grid(True)

        if text:
            for (i, j), z in numpy.ndenumerate(mesh.astype(float)):
                ax.text(j, i, f'{z:.0f}', ha='center', va='center', size=8)

    plt.show()


def get_2D_circular_mesh_triplet(
        n_x: int,
        n_y: int,
        radius: float,
        x_offset: float = 0,
        y_offset: float = 0,
        value_out: float = 0,
        value_in: float = 1) -> DiagonalTriplet:
    """
    Gets a Triplet corresponding to a 2d mesh with
    circular structure of value_in inside and value_out outside.

    :param      n_x:       The number of point in the x-axis
    :type       n_x:       int
    :param      n_y:       The number of point in the y-axis
    :type       n_y:       int
    :param      radius:    The radius of the structure
    :type       radius:    float
    :param      x_offset:  The x offset of the circular structure
    :type       x_offset:  float
    :param      y_offset:  The y offset of the circular structure
    :type       y_offset:  float
    :param      value_in:  The value inside
    :type       value_in:  float
    :param      value_out: The value outside
    :type       value_out: float

    :returns:   The 2d circular mesh triplet.
    :rtype:     DiagonalTriplet
    """
    y, x = numpy.mgrid[
        -100:100:complex(n_y),
        -100:100:complex(n_x)
    ]

    r = numpy.sqrt((x - x_offset)**2 + (y - y_offset)**2)
    mesh = numpy.ones(x.shape) * value_out
    mesh[r < radius] = value_in

    return DiagonalTriplet(mesh, shape=x.shape)


def get_1D_circular_mesh_triplet(
        n_x: int,
        radius: float,
        x_offset: float = 0,
        value_out: float = 0,
        value_in: float = 1) -> DiagonalTriplet:
    """
    Gets a Triplet corresponding to a 1d mesh with
    circular structure of value_in inside and value_out outside.

    :param      n_x:        The number of point in the x-axis
    :type       n_x:        int
    :param      radius:     The radius of the structure
    :type       radius:     float
    :param      x_offset:   The x offset of the circular structure
    :type       x_offset:   float
    :param      value_out:  The value inside
    :type       value_out:  float
    :param      value_in:   The value outside
    :type       value_in:   float

    :returns:   The 1d circular mesh triplet.
    :rtype:     DiagonalTriplet
    """
    x = numpy.linspace(-100, 100, n_x)

    r = numpy.sqrt((x - x_offset)**2)
    mesh = numpy.ones(x.shape) * value_out
    mesh[r < radius] = value_in

    return DiagonalTriplet(mesh, shape=x.shape)

# -
