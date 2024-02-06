# Built-in imports
import numpy
from dataclasses import dataclass


# Local imports
from PyFinitDiff.triplet import Triplet
import PyFinitDiff.finite_difference_2D as module


@dataclass
class VariableDiagonal():
    """
    This class is a construction of diagonals element of the finit-difference method.
    The class can be initialized with different parameters suchs as it's offset or
    boundary condition.

    """
    shape: list[int]
    """ Shape of the mesh to be discetized. """
    offset: int
    """ Offset of the column index for the diagonal. """
    values: float = 1.
    """ Value associated with the diagonal. """
    boundary: module.Boundary = None
    """ Instance of the boundary used for that diagonal. """

    @property
    def triplet(self) -> Triplet:
        """
        Return the Triplet instance of the diagonal.

        """
        self.array: numpy.ndarray = numpy.c_[self.rows, self.columns, self.values]

        return Triplet(array=self.array, shape=self.shape)

    def get_shift_vector(self) -> numpy.ndarray:
        offset = abs(self.offset)

        print(self.boundary.name.lower())

        match self.boundary.name.lower():
            case 'center':
                shift_vector = None
            case 'bottom':
                size = self.shape[0] * self.shape[1]
                shift_vector = numpy.zeros(size)
                shift_vector[:offset] += offset
            case 'top':
                size = self.shape[0] * self.shape[1]
                shift_vector = numpy.zeros(size)
                shift_vector[-offset:] -= offset
            case 'right':
                shift_vector = numpy.zeros(self.shape[1])
                shift_vector[-offset:] = - numpy.arange(1, offset + 1)
                shift_vector = numpy.tile(shift_vector, self.shape[0])
            case 'left':
                shift_vector = numpy.zeros(self.shape[1])
                shift_vector[:offset] = numpy.arange(1, offset + 1)[::-1]
                shift_vector = numpy.tile(shift_vector, self.shape[0])

        return shift_vector

    def compute_triplet(self) -> None:
        """
        Compute the diagonal index and generate a Triplet instance out of it.
        The value of the third triplet column depends on the boundary condition.

        :returns:   No return
        :rtype:     None
        """
        size = self.shape[0] * self.shape[1]

        self.rows: numpy.ndarray = numpy.arange(0, size)

        self.columns: numpy.ndarray = self.rows + self.offset

        self.apply_symmetry()

        self.array: numpy.ndarray = numpy.c_[self.rows, self.columns, self.values]

        self._triplet = Triplet(
            array=self.array,
            shape=self.shape,
        )

    def apply_symmetry(self) -> None:
        """
        Return the value of the diabonal index as defined by the boundary condition.
        If boundary is symmetric the value stays the same, if anti-symmetric a minus sign
        is added, if zero it returns zero.

        :param      values:       The values
        :type       values:       The initial value
        :param      shift_array:  The shift array
        :type       shift_array:  numpy.ndarray

        :returns:   The symmetrized value
        :rtype:     float
        """
        shift_array: numpy.ndarray = self.get_shift_vector()

        if shift_array is None:
            return

        self.columns = self.columns + 2 * shift_array

        self.values[shift_array != 0] *= self.boundary.get_factor()

        self.validate_index()

    def validate_index(self) -> None:
        """
        Removes all negative index

        :returns:   No return
        :rtype:     None
        """
        valid_index = self.columns >= 0

        self.columns = self.columns[valid_index]

        self.rows = self.rows[valid_index]

        self.values = self.values[valid_index]

    def remove_out_of_boundd(self, array: numpy.ndarray) -> numpy.ndarray:
        """
        Remove entries of the diagonal that are out of boundary and then return the array.
        The boundary is defined by [size, size].

        """
        size = self.shape[0] * self.shape[1]

        i: numpy.ndarray = array[:, 0]
        j: numpy.ndarray = array[:, 1]

        return array[(0 <= i) & (i <= size - 1) & (0 <= j) & (j <= size - 1)]

    def plot(self) -> None:
        """
        Plots the Triplet instance.

        """
        self.triplet.plot()


class ConstantDiagonal(VariableDiagonal):
    def __init__(self, offset: int, value: float, shape: list, boundary: module.Boundary):
        super().__init__(
            offset=offset,
            shape=shape,
            values=numpy.ones(shape[0] * shape[1]) * value,
            boundary=boundary,
        )

# -
