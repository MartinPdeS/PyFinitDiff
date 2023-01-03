@dataclass
class Diagonal():
    size: int
    offset: int
    value: float = 1.
    boundary: str = None

    def __post_init__(self):
        self._triplet = None
        self.boundary.offset = self.offset

    @property
    def triplet(self):
        if self._triplet is None:
            self.compute_triplet()
        return self._triplet

    @property
    def value_with_symmetry(self):
        if self.boundary.symmetry == 'symmetric':
            return self.value
        if self.boundary.symmetry == 'anti-symmetric':
            return -self.value
        if self.boundary.symmetry == 'zero':
            return 0.
        else:
            return self.value

    def mask_to_reverse_section(self, flip=False, inverse=True):
        if self.boundary is None:
            return 0
        mask = self.boundary.mask.astype(int)
        splited_mask = numpy.split(mask, numpy.where(numpy.diff(mask))[0]+1)

        s = 1 if not flip else -1
        sign = -1 if inverse else 1
        cum_sum = [numpy.cumsum(sub_mask)[::s] for sub_mask in splited_mask]

        return sign * 2 * numpy.concatenate(cum_sum, axis=0)

    def compute_triplet(self, reverse_zone=None):
        col_ref = numpy.arange(0, self.size)
        values = numpy.ones(self.size) * self.value

        col_0 = col_ref
        col_1 = col_ref + self.offset

        if self.offset > 0:
            reverse_zone = self.mask_to_reverse_section(flip=False, inverse=True)
        else:
            reverse_zone = self.mask_to_reverse_section(flip=True, inverse=False)

        if self.boundary is not None:
            col_1 += reverse_zone
            values[self.boundary.mask != 0] = self.value_with_symmetry

        array = numpy.c_[col_0, col_1, values]

        array = self.remove_out_of_bound(array)

        self._triplet = Triplet(array)

    def remove_out_of_bound(self, array: numpy.ndarray):
        i = array[:,0]
        j = array[:,1]

        return array[(0<=i) & (i<=self.size-1) & (0<=j) & (j<=self.size-1)]

    def plot(self):
        self.triplet.plot(max_i=self.size, max_j=self.size)


@dataclass
class Boundary():
    shape: list
    type: str
    symmetry: str = None

    def __post_init__(self):
        self.size = self.shape[0] * self.shape[1]
        self._mask = None
        self.row_range = numpy.arange(0, self.size)


    @property
    def mask(self):
        if self._mask is None:
            self._construct_mask_()
        return self._mask

    def get_triplet(self) -> Triplet:
        index_0_init = numpy.nonzero(self.mask)[0]
        index_1_init = numpy.arange(self.size)

        index_0 = numpy.repeat(index_0_init, repeats=index_1_init.size)

        index_1 = numpy.tile(index_1_init, reps=index_0_init.size)

        values = numpy.ones(index_1.size)

        array = numpy.c_[index_0, index_1, values]

        return Triplet(array)

    def plot(self) -> None:
        triplet = self.get_triplet()

        triplet.plot(max_i=self.size, max_j=self.size)


    def _get_n0_n1_pattern_(self, n_0, n_1, offset=0, start_with_zero=False):
        if start_with_zero:
            array = numpy.ones(self.size)
            array[(self.row_range+offset) % (n_1 + n_0) < n_0] = 0

        else:
            array = numpy.zeros(self.size)
            array[(self.row_range+offset) % (n_1 + n_0) < n_1] = 1

        return array

    def _construct_mask_(self) -> None:
        match self.type.lower():
            case 'left':
                boundary_mask = self._get_n0_n1_pattern_(n_0=shape[0] - abs(self.offset),
                                                         n_1=abs(self.offset),
                                                         start_with_zero=True)
            case 'right':
                boundary_mask = self._get_n0_n1_pattern_(n_0=shape[0] - abs(self.offset),
                                                         n_1=abs(self.offset),
                                                         start_with_zero=False)
            case 'top':
                boundary_mask = numpy.zeros(self.size)
                boundary_mask[:-self.offset] = 1
            case 'bottom':
                boundary_mask = numpy.zeros(self.size)
#                 boundary_mask[-(shape[0]+self.offset):] = 1
                boundary_mask[-self.offset:] = 1
            case 'none':
                boundary_mask = numpy.zeros(self.size)

        self._mask = boundary_mask


shape = [6, 6]
size = shape[0]*shape[1]



d_central = Diagonal(value=6, offset=0, size=size, boundary=Boundary(shape=shape, type='none'))

d0 = Diagonal(value=-4, offset=-6, size=size, boundary=Boundary(shape=shape, type='top', symmetry='symmetric'))
d1 = Diagonal(value=-4, offset=+6, size=size, boundary=Boundary(shape=shape, type='bottom', symmetry='symmetric'))


d2 = Diagonal(value=-2, offset=-12, size=size, boundary=Boundary(shape=shape, type='top', symmetry='symmetric'))
d3 = Diagonal(value=-2, offset=+12, size=size, boundary=Boundary(shape=shape, type='bottom', symmetry='symmetric'))

d4 = Diagonal(value=-2, offset=-1, size=size, boundary=Boundary(shape=shape, type='right', symmetry='symmetric'))
d5 = Diagonal(value=-2, offset=+1, size=size, boundary=Boundary(shape=shape, type='left', symmetry='anti-symmetric'))

d6 = Diagonal(value=-2, offset=-2, size=size, boundary=Boundary(shape=shape, type='right', symmetry='symmetric'))
d7 = Diagonal(value=-2, offset=+2, size=size, boundary=Boundary(shape=shape, type='left', symmetry='anti-symmetric'))

diagonals = [
             d0,
             d1,
             d2,
             d3,
             d4,
             d5,
             d6,
             d7
]

triplet = d_central.triplet

for d in diagonals:
    triplet += d.triplet


triplet.plot()


