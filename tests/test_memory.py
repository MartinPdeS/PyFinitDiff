#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest.mock import patch
from PyFinitDiff.Dense import FiniteDifference2D as DenseFD
from PyFinitDiff.Sparse import FiniteDifference2D as SparseFD
import tracemalloc


test_kwargs = {'n_x': 20, 'n_y': 20, 'dx': 1, 'dy': 1, 'derivative': 2, 'accuracy': 2}
def test_memory_monitoring_dense_0():
    tracemalloc.start()
    instance = DenseFD(**test_kwargs)

    instance.construct_matrix()
    instance.debug = False

    current, peak = tracemalloc.get_traced_memory()

    print(f'Current memory use: {current * 1e-6:.1f}MB \t peak memory use: {peak * 1e-6:.1f}MB')

    tracemalloc.stop()


def test_memory_monitoring_sparse_0():
    tracemalloc.start()
    sparse_instance = SparseFD(**test_kwargs, symmetries={'left': 0, 'right': 0, 'top': 0, 'bottom': 0})

    current, peak = tracemalloc.get_traced_memory()

    sparse_instance._construct_triplet_()

    print(f'Current memory use: {current * 1e-6:.1f}MB \t peak memory use: {peak * 1e-6:.1f}MB')

    tracemalloc.stop()


# -
