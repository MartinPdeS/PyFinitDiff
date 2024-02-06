#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from PyFinitDiff.finite_difference_1D import FiniteDifference
from PyFinitDiff.finite_difference_1D import Boundaries

boundaries = [
    Boundaries(left='zero', right='zero'),
    Boundaries(left='symmetric', right='zero')
]


@pytest.mark.parametrize("boundaries", boundaries)
@pytest.mark.parametrize('accuracy', [2, 4, 6], ids=[2, 4, 6])
@pytest.mark.parametrize('derivative', [1, 2], ids=[1, 2])
def test_0(boundaries, accuracy, derivative):
    sparse_instance = FiniteDifference(
        n_x=20,
        dx=1,
        derivative=derivative,
        accuracy=accuracy,
        boundaries=boundaries
    )

    sparse_instance.construct_triplet()

# -
