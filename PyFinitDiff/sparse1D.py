import numpy
from dataclasses import dataclass, field
from typing import Dict

from PyFinitDiff.triplet import Triplet
from PyFinitDiff.coefficients import FinitCoefficients


@dataclass
class VariableDiagonal1d():
    """
    This class is a construction of diagonals element of the finit-difference method.
    The class can be initialized with different parameters suchs as it's offset or
    boundary condition.

    """
    offset: int
    """Offset of the column index for the diagonal."""
    values: numpy.ndarray
    """Value associated with the diagonal."""
    boundary: str = 'none'
    """Boundary condition. ['symmetric', 'anti-symmetric', 'zero']"""
    boundary_type: int = 0
    """Define the boundary position. [0, 1, 2, 3]"""

    def __post_init__(self):
        self.size = len(self.values.ravel())
        self._triplet: numpy.ndarray = None

    @property
    def triplet(self) -> Triplet:
        """
        Return the Triplet instance of the diagonal.

        """
        if self._triplet is None:
            self.compute_triplet()
        return self._triplet

    def symmetrize_values(self, values: numpy.ndarray, shift_array: numpy.ndarray) -> float:
        """
        Return the value of the diabonal index as defined by the boundary condition.
        If boundary is symmetric the value stays the same, if anti-symmetric a minus sign
        is added, if zero it returns zero.

        """
        match self.boundary:
            case 'symmetric':
                values[shift_array != 0] *= +1
            case 'anti-symmetric':
                values[shift_array != 0] *= -1
            case 'zero':
                values[shift_array != 0] *= 0
            case 'none':
                pass

        return values

    def _get_shift_vector_(self) -> numpy.ndarray:
        """


        """
        match self.boundary_type:
            case 0:
                shift_vector = numpy.zeros(self.size)
            case 1:
                shift_vector = numpy.zeros(self.size)
                shift_vector[:abs(self.offset)] = numpy.arange(abs(self.offset))[::-1] + 1
            case 2:
                shift_vector = numpy.zeros(self.size)
                shift_vector[-abs(self.offset) - 1:] = - numpy.arange(abs(self.offset) + 1)

        return shift_vector

    def get_boundary_row(self) -> numpy.ndarray:
        return self._get_shift_vector_().astype(bool)

    def compute_triplet(self) -> None:
        """
        Compute the diagonal index and generate a Triplet instance out of it.
        The value of the third triplet column depends on the boundary condition.

        """
        row = numpy.arange(0, self.size)

        shift = self._get_shift_vector_()

        col = row + self.offset + 2 * shift

        values = self.symmetrize_values(self.values, shift)

        self._triplet = Triplet(numpy.c_[row, col, values])

    def remove_out_of_bound(self, array: numpy.ndarray) -> numpy.ndarray:
        """
        Remove entries of the diagonal that are out of boundary and then return the array.
        The boundary is defined by [size, size].

        """
        i: numpy.ndarray = array[:, ]
        j: numpy.ndarray = array[:, 1]

        return array[(0 <= i) & (i <= self.size - 1) & (0 <= j) & (j <= self.size - 1)]

    def plot(self) -> None:
        """
        Plots the Triplet instance.

        """
        self.triplet.plot()


class ConstantDiagonal1d(VariableDiagonal1d):
    def __init__(self, offset: int, value: float, size: int, boundary: str = 'none', boundary_type: int = 0):
        super().__init__(
            offset=offset,
            values=numpy.ones(size) * value,
            boundary=boundary,
            boundary_type=boundary_type
        )


@dataclass
class FiniteDifference1D():
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
    dx: float = 1
    """ Infinetisemal displacement in x direction """
    derivative: int = 1
    """ Derivative order to convert into finit-difference matrix. """
    accuracy: int = 2
    """ Accuracy of the derivative approximation [error is inversly proportional to the power of that value]. """
    boundaries: Dict[str, str] = field(default_factory=lambda: ({'left': 'zero', 'right': 'zero'}))
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
            self.construct_triplet()
        return self._triplet

    @property
    def size(self):
        return self.n_x

    @property
    def shape(self):
        return [self.size, self.size]

    @property
    def _dx(self):
        return self.dx ** self.derivative

    def offset_to_boundary_name(self, offset: int) -> str:
        if offset == 0:
            return 'center'
        elif offset < 0:
            return 'left'
        elif offset > 0:
            return 'right'

    def boundary_name_to_boundary_type(self, boundary_name: str) -> int:
        match boundary_name:
            case 'center':
                return 0
            case 'left':
                return 1
            case 'right':
                return 2

    def construct_central_triplet(self):
        diagonals = []
        for offset, value in self.finit_coefficient.central:
            boundary_name = self.offset_to_boundary_name(offset=offset)
            boundary_type = self.boundary_name_to_boundary_type(boundary_name=boundary_name)

            diagonal = ConstantDiagonal1d(
                value=value,
                size=self.n_x,
                offset=offset,
                boundary=self.boundaries.dictionary.get(boundary_name),
                boundary_type=boundary_type
            )

            diagonals.append(diagonal.triplet)

        return sum(diagonals, start=Triplet())

    def construct_triplet(self):
        self._triplet = self.construct_central_triplet()

# -
