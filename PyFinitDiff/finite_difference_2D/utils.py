#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import matplotlib.pyplot as plt
from collections.abc import Iterable
import numpy
import scipy


@dataclass
class MeshInfo():
    n_x: int
    """ Number of point in the x direction """
    n_y: int
    """ Number of point in the y direction """
    dx: float = 1
    """ Infinetisemal displacement in x direction """
    dy: float = 1
    """ Infinetisemal displacement in y direction """

    def __post_init__(self):
        self.size = self.n_x * self.n_y
        self.shape = (self.n_x, self.n_y)


def plot_mesh(*meshes, text=False, title=''):
    figure, axes = plt.subplots(1, len(meshes), figsize=(5 * len(meshes), 5))

    if not isinstance(axes, Iterable):
        axes = [axes]

    for ax, mesh in zip(axes, meshes):

        if isinstance(mesh, scipy.sparse._csr.csr_matrix):
            mesh = mesh.todense()

        im0 = ax.imshow(mesh, cmap='viridis')
        plt.colorbar(im0, ax=ax)
        ax.set_title(f'FD:  {title}')
        ax.grid(True)

        if text:
            for (i, j), z in numpy.ndenumerate(mesh.astype(float)):
                ax.text(j, i, f'{z:.0f}', ha='center', va='center', size=8)

    plt.show()


# -
