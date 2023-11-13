#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy
import math

from PyFinitDiff.tools.derivatives import get_derivative_1d


def foo(x, power: int):
    return x**power


coefficient_type_list = ['central', 'backward', 'forward']
accuracy_list = [2, 4, 6]
order_list = [1, 2, 3]


@pytest.mark.parametrize("coefficient_type", coefficient_type_list)
@pytest.mark.parametrize("accuracy", accuracy_list)
@pytest.mark.parametrize("order", order_list)
def test_central_derivative(accuracy: int, coefficient_type: str, order: int):
    derivative = get_derivative_1d(
        function=foo,
        x_eval=3,
        order=order,
        accuracy=accuracy,
        delta=1,
        function_kwargs=dict(power=order),
        coefficient_type=coefficient_type
    )

    assert numpy.isclose(derivative, math.factorial(order), atol=1e-5), "Derivative evaluation output is unexpected."

# -
