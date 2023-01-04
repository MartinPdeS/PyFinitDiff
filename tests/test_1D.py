#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyFinitDiff.Sparse1D import FiniteDifference1D as SparseFD

test_kwargs = {'n_x': 20, 'dx': 1}

boundaries_0 = {'left': 0, 'right': 0}


def test_0():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=2,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_1():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=4,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_2():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=2,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_3():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=4,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_4():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=6,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


boundaries_1 = {'left': 1, 'right': 0}

def test_5():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=2,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_6():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=1,
                               accuracy=4,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_7():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=2,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_8():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=4,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()


def test_9():
    sparse_instance = SparseFD(**test_kwargs,
                               derivative=2,
                               accuracy=6,
                               boundaries=boundaries_0)

    sparse_instance._construct_triplet_()
# -
