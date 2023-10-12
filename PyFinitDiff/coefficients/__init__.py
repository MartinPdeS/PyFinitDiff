from .central import coefficients as central_coefficent
from .forward import coefficients as forward_coefficent
from .backward import coefficients as backward_coefficent


class FinitCoefficients():
    accuracy_list = [2, 4, 6]
    derivative_list = [1, 2]

    def __init__(self, derivative, accuracy):
        self.derivative = derivative
        self.accuracy = accuracy

        assert accuracy in self.accuracy_list, f'Error accuracy: {self.accuracy} has to be in the list {self.accuracy_list}'
        assert derivative in self.derivative_list, f'Error derivative: {self.derivative} has to be in the list {self.derivative_list}'

        self.central = central_coefficent[f"d{self.derivative}"][f"a{self.accuracy}"]
        self.forward = forward_coefficent[f"d{self.derivative}"][f"a{self.accuracy}"]
        self.backward = backward_coefficent[f"d{self.derivative}"][f"a{self.accuracy}"]

    def __repr__(self):
        return f""" \
        \rcentral coefficients: {self.central}\
        \rforward coefficients: {self.forward}\
        \rbackward coefficients: {self.backward}\
        """
