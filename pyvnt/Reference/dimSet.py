from enum import IntEnum, auto
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
    __slots__ = ['_ValueProperty__name', '_DimmSet__dimmtype', '_DimmSet__dimm']

    def __init__(self, name, dimms: [] = [0] * 7):
        super(DimmSet, self).__init__()

        self.__dimmtype = DimmType
        self.__dimm = [0] * 7
        self._ValueProperty__name = name

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
            self.__dimm[DimmType.MASS - 1] = m
        if l:
            self.__dimm[DimmType.LENGTH - 1] = l
        if t:
            self.__dimm[DimmType.TIME - 1] = t
        if temp:
            self.__dimm[DimmType.TEMPERATURE - 1] = temp 
        if mol:
            self.__dimm[DimmType.MOLES - 1] = mol 
        if c:
            self.__dimm[DimmType.CURRENT - 1] = c
        if li:
            self.__dimm[DimmType.LUMINOUS_INTENSITY - 1] = li
    
    def __repr__(self):
        return f"DimmSet(name : {self._ValueProperty__name}, dimm : {self.__dimm})"
    
    def giveVal(self):
        '''
        Returns the dimensions of the physical quantity.
        '''

        return self.__dimm

    
