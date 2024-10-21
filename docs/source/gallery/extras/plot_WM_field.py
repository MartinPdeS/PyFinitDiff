"""
Generating Whittle-Matérn field
=================================

In this example, we generate a Whittle-Matérn field using a finite difference Laplacian operator.
We will explore different correlation lengths and observe their effect on the resulting fields.
"""

# %%
# Importing required packages
# ---------------------------
# Here we import the necessary libraries for numerical computations, rendering, and finite difference operations.

import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
from PyFinitDiff.finite_difference_2D import FiniteDifference, Boundaries

# %%
# Setting up the finite difference Laplacian
# ------------------------------------------
# We define a grid and create a finite difference instance that provides us with a Laplacian operator.

n_x = n_y = 20

sparse_instance = FiniteDifference(
    n_x=n_x,
    n_y=n_y,
    dx=1000 / n_x,
    dy=1000 / n_y,
    derivative=2,
    accuracy=2,
    boundaries=Boundaries(top='symmetric')
)

laplacian = sparse_instance.triplet.to_dense()

# %%
# Defining the function to generate the Whittle-Matérn field
# -----------------------------------------------------------
# The following function generates a field by solving a linear system involving the Laplacian and random noise.


def get_field(D: float, lc: float, Nc: float, shape: list):
    n_x, n_y = shape
    eta = np.random.rand(n_x * n_y)

    left_hand_side = (-laplacian + lc**2) ** (3 / 2)
    right_hand_side = eta

    field = linalg.solve(left_hand_side, right_hand_side)

    return Nc * field

# %%
# Visualizing the fields for different correlation lengths
# ---------------------------------------------------------
# We generate and visualize fields with varying correlation lengths to see their impact on the structure of the field.


fig, axes = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)
axes = axes.flatten()

for ax, correlation_length in zip(axes, [1, 2, 4]):
    field = get_field(D=3, lc=correlation_length, Nc=1, shape=[n_x, n_y]).reshape([n_x, n_y])
    mesh = ax.pcolormesh(field, shading='auto', cmap='viridis')
    ax.set_title(f'Correlation length: {correlation_length}')
    ax.set_aspect('equal')
    plt.colorbar(mesh, ax=ax)

plt.show()
