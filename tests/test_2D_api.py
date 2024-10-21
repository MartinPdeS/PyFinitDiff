#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from PyFinitDiff.finite_difference_2D import FiniteDifference, Boundaries

# Define parameters for testing
ACCURACIES = [2, 4, 6]
DERIVATIVES = [1, 2]

BOUNDARY_CONDITIONS = [
    dict(left='zero', right='zero', top='zero', bottom='zero'),
    dict(left='symmetric', right='zero', top='zero', bottom='zero'),
    dict(left='anti-symmetric', right='zero', top='zero', bottom='zero'),
    dict(left='anti-symmetric', right='zero', top='symmetric', bottom='zero')
]


def test_init_boundaries():
    """
    Test initialization of Boundaries with various valid and invalid boundary condition inputs.

    This function tests whether the Boundaries class can be successfully initialized with valid
    boundary conditions and raises the appropriate exceptions when provided with invalid inputs.
    """
    valid_kwargs_list = [
        dict(left='zero', right='zero', top='zero', bottom='zero'),
        dict(left='symmetric', right='zero', top='zero', bottom='zero'),
        dict(left='anti-symmetric', right='zero', top='zero', bottom='zero'),
        dict(left='anti-symmetric', right='zero', top='symmetric', bottom='zero')
    ]

    for kwargs in valid_kwargs_list:
        boundaries = Boundaries(**kwargs)
        assert isinstance(boundaries, Boundaries)

    with pytest.raises(ValueError):
        Boundaries(left='bad_input')


@pytest.mark.parametrize("boundaries_kwargs", BOUNDARY_CONDITIONS, ids=lambda x: f'{x}')
@pytest.mark.parametrize('accuracy', ACCURACIES, ids=lambda x: f'accuracy_{x}')
@pytest.mark.parametrize('derivative', DERIVATIVES, ids=lambda x: f'derivative_{x}')
def test_init_2D_triplet(boundaries_kwargs, accuracy, derivative):
    """
    Test the FiniteDifference class initialization and triplet construction with various parameters.

    This function tests the FiniteDifference class by initializing it with different boundary
    conditions, accuracy levels, and derivative orders, and checks if the triplet construction
    proceeds without errors.

    Args:
        boundaries_kwargs (dict): Dictionary containing boundary conditions.
        accuracy (int): Desired accuracy level for the finite difference calculation.
        derivative (int): Order of the derivative for the finite difference calculation.
    """
    boundaries = Boundaries(**boundaries_kwargs)

    finite_diff_instance = FiniteDifference(
        n_x=20,
        n_y=20,
        dx=1,
        dy=1,
        derivative=derivative,
        accuracy=accuracy,
        boundaries=boundaries
    )

    finite_diff_instance.construct_triplet()


def test_raise_fails():
    """
    Test that invalid boundary condition inputs raise the appropriate exceptions.

    This function ensures that the Boundaries class raises a ValueError when provided
    with invalid boundary condition inputs.
    """
    with pytest.raises(ValueError):
        Boundaries(left='andti-symmetric', right='zero', top='symmetric', bottom='zero')


if __name__ == "__main__":
    pytest.main(["-W error", __file__])
