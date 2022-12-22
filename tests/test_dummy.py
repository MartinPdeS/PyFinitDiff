#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest.mock import patch
from PyFinitDiff.Dense import FiniteDifference2D
from PyFinitDiff.Sparse import SparseFiniteDifference2D
import tracemalloc


def test_memory_monitoring_dense_0():
    tracemalloc.start()
    instance = FiniteDifference2D(n_x=5, n_y=5, dx=1, dy=1, derivative=2, accuracy=2)

    instance.construct_matrix()
    instance.debug = False

    current, peak = tracemalloc.get_traced_memory()

    print(f'Current memory use: {current * 1e-6:.1f}MB \t peak memory use: {peak * 1e-6:.1f}MB')

    tracemalloc.stop()

    return instance.M.todense()


def test_memory_monitoring_sparse_0():
    tracemalloc.start()
    instance = SparseFiniteDifference2D(n_x=5, n_y=5, dx=1, dy=1, derivative=2, accuracy=2)

    instance.construct_matrix()
    instance.debug = True

    current, peak = tracemalloc.get_traced_memory()

    print(f'Current memory use: {current * 1e-6:.1f}MB \t peak memory use: {peak * 1e-6:.1f}MB')

    tracemalloc.stop()

    return instance.M.todense()


a = test_memory_monitoring_dense_0()

b = test_memory_monitoring_sparse_0()

assert (a == b).all(), "Error: Finit difference matrix generation sparse and dense do not match!"
# import numpy as np
# a = np.mgrid[0:10:2, 15:80]

# print(a)