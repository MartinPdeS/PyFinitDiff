#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class BoundaryValue(Enum):
    """
    Enumeration for boundary values.
    """
    SYMMETRIC = 'symmetric'
    ANTI_SYMMETRIC = 'anti-symmetric'
    ZERO = 'zero'
    NONE = 'none'

    @classmethod
    def from_string(cls, value: str) -> 'BoundaryValue':
        """
        Convert a string to a BoundaryValue enum.

        Parameters
        ----------
        value : str
            String value to convert.

        Returns
        -------
        BoundaryValue
            The corresponding enum value.

        Raises
        ------
        ValueError
            If the string doesn't correspond to a valid BoundaryValue.
        """
        for boundary_val in cls:
            if boundary_val.value == value:
                return boundary_val
        raise ValueError(f"No BoundaryValue found for string: '{value}'")




