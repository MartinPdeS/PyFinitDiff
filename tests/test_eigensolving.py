#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
import matplotlib.pyplot as plt
from numpy import linalg as LA
from scipy.sparse import linalg

from unittest.mock import patch
from PyFinitDiff.Sparse import FiniteDifference2D as SparseFD



def test_compute_eigenmode_0():
    kwargs = {'n_x': 15, 'n_y': 15, 'dx': 1, 'dy': 1, 'derivative': 2, 'accuracy': 2}

    sparse_instance = SparseFD(**kwargs)

    triplet = sparse_instance.get_triplet()

    EigenValues, EigenVectors = linalg.eigs(triplet.to_dense(), k=5)

    fig, axes = plt.subplots(1, EigenValues.size, figsize=(10, 5))

    shape = kwargs['n_x'], kwargs['n_y']

    for i, ax in enumerate(axes[:-1]):
        Vector = EigenVectors.T[i].real.reshape(shape).T
        Vector = numpy.flip(Vector, -1)
        ax.imshow(Vector.T)

    plt.show()


test_compute_eigenmode_0()

# -
