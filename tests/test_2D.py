#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyFinitDiff.Sparse2D import FiniteDifference2D as SparseFD

test_kwargs = {'n_x': 20, 'n_y': 20, 'dx': 1, 'dy': 1}

boundaries_0 = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}


def test_compare_sparse_dense_0():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=2,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_1():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=4,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_2():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=2,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_3():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=4,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_4():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=6,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


boundaries_1 = {'left': 1, 'right': 0, 'top': 0, 'bottom': 0}


def test_compare_sparse_dense_5():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=2,
                               boundaries=boundaries_1)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_6():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=4,
                               boundaries=boundaries_1)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_7():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=2,
                               boundaries=boundaries_1)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_8():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=4,
                               boundaries=boundaries_1)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_9():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=6,
                               boundaries=boundaries_1)

    sparse_instance._construct_triplet_()


boundaries_2 = {'left': -1, 'right': 0, 'top': 0, 'bottom': 0}


def test_compare_sparse_dense_10():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=2,
                               boundaries=boundaries_2)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_11():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=4,
                               boundaries=boundaries_2)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_12():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=2,
                               boundaries=boundaries_2)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_13():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=4,
                               boundaries=boundaries_2)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_14():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=6,
                               boundaries=boundaries_2)

    sparse_instance._construct_triplet_()


boundaries_3 = {'left': -1, 'right': 0, 'top': 1, 'bottom': 0}


def test_compare_sparse_dense_15():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=2,
                               boundaries=boundaries_3)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_16():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=4,
                               boundaries=boundaries_3)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_17():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=2,
                               boundaries=boundaries_3)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_18():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=4,
                               boundaries=boundaries_3)

    sparse_instance._construct_triplet_()


def test_compare_sparse_dense_19():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=6,
                               boundaries=boundaries_3)

    sparse_instance._construct_triplet_()

# -
