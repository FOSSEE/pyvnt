from dataclasses import dataclass, replace, field
from typing import Any
import enum
from abc import ABC, abstractmethod
from pyvnt.Reference.error_classes import *

# Property Classes

class Value_P(ABC):
    '''
    Abstract parent class for all the property classes

    Do not create oobject of this class
    '''
    __slots__ = ('_Value_P__name')

    def __init__(self):
        self.__name = ""

    @abstractmethod
    def instance_restricted(self):
        pass

class Int_P(Value_P):
    '''
    Property class to store integer values

    Contructor Parameters:
        name: Name of the property of which integer value is to be stored
        default: Current value of the property (Optional, default = 1)
        minimum: Minimum value of the range of values that can be stored in the property object (Optional, default = 0)
        maximum: Maximum value of the range of values that can be stored in the property object (Optional, default = 100)

    '''
    __slots__ = ('_Value_P__name', '_Int_P__default',
                 '_Int_P__minimum', '_Int_P__maximum')

    def __init__(self, name: str, default: int = 1, minimum: int = 0, maximum: int = 100):
        super(Int_P, self).__init__()
        self.set_properties(name, default, minimum, maximum)

    def instance_restricted(self):
        pass

    def set_properties(self, name: str, default: int, minimum: int, maximum: int):
        '''
        Function to edit the values stored in the object

        Paramters:
            name: Name of the property 
            default: Current value of the property 
            minimum: Minimum value of the range of values that can be stored in the property object 
            maximum: Maximum value of the range of values that can be stored in the property object 

        '''
        if minimum > maximum:
            raise InvalidRangeError()
        elif default not in range(minimum, maximum+1):
            raise DefaultOutofRangeError(default)
        else:
            self._Value_P__name = name
            self.__default = default
            self.__minimum = minimum
            self.__maximum = maximum

    def give_val(self):
        '''
        Funciton to return the current value of the property
        '''
        res = self.__default
        return res
        
    def __repr__(self):
        return f"Int_P(name = {self._Value_P__name}, default = {self.__default}, minimum = {self.__minimum}, maximum = {self.__maximum})"
    
    def __add__(self, other):
        return self.__default + other._Flt_P__default
    
    def __sub__(self, other):
        return self.__default - other._Flt_P__default
    
    def __mul__(self, other):
        return self.__default * other._Flt_P__default

    def __truediv__(self, other):
        return self.__default / other._Flt_P__default
    
    def __gt__(self, other):
        return self.__default > other._Flt_P__default
    
    def __lt__(self, other):
        return self.__default < other._Flt_P__default
    
    def __le__(self, other):
        return self.__default <= other._Flt_P__default
    
    def __ge__(self, other):
        return self.__default >= other._Flt_P__default
    
    def __eq__(self, other):
        return self.__default == other._Flt_P__default
    
    def __ne__(self, other):
        return self.__default != other._Flt_P__default

    def write_out(self, file):
        '''
        Function to write the object to a file
        '''
        file.write(f"{self.__default}")

class Flt_P(Value_P):
    '''
    Property class to store float values

    Contructor Parameters:
        name: Name of the property of which float value is to be stored
        default: Current value of the property (Optional, default = 1.0)
        minimum: Minimum value of the range of values that can be stored in the property object (Optional, default = 0.0)
        maximum: Maximum value of the range of values that can be stored in the property object (Optional, default = 100.0)

    '''

    __slots__ = ('_Value_P__name', '_Flt_P__default',
                 '_Flt_P__minimum', '_Flt_P__maximum')

    def __init__(self, name=str, default: float = 1.0, minimum: float = 0.0, maximum: float = 100.0):
        super(Flt_P, self).__init__()
        self.set_properties(name, default, minimum, maximum)

    def instance_restricted(self):
        pass

    def set_properties(self, name: str, default: float, minimum: float, maximum: float):
        '''
        Function to edit the values stored in the object

        Paramters:
            name: Name of the property 
            default: Current value of the property 
            minimum: Minimum value of the range of values that can be stored in the property object 
            maximum: Maximum value of the range of values that can be stored in the property object 

        '''
        if minimum > maximum:
            raise InvalidRangeError()
        elif default > maximum or default < minimum:
            raise DefaultOutofRangeError(default)
        else:
            self._Value_P__name = name
            self.__default = default
            self.__minimum = minimum
            self.__maximum = maximum
    
    def give_val(self):
        '''
        Funciton to return the current value of the property
        '''
        res = self.__default
        return res

    def __repr__(self):
        return f"Flt_P(name = {self._Value_P__name}, default = {self.__default}, minimum = {self.__minimum}, maximum = {self.__maximum})"
    
    def __add__(self, other):
        return self.__default + other._Flt_P__default
    
    def __sub__(self, other):
        return self.__default - other._Flt_P__default
    
    def __mul__(self, other):
        return self.__default * other._Flt_P__default

    def __truediv__(self, other):
        return self.__default / other._Flt_P__default
    
    def __gt__(self, other):
        return self.__default > other._Flt_P__default
    
    def __lt__(self, other):
        return self.__default < other._Flt_P__default
    
    def __le__(self, other):
        return self.__default <= other._Flt_P__default
    
    def __ge__(self, other):
        return self.__default >= other._Flt_P__default
    
    def __eq__(self, other):
        return self.__default == other._Flt_P__default
    
    def __ne__(self, other):
        return self.__default != other._Flt_P__default
      
    def write_out(self, file):
        '''
        Function to write the object to a file
        '''
        file.write(f"{self.__default}")

class Str_P(Value_P): # for testing purposes only, to be scrapped
    '''
    Property class to store string values

    Contructor Parameters:
        name: Name of the property of which string value is to be stored
        default: Current value of the property (Optional, default = "")

    '''
    __slots__ = ('_Value_P__name', '_Str_P__default')

    def __init__(self, name: str,  default: str = ""):
        super(Str_P, self).__init__()
        self.set_properties(name, default)

    def instance_restricted(self):
        pass

    def set_properties(self, name: str, default: str):
        '''
        Function to edit the values stored in the object

        Paramters:
            name: Name of the property 
            default: Current value of the property 
            
        '''
        self._Value_P__name = name
        self.__default = default
    
    def give_val(self):
        '''
        Funciton to return the current value of the property
        '''
        res = self.__default
        return res

    def __repr__(self):
        return f"Str_P(name = {self._Value_P__name}, default = '{self.__default}')"

class Enm_P(Value_P):
    '''
    Property class to store values that are usually a choice out of many possible choices(string data)

    Contructor Parameters:
        name: Name of the property 
        items: set of all the possible choices
        default: Current value of the property

    '''

    __slots__ = ('_Value_P__name', '_Enm_P__items', '_Enm_P__default')

    def __init__(self, name: str, items: {str}, default: str):
        super(Enm_P, self).__init__()
        self.set_properties(name, items, default)

    def instance_restricted(self):
        pass

    def add_val(self, val: str) -> None:
        '''
        Function to add an option to the existing set of options

        Parameters: 
            val: The new option that is to be added
        '''
        self.__items.add(val)

    def get_items(self) -> {str}:
        '''
        Function to get the current set of choices available for the property

        Returns: 
            items: set of current available options in the property
        '''
        return self.__items

    def remove_item(self, val: str) -> None:
        '''
        Function to remove a choice from the set of choices in the property

        Parameters:
            val: The option that is to be removed
        '''
        if val != self.__default:
            self.__items.remove(val)
        else:
            raise IsDefaultError(val)

    def set_default(self, val: str) -> None:
        '''
        Function to change the current value of the property

        Parameters: 
            val: The new value of the property
        '''
        if val in self.__items:
            self.__default = val
        else:
            raise ValueOutofRangeError(val)

    def set_properties(self, name: str, items: {str}, default: str):
        '''
        Function to edit the values stored in the object

        Paramters:
            name: Name of the property 
            items: set of all the possible choices
            default: Current value of the property 
            
        '''
        if type(items) != set:
            raise NotSetType(items)
        else:
            for item in items:
                if type(item) != str:
                    raise NotStringType(item)
                else:
                    pass

        if default not in items:
            raise DefaultOutofRangeError(default)

        self._Value_P__name = name
        self.__items = items
        self.__default = default

    def __repr__(self):
        return f"Enm_P(name = {self._Value_P__name}, items = {self.__items}, default = {self.__default})"

    def give_val(self):
        '''
        Funciton to return the current value of the property
        '''
        res = self.__default
        return res
    
    def write_out(self, file):
        '''
        Function to write the object to a file
        '''
        file.write(f"{self.__default}")