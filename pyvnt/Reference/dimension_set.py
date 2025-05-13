from enum import IntEnum, auto
from pyvnt.Reference.error_classes import IncorrectLengthError
from pyvnt.Reference.basic import *

class Dim_Type(IntEnum):
    MASS = auto()
    LENGTH = auto()
    TIME = auto()
    TEMPERATURE = auto()
    MOLES = auto()
    CURRENT = auto()
    LUMINOUS_INTENSITY = auto()

class Dim_Set_P(Value_P):
    '''
    Dim_Set_P class is a class that represents a set of dimensions.
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
    __slots__ = ['_Value_P__name', '_Dim_Set_P__Dim_Type', '_Dim_Set_P__dimm']

    def __init__(self, name, dimms: [] = [0] * 7):
        super(Dim_Set_P, self).__init__()

        self.__Dim_Type = Dim_Type
        self.__dimm = [0] * 7
        self._Value_P__name = name

        if len(dimms) == 7:
            self.set_properties(*dimms)
        else:
            raise IncorrectLengthError(len(dimms))
    
    def instance_restricted(self):
        pass
    
    def set_properties(self, m = 0, l = 0, t = 0, temp = 0, mol = 0, c = 0, li = 0):
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
            self.__dimm[Dim_Type.MASS - 1] = m
        if l:
            self.__dimm[Dim_Type.LENGTH - 1] = l
        if t:
            self.__dimm[Dim_Type.TIME - 1] = t
        if temp:
            self.__dimm[Dim_Type.TEMPERATURE - 1] = temp 
        if mol:
            self.__dimm[Dim_Type.MOLES - 1] = mol 
        if c:
            self.__dimm[Dim_Type.CURRENT - 1] = c
        if li:
            self.__dimm[Dim_Type.LUMINOUS_INTENSITY - 1] = li
    
    def __repr__(self):
        return f"Dim_Set_P(name : {self._Value_P__name}, dimm : {self.__dimm})"
    
    def give_val(self):
        '''
        Returns the dimensions of the physical quantity.
        '''
        return self.__dimm
    
    def write_out(self, file):
        '''
        Returns the dimensions value in a string format
        '''
        file.write(" ".join(i for i in str(self.__dimm).split(",")))

    
