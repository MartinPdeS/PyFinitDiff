#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
import matplotlib.pyplot as plt
from scipy.sparse import linalg

from unittest.mock import patch
from PyFinitDiff.Sparse import FiniteDifference2D as SparseFD, DiagonalTriplet
from PyFinitDiff.Dense import FiniteDifference2D as DenseFD
from PyFinitDiff.Utils import plot_mesh

def get_circular_mesh_triplet(n_x: int,
                              n_y: int,
                              radius: float,
                              x_offset: float = 0,
                              y_offset: float = 0,
                              value0: float = 0,
                              value1: float = 1,
                              plot: bool = False):

    x, y = numpy.mgrid[-100:100:complex(n_x),
                       -100:100:complex(n_y)]

    r = numpy.sqrt((x - x_offset)**2 + (y - y_offset)**2)
    mesh = numpy.ones(x.shape) * value0
    mesh[r < radius] = value1
    if plot:
        plt.figure()
        plt.pcolormesh(x[:, 0], y[0, :], mesh.T)
        plt.show()

    return DiagonalTriplet(mesh)


def test_compute_eigenmode_sparse_0(n_x: int,
                              n_y: int,
                              radius: float,
                              x_offset: float = 0,
                              y_offset: float = 0,
                              value0: float = 0,
                              value1: float = 1,
                              plot: bool = False):

    sparse_instance = SparseFD(n_x=n_x, n_y=n_y, dx=1, dy=1, derivative=2, accuracy=2)

    s = 0
    sparse_instance.symmetries = {'left': s, 'right': s, 'top': s, 'bottom': s}

    laplacian_triplet = sparse_instance.get_triplet()
    laplacian_triplet.plot()

    mesh_triplet = get_circular_mesh_triplet(n_x=n_x, n_y=n_y, value0=value0, value1=value1, x_offset=x_offset, y_offset=y_offset, radius=radius)
    mesh_triplet.values *= 5

    dynamic_triplet = laplacian_triplet + mesh_triplet
    eigen_values, eigen_vectors = linalg.eigs(dynamic_triplet.to_dense(), k=5, which='LM')

    if plot:
        fig, axes = plt.subplots(1, eigen_values.size, figsize=(10, 5))

        shape = [n_x, n_y]

        for i, ax in enumerate(axes[:]):
            Vector = eigen_vectors.T[i].real.reshape(shape).T
            Vector = numpy.flip(Vector, -1)
            ax.imshow(Vector.T)
            ax.set_title(f'eigen_values: {eigen_values[i]}')

        plt.show()


def test_compute_eigenmode_dense_0(n_x: int,
                              n_y: int,
                              radius: float,
                              x_offset: float = 0,
                              y_offset: float = 0,
                              value0: float = 0,
                              value1: float = 1,
                              plot: bool = False):

    FD_instance = DenseFD(n_x=n_x, n_y=n_y, dx=1, dy=1, derivative=2, accuracy=2)

    s = 0
    FD_instance.symmetries = {'left': s, 'right': s, 'top': s, 'bottom': s}

    FD_instance.construct_matrix()

    mesh_triplet = get_circular_mesh_triplet(n_x=n_x, n_y=n_y, value0=value0, value1=value1, x_offset=x_offset, y_offset=y_offset, radius=radius)

    dynamic_triplet = FD_instance.M.todense()

    plot_mesh(dynamic_triplet)
    numpy.fill_diagonal(dynamic_triplet, mesh_triplet.to_dense().diagonal())

    eigen_values, eigen_vectors = linalg.eigs(dynamic_triplet, k=5, which='LM')

    if plot:
        fig, axes = plt.subplots(1, eigen_values.size, figsize=(10, 5))

        shape = [n_x, n_y]

        for i, ax in enumerate(axes[:]):
            Vector = eigen_vectors.T[i].real.reshape(shape).T
            Vector = numpy.flip(Vector, -1)
            ax.imshow(Vector.T)
            ax.set_title(f'eigen_values: {eigen_values[i]}')

        plt.show()


test_compute_eigenmode_sparse_0(n_x=7, n_y=7, value0=1, value1=5 * 1.4444, radius=50, x_offset=100)
test_compute_eigenmode_dense_0(n_x=7, n_y=7, value0=1, value1=5 * 1.4444, radius=50, x_offset=100)

# -
