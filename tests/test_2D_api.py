#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from PyFinitDiff.finite_difference_2D import FiniteDifference, Boundaries

# Define accuracies and derivatives to be tested
accuracies = [2, 4, 6]
derivatives = [1, 2]

# Define boundary conditions for testing
boundary_conditions = [
    Boundaries(left='zero', right='zero', top='zero', bottom='zero'),
    Boundaries(left='symmetric', right='zero', top='zero', bottom='zero'),
    Boundaries(left='anti-symmetric', right='zero', top='zero', bottom='zero'),
    Boundaries(left='anti-symmetric', right='zero', top='symmetric', bottom='zero')
]


@pytest.mark.parametrize("boundaries", boundary_conditions, ids=[b.__repr__() for b in boundary_conditions])
@pytest.mark.parametrize('accuracy', accuracies, ids=['accuracy_2', 'accuracy_4', 'accuracy_6'])
@pytest.mark.parametrize('derivative', derivatives, ids=['derivative_1', 'derivative_2'])
def test_compare_sparse_dense_0(boundaries, accuracy, derivative):
    """
    Tests the FiniteDifference class with various boundary conditions, accuracy levels, and derivatives.

    Args:
        boundaries (Boundaries): Boundary conditions for the finite difference calculation.
        accuracy (int): Accuracy level of the finite difference calculation.
        derivative (int): Order of the derivative for the finite difference calculation.
    """
    # Initialize a FiniteDifference instance with specified parameters
    finite_diff_instance = FiniteDifference(
        n_x=20,
        n_y=20,
        dx=1,
        dy=1,
        derivative=derivative,
        accuracy=accuracy,
        boundaries=boundaries
    )

    # Construct the finite difference triplet representation
    finite_diff_instance.construct_triplet()
