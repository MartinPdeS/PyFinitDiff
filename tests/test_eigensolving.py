#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy.sparse import linalg


from PyFinitDiff.sparse2D import FiniteDifference2D
from PyFinitDiff.utils import get_2D_circular_mesh_triplet
from PyFinitDiff.boundaries import Boundaries2D


def test_compute_eigenmode_sparse_0():
    n_x = n_y = 40

    sparse_instance = FiniteDifference2D(
        n_x=n_x,
        n_y=n_y,
        dx=1,
        dy=1,
        derivative=2,
        accuracy=2,
        boundaries=Boundaries2D()
    )

    mesh_triplet = get_2D_circular_mesh_triplet(
        n_x=n_x,
        n_y=n_y,
        value_in=1.0,
        value_out=1.4444,
        x_offset=0,
        y_offset=0,
        radius=70
    )

    dynamic_triplet = sparse_instance.triplet + mesh_triplet

    eigen_values, eigen_vectors = linalg.eigs(
        dynamic_triplet.to_dense(),
        k=5,
        which='LM',
        sigma=1.44
    )

# -
