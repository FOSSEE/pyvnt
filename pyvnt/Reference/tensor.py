from pyvnt.Reference.basic import *
from pyvnt.Reference.error_classes import InvalidTupleError
from pyvnt.Reference.vector import Vector_P
import numpy as np
from typing import TypeVar
Self = TypeVar("Self", bound="Tensor_P") # Cause python version < 3.11 dont support Self as in built function
import math


class Tensor_P(Value_P):
    '''
    A property that holds a tensor value.

    Tensor is stored in the following manner:
    [[xx, xy, xz],
    [yx, yy, yz],
    [zx, zy, zz]]

    Constructor Parameters:
        name: The name of the property.
        value: list
    '''

    __slots__ = ('_Tensor_P__name', '_Tensor_P__values')

    def instance_restricted(self):
        pass

    def __init__(self, name, value: [Flt_P]):
        super(Tensor_P, self).__init__()

        inputs = []

        for i in range(3):
            for j in range(3):
                inputs.append((i+1, j+1, value[i*3+j]))
        self.set_properties(name, *inputs)

    # TODO: Implement matrix operations for tensors, refer to the OpenFOAM team for details

    # TODO: Change the way input is taken in this method, refer Matlab's matrix slicing --done
    def set_properties(self, name: str, *args: (int, int, Flt_P)) -> None:
        '''
        Function to edit the values stored in the object

        Parameters:
        name: The name of the property.
        *args: The values of the tensor in the form of tuples.

        The tuples should be in the form of (i, j, Flt_P) where i and j are the indices of the tensor in 1-based indexing.
        In order to set the value for an entire row or column, set the index to 0 for the row or column respectively.

        Example: 
        To set the value of the entire row 1 to 5, the tuple should be (1, 0, Flt_P(name, 5))
        To set the value of the entire column 2 to 5, the tuple should be (0, 2, Flt_P(name, 5))
        To set the value of the element at row 1 and column 2 to 5, the tuple should be (1, 2, Flt_P(name, 5))

        '''
        self._Value_P__name = name

        inputs = list(args)
        self.__values = [[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]]

        for t in inputs:
            if len(t) != 3 or type(t[0]) != int or type(t[1]) != int or type(t[2]) != Flt_P:
                raise InvalidTupleError(t)
            else:
                if t[0] == 0 and t[1] == 0:
                    val = t[2]
                    self.__values = [[val, val, val], 
                                     [val, val, val], 
                                     [val, val, val]]
                elif t[0] == 0:
                    for i in range(3):
                        self.__values[i][t[1]-1] = t[2]
                elif t[1] == 0:
                    for i in range(3):
                        self.__values[t[0]-1][i] = t[2]
                elif t[0] != 0 and t[1] != 0:
                    self.__values[t[0]-1][t[1]-1] = t[2]
                else:
                    raise InvalidTupleError(t)
    
    def xx(self) -> Flt_P:
        '''
        Returns the xx value of the tensor
        '''
        return self.__values[0][0].give_val()
    
    def xy(self) -> Flt_P:
        '''
        Returns the xy value of the tensor
        '''
        return self.__values[0][1].give_val()
    
    def xz(self) -> Flt_P:
        '''
        Returns the xz value of the tensor
        '''
        return self.__values[0][2].give_val()
    
    def yx(self) -> Flt_P:
        '''
        Returns the yx value of the tensor
        '''
        return self.__values[1][0].give_val()
    
    def yy(self) -> Flt_P:
        '''
        Returns the yy value of the tensor
        '''
        return self.__values[1][1].give_val()
    
    def yz(self) -> Flt_P:
        '''
        Returns the yz value of the tensor
        '''
        return self.__values[1][2].give_val()
    
    def zx(self) -> Flt_P:
        '''
        Returns the zx value of the tensor
        '''
        return self.__values[2][0].give_val()
    
    def zy(self) -> Flt_P:
        '''
        Returns the zy value of the tensor
        '''
        return self.__values[2][1].give_val()
    
    def zz(self) -> Flt_P:
        '''
        Returns the zz value of the tensor
        '''
        return self.__values[2][2].give_val()
    
    def row(self, r: int) -> Vector_P:
        '''
        Returns the row vector of the tensor

        Parameters:
        r: The row number of the tensor in 1 based indexing
        '''
        return Vector_P(self._Value_P__name + "_row", self.__values[r - 1][0], self.__values[r - 1][1], self.__values[r - 1][2])
    
    def col(self, c: int) -> Vector_P:
        '''
        Returns the column vector of the tensor

        Parameters:
        c: The column number of the tensor in 1 based indexing
        '''
        return Vector_P(self._Value_P__name + "_col", self.__values[0][c - 1], self.__values[1][c - 1], self.__values[2][c - 1])
    
    def diag(self) -> Vector_P:
        '''
        Returns the diagonal vector of the tensor
        '''
        return Vector_P(self._Value_P__name + "_diag", self.__values[0][0], self.__values[1][1], self.__values[2][2])

    def T(self) -> Self:
        '''
        Return non-Hermitian transpose of the tensor
        '''
        return Tensor_P(self._Value_P__name + "_T", [self.__values[0][0], self.__values[1][0], self.__values[2][0],
                                                                 self.__values[0][1], self.__values[1][1], self.__values[2][1],
                                                                 self.__values[0][2], self.__values[1][2], self.__values[2][2]])

    def inv(self) -> Self:
        '''
        Returns the inverse of the tensor
        '''
        ar = np.array([[self.xx().give_val(), self.xy().give_val(), self.xz().give_val()],
                       [self.yx().give_val(), self.yy().give_val(), self.yz().give_val()],
                       [self.zx().give_val(), self.zy().give_val(), self.zz().give_val()]])

        res = np.linalg.inv(ar)

        return Tensor_P(self._Value_P__name + "_inv", [res[0][0], res[0][1], res[0][2],
                                                                   res[1][0], res[1][1], res[1][2],
                                                                   res[2][0], res[2][1], res[2][2]])

    def inner(self, t: Self) -> Self:
        '''
        Returns the inner product of the tensor with another tensor
        '''
        return Tensor_P(self._Value_P__name + "_inner", [self.xx()*t.xx() + self.xy()*t.yx() + self.xz()*t.zx(),
                                                                     self.xx()*t.xy() + self.xy()*t.yy() + self.xz()*t.zy(),
                                                                     self.xx()*t.xz() + self.xy()*t.yz() + self.xz()*t.zz(),

                                                                     self.yx()*t.xx() + self.yy()*t.yx() + self.yz()*t.zx(),
                                                                     self.yx()*t.xy() + self.yy()*t.yy() + self.yz()*t.zy(),
                                                                     self.yx()*t.xz() + self.yy()*t.yz() + self.yz()*t.zz(),

                                                                     self.zx()*t.xx() + self.zy()*t.yx() + self.zz()*t.zx(),
                                                                     self.zx()*t.xy() + self.zy()*t.yy() + self.zz()*t.zy(),
                                                                     self.zx()*t.xz() + self.zy()*t.yz() + self.zz()*t.zz()])

    def schur(self, t: Self) -> Self:
        '''
        Returns the Schur product of the tensor with another tensor
        '''
        return Tensor_P(self._Value_P__name + "_schur", [self.xx()*t.xx(), self.xy()*t.xy(), self.xz()*t.xz(),
                                                                     self.yx()*t.yx(), self.yy()*t.yy(), self.yz()*t.yz(),
                                                                     self.zx()*t.zx(), self.zy()*t.zy(), self.zz()*t.zz()])
    
    def give_val(self):
        '''
        Returns the tensor value
        '''
        res = (self.xx(), self.xy(), self.xz(),
               self.yx(), self.yy(), self.yz(),
               self.zx(), self.zy(), self.zz())
        return res
    
    def write_out(self, file):
        '''
        Writes the tensor value to a file

        Parameters:
        file: The file object to write the value to
        '''
        file.write(f"{self.give_val()}")

    def __repr__(self):
        return f"Tensor_P(name = {self._Value_P__name}, xx = {self.xx()}, xy = {self.xy()}, xz = {self.xz()}, yx = {self.yx()}, yy = {self.yy()}, yz = {self.yz()}, zx = {self.zx()}, zy = {self.zy()}, zz = {self.zz()})"


        
        