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


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class FiniteCoefficients():
    derivative: int
    """ The order of the derivative to consider """
    accuracy: int
    """ The accuracy of the finit difference """
    coefficient_type: str = 'central'
    """ Type of coefficient, has to be either 'central', 'forward' or 'backward' """

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

    @property
    def derivative_string(self) -> str:
        return f'd{self.derivative}'

    @property
    def accuracy_string(self) -> str:
        return f'a{self.accuracy}'

    @property
    def central(self) -> dict:
        return central_coefficent[self.derivative_string][self.accuracy_string]

    @property
    def forward(self) -> dict:
        return forward_coefficent[self.derivative_string][self.accuracy_string]

    @property
    def backward(self) -> dict:
        return backward_coefficent[self.derivative_string][self.accuracy_string]

    def get_coeffcient(self) -> numpy.ndarray:
        """
        Gets the finit difference coeffcients.

        :returns:   The coeffcient.
        :rtype:     numpy.ndarray
        """
        coefficients_dictionnary = self.module.coefficients

        coefficients_array = coefficients_dictionnary[self.derivative_string][self.accuracy_string]

        coefficients_array = numpy.array(coefficients_array)

        reduced_coefficients = coefficients_array[coefficients_array[:, 1] != 0]

        return reduced_coefficients

    @property
    def array(self) -> numpy.ndarray:
        return self.get_coeffcient()

    @property
    def module(self) -> object:
        """
        Returns the right module depending on which type of coefficient ones need.
        The method also asserts that the right accuracy and derivative exists on that module.

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
    def max_central_index(self) -> int:
        return self.index.max()

    @property
    def values(self) -> numpy.ndarray:
        return self.array[:, 1]

    def __iter__(self) -> tuple[int, float]:
        for index, values in zip(self.index, self.values):
            yield index, values

    def print(self):
        table = tabulate(self.array, headers=['index', 'value'])
        print(table)

# -
