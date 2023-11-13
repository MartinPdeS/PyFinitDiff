#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from PyFinitDiff.sparse1D import FiniteDifference1D
from PyFinitDiff.boundaries import Boundaries1D

accuracies = [2, 4, 6]

derivatives = [1, 2]

boundaries = [
    Boundaries1D(left='zero', right='zero'),
    Boundaries1D(left='symmetric', right='zero')
]


@pytest.mark.parametrize("boundaries", boundaries)
@pytest.mark.parametrize('accuracy', accuracies, ids=accuracies)
@pytest.mark.parametrize('derivative', derivatives, ids=derivatives)
def test_0(boundaries, accuracy, derivative):
    sparse_instance = FiniteDifference1D(
        n_x=20,
        dx=1,
        derivative=derivative,
        accuracy=accuracy,
        boundaries=boundaries
    )

    sparse_instance.construct_triplet()

# -
