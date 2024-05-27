from dataclasses import dataclass, replace, field
from typing import Any
import enum
from abc import ABC, abstractmethod
from pyvnt.Reference.errorClasses import *

# Property Classes

class ValueProperty(ABC):
    '''
    Abstract parent class for all the property classes

    Do not create oobject of this class
    '''
    __slots__ = ('_ValueProperty__name')

    def __init__(self):
        self.__name = ""

    @abstractmethod
    def instance_restricted(self):
        pass


class PropertyInt(ValueProperty):
    '''
    Property class to store integer values

    Contructor Parameters:
        name: Name of the property of which integer value is to be stored
        default: Current value of the property (Optional, default = 1)
        minimum: Minimum value of the range of values that can be stored in the property object (Optional, default = 0)
        maximum: Maximum value of the range of values that can be stored in the property object (Optional, default = 100)

    '''
    __slots__ = ('_ValueProperty__name', '_PropertyInt__default',
                 '_PropertyInt__minimum', '_PropertyInt__maximum')

    def __init__(self, name: str, default: int = 1, minimum: int = 0, maximum: int = 100):
        super(PropertyInt, self).__init__()
        self.setProperties(name, default, minimum, maximum)

    def instance_restricted(self):
        pass

    def setProperties(self, name: str, default: int, minimum: int, maximum: int):
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
            self._ValueProperty__name = name
            self.__default = default
            self.__minimum = minimum
            self.__maximum = maximum

    def giveVal(self):
        '''
        Funciton to return the current value of the property
        '''
        res = self.__default
        return res
        
    def __repr__(self):
        return f"PropertyInt(name = {self._ValueProperty__name}, default = {self.__default}, minimum = {self.__minimum}, maximum = {self.__maximum})"
    
    def __add__(self, other):
        return self.__default + other._PropertyFloat__default
    
    def __sub__(self, other):
        return self.__default - other._PropertyFloat__default
    
    def __mul__(self, other):
        return self.__default * other._PropertyFloat__default

    def __truediv__(self, other):
        return self.__default / other._PropertyFloat__default
    
    def __gt__(self, other):
        return self.__default > other._PropertyFloat__default
    
    def __lt__(self, other):
        return self.__default < other._PropertyFloat__default
    
    def __le__(self, other):
        return self.__default <= other._PropertyFloat__default
    
    def __ge__(self, other):
        return self.__default >= other._PropertyFloat__default
    
    def __eq__(self, other):
        return self.__default == other._PropertyFloat__default
    
    def __ne__(self, other):
        return self.__default != other._PropertyFloat__default

    def writeOut(self, file):
        '''
        Function to write the object to a file
        '''
        file.write(f"{self.__default}")



class PropertyFloat(ValueProperty):
    '''
    Property class to store float values

    Contructor Parameters:
        name: Name of the property of which float value is to be stored
        default: Current value of the property (Optional, default = 1.0)
        minimum: Minimum value of the range of values that can be stored in the property object (Optional, default = 0.0)
        maximum: Maximum value of the range of values that can be stored in the property object (Optional, default = 100.0)

    '''

    __slots__ = ('_ValueProperty__name', '_PropertyFloat__default',
                 '_PropertyFloat__minimum', '_PropertyFloat__maximum')

    def __init__(self, name=str, default: float = 1.0, minimum: float = 0.0, maximum: float = 100.0):
        super(PropertyFloat, self).__init__()
        self.setProperties(name, default, minimum, maximum)

    def instance_restricted(self):
        pass

    def setProperties(self, name: str, default: float, minimum: float, maximum: float):
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
            self._ValueProperty__name = name
            self.__default = default
            self.__minimum = minimum
            self.__maximum = maximum
    
    def giveVal(self):
        '''
        Funciton to return the current value of the property
        '''
        res = self.__default
        return res

    def __repr__(self):
        return f"PropertyFloat(name = {self._ValueProperty__name}, default = {self.__default}, minimum = {self.__minimum}, maximum = {self.__maximum})"
    
    def __add__(self, other):
        return self.__default + other._PropertyFloat__default
    
    def __sub__(self, other):
        return self.__default - other._PropertyFloat__default
    
    def __mul__(self, other):
        return self.__default * other._PropertyFloat__default

    def __truediv__(self, other):
        return self.__default / other._PropertyFloat__default
    
    def __gt__(self, other):
        return self.__default > other._PropertyFloat__default
    
    def __lt__(self, other):
        return self.__default < other._PropertyFloat__default
    
    def __le__(self, other):
        return self.__default <= other._PropertyFloat__default
    
    def __ge__(self, other):
        return self.__default >= other._PropertyFloat__default
    
    def __eq__(self, other):
        return self.__default == other._PropertyFloat__default
    
    def __ne__(self, other):
        return self.__default != other._PropertyFloat__default
      
    def writeOut(self, file):
        '''
        Function to write the object to a file
        '''
        file.write(f"{self.__default}")



class PropertyString(ValueProperty): # for testing purposes only, to be scrapped
    '''
    Property class to store string values

    Contructor Parameters:
        name: Name of the property of which string value is to be stored
        default: Current value of the property (Optional, default = "")

    '''
    __slots__ = ('_ValueProperty__name', '_PropertyString__default')

    def __init__(self, name: str,  default: str = ""):
        super(PropertyString, self).__init__()
        self.setProperties(name, default)

    def instance_restricted(self):
        pass

    def setProperties(self, name: str, default: str):
        '''
        Function to edit the values stored in the object

        Paramters:
            name: Name of the property 
            default: Current value of the property 
            
        '''
        self._ValueProperty__name = name
        self.__default = default
    
    def giveVal(self):
        '''
        Funciton to return the current value of the property
        '''
        res = self.__default
        return res

    def __repr__(self):
        return f"PropertyString(name = {self._ValueProperty__name}, default = '{self.__default}')"


class EnumProp(ValueProperty):
    '''
    Property class to store values that are usually a choice out of many possible choices(string data)

    Contructor Parameters:
        name: Name of the property 
        items: set of all the possible choices
        default: Current value of the property

    '''

    __slots__ = ('_ValueProperty__name', '_EnumProp__items', '_EnumProp__default')

    def __init__(self, name: str, items: {str}, default: str):
        super(EnumProp, self).__init__()
        self.setProperties(name, items, default)

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

    def setProperties(self, name: str, items: {str}, default: str):
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

        self._ValueProperty__name = name
        self.__items = items
        self.__default = default

    def __repr__(self):
        return f"EnumProp(name = {self._ValueProperty__name}, items = {self.__items}, default = {self.__default})"

    def giveVal(self):
        '''
        Funciton to return the current value of the property
        '''
        res = self.__default
        return res
    
    def writeOut(self, file):
        '''
        Function to write the object to a file
        '''
        file.write(f"{self.__default}")