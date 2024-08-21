#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from PyFinitDiff.finite_difference_1D import FiniteDifference, Boundaries

# Define boundary conditions for testing
boundary_conditions = [
    Boundaries(left='zero', right='zero'),
    Boundaries(left='symmetric', right='zero')
]


@pytest.mark.parametrize("boundaries", boundary_conditions, ids=[b.__repr__() for b in boundary_conditions])
@pytest.mark.parametrize('accuracy', [2, 4, 6], ids=['accuracy_2', 'accuracy_4', 'accuracy_6'])
@pytest.mark.parametrize('derivative', [1, 2], ids=['derivative_1', 'derivative_2'])
def test_finite_difference(boundaries, accuracy, derivative):
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
        dx=1,
        derivative=derivative,
        accuracy=accuracy,
        boundaries=boundaries
    )

    # Construct the finite difference triplet representation
    finite_diff_instance.construct_triplet()
