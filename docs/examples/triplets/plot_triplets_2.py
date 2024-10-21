"""
Example: triplets 2
===================

In this example, we generate a finite difference instance and visualize the resulting triplets.
The boundary conditions, derivative, and accuracy settings are specified for demonstration purposes.
"""

# %%
# .. list-table:: Finite-difference parameters
#    :widths: 25
#    :header-rows: 1
#
#    * - boundaries: {left: 1, right: 0, top: 0, bottom: 0}
#    * - derivative: 2
#    * - accuracy: 4

# %%
# Importing required packages
# ---------------------------
# Here we import the necessary libraries for numerical computations and finite difference operations.

from PyFinitDiff.finite_difference_2D import FiniteDifference, Boundaries
import matplotlib.pyplot as plt

# %%
# Setting up the finite difference instance and boundaries
# ---------------------------------------------------------
# We define the grid size and set up the finite difference instance with specified boundary conditions.

sparse_instance = FiniteDifference(
    n_x=12,
    n_y=12,
    dx=1,
    dy=1,
    derivative=2,
    accuracy=4,
    boundaries=Boundaries(left='symmetric', right='zero', top='zero', bottom='zero')
)

# %%
# Visualizing the triplets with matplotlib
# -----------------------------------------
# We plot the triplets using matplotlib to visualize the finite difference operator.

sparse_instance.triplet.plot()

plt.show()

# -
