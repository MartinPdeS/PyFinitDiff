#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from PyFinitDiff.finite_difference_1D import FiniteDifference, Boundaries

# Define boundary conditions for testing as a list of dictionaries
BOUNDARY_CONDITIONS = [
    {'left': 'zero', 'right': 'zero'},
    {'left': 'symmetric', 'right': 'zero'},
    {'left': 'anti-symmetric', 'right': 'zero'},
    {'left': 'symmetric', 'right': 'none'}
]

ACCURACIES = [2, 4, 6]
DERIVATIVES = [1, 2]


@pytest.mark.parametrize("boundaries_kwargs", BOUNDARY_CONDITIONS, ids=lambda x: f"{x}")
@pytest.mark.parametrize('accuracy', ACCURACIES, ids=[f'accuracy_{acc}' for acc in ACCURACIES])
@pytest.mark.parametrize('derivative', DERIVATIVES, ids=[f'derivative_{deriv}' for deriv in DERIVATIVES])
def test_finite_difference(boundaries_kwargs, accuracy, derivative):
    """
    Test the FiniteDifference class with various boundary conditions, accuracy levels, and derivatives.

    This test checks the initialization and triplet construction for different boundary conditions,
    accuracy levels, and derivative orders.

    Args:
        boundaries_kwargs (dict): Dictionary containing boundary conditions for the FiniteDifference class.
        accuracy (int): The accuracy level of the finite difference calculation.
        derivative (int): The derivative order for the finite difference calculation.
    """
    boundaries = Boundaries(**boundaries_kwargs)

    finite_diff_instance = FiniteDifference(
        n_x=20,
        dx=1,
        derivative=derivative,
        accuracy=accuracy,
        boundaries=boundaries
    )

    # Attempt to construct the finite difference triplet representation
    finite_diff_instance.construct_triplet()


if __name__ == "__main__":
    pytest.main(["-W error", __file__])
