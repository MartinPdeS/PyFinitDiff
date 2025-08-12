#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from scipy.sparse import linalg
from PyFinitDiff.finite_difference_2D import FiniteDifference, Boundaries
from PyFinitDiff.finite_difference_2D.utils import get_circular_mesh_triplet
from PyFinitDiff import BoundaryValue

# Define boundary conditions for testing
boundary_conditions = [
    Boundaries(left=BoundaryValue.ZERO, right=BoundaryValue.ZERO, top=BoundaryValue.ZERO, bottom=BoundaryValue.ZERO),
    Boundaries(left=BoundaryValue.SYMMETRIC, right=BoundaryValue.ZERO, top=BoundaryValue.ZERO, bottom=BoundaryValue.ZERO),
    Boundaries(left=BoundaryValue.ANTI_SYMMETRIC, right=BoundaryValue.ZERO, top=BoundaryValue.ZERO, bottom=BoundaryValue.ZERO),
    Boundaries(left=BoundaryValue.ANTI_SYMMETRIC, right=BoundaryValue.ZERO, top=BoundaryValue.SYMMETRIC, bottom=BoundaryValue.ZERO)
]


@pytest.mark.parametrize("boundaries", boundary_conditions, ids=[b.__repr__() for b in boundary_conditions])
def test_compute_eigenmode_sparse_0(boundaries):
    """
    Tests the computation of eigenmodes using sparse matrices with a 2D finite difference method.
    """
    n_x = n_y = 40

    # Create a FiniteDifference instance with specified parameters
    sparse_instance = FiniteDifference(
        n_x=n_x,
        n_y=n_y,
        dx=1,
        dy=1,
        derivative=2,
        accuracy=2,
        boundaries=boundaries
    )

    # Create a 2D circular mesh triplet
    mesh_triplet = get_circular_mesh_triplet(
        n_x=n_x,
        n_y=n_y,
        value_in=1.0,
        value_out=1.4444,
        x_offset=0,
        y_offset=0,
        radius=70
    )

    # Combine the finite difference triplet with the mesh triplet
    dynamic_triplet = sparse_instance.triplet + mesh_triplet

    # Compute the eigenvalues and eigenvectors
    eigen_values, eigen_vectors = linalg.eigs(
        dynamic_triplet.to_dense(),
        k=5,
        which='LM',
        sigma=1.44
    )


if __name__ == "__main__":
    pytest.main(["-W error", __file__])
