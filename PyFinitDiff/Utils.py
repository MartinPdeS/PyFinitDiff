class NameSpace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class BoundaryClass:

    _acceptedValues = ['symmetric', 'anti_symmetric', 'zero', 'none', 1, -1, 0]

    def __init__(self, left='None', right='None', top='None', bottom='None'):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

    def __repr__(self):
        return f"symmetries \n{'-'*50} \n{self.top = }\n{self.bottom = }\n{self.left = }\n{self.right = }"

    def AssertValues(self, value):
        assert value in self.symmetries, f"Error unexpected symmetry value {value}. Accepted are {self.symmetries}"

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        assert value in self._acceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self._acceptedValues}"

        self._top = value

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        assert value in self._acceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self._acceptedValues}"

        self._bottom = value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        assert value in self._acceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self._acceptedValues}"

        self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        assert value in self._acceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self._acceptedValues}"

        self._right = value
