#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy.sparse import linalg


from PyFinitDiff.Sparse2D import FiniteDifference2D
from PyFinitDiff.Utils import get_2D_circular_mesh_triplet


test_kwargs = {'plot': False, 'n_x': 40, 'n_y': 40, 'value0': 1, 'value1': 5 * 1.4444, 'radius': 70}


def test_compute_eigenmode_sparse_0():
    n_x = n_y = 40
    value0 = 1.
    value1 = 1.4444
    radius = 70
    x_offset = y_offset = 0
    symmetries = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}

    sparse_instance = FiniteDifference2D(n_x=n_x, n_y=n_y, dx=1, dy=1, derivative=2, accuracy=2, symmetries=symmetries)

    sparse_instance.triplet.plot()
    # mesh_triplet = get_2D_circular_mesh_triplet(n_x=n_x, n_y=n_y, value0=value0, value1=value1, x_offset=x_offset, y_offset=y_offset, radius=radius)

    # dynamic_triplet = sparse_instance.triplet + mesh_triplet

    # eigen_values, eigen_vectors = linalg.eigs(dynamic_triplet.to_dense(), k=5, which='LM', sigma=value1)

    # return None

test_compute_eigenmode_sparse_0()

# -
