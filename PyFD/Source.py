import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.special import jv, kv
from scipy import interpolate
from scipy.special import kv
EigenSolver = np.linalg.eig
pi = np.pi
from numpy.linalg import solve as SystemSolver
from scipy.sparse.linalg import eigs as EigenSolverS
from scipy import sparse
import pprint
EigenSolver = np.linalg.eig



import .PlotConfig




class FiniteDifference2D():
    Reference = ['math.toronto.edu/mpugh/Teaching/Mat1062/notes2.pdf']

    def __init__(self,
                 Nx: int,
                 Ny: int,
                 dx: float,
                 dy: float,
                 Derivative: int,
                 Accuracy: int = 2,
                 Boundary: str ='Dirichlet',
                 Naive: bool = False):

        self.Naive    = Naive
        self.Nx       = Nx
        self.Ny       = Ny
        self.Size     = Nx*Ny
        self.Shape    = [Nx*Ny, Nx*Ny]
        self.dx       = dx
        self.dy       = dy
        self.Boundary = BoundaryClass()

        self.FinitCoefficients = FinitCoefficients(Derivative=Derivative, Accuracy=Accuracy)


    def SetRightBoundary(self, Mesh):
        if self.Boundary.Right == 'Symmetric':
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx] = (value if idx==0 else 2*value if idx >0 else 0)

        elif self.Boundary.Right == 'AntiSymmetric':
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx] = (value if idx==0 else 0 if idx >0 else 0)

        elif self.Boundary.Bottom == 'Zero':
            for idx, value in {0: -2, 1: 1}.items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        elif self.Boundary.Right == 'None':
            for idx, value in self.FinitCoefficients.Forward().items():
                Mesh[self.Index.i == self.Index.j+idx] = value

        return Mesh


    def SetLeftBoundary(self, Mesh):
        if self.Boundary.Left == 'Symmetric':
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx] = (value if idx==0 else 2*value if idx <0 else 0)

        elif self.Boundary.Left == 'AntiSymmetric':
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx] = (value if idx==0 else 0 if idx <0 else 0)


        elif self.Boundary.Bottom == 'Zero':
            for idx, value in {0: -2, -1: 1}.items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        elif self.Boundary.Left == 'None':
            for idx, value in self.FinitCoefficients.Backward().items():
                Mesh[self.Index.i == self.Index.j+idx] = value

        return Mesh


    def SetTopBoundary(self, Mesh):
        if self.Boundary.Top == 'Symmetric':
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = (value if idx==0 else 2*value if idx >0 else 0)

        elif self.Boundary.Top == 'AntiSymmetric':
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = (value if idx==0 else 0 if idx >0 else 0)

        elif self.Boundary.Bottom == 'Zero':
            for idx, value in {0: -2, 1: 1}.items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        elif self.Boundary.Top == 'None':
            for idx, value in self.FinitCoefficients.Forward().items():
                print('Top Boundary = None', idx, value)
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

        self.XMeshes.Right = self.SetRightBoundary(self.XMeshes.Right)
        self.XMeshes.Left = self.SetLeftBoundary(self.XMeshes.Left)



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
            print('YCentral', idx, value)
            self.YMeshes.Center[self.Index.i == self.Index.j - idx*self.Nx] = value

        self.YMeshes.Top = self.SetTopBoundary(self.YMeshes.Top)
        self.YMeshes.Bottom = self.SetBottomBoundary(self.YMeshes.Bottom)



    def Plot(self):
        from pylab import cm
        cmap = cm.get_cmap('viridis', 101)

        Figure, Axes = plt.subplots(1,1, figsize=(10,9))

        Axes.grid(False)
        im0 = Axes.pcolor(self.M.real[::-1,::1], shading='auto', cmap=cmap)
        plt.colorbar(im0, ax=Axes)

        plt.show()


    def SetBottomBoundary(self, Mesh):
        if self.Boundary.Bottom == 'Symmetric':
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = (value if idx==0 else 2*value if idx <0 else 0)

        elif self.Boundary.Bottom == 'AntiSymmetric':
            for idx, value in self.FinitCoefficients.Central().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = (value if idx==0 else 0 if idx >0 else 0)

        elif self.Boundary.Bottom == 'Zero':
            for idx, value in {0: -2, -1: 1}.items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        elif self.Boundary.Bottom == 'None':
            for idx, value in self.FinitCoefficients.Backward().items():
                Mesh[self.Index.i == self.Index.j+idx*self.Nx] = value

        return Mesh


    def Compute(self):
        i, j = np.indices( self.Shape )

        self.Index = NameSpace(i=i, j=j)

        self.ComputeSlices()

        self.ComputeMeshes()

        self.GetYDiagonal()

        self.GetXDiagonal()

        self.SlicesMeshes()

        self.AddMeshes()
