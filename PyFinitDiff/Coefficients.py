CCoefficients = \
{'derivative 1':
  {'accuracy 2': {-4: +0.0,  -3: +0.0,  -2: 0.0,  -1: -1/2, 0: 0.,  +1: 1/2, +2: 0.0,   +3: 0.0,   +4: 0.0},
   'accuracy 4': {-4: +0.0,  -3: +0.0,  -2: 1/12, -1: -2/3, 0: 0.,  +1: 2/3, +2: -1/12, +3: 0.0,   +4: 0.0},
   'accuracy 6': {-4: +0.0,  -3: -1/60, -2: 3/20, -1: -3/4, 0: 0.,  +1: 3/4, +2: -3/20, +3: 1/60,  +4: 0.0},
   'accuracy 8': {-4: 1/280, -3: 4/105, -2: 1/5,  -1: +4/5, 0: 0.,  +1: 4/5, +2: -1/5,  +3: 4/105, +4: -1/280},
 },

 'derivative 2':
  {
   'accuracy 2': {-4: +0.,    -3:0.,     -2: 0.,    -1: 1.,  0: -2,      +1:1.,   +2:0.,     +3: 0.,    +4: +0.},
   'accuracy 4': {-4: +0.,    -3:0.,     -2: -1/12, -1: 4/3, 0: -5/2,    +1: 4/3, +2: -1/12, +3: 0.,    +4: +0.},
   'accuracy 6': {-4: +0.,    -3: 1/90,  -2: -3/20, -1: 3/2, 0: -49/18,  +1: 3/2, +2: -3/20, +3: 1/90,  +4: +0.},
   'accuracy 8': {-4: -1/560, -3: 8/315, -2: -1/5,  -1: 8/5, 0: -205/72, +1: 8/5, +2: -1/5,  +3: 8/315, +4: -1/560},
  },
}


FCoefficients = \
{'derivative 1':
  { 'accuracy 2': {0: -3/2,    +1: 2, +2: -1/2,  +3: 0.,   +4: 0.,   +5: 0.,  +6: 0.},
    'accuracy 4': {0: -25/12,  +1: 4, +2: -3,    +3: 4/3,  +4: -1/4, +5: 0.,  +6: 0.},
    'accuracy 6': {0: -49/20 , +1: 6, +2: -15/2, +3: 20/3, +4: -15/4, 5: 6/5, +6: -1/6},
  },
 'derivative 2':
  { 'accuracy 2': {0: +2 ,     +1: -5 ,     +2: 4,      +3: -1,      +4: +0.,    +5:0.,       +6: +0.,        +7: +0.},
    'accuracy 4': {0: +15/4,   +1: -77/6,   +2: 107/6,  +3: -13,     +4: +61/12, +5: -5/6,    +6: +0.,        +7: +0.},
    'accuracy 6': {0: +469/90, +1: -223/10, +2: 879/20, +3: -949/18, +4: +41,    +5: -201/10, +6: +1019/180,  +7: -7/10},
  },
}


BCoefficients = \
{'derivative 1':
 { 'accuracy 2': {0: +3/2,    -1: -2, -2: +1/2,  -3: +0.,   -4: +0.,   -5: +0.,  -6: +0.},
   'accuracy 4': {0: +25/12,  -1: -4, -2: +3,    -3: -4/3,  -4: +1/4,  -5: +0.,  -6: +0.},
   'accuracy 6': {0: +49/20 , -1: -6, -2: +15/2, -3: -20/3, -4: +15/4, -5: -6/5, -6: +1/6},
 },
 'derivative 2':
  { 'accuracy 2': {0: +2 ,     -1: -5 ,     -2: +4,      -3: -1,      -4: +0.,    -5: +0.,     -6: +0.,      -7: +0.},
    'accuracy 4': {0: +15/4,   -1: -77/6,   -2: +107/6,  -3: -13,     -4: +61/12, -5: -5/6,    -6: +0.,      -7: +0.},
    'accuracy 6': {0: +469/90, -1: -223/10, -2: +879/20, -3: -949/18, -4: +41,    -5: -201/10, -6: 1019/180, -7: -7/10},
  },
}


class FinitCoefficients():
    accuracyList = [2, 4, 6]
    derivativeList = [1, 2]

    _CentralCoef = CCoefficients
    _ForwardCoef = FCoefficients
    _BackwardCoef = BCoefficients

    def __init__(self, derivative, accuracy):
        self.derivative = derivative
        self.accuracy = accuracy

        assert accuracy in self.accuracyList, f'Error accuracy has to be in the list {self.accuracyList}'
        assert derivative in self.derivativeList, f'Error derivative has to be in the list {self.derivative}'

        D = f"derivative {self.derivative}"
        A = f"accuracy {self.accuracy}"
        self._Central = {key: value for key, value in self._CentralCoef[D][A].items() if value != 0.}
        self._Backward = {key: value for key, value in self._BackwardCoef[D][A].items() if value != 0.}
        self._Forward = {key: value for key, value in self._ForwardCoef[D][A].items() if value != 0.}

    def Central(self, attribute='zero'):
        if attribute == 'zero':
            return self._Central
        elif attribute == 'symmetric':
            return {key: (value if key == 0 else 2 * value) for key, value in self._Central.items()}
        elif attribute == 'anti_symmetric':
            return {key: (value if key == 0 else 0) for key, value in self._Central.items()}

    def Backward(self, attribute='zero'):
        if attribute == 'zero':
            return self._Backward
        elif attribute == 'symmetric':
            return {key: (value if key == 0 else 2 * value) for key, value in self._Forward.items()}
        elif attribute == 'anti_symmetric':
            return {key: (value if key == 0 else 0) for key, value in self._Forward.items()}

    def Forward(self, attribute='zero'):
        if attribute == 'zero':
            return self._Forward
        elif attribute == 'symmetric':
            return {key: (value if key == 0 else 2 * value) for key, value in self._Forward.items()}
        elif attribute == 'anti_symmetric':
            return {key: (value if key == 0 else 0) for key, value in self._Forward.items()}

    def Test(self):
        Sum = 0
        for key, value in self.Central.items():
            Sum += value
        print(f'Central sum: {Sum}')

        Sum = 0
        for key, value in self.Forward.items():
            Sum += value
        print(f'Forward sum: {Sum}')

        Sum = 0
        for key, value in self.Backward.items():
            Sum += value
        print(f'Backward sum: {Sum}')

    def Print(self):
        import pprint
        temp = {'Central': self.Central,
                'Forward': self.Forward,
                'Backward': self.Backward}
        pprint.PrettyPrinter(indent=4).pprint(temp)

    @property
    def OffsetIndex(self):
        OffsetIndex = 0
        for Index, value in self.Central().items():
            if value != 0 and Index > OffsetIndex:
                OffsetIndex = Index

        return OffsetIndex
