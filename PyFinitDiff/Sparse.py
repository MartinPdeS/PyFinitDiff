import numpy
from dataclasses import dataclass, field
from typing import Dict
from MPSPlots.Render2D import Scene2D, Axis, Mesh, ColorBar

from PyFinitDiff.Coefficients import FinitCoefficients


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Triplet():
    def __init__(self, array: numpy.ndarray = None, add_extra_column=None):
        self._array = numpy.asarray(array)
        self._array = numpy.atleast_2d(self._array)

        if add_extra_column:
            self._array = numpy.c_[self._array, numpy.ones(self._array.shape[0])]

        assert self._array.shape[1] == 3, 'Array shape error'

    @property
    def index(self) -> numpy.ndarray:
        return self._array[:, 0:2].astype(int)

    @property
    def index_with_label(self) -> numpy.ndarray:
        return numpy.c_[self.label, self.index].astype(int)

    @property
    def i(self) -> numpy.ndarray:
        return self._array[:, 0].astype(int)

    @property
    def j(self) -> numpy.ndarray:
        return self._array[:, 1].astype(int)

    @property
    def values(self) -> numpy.ndarray:
        return self._array[:, 2]

    @property
    def size(self):
        return self.i.size

    @values.setter
    def values(self, value) -> numpy.ndarray:
        self._array[:, 2] = value

    def delete(self, index):
        self._array = numpy.delete(self._array, index.astype(int), axis=0)

    def append(self, other):
        self._array = numpy.r_[self._array, other._array]

    def __add__(self, other) -> 'Triplet':
        """
        The methode concatenate the two triplet array and
        reduce if any coinciding index values.
        """

        new_array = numpy.r_[self._array, other._array]

        new_triplet = Triplet(new_array)

        return new_triplet.remove_duplicate()

    def add_triplet(self, *others) -> 'Triplet':
        others_array = (other._array for other in others)

        self._array = numpy.r_[(self._array, *others_array)]

        self.merge_duplicate()

    def remove_duplicate(self) -> 'Triplet':
        new_array = self._array
        index_to_delete = []
        duplicate = self.get_duplicate_index()

        if duplicate.size == 0:
            return Triplet(self._array)

        for duplicate in duplicate:
            index_to_keep = duplicate[0]
            for index_to_merge in duplicate[1:]:
                index_to_delete.append(index_to_merge)
                new_array[index_to_keep, 2] += new_array[index_to_merge, 2]

        triplet_array = numpy.delete(new_array, index_to_delete, axis=0)

        return Triplet(triplet_array)

    def coincide_i(self, mask) -> 'Triplet':
        """
        The methode removing all index i which do not coincide with the
        other triplet
        """
        mask_i = numpy.unique(mask.i[mask.values != 0])

        temp = (self._array[self.i == i] for i in mask_i)

        self._array = numpy.r_[tuple(temp)]

    def __sub__(self, other) -> 'Triplet':
        """
        The methode removing index[i] (rows) value corresponding between the two triplets.
        It doesn't change the other triplet, only the instance that called the method.
        """
        index_duplicate = numpy.isin(self.i, other.i)
        index_duplicate = numpy.arange(self.size)[index_duplicate]

        triplet_array = numpy.delete(self._array, index_duplicate, axis=0)

        return Triplet(triplet_array)

    def __iter__(self):
        for i, j, value in self._array:
            yield (int(i), int(j)), value

    def enumerate(self, start=None, stop=None):
        for n, (i, j, value) in enumerate(self._array[start:stop, :]):
            yield n, (int(i), int(j), value)

    def get_duplicate_index(self) -> numpy.ndarray:

        _, inverse, count = numpy.unique(self.index, axis=0, return_inverse=True, return_counts=True)

        index_duplicate = numpy.where(count > 1)[0]

        rows, cols = numpy.where(inverse == index_duplicate[:, numpy.newaxis])

        _, inverse_rows = numpy.unique(rows, return_index=True)

        return numpy.asarray(numpy.split(cols, inverse_rows[1:]), dtype=object)

    def merge_duplicate(self):
        duplicates = self.get_duplicate_index()

        if numpy.size(duplicates) == 0:
            return self._array

        for duplicate in duplicates:  # merge values
            self._array[int(duplicate[0]), 2] = self._array[duplicate.astype(int)][:, 2].sum()

        duplicates = [d[1:] for d in duplicates]

        self._array = numpy.delete(self._array, numpy.concatenate(duplicates).astype(int), axis=0)

    @property
    def max_i(self) -> int:
        """
        Return max i value, which is the first element of the index format.
        """
        return self.i.max()

    @property
    def max_j(self) -> int:
        """
        Return max j value, which is the second element of the index format.
        """
        return self.j.max()

    @property
    def min_i(self) -> float:
        """
        Return min i value, which is the first element of the index format.
        """
        return self.i.min()

    @property
    def min_j(self) -> float:
        """
        Return max j value, which is the second element of the index format.
        """
        return self.j.min()

    def to_dense(self, max_i: int = None, max_j: int = None) -> numpy.ndarray:
        """
        Return dense representation of the triplet, if none of max_i and max_j is provided
        it assumes the max_i and max_j is the shape of the dense matrix.
        """
        max_i = self.max_i + 1 if max_i is None else max_i
        max_j = self.max_j + 1 if max_j is None else max_j

        matrix = numpy.zeros([max_i, max_j])
        for index, value in self:
            matrix[index] = value

        return matrix

    def plot(self, max_i: int = None, max_j: int = None) -> None:
        """
        Plot the dense matrix representation of the triplet.
        """
        max_i = self.max_i + 1 if max_i is None else max_i
        max_j = self.max_j + 1 if max_j is None else max_j

        figure = Scene2D(unit_size=(6, 6), tight_layout=True)
        colorbar = ColorBar(discreet=False, position='right', numeric_format='%.4f')

        ax = Axis(row=0,
                  col=0,
                  title='Finite-difference coefficients structure',
                  show_legend=False,
                  show_grid=True,
                  colorbar=colorbar)

        artist = Mesh(scalar=numpy.flip(self.to_dense(max_i, max_j), axis=[0]), colormap='Blues')

        ax.AddArtist(artist)

        figure.AddAxes(ax)

        figure.Show()


class DiagonalTriplet(Triplet):
    def __init__(self, mesh: numpy.ndarray):
        size = mesh.size
        triplet_array = numpy.zeros([size, 3])
        triplet_array[:, 0] = numpy.arange(size)
        triplet_array[:, 1] = numpy.arange(size)
        triplet_array[:, 2] = mesh.ravel()

        super().__init__(triplet_array)


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
        return [self.size, self.size]

    def _get_diagonal_triplet_(self, coefficients: dict, offset: int, boundary=None):
        triplet = numpy.array([[0, 0, 0]])

        if boundary in ['anti-symmetric', 'symmetric']:
            coefficients = self.finit_coefficient.central()

        for idx, value in coefficients.items():
            if boundary == 'symmetric':
                value = value if idx == 0 else 2 * value
            if boundary == 'anti-symmetric':
                value = value if idx == 0 else 0

            end_idx = self.size - abs(idx * offset)
            line_0 = numpy.arange(end_idx)
            line_2 = numpy.ones(line_0.size) * value

            if idx < 0:
                sub_triplet = numpy.c_[line_0,
                                       line_0 - idx * offset,
                                       line_2]

            if idx == 0:
                sub_triplet = numpy.c_[line_0,
                                       line_0 - idx * offset,
                                       line_2]

            if idx > 0:
                sub_triplet = numpy.c_[line_0 + idx * offset,
                                       line_0,
                                       line_2]

            triplet = numpy.r_[triplet, sub_triplet]

        return Triplet(triplet[1:, :])

    def _get_top_boundary_(self):
        return self._get_diagonal_triplet_(boundary=self.boundaries['top'],
                                           coefficients=self.finit_coefficient.forward(),
                                           offset=self.n_y)

    def _get_bottom_boundary_(self):
        return self._get_diagonal_triplet_(boundary=self.boundaries['bottom'],
                                           coefficients=self.finit_coefficient.backward(),
                                           offset=self.n_y)

    def _get_right_boundary_(self):
        return self._get_diagonal_triplet_(boundary=self.boundaries['right'],
                                           coefficients=self.finit_coefficient.forward(),
                                           offset=1)

    def _get_left_boundary_(self):
        return self._get_diagonal_triplet_(boundary=self.boundaries['left'],
                                           coefficients=self.finit_coefficient.backward(),
                                           offset=1)

    def _compute_slices_idx_(self):
        for offset in range(1, self.finit_coefficient.offset_index + 1):
            x_idx, y_idx = numpy.mgrid[self.n_y - offset:self.size:self.n_y, 0:self.size]
            array = numpy.asarray([x_idx.ravel(), y_idx.ravel()]).T
            right_slice_triplet = Triplet(array, add_extra_column=True)

        for offset in range(0, self.finit_coefficient.offset_index):
            x_idx, y_idx = numpy.mgrid[offset:self.size:self.n_y, 0:self.size]
            array = numpy.asarray([x_idx.ravel(), y_idx.ravel()]).T
            left_slice_triplet = Triplet(array, add_extra_column=True)

        for offset in range(1, self.finit_coefficient.offset_index + 1):
            x_idx, y_idx = numpy.mgrid[self.size - offset * self.n_y:self.size, 0:self.size]
            array = numpy.asarray([x_idx.ravel(), y_idx.ravel()]).T
            top_slice_triplet = Triplet(array, add_extra_column=True)

        for offset in range(1, self.finit_coefficient.offset_index + 1):
            x_idx, y_idx = numpy.mgrid[0:offset * self.n_y, 0:self.size]
            array = numpy.asarray([x_idx.ravel(), y_idx.ravel()]).T
            bottom_slice_triplet = Triplet(array, add_extra_column=True)

        return right_slice_triplet, left_slice_triplet, top_slice_triplet, bottom_slice_triplet

    def _get_y_diagonal_triplet_(self):
        return self._get_diagonal_triplet_(coefficients=self.finit_coefficient.central(), offset=self.n_y)

    def _get_x_diagonal_triplet_(self):
        return self._get_diagonal_triplet_(coefficients=self.finit_coefficient.central(), offset=1)

    def _construct_triplet_(self, Addmesh: numpy.ndarray = None):
        right_slice_triplet, left_slice_triplet, top_slice_triplet, bottom_slice_triplet = self._compute_slices_idx_()

        self.triplets_component = Namespace(x=self._get_x_diagonal_triplet_(),
                                            y=self._get_y_diagonal_triplet_(),
                                            bottom=self._get_bottom_boundary_(),
                                            top=self._get_top_boundary_(),
                                            left=self._get_left_boundary_(),
                                            right=self._get_right_boundary_())

        self.triplets_component.x = self.triplets_component.x - left_slice_triplet - right_slice_triplet
        self.triplets_component.y = self.triplets_component.y - top_slice_triplet - bottom_slice_triplet

        self.triplets_component.top.coincide_i(mask=top_slice_triplet)
        self.triplets_component.bottom.coincide_i(mask=bottom_slice_triplet)
        self.triplets_component.right.coincide_i(mask=right_slice_triplet)
        self.triplets_component.left.coincide_i(mask=left_slice_triplet)

        self._triplet = self.triplets_component.y

        self._triplet.add_triplet(self.triplets_component.x, self.triplets_component.top, self.triplets_component.bottom, self.triplets_component.left, self.triplets_component.right)


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
    boundaries: Dict[str, str] = field(default_factory=lambda: ({'left': 'none', 'right': 'none'}))
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
        return self.n_x

    @property
    def shape(self):
        return [self.size, self.size]

    def _get_diagonal_triplet_(self, coefficients: dict, offset: int):
        triplet = numpy.array([[0, 0, 0]])

        for idx, value in coefficients.items():
            end_idx = self.size - abs(idx * offset)
            line_0 = numpy.arange(end_idx)
            line_2 = numpy.ones(line_0.size) * value

            # sub_triplet = numpy.c_[line_0, line_0 - idx * offset, line_2]

            if idx < 0:
                sub_triplet = numpy.c_[line_0, line_0 - idx * offset, line_2]

            if idx == 0:
                sub_triplet = numpy.c_[line_0, line_0 - idx * offset, line_2]

            if idx > 0:
                sub_triplet = numpy.c_[line_0 + idx * offset, line_0, line_2]

            triplet = numpy.r_[triplet, sub_triplet]

        return Triplet(triplet[1:, :])

    def _get_right_boundary_(self):
        return self._get_diagonal_triplet_(coefficients=self.finit_coefficient.forward(),
                                           offset=1)

    def get_diagonal_index(self, value, offset=0, mirror_values=True, mirror_multiplicator=1.):
        col_0 = numpy.arange(abs(offset), self.size)
        values = numpy.ones(col_0.size) * value

        array = numpy.c_[col_0 - abs(offset), col_0, values]

        if mirror_values:
            col_1 = numpy.arange(array[-1, 0] + 1, self.size)
            col_2 = array[-1, 1] - (1 + numpy.arange(col_1.size))

            values = numpy.ones(col_1.size) * value
            mirror_array0 = numpy.c_[col_1, col_2, values * mirror_multiplicator]

            col_3 = numpy.arange(array[0, 0], array[0, 0] + abs(offset))
            col_4 = array[0, 1] - (1 + numpy.arange(col_3.size))
            values = numpy.ones(col_4.size) * value
            mirror_array1 = numpy.c_[col_4, col_3 + 1, values * mirror_multiplicator]

        if offset < 0:
            array[:, 0], array[:, 1] = array[:, 1].copy(), array[:, 0].copy()
            array = numpy.r_[array, mirror_array1]
        else:
            array = numpy.r_[array, mirror_array0]

        return Triplet(array)

    def _get_left_boundary_(self):
        return self._get_diagonal_triplet_(coefficients=self.finit_coefficient.backward(),
                                           offset=1)

    def _compute_slices_idx_(self):
        right_slice = [[self.size - 1, 0, 1]]
        right_slice = Triplet(right_slice)

        left_slice = [[0, 0, 1]]
        left_slice = Triplet(left_slice)
        return right_slice, left_slice

    def _iterate_left_coefficients_(self):
        central = self.finit_coefficient.central().items()

    def _get_x_diagonal_triplet_(self):
        diagonals = []
        for idx, value in self.finit_coefficient.central().items():
            if idx < 0 and self.boundaries['left'] == 'symmetric':
                mirror_multiplicator = 1

            if idx < 0 and self.boundaries['left'] == 'anti-symmetric':
                mirror_multiplicator = -1

            if idx > 0 and self.boundaries['right'] == 'symmetric':
                mirror_multiplicator = 1

            if idx > 0 and self.boundaries['right'] == 'anti-symmetric':
                mirror_multiplicator = -1

            d = self.get_diagonal_index(value=value, offset=idx, mirror_multiplicator=mirror_multiplicator)
            diagonals.append(d)

        d0 = diagonals[0]
        for d in diagonals[1:]:
            d0 += d

        d0.plot()
        return d0

    def _construct_triplet_(self, Addmesh: numpy.ndarray = None):
        right_slice_triplet, left_slice_triplet = self._compute_slices_idx_()

        self.triplets_component = Namespace(x=self._get_x_diagonal_triplet_(),
                                            left=self._get_left_boundary_(),
                                            right=self._get_right_boundary_())

        # self.triplets_component.x = self.triplets_component.x - left_slice_triplet - right_slice_triplet

        # self.triplets_component.right.coincide_i(mask=right_slice_triplet)
        # self.triplets_component.left.coincide_i(mask=left_slice_triplet)

        self._triplet = self.triplets_component.x
        self._triplet.plot()
        # print()

        # self._triplet.add_triplet(self.triplets_component.left, self.triplets_component.right)

# -
