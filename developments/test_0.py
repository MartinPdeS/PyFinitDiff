
from PyFinitDiff.finite_difference_1D import FiniteDifference
from PyFinitDiff.finite_difference_1D import Boundaries

boundaries = Boundaries(left='none', right='none')

n_x = 12
fd = FiniteDifference(
    n_x=n_x,
    dx=1,
    derivative=2,
    accuracy=2,
    boundaries=boundaries
)

fd.triplet.plot()

dense_matrix = fd.triplet.to_scipy_sparse()

sparse_matrix = fd.triplet.to_scipy_sparse()