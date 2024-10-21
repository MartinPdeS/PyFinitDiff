#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy
from PyFinitDiff.triplet import Triplet
from unittest.mock import patch


@pytest.fixture
def triplet():
    i_index = numpy.arange(100)
    j_index = numpy.arange(100)
    values = numpy.random.rand(100)
    array = numpy.c_[i_index, j_index, values]

    return Triplet(array=array, shape=(10, 10))


@patch('matplotlib.pyplot.show')
def test_triplet_operations(mock_show, triplet):
    triplet *= 2

    _ = triplet.max_i
    _ = triplet.max_j
    _ = triplet.min_i
    _ = triplet.min_j
    _ = triplet.diagonal

    triplet.shift_diagonal(value=10)

    triplet.plot()


if __name__ == "__main__":
    pytest.main(["-W error", __file__])
