
from pyvnt.Reference.basic import * 
from typing import TypeVar
import math
Self = TypeVar("Self", bound="Vector_P") # Cause python version < 3.11 dont support Self as in built function
class Vector_P(Value_P):
    '''
    Property Class to store vector values 
    
    Constructor Parameters:
        name: Name of the property of which vector value is to be stored
        x: Flt_P object to store x value of the vector
        y: Flt_P object to store y value of the vector
        z: Flt_P object to store z value of the vector
    '''
    
    __slots__ = ('_Value_P__name', '_Vector_P__x', '_Vector_P__y', '_Vector_P__z')
    
    def instance_restricted(self):
        pass
        
    # TODO: Confirm about the format exoected from a vector
    def __init__(self, name: str, x: Flt_P, y: Flt_P, z: Flt_P):
        super(Vector_P, self).__init__()
        self.set_properties(name, x, y, z)
        
    def set_properties(self, name: str = None, x: Flt_P = None, y: Flt_P = None, z: Flt_P = None) -> None:
        '''
        Function to edit the values stored in the object
        
        Parameters:
        name: Name of the property of which vector value is to be stored
        x: Flt_P object to store x value of the vector
        y: Flt_P object to store y value of the vector
        z: Flt_P object to store z value of the vector
        '''
        if name:
            self._Value_P__name = name
            
        if x:
            self._Vector_P__x = x
            
        if y:
            self._Vector_P__y = y
            
        if z:
            self._Vector_P__z = z
        
    def x(self) -> float:
        '''
        Returns the x value of the vector
        '''
        
        return self._Vector_P__x.give_val()
        
    def y(self) -> float:
        '''
        Returns the y value of the vector
        '''
        return self._Vector_P__y.give_val()
        
    def z(self) -> float:
        '''
        Returns the z value of the vector
        '''
        return self._Vector_P__z.give_val()
        
    def magnitude(self) -> float:
        '''
        Returns the magnitude of the vector
        '''
        return math.sqrt(self._Vector_P__x.give_val()**2 + self._Vector_P__y.give_val()**2 + self._Vector_P__z.give_val()**2)
        
    def normalise(self, tol: Flt_P) -> Self:
        '''
        Normalises the vector
        
        Parameters:
            tol: The tolerance value for the normalisation. If the magnitude of the vector is less than the tolerance, the vector is set to 0.
        '''
        s = self.magnitude()
        if s < tol.give_val():
            self.set_properties(self._Value_P__name, Flt_P(self._Value_P__name + "_x", 0), Flt_P(self._Value_P__name + "_y", 0), Flt_P(self._Value_P__name + "_z", 0))
        else:
            self.set_properties(self._Value_P__name, Flt_P(self._Value_P__name + "_x", self._Vector_P__x.give_val()/s), Flt_P(self._Value_P__name + "_y", self._Vector_P__y.give_val()/s), Flt_P(self._Value_P__name + "_z", self._Vector_P__z.give_val()/s))
        return self
        
    def give_val(self):
        '''
        Returns the vector value
        '''
        
        res = (self._Vector_P__x.give_val(), self._Vector_P__y.give_val(), self._Vector_P__z.give_val())
        
        return res
    
    def write_out(self, file):
        '''
        Returns the vector value in a string format
        '''
        file.write(f"({self._Vector_P__x.give_val()} {self._Vector_P__y.give_val()} {self._Vector_P__z.give_val()})")
    
    def __repr__(self):
        return f"Vector_P(name = {self._Value_P__name}, x = {self._Vector_P__x.give_val()}, y = {self._Vector_P__y.give_val()}, z = {self._Vector_P__z.give_val()})"