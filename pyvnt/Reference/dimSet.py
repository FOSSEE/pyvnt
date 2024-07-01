from enum import IntEnum
from pyvnt.Reference.errorClasses import IncorrectLengthError
from pyvnt.Reference.basic import *

class DimmType(IntEnum):
    MASS = auto()
    LENGTH = auto()
    TIME = auto()
    TEMPERATURE = auto()
    MOLES = auto()
    CURRENT = auto()
    LUMINOUS_INTENSITY = auto()

class DimmSet(ValueProperty):
    '''
    DimmSet class is a class that represents a set of dimensions.
    It is used to represent the dimensions of a physical quantity.

    Contrsucor Parameters:
        name: str
            The name of the physical quantity
        dimms: list
            A list of 7 elements representing the dimensions of the physical quantity.
            The elements should be in the following order:
                1. Mass
                2. Length
                3. Time
                4. Temperature
                5. Moles
                6. Current
                7. Luminous Intensity

    '''
    __slots__ = ['name', 'dimmtype', 'dimm']

    def __init__(self, name, dimms: [] = [0] * 7):
        super(DimmSet, self).__init__()

        self.dimmtype = DimmType
        self.dimm = [0] * 7
        self.name = name

        if len(dimms) == 7:
            self.setProperties(*dimms)
        else:
            raise IncorrectLengthError(len(dimms))
    
    def instance_restricted(self):
        pass
    
    def setProperties(self, m = 0, l = 0, t = 0, temp = 0, mol = 0, c = 0, li = 0):
        '''
        Sets the dimensions of the physical quantity.

        Parameters:
            m: int
                The dimension of mass.
            l: int
                The dimension of length.
            t: int
                The dimension of time.
            temp: int
                The dimension of temperature.
            mol: int
                The dimension of moles.
            c: int
                The dimension of current.
            li: int
                The dimension of luminous intensity.
        '''
        if m:
            self.dimm[DimmType.MASS] = m
        if l:
            self.dimm[DimmType.LENGTH] = l
        if t:
            self.dimm[DimmType.TIME] = t
        if temp:
            self.dimm[DimmType.TEMPERATURE] = tmp 
        if mol:
            self.dimm[DimmType.MOLES] = mol 
        if c:
            self.dimm[DimmType.CURRENT] = c
        if li:
            self.dimm[DimmType.LUMINOUS_INTENSITY] = li
    
    def __repr__(self):
        return f"DimmSet({self.dimm})"
    
    def giveVal(self):
        '''
        Returns the dimensions of the physical quantity.
        '''

        return self.dimm

    
