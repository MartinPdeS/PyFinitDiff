# Built-in imports
import numpy
from dataclasses import dataclass, field


# Local imports
from PyFinitDiff.coefficients import FinitCoefficients
from PyFinitDiff.triplet import Triplet
from PyFinitDiff.boundaries import Boundaries2D


@dataclass
class VariableDiagonal2d():
    """
    This class is a construction of diagonals element of the finit-difference method.
    The class can be initialized with different parameters suchs as it's offset or
    boundary condition.

    """
    shape: list[int]
    """Shape of the mesh to be discetized."""
    offset: int
    """Offset of the column index for the diagonal."""
    values: float = 1.
    """Value associated with the diagonal."""
    boundary: str = None
    """Boundary condition. ['symmetric', 'anti-symmetric', 'zero']"""
    boundary_type: int = 0
    """Define the boundary position. [0, 1, 2, 3]"""

    def __post_init__(self):
        self.size = self.shape[0] * self.shape[1]
        self._triplet = None

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

    def _get_shift_vector_(self):
        """


        """
        match self.boundary_type:
            case 0:
                shift_vector = 0
            case 1:
                shift_vector = numpy.zeros(self.size)
                shift_vector[:abs(self.offset)] += abs(self.offset)
            case 2:
                shift_vector = numpy.zeros(self.size)
                shift_vector[-abs(self.offset):] -= abs(self.offset)
            case 3:
                shift_vector = numpy.zeros(self.shape[1])
                shift_vector[-abs(self.offset):] = - numpy.arange(1, abs(self.offset) + 1)
                shift_vector = numpy.tile(shift_vector, self.shape[0])
            case 4:
                shift_vector = numpy.zeros(self.shape[1])
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

        values = self.symmetrize_values(self.values, shift)

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
        self.triplet.plot()


class ConstantDiagonal2d(VariableDiagonal2d):
    def __init__(self, offset: int, value: float, shape: list, boundary: str = 'none', boundary_type: int = 0):
        super().__init__(
            offset=offset,
            shape=shape,
            values=numpy.ones(shape[0] * shape[1]) * value,
            boundary=boundary,
            boundary_type=boundary_type
        )


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
    boundaries: Boundaries2D = field(default_factory=Boundaries2D())
    """ Values of the four possible boundaries of the system. """

    def __post_init__(self):
        self.finit_coefficient = FinitCoefficients(
            derivative=self.derivative,
            accuracy=self.accuracy
        )
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
        return self.n_y * self.n_x

    @property
    def shape(self):
        return [self.n_y, self.n_x]

    @property
    def _dx(self):
        return self.dx ** self.derivative

    @property
    def _dy(self):
        return self.dy ** self.derivative

    def offset_to_boundary_name(self, offset: int) -> str:
        if offset == 0:
            return 'center'

        if offset > 0:
            if offset < self.n_x:
                return 'right'
            else:
                return 'top'

        if offset < 0:
            if -self.n_x < offset:
                return 'left'
            else:
                return 'bottom'

    def boundary_name_to_boundary_type(self, boundary_name: str) -> int:
        match boundary_name:
            case 'center':
                return 0
            case 'bottom':
                return 1
            case 'top':
                return 2
            case 'left':
                return 4
            case 'right':
                return 3

    def iterate_central_coefficient(self, offset_multiplier: int):
        for offset, value in self.finit_coefficient.central:
            offset *= offset_multiplier
            boundary_name = self.offset_to_boundary_name(offset=offset)
            boundary_type = self.boundary_name_to_boundary_type(boundary_name=boundary_name)
            yield offset, value, self.boundaries.dictionary.get(boundary_name), boundary_type

    def construct_triplet(self):
        diagonals = []

        x_iterator = self.iterate_central_coefficient(offset_multiplier=1)
        y_iterator = self.iterate_central_coefficient(offset_multiplier=self.n_x)

        iterators = [
            (x_iterator, self._dx),
            (y_iterator, self._dy)
        ]

        for iterator, d in iterators:
            for offset, value, boundary, boundary_type in iterator:
                diagonal = ConstantDiagonal2d(
                    shape=self.shape,
                    offset=offset,
                    boundary=boundary,
                    value=value,
                    boundary_type=boundary_type
                )

                diagonal = (1 / d) * diagonal.triplet
                diagonals.append(diagonal)

        self._triplet = sum(diagonals, start=Triplet())

# -
