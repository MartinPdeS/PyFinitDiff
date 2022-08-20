class NameSpace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)



class BoundaryClass:

    __AcceptedValues = ['Symmetric', 'AntiSymmetric', 'Zero', 'None', 1, -1, 0]

    def __init__(self, Left='None', Right='None', Top='None', Bottom='None'):
        self.Left   = Left
        self.Right  = Right
        self.Bottom = Bottom
        self.Top    = Top


    def __repr__(self):
        return f"Symmetries \n{'-'*50} \n{self.Top = }\n{self.Bottom = }\n{self.Left = }\n{self.Right = }"

    def AssertValues(self, value):
        assert value in self.Symmetries, f"Error unexpected symmetry value {value}. Accepted are {self.Symmetries}"

    @property
    def Top(self):
        return self._Top

    @Top.setter
    def Top(self, value):
        assert value in self.__AcceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self.__AcceptedValues}"

        self._Top = value

    @property
    def Bottom(self):
        return self._Bottom

    @Bottom.setter
    def Bottom(self, value):
        assert value in self.__AcceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self.__AcceptedValues}"

        self._Bottom = value

    @property
    def Left(self):
        return self._Left

    @Left.setter
    def Left(self, value):
        assert value in self.__AcceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self.__AcceptedValues}"

        self._Left = value

    @property
    def Right(self):
        return self._Right

    @Right.setter
    def Right(self, value):
        assert value in self.__AcceptedValues, f"Error unexpected symmetry value {value}. Accepted are {self.__AcceptedValues}"

        self._Right = value
