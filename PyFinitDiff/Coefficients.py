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
        self.central_max_offset = self._central['max_offset']

    def central(self, symmetry=None):
        coefficients = {key: float(value) for key, value in self._central['coefficients'].items() if value != 0.}
        match symmetry:
            case None:
                return coefficients
            case 'symmetric':
                return {idx: 2 * value if idx != 0 else value for idx, value in coefficients.items()}
            case 'anti-symmetric':
                return {idx: value if idx == 0 else 0. for idx, value in coefficients.items()}

    def backward(self):
        return {key: float(value) for key, value in self._backward['coefficients'].items() if value != 0.}

    def forward(self):
        return {key: float(value) for key, value in self._forward['coefficients'].items() if value != 0.}

    def __repr__(self):
        return f""" \
        \rcentral coefficients: {self.central()}\
        \rforward coefficients: {self.forward()}\
        \rbackward coefficients: {self.backward()}\
        """

    @property
    def offset_index(self):
        offset_index = 0
        for Index, value in self.Central().items():
            if value != 0 and Index > offset_index:
                offset_index = Index

        return offset_index

# -
