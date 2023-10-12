#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from PyFinitDiff.sparse2D import FiniteDifference2D
from PyFinitDiff.boundaries import Boundaries2D

accuracies = [2, 4, 6]

derivatives = [1, 2]

boundaries = [
    Boundaries2D(left='zero', right='zero', top='zero', bottom='zero'),
    Boundaries2D(left='symmetric', right='zero', top='zero', bottom='zero'),
    Boundaries2D(left='anti-symmetric', right='zero', top='zero', bottom='zero'),
    Boundaries2D(left='anti-symmetric', right='zero', top='symmetric', bottom='zero')
]


@pytest.mark.parametrize("boundaries", boundaries)
@pytest.mark.parametrize('accuracy', accuracies)
@pytest.mark.parametrize('derivative', derivatives)
def test_compare_sparse_dense_0(boundaries, accuracy, derivative):
    sparse_instance = FiniteDifference2D(
        n_x=20,
        n_y=20,
        dx=1,
        dy=1,
        derivative=derivative,
        accuracy=accuracy,
        boundaries=boundaries
    )

    sparse_instance.construct_triplet()


# -
