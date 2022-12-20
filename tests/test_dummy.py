#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch


@patch("matplotlib.pyplot.show")
def test_fused1(patch):
    return 0

# -
