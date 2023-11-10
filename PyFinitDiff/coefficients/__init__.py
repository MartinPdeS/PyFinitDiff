#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import numpy

from .central import coefficients as central_coefficent
from .forward import coefficients as forward_coefficent
from .backward import coefficients as backward_coefficent

from . import central, forward, backward

__accuracy_list__ = [2, 4, 6]
__derivative_list__ = [1, 2]


class FinitCoefficients():
    def __init__(self, derivative, accuracy):
        self.derivative = derivative
        self.accuracy = accuracy

        assert accuracy in __accuracy_list__, f'Error accuracy: {self.accuracy} has to be in the list {self.accuracy_list}'
        assert derivative in __derivative_list__, f'Error derivative: {self.derivative} has to be in the list {self.derivative_list}'

        self.central = central_coefficent[f"d{self.derivative}"][f"a{self.accuracy}"]
        self.forward = forward_coefficent[f"d{self.derivative}"][f"a{self.accuracy}"]
        self.backward = backward_coefficent[f"d{self.derivative}"][f"a{self.accuracy}"]

    def __repr__(self):
        return f""" \
        \rcentral coefficients: {self.central}\
        \rforward coefficients: {self.forward}\
        \rbackward coefficients: {self.backward}\
        """


@dataclass
class FiniteCoefficients():
    derivative: int
    """ The order of the derivative to consider """
    accuracy: int
    """ The accuracy of the finit difference """
    coefficient_type: str = 'central'
    """ Type of coefficient, has to be either 'central', 'forward' or 'backward' """

    def __post_init__(self):
        self.derivative_string = f'd{self.derivative}'
        self.accuracy_string = f'a{self.accuracy}'

        match self.coefficient_type.lower():
            case 'central':
                self.module = central
            case 'forward':
                self.module = forward
            case 'backward':
                self.module = backward

        assert self.accuracy in self.module.__accuracy_list__, f'Error accuracy: {self.accuracy} has to be in the list {self.module.__accuracy_list__}'
        assert self.derivative in self.module.__derivative_list__, f'Error derivative: {self.derivative} has to be in the list {self.module.__derivative_list__}'

        self.coefficients_dictionnary = self.module.coefficients
        coefficients_array = self.coefficients_dictionnary[self.derivative_string][self.accuracy_string]

        coefficients_array = numpy.array(coefficients_array)

        reduced_coefficients = coefficients_array[coefficients_array[:, 1] != 0]

        self.array = reduced_coefficients

    @property
    def index(self) -> numpy.ndarray:
        return self.array[:, 0]

    @property
    def values(self) -> numpy.ndarray:
        return self.array[:, 1]

    def __iter__(self) -> tuple[int, float]:
        for index, values in zip(self.index, self.values):
            yield index, values
# -
