#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from PyFinitDiff.finite_difference_2D import FiniteDifference
from PyFinitDiff.finite_difference_2D import Boundaries

accuracies = [2, 4, 6]

derivatives = [1, 2]

boundaries = [
    Boundaries(left='zero', right='zero', top='zero', bottom='zero'),
    Boundaries(left='symmetric', right='zero', top='zero', bottom='zero'),
    Boundaries(left='anti-symmetric', right='zero', top='zero', bottom='zero'),
    Boundaries(left='anti-symmetric', right='zero', top='symmetric', bottom='zero')
]


@pytest.mark.parametrize("boundaries", boundaries)
@pytest.mark.parametrize('accuracy', accuracies)
@pytest.mark.parametrize('derivative', derivatives)
def test_compare_sparse_dense_0(boundaries, accuracy, derivative):
    sparse_instance = FiniteDifference(
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
