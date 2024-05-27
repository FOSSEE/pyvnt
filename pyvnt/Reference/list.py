from pyvnt.Reference.basic import *
from pyvnt.Reference.errorClasses import SizeError, NoPlaceholdersError, NoValueError, KeyRepeatError
import warnings

class PropertyList(ValueProperty):
    '''
    A property that holds a list of values.

    Constructor Parameters:
        name: The name of the property.
        size: The size of the list.
        values: The values of the list.
        default: The default value of the list.
    
    Class constructor can be called in the following ways:
        PropertyList(name, size, values)
        PropertyList(name, values)
        PropertyList(name, size, default)

    '''

    __slots__ = ['_ValuePorperty__name', '_PropertyList__values']

    def __init__(self, name: int, size: int = None, values: [ValueProperty] = [], default: ValueProperty = None):
        super().__init__(name, default)
        self.setProperties(name, size, values, default)
        
    
    def setProperties(self, name: int, size: int, values: [ValueProperty], default: ValueProperty = None):
        '''
        Sets the values of the list.
        '''
        self._ValueProperty__name = name

        if size and values != []:
            if default:
                warnings.warn("Default value will be ignored")
            else:
                pass

            if size != len(values):
                raise SizeError(size)
            else:
                self._PropertyList__values = values

        elif not size and values != []:
            if default:
                warnings.warn("Default value will be ignored")
            else:
                pass

            self._PropertyList__values = values

        elif size and values == []:
            if default:
                warnings.warn("Default value will be ignored")
            else:
                pass

            if not default:
                raise NoPlaceholdersError("No default value")
            else:    
                self._PropertyList__values = [default] * size

        else:
            raise NoValueError("No values given for list construction")
    
    def getItem(self, index: int):
        '''
        Returns the value at the given index.
        '''
        return self._PropertyList__values[index]
    
    def append_value(self, val: ValueProperty):
        '''
        Appends the value to the list.
        '''
        self._PropertyList__values.append(val)
    
    def append_uniq_value(self, val: ValueProperty):
        '''
        Appends the value to the list if it is not already present.
        '''
        if val not in self._PropertyList__values:
            self._PropertyList__values.append(val)
        else:
            raise KeyRepeatError(val)
    
    def __repr__(self):
        return f"{self._ValueProperty__name}: {self._PropertyList__values}"
    
    def size(self):
        '''
        Returns the size of the list.
        '''
        return len(self._PropertyList__values)
    
    def giveVal(self):
        '''
        Returns the list.
        '''
        return self._PropertyList__values
    
    def __eq__(self, other):
        return self._PropertyList__values == other.giveVal()
            


