#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy
import math

from PyFinitDiff.finite_difference_1D import get_function_derivative


def foo(x, power: int):
    return x**power


coefficient_type_list = ['central', 'backward', 'forward']


@pytest.mark.parametrize("coefficient_type", coefficient_type_list)
@pytest.mark.parametrize("accuracy", [2, 4, 6], ids=[2, 4, 6])
@pytest.mark.parametrize("derivative", [1, 2, 3], ids=[1, 2, 3])
def test_central_derivative(accuracy: int, coefficient_type: str, derivative: int):
    evaluation = get_function_derivative(
        function=foo,
        x_eval=3,
        derivative=derivative,
        accuracy=accuracy,
        delta=1,
        function_kwargs=dict(power=derivative),
        coefficient_type=coefficient_type
    )

    theoretical = math.factorial(derivative)

    discrepency = numpy.isclose(evaluation, theoretical, atol=1e-5)

    assert discrepency, f"[{derivative = } | {accuracy = }] Evaluation output is unexpected. {evaluation = :.7f} | {theoretical = :.7f}"


# -
