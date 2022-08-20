import numpy as np
import numpy
import matplotlib.pyplot as plt
from scipy import sparse
from dataclasses import dataclass, field
from typing import Dict

from PyFinitDiff.Utils import BoundaryClass, NameSpace
from PyFinitDiff.Coefficients import FinitCoefficients




@dataclass
class FiniteDifference2D():
    """
    Reference : ['math.toronto.edu/mpugh/Teaching/Mat1062/notes2.pdf']
    """
    Nx: int
    Ny: int
    dx: float = 1
    dy: float = 1
    Derivative: int = 1
    Accuracy: int = 2
    Naive: bool = False
    Symmetries: Dict[str, str] = field(default_factory = lambda: ({'Left': None, 'Right': None, 'Top': None, 'Bottom': None}))

    def __post_init__(self):
        self.FinitCoefficients = FinitCoefficients(Derivative=self.Derivative, Accuracy=self.Accuracy)


    @property
    def Size(self):
        return self.Nx * self.Ny

    @property
    def Shape(self):
        return [self.Size, self.Size]

    def SetRightBoundary(self, Value, Mesh):
        if Value in ['Symmetric', 1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx] = (value if idx==0 else 2*value if idx >0 else 0)

        elif Value in ['AntiSymmetric', -1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx] = (value if idx==0 else 0 if idx >0 else 0)

        elif Value in ['Zero', 0]:
            for idx, value in {0: -2, 1: 1}.items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        elif Value == 'None':
            for idx, value in self.FinitCoefficients.Forward().items():
                Mesh[self.Index.i == self.Index.j+idx] = value

        return Mesh


    def SetLeftBoundary(self, Value, Mesh):
        if Value in ['Symmetric', 1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx] = (value if idx==0 else 2*value if idx <0 else 0)

        elif Value in ['AntiSymmetric', -1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx] = (value if idx==0 else 0 if idx <0 else 0)


        elif Value in ['Zero', 0]:
            for idx, value in {0: -2, -1: 1}.items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        elif Value == 'None':
            for idx, value in self.FinitCoefficients.Backward().items():
                Mesh[self.Index.i == self.Index.j+idx] = value

        return Mesh


    def SetTopBoundary(self, Value, Mesh):
        if Value in ['Symmetric', 1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = (value if idx==0 else 2*value if idx >0 else 0)

        elif Value in ['AntiSymmetric', -1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = (value if idx==0 else 0 if idx >0 else 0)

        elif Value in ['Zero', 0]:
            for idx, value in {0: -2, 1: 1}.items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        elif Value == 'None':
            for idx, value in self.FinitCoefficients.Forward().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        return Mesh


    def SetBottomBoundary(self, Value, Mesh):
        if Value in ['Symmetric', 1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = (value if idx==0 else 2*value if idx <0 else 0)

        elif Value in ['AntiSymmetric', -1]:
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = (value if idx==0 else 0 if idx >0 else 0)

        elif Value in ['Zero', 0]:
            for idx, value in {0: -2, -1: 1}.items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        elif Value == 'None':
            for idx, value in self.FinitCoefficients.Backward().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        return Mesh



    def ComputeSlices(self):
        self.SliceRight, self.SliceLeft, self.SliceBottom, self.SliceTop = self.GetZeros(n=4, Type=bool)

        for Offset in range(1, self.FinitCoefficients.OffsetIndex+1):
            self.SliceRight[self.Nx-Offset::self.Nx, :] = True

        for Offset in range(0, self.FinitCoefficients.OffsetIndex ):
            self.SliceLeft[Offset::self.Nx, :] = True

        for Offset in range(1, self.FinitCoefficients.OffsetIndex+1 ):
            self.SliceTop[self.Size-Offset*self.Nx:, :] = True

        for Offset in range(1, self.FinitCoefficients.OffsetIndex+1):
            self.SliceBottom[:Offset*self.Nx, :] = True

        




    def GetXDiagonal(self):
        for idx, value in self.FinitCoefficients.Central().items():
            self.XMeshes.Center[self.Index.i == self.Index.j+idx] = value

        self.XMeshes.Right = self.SetRightBoundary(self.Symmetries['Right'], self.XMeshes.Right)
        self.XMeshes.Left = self.SetLeftBoundary(self.Symmetries['Left'], self.XMeshes.Left)



    def GetZeros(self, n, Type=float):
        return [ np.zeros(self.Shape).astype(Type) for i in range(n)]

    def GetOnes(self, n, Type=float):
        return [ np.ones(self.Shape).astype(Type) for i in range(n)]


    def ComputeMeshes(self):
        self.XMeshes = NameSpace(Right  = self.GetZeros(1)[0],
                                 Left   = self.GetZeros(1)[0],
                                 Center = self.GetZeros(1)[0] )

        self.YMeshes = NameSpace(Top    = self.GetZeros(1)[0],
                                 Bottom = self.GetZeros(1)[0],
                                 Center = self.GetZeros(1)[0] )


    def SlicesMeshes(self):
        if self.Naive:
            self.YMeshes.Bottom = 0
            self.YMeshes.Top    = 0

            self.XMeshes.Right  = 0
            self.XMeshes.Left   = 0

        else:
            self.YMeshes.Bottom[~self.SliceBottom]                  = 0
            self.YMeshes.Top[~self.SliceTop]                        = 0
            self.YMeshes.Center[self.SliceBottom + self.SliceTop]   = 0

            self.XMeshes.Right[~self.SliceRight]                    = 0
            self.XMeshes.Left[~self.SliceLeft]                      = 0
            self.XMeshes.Center[ self.SliceRight + self.SliceLeft ] = 0


    def AddMeshes(self):
        self.M = (self.YMeshes.Top + self.YMeshes.Bottom + self.YMeshes.Center)/(self.dy**self.FinitCoefficients.Derivative) # Y Derivative

        self.M += (self.XMeshes.Left + self.XMeshes.Right + self.XMeshes.Center)/(self.dx**self.FinitCoefficients.Derivative) # X Derivative


    def GetYDiagonal(self):
        for idx, value in self.FinitCoefficients.Central().items():
            self.YMeshes.Center[self.Index.i == self.Index.j - idx*self.Nx] = value

        self.YMeshes.Top = self.SetTopBoundary(self.Symmetries['Top'], self.YMeshes.Top)
        self.YMeshes.Bottom = self.SetBottomBoundary(self.Symmetries['Bottom'], self.YMeshes.Bottom)



    def Plot(self, Text=False):
        from pylab import cm
        cmap = cm.get_cmap('viridis', 101)

        Figure, Axes = plt.subplots(1,1, figsize=(10,9))
        Axes.set_title('Finite-difference coefficients.')
        Data = self.M

        Axes.grid(True)
        im0 = Axes.imshow(Data, cmap=cmap)
        plt.colorbar(im0, ax=Axes)
        if Text:
            for (i, j), z in np.ndenumerate(Data.astype(float)):
                Axes.text(j, i, '{:.0e}'.format(z), ha='center', va='center', size=8)

        plt.show()


    def Compute(self, AddMesh: numpy.ndarray = None):
        i, j = np.indices( self.Shape )

        self.Index = NameSpace(i=i, j=j)

        self.ComputeSlices()

        self.ComputeMeshes()

        self.GetYDiagonal()

        self.GetXDiagonal()

        self.SlicesMeshes()

        self.AddMeshes()

        # if AddMesh is not None:
            # np.fill_diagonal(self.M, self.M.diagonal() + AddMesh.flatten())



    @property
    def Dense(self):
        return self.M

    @property
    def Sparse(self):
        return sparse.csr_matrix(self.M) 

    def ToTriplet(self):
        Coordinate = self.Sparse.tocoo()
        return numpy.array( [Coordinate.col, Coordinate.row, Coordinate.data] )
