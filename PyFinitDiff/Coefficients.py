from PyFinitDiff.coefficients.central import coefficients as central_coefficent
from PyFinitDiff.coefficients.forward import coefficients as forward_coefficent
from PyFinitDiff.coefficients.backward import coefficients as backward_coefficent


class FinitCoefficients():
    accuracy_list = [2, 4, 6]
    derivative_list = [1, 2]

    def __init__(self, derivative, accuracy):
        self.derivative = derivative
        self.accuracy = accuracy

        assert accuracy in self.accuracy_list, f'Error accuracy: {self.accuracy} has to be in the list {self.accuracy_list}'
        assert derivative in self.derivative_list, f'Error derivative: {self.derivative} has to be in the list {self.derivative_list}'
        self._central = central_coefficent[f"d{self.derivative}"][f"a{self.accuracy}"]
        self._forward = forward_coefficent[f"d{self.derivative}"][f"a{self.accuracy}"]
        self._backward = backward_coefficent[f"d{self.derivative}"][f"a{self.accuracy}"]

    def central(self, offset_multiplier: int = 1):
        return {offset * offset_multiplier: float(value) for offset, value in self._central['coefficients'].items() if value != 0.}

    def backward(self, offset_multiplier: int = 1):
        return {offset * offset_multiplier: float(value) for offset, value in self._backward['coefficients'].items() if value != 0.}

    def forward(self, offset_multiplier: int = 1):
        return {offset * offset_multiplier: float(value) for offset, value in self._forward['coefficients'].items() if value != 0.}

    def __repr__(self):
        return f""" \
        \rcentral coefficients: {self.central()}\
        \rforward coefficients: {self.forward()}\
        \rbackward coefficients: {self.backward()}\
        """


# -
