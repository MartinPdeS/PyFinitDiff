#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class MeshInfo():
    n_x: int
    """ Number of point in the x direction """
    dx: float = 1
    """ Infinetisemal displacement in x direction """

    def __post_init__(self):
        self.size = self.n_x
        self.shape = (self.n_x,)

# -
