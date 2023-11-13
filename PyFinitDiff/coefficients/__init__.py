#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from tabulate import tabulate
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

    def __setattr__(self, attribute, value):
        if attribute == "coefficient_type":
            assert value in ['central', 'forward', 'backward']
            super().__setattr__(attribute, value)

        if attribute == "accuracy":
            assert value in self.module.__accuracy_list__, f"Accuracy: {value} is not avaible for this configuration. Valid in put: {self.module.__accuracy_list__}"
            super().__setattr__(attribute, value)

        if attribute == "derivative":
            assert value in self.module.__derivative_list__, f"Derivative: {value} is not avaible for this configuration. Valid in put: {self.module.__derivative_list__}"
            super().__setattr__(attribute, value)

    def get_coeffcient(self) -> numpy.ndarray:
        """
        Gets the finit difference coeffcients.

        :returns:   The coeffcient.
        :rtype:     numpy.ndarray
        """
        coefficients_dictionnary = self.module.coefficients

        coefficients_array = coefficients_dictionnary[f"d{self.derivative}"][f"a{self.accuracy}"]

        coefficients_array = numpy.array(coefficients_array)

        reduced_coefficients = coefficients_array[coefficients_array[:, 1] != 0]

        return reduced_coefficients

    @property
    def array(self) -> numpy.ndarray:
        return self.get_coeffcient()

    @property
    def module(self) -> object:
        """
        Returns the right module depending on which
        type of coefficient ones need. The method also asserts
        that the right accuracy and derivative exists on that module.

        :returns:   The module.
        :rtype:     object
        """
        match self.coefficient_type.lower():
            case 'central':
                return central
            case 'forward':
                return forward
            case 'backward':
                return backward

        assert self.accuracy in self.module.__accuracy_list__, f'Error accuracy: {self.accuracy} has to be in the list {self.module.__accuracy_list__}'
        assert self.derivative in self.module.__derivative_list__, f'Error derivative: {self.derivative} has to be in the list {self.module.__derivative_list__}'

    @property
    def index(self) -> numpy.ndarray:
        return self.array[:, 0]

    @property
    def values(self) -> numpy.ndarray:
        return self.array[:, 1]

    def __iter__(self) -> tuple[int, float]:
        for index, values in zip(self.index, self.values):
            yield index, values

    def print(self):
        table = tabulate(self.array, headers=['Index', 'Value'])
        print(table)

# -
