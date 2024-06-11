from pyvnt.Reference.basic import *
from pyvnt.DictionaryElement.foamDS import Foam
from anytree import Node, RenderTree, AsciiStyle, NodeMixin
from pyvnt.Reference.errorClasses import SizeError, NoPlaceholdersError, NoValueError, KeyRepeatError
import warnings

class PropertyList(ValueProperty, NodeMixin):
    '''
    A property that holds a list of values.

    Constructor Parameters:
        name: The name of the property.
        size: The size of the list.
        values: The values of the list.
        default: The default value of the list.
        isNode: If the list is a list of nodes.
    
    Class constructor can be called in the following ways:
        PropertyList(name, size, values)
        PropertyList(name, values)
        PropertyList(name, size, default)

    '''

    __slots__ = ['_ValuePorperty__name', '_PropertyList__values', '_PropertyList__isNode']

    def __init__(self, name: int, size: int = None, values: [ValueProperty] = [], default: ValueProperty = None, isNode: bool = False, parent: Foam = None):
        super(PropertyList, self).__init__()
        self._PropertyList__isNode = isNode

        if not self._PropertyList__isNode:
            self.setProperties(name, size, values, default)
        else:
            self.checkType(values = values)
            self.name = name
            self.data = []

            if not parent:
                raise NoValueError("No parent given for node")
            else:
                self.parent = parent

            self.children = values
    
    def instance_restricted(self):
        pass
    
    def checkType(self, values: [ValueProperty] = None, value: ValueProperty = None):
        '''
        Checks if all the values are of the same type.
        '''
        if value:
            if self._PropertyList__isNode:
                if not isinstance(value, Foam):
                    raise TypeError("Value should be of type Foam")
                else:
                    pass
            else:
                if not isinstance(value, ValueProperty):
                    raise TypeError("Value should be of type ValueProperty")
                else:
                    pass
        elif values:
            if self._PropertyList__isNode:
                if not all(isinstance(i, Foam) for i in values):
                    raise TypeError("All values should be of type Foam")
                else:
                    pass
            else:
                if not all(isinstance(i, ValueProperty) for i in values):
                    raise TypeError("All values should be of type ValueProperty")
                else:
                    pass
        else:
            raise NoValueError("No values given for type checking")
    
    def setProperties(self, name: int, size: int, values: [ValueProperty], default: ValueProperty = None):
        '''
        Sets the values of the list.
        '''
        self._ValueProperty__name = name

        self.checkType(values = values)
        
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
        self.checkType(value = val)

        self._PropertyList__values.append(val)
    
    def append_uniq_value(self, val: ValueProperty):
        '''
        Appends the value to the list if it is not already present.
        '''
        self.checkType(value = val)

        if val not in self._PropertyList__values:
            self._PropertyList__values.append(val)
        else:
            raise KeyRepeatError(val)
    
    def __repr__(self):
        return f"PropertyList(name : {self._ValueProperty__name}, values : {self._PropertyList__values})"
    
    def size(self):
        '''
        Returns the size of the list.
        '''
        return len(self._PropertyList__values)
    
    def giveVal(self):
        '''
        Returns the list.
        '''
        return tuple(elem.giveVal() for elem in self._PropertyList__values)
    
    def checkSimilarData(self):
        '''
        Checks if all the items inside the list are of the same type.
        '''
        return all(isinstance(i, type(self._PropertyList__values[0])) for i in self._PropertyList__values)
    
    def writeOut(self, file):
        '''
        Writes the list to a file
        '''
        # TODO: Figure out a way to know when to write multiline lists
        res = f"{self.giveVal()}".replace(",", " ")
        file.write(res)
    
    def __eq__(self, other):
        return self.giveVal() == other.giveVal()
    
    def __ne__(self, other):
        return not self.__eq__(other)
            


