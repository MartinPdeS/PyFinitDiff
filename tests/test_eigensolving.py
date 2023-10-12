#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy.sparse import linalg


from PyFinitDiff.sparse2D import FiniteDifference2D
from PyFinitDiff.utils import get_2D_circular_mesh_triplet
from PyFinitDiff.boundaries import Boundaries2D

test_kwargs = {
    'plot': False,
    'n_x': 40,
    'n_y': 40,
    'value0': 1,
    'value1': 5 * 1.4444,
    'radius': 70
}


def test_compute_eigenmode_sparse_0():
    n_x = n_y = 40
    value0 = 1.
    value1 = 1.4444
    radius = 70
    x_offset = y_offset = 0
    boundaries = Boundaries2D()

    sparse_instance = FiniteDifference2D(
        n_x=n_x,
        n_y=n_y,
        dx=1,
        dy=1,
        derivative=2,
        accuracy=2,
        boundaries=boundaries
    )

    mesh_triplet = get_2D_circular_mesh_triplet(
        n_x=n_x,
        n_y=n_y,
        value0=value0,
        value1=value1,
        x_offset=x_offset,
        y_offset=y_offset,
        radius=radius
    )

    dynamic_triplet = sparse_instance.triplet + mesh_triplet

    eigen_values, eigen_vectors = linalg.eigs(
        dynamic_triplet.to_dense(),
        k=5,
        which='LM',
        sigma=value1
    )

    return None

# -
