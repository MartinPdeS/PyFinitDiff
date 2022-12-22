#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest.mock import patch
from PyFinitDiff.Dense import FiniteDifference2D as DenseFD
from PyFinitDiff.Sparse import FiniteDifference2D as SparseFD
import tracemalloc


def test_memory_monitoring_dense_0():
    tracemalloc.start()
    instance = DenseFD(n_x=5, n_y=5, dx=1, dy=1, derivative=2, accuracy=2)

    instance.construct_matrix()
    instance.debug = False

    current, peak = tracemalloc.get_traced_memory()

    print(f'Current memory use: {current * 1e-6:.1f}MB \t peak memory use: {peak * 1e-6:.1f}MB')

    tracemalloc.stop()

    return instance.M.todense()


def test_memory_monitoring_sparse_0():
    tracemalloc.start()
    instance = SparseFD(n_x=5, n_y=5, dx=1, dy=1, derivative=2, accuracy=2)

    instance.construct_matrix()
    instance.debug = True

    current, peak = tracemalloc.get_traced_memory()

    print(f'Current memory use: {current * 1e-6:.1f}MB \t peak memory use: {peak * 1e-6:.1f}MB')

    tracemalloc.stop()

    return instance.M.todense()


def test_compare_sparse_dense_0():
    kwargs = {'n_x': 5, 'n_y': 5, 'dx': 1, 'dy': 1, 'derivative': 2, 'accuracy': 2}

    sparse_instance = SparseFD(**kwargs, symmetries={'left': 1, 'right': 1, 'top': 1, 'bottom': 1})
    dense_instance = DenseFD(**kwargs, symmetries={'left': 1, 'right': 1, 'top': 1, 'bottom': 1})

    # dense_instance.construct_matrix()
    sparse_instance.construct_matrix()

    # assert (sparse_instance.M.todense() == dense_instance.M.todense()).all(), "Error: Finit difference matrix generation sparse and dense do not match!"
    print('test finished')


def test_compare_sparse_dense_1():
    kwargs = {'n_x': 6, 'n_y': 5, 'dx': 1, 'dy': 1, 'derivative': 2, 'accuracy': 2}

    sparse_instance = SparseFD(**kwargs)
    dense_instance = DenseFD(**kwargs)

    # dense_instance.construct_matrix()
    sparse_instance.construct_matrix()

    assert (sparse_instance.M.todense() == dense_instance.M.todense()).all(), "Error: Finit difference matrix generation sparse and dense do not match!"
    print('test finished')


def test_compare_sparse_dense_2():
    kwargs = {'n_x': 6, 'n_y': 5, 'dx': 2, 'dy': 1, 'derivative': 2, 'accuracy': 2}

    sparse_instance = SparseFD(**kwargs)
    dense_instance = DenseFD(**kwargs)

    dense_instance.construct_matrix()
    sparse_instance.construct_matrix()

    assert (sparse_instance.M.todense() == dense_instance.M.todense()).all(), "Error: Finit difference matrix generation sparse and dense do not match!"
    print('test finished')


def test_compare_sparse_dense_3():
    kwargs = {'n_x': 6, 'n_y': 5, 'dx': 2, 'dy': 1, 'derivative': 2, 'accuracy': 2}

    sparse_instance = SparseFD(**kwargs)
    dense_instance = DenseFD(**kwargs)

    dense_instance.construct_matrix()
    sparse_instance.construct_matrix()

    assert (sparse_instance.M.todense() == dense_instance.M.todense()).all(), "Error: Finit difference matrix generation sparse and dense do not match!"
    print('test finished')


def test_compare_sparse_dense_4():
    kwargs = {'n_x': 12, 'n_y': 12, 'dx': 2, 'dy': 1, 'derivative': 2, 'accuracy': 4}

    sparse_instance = SparseFD(**kwargs)
    dense_instance = DenseFD(**kwargs)

    dense_instance.construct_matrix()
    sparse_instance.construct_matrix()

    assert (sparse_instance.M.todense() == dense_instance.M.todense()).all(), "Error: Finit difference matrix generation sparse and dense do not match!"
    print('test finished')


test_compare_sparse_dense_0()
# test_compare_sparse_dense_1()
# test_compare_sparse_dense_2()
# test_compare_sparse_dense_3()
# test_compare_sparse_dense_4()


# -
