import numpy
from dataclasses import dataclass, field
from typing import Dict


from PyFinitDiff.Coefficients import FinitCoefficients
from PyFinitDiff.Tools import Triplet


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@dataclass
class Diagonal2D():
    """
    This class is a construction of diagonals element of the finit-difference method.
    The class can be initialized with different parameters suchs as it's offset or
    boundary condition.

    """
    shape: list[int]
    """Shape of the mesh to be discetized."""
    offset: int
    """Offset of the column index for the diagonal."""
    value: float = 1.
    """Value associated with the diagonal."""
    boundary: str = None
    """Boundary condition. ['symmetric', 'anti-symmetric', 'zero']"""
    type: int = 0
    """Define the boundary position. [0, 1, 2, 3]"""

    def __post_init__(self):
        self.size: int = self.shape[0] * self.shape[1]
        self._triplet: numpy.ndarray = None

    @property
    def triplet(self) -> Triplet:
        """
        Return the Triplet instance of the diagonal.

        """
        if self._triplet is None:
            self.compute_triplet()
        return self._triplet

    @property
    def value_with_symmetry(self) -> float:
        """
        Return the value of the diabonal index as defined by the boundary condition.
        If boundary is symmetric the value stays the same, if anti-symmetric a minus sign
        is added, if zero it returns zero.

        """
        match self.boundary:
            case 'symmetric':
                return self.value
            case 'anti-symmetric':
                return -self.value
            case 'zero':
                return 0.

        return self.value

    def _get_shift_vector_(self):
        """


        """
        match self.type:
            case 0:
                shift_vector = 0
            case 1:
                shift_vector = numpy.zeros(self.size)
                shift_vector[:abs(self.offset)] += abs(self.offset)
            case 2:
                shift_vector = numpy.zeros(self.size)
                shift_vector[-abs(self.offset):] -= abs(self.offset)
            case 3:
                shift_vector = numpy.zeros(self.shape[0])
                shift_vector[-abs(self.offset):] = - numpy.arange(1, abs(self.offset) + 1)
                shift_vector = numpy.tile(shift_vector, self.shape[0])
            case 4:
                shift_vector = numpy.zeros(self.shape[0])
                shift_vector[:abs(self.offset)] = numpy.arange(1, abs(self.offset) + 1)[::-1]
                shift_vector = numpy.tile(shift_vector, self.shape[0])

        return shift_vector

    def compute_triplet(self) -> None:
        """
        Compute the diagonal index and generate a Triplet instance out of it.
        The value of the third triplet column depends on the boundary condition.

        """
        row = numpy.arange(0, self.size)

        shift = self._get_shift_vector_()

        col = row + self.offset + 2 * shift

        values = numpy.ones(self.size) * self.value

        values[shift != 0] = self.value_with_symmetry

        self._triplet = Triplet(numpy.c_[row, col, values])

    def remove_out_of_bound(self, array: numpy.ndarray) -> numpy.ndarray:
        """
        Remove entries of the diagonal that are out of boundary and then return the array.
        The boundary is defined by [size, size].

        """
        i: numpy.ndarray = array[:, 0]
        j: numpy.ndarray = array[:, 1]

        return array[(0 <= i) & (i <= self.size - 1) & (0 <= j) & (j <= self.size - 1)]

    def plot(self) -> None:
        """
        Plots the Triplet instance.

        """
        self.triplet.plot(max_i=self.size, max_j=self.size)


@dataclass
class FiniteDifference2D():
    """
    .. note::
        This class represent a specific finit difference configuration,
        which is defined with the descretization of the mesh, the derivative order,
        accuracy and the boundary condition that are defined.
        More information is providided at the following link:
        'math.toronto.edu/mpugh/Teaching/Mat1062/notes2.pdf'
    """
    n_x: int
    """ Number of point in the x direction """
    n_y: int
    """ Number of point in the y direction """
    dx: float = 1
    """ Infinetisemal displacement in x direction """
    dy: float = 1
    """ Infinetisemal displacement in y direction """
    derivative: int = 1
    """ Derivative order to convert into finit-difference matrix. """
    accuracy: int = 2
    """ Accuracy of the derivative approximation [error is inversly proportional to the power of that value]. """
    boundaries: Dict[str, str] = field(default_factory=lambda: ({'left': 'none', 'right': 'none', 'top': 'none', 'bottom': 'none'}))
    """ Values of the four possible boundaries of the system. """

    def __post_init__(self):
        self.finit_coefficient = FinitCoefficients(derivative=self.derivative, accuracy=self.accuracy)
        self._triplet = None

    @property
    def triplet(self):
        """
        Triplet representing the non-nul values of the specific
        finit-difference configuration.

        """
        if not self._triplet:
            self._construct_triplet_()
        return self._triplet

    @property
    def size(self):
        return self.n_y * self.n_x

    @property
    def shape(self):
        return [self.n_x, self.n_y]

    def iterate_center(self, multiplier: int = 1):
        fd_coeffcient = {k: v for k, v in self.finit_coefficient.central(offset_multiplier=multiplier).items() if k == 0}

        for offset, value in fd_coeffcient.items():
            yield {'offset': offset, 'value': value, 'boundary': 'zero', 'type': 0}

    def iterate_top(self, multiplier: int = 1):
        fd_coeffcient = {k: v for k, v in self.finit_coefficient.central(offset_multiplier=multiplier).items() if k > 0}

        for offset, value in fd_coeffcient.items():
            yield {'offset': offset, 'value': value, 'boundary': self.boundaries['top'], 'type': 2}

    def iterate_right(self, multiplier: int = 1):
        fd_coeffcient = {k: v for k, v in self.finit_coefficient.central(offset_multiplier=multiplier).items() if k > 0}

        for offset, value in fd_coeffcient.items():
            yield {'offset': offset, 'value': value, 'boundary': self.boundaries['right'], 'type': 3}

    def iterate_left(self, multiplier: int = 1):
        fd_coeffcient = {k: v for k, v in self.finit_coefficient.central(offset_multiplier=multiplier).items() if k < 0}

        for offset, value in fd_coeffcient.items():
            yield {'offset': offset, 'value': value, 'boundary': self.boundaries['left'], 'type': 4}

    def iterate_bottom(self, multiplier: int = 1):
        fd_coeffcient = {k: v for k, v in self.finit_coefficient.central(offset_multiplier=multiplier).items() if k < 0}

        for offset, value in fd_coeffcient.items():
            yield {'offset': offset, 'value': value, 'boundary': self.boundaries['bottom'], 'type': 1}

    def _construct_central_triplet_(self):
        center_diagonals = []

        for parameters in self.iterate_left():
            center_diagonals.append(
                Diagonal2D(shape=self.shape, **parameters).triplet
            )

        for parameters in self.iterate_right():
            center_diagonals.append(
                Diagonal2D(shape=self.shape, **parameters).triplet
            )

        for parameters in self.iterate_center():
            center_diagonals.append(
                Diagonal2D(shape=self.shape, **parameters).triplet
            )

        for parameters in self.iterate_top(multiplier=self.n_x):
            center_diagonals.append(
                Diagonal2D(shape=self.shape, **parameters).triplet
            )

        for parameters in self.iterate_bottom(multiplier=self.n_x):
            center_diagonals.append(
                Diagonal2D(shape=self.shape, **parameters).triplet
            )

        for parameters in self.iterate_center():
            center_diagonals.append(
                Diagonal2D(shape=self.shape, **parameters).triplet
            )

        return sum(center_diagonals, start=Triplet())

    def _construct_triplet_(self):
        self._triplet = self._construct_central_triplet_()


# -
