from pyvnt.Reference.basic import *
from pyvnt.DictionaryElement.foamDS import Foam
from anytree import Node, RenderTree, AsciiStyle, NodeMixin
from pyvnt.Reference.errorClasses import SizeError, NoPlaceholdersError, NoValueError, KeyRepeatError
import warnings

class PropertyList(ValueProperty, NodeMixin):
    '''
    A property that holds a list of elements.

    An element of a list can be defined as the smallest group of values that fulfills the syntax of the list in OpenFOAM

    Example:
        blocks
        (
            hex (0 1 2 3 4 5 6 7) (100 150 1) simpleGrading (1 1 1) 
            hex (8 9 10 11 12 13 14) (100 150 1) simpleGrading (1 1 1) 
        );

        Here, in the list blocks, the group of values "hex (0 1 2 3 4 5 6 7) (100 150 1) simpleGrading (1 1 1) " can be treated as an element, 
        as it is the smallest group of values that completes the syntax of the list blocks so that the list blocks works without any errors. 

        Internally an element is a list of such values. 

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

    __slots__ = ['_ValueProperty__name', '_PropertyList__values', '_PropertyList__isNode']

    def __init__(self, name: int, size: int = None, values: [ValueProperty] = [], elems: [[ValueProperty]] or [Foam] = [], default: ValueProperty = None, isNode: bool = False, parent: Foam = None):
        super(PropertyList, self).__init__()
        self.__isNode = isNode

        if not self.__isNode:
            self.setProperties(name, size, elems, default) # TODO: Change the method such that the class takes inputs in elements and the class stores list of elements when not acting as a node.
        else:
            self.checkType(values = values)
            self.name = name
            self.__values = []
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
            if self.__isNode:
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
            if self.__isNode:
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
    
    def setProperties(self, name: int, size: int, values: [[ValueProperty]], default: ValueProperty = None):
        '''
        Sets the values of the list is it is not a node.
        '''
        self._ValueProperty__name = name

        # self.checkType(values = values)
        
        if size and values != []:
            '''
            If both size and list of values are given
            '''
            if default:
                warnings.warn("Default value will be ignored")
            else:
                pass

            if size != len(values):
                raise SizeError(size)
            else:
                self.__values = values

        elif not size and values != []:
            '''
            Only list of values is given
            '''

            if default:
                warnings.warn("Default value will be ignored")
            else:
                pass

            self.__values = values

        elif size and values == []:
            '''
            Only size is given but not list of values
            '''

            if default:
                warnings.warn("Default value will be ignored")
            else:
                pass

            if not default:
                raise NoPlaceholdersError("No default value")
            else:    
                self.__values = [[default]] * size

        else:
            '''
            None of the above conditions are met
            '''
            raise NoValueError("No values given for list construction")
    
    def getItem(self, elem: int, index: int = None):
        '''
        Returns the value at the given index.

        Parameters: 
            elem: The index of the element.
            index: The index of the value in the element.(Optional)
        '''

        if index:
            return self.__values[elem][index]
        else:
            return self.__values[elem]
    
    def append_value(self, elem: int, val: ValueProperty):
        '''
        Appends a value to the list.
        
        Parameters:
            elem: The index of the element in which the value is to be appended.
            val: The value to be appended.
        '''
        self.checkType(value = val)

        self.__values.append(val)
    
    def append_uniq_value(self, elem: int, val: ValueProperty):
        '''
        Appends a value to the element of the list if it is not already present.
        
        Parameters:
            elem: The index of the element in which the value is to be appended.
            val: The value to be appended.
        
        '''

        self.checkType(value = val)

        if val not in self.__values[elem]:
            self.__values[elem].append(val)
        else:
            raise KeyRepeatError(val)
    
    def append_elem(self, elem: [ValueProperty]):
        '''
        Appends an element to the list.

        Parameters:
            elem: The element to be appended.
        '''
        self.checkType(values = elem)

        self.__values.append(elem)
    
    def append_uniq_elem(self, elem: [ValueProperty]):
        '''
        Appends an element to the list if it is not already present.

        Parameters:
            elem: The element to be appended.
        '''
        self.checkType(values = elem)

        if elem not in self.__values:
            self.__values.append(elem)
        else:
            raise KeyRepeatError(elem)
    
    def __repr__(self):
        if not self.__isNode:
            return f"PropertyList(name : {self._ValueProperty__name}, values : {self.__values})"
        else:
            return f"PropertyList(name : {self.name}, values : {self.children})"
        
    def size(self):
        '''
        Returns the size of the list.
        '''
        s = 0
        for elem in self.__values:
            s = s + len(elem)
        return s
    
    def giveVal(self):
        '''
        Returns the list.
        '''
        res = tuple()

        for elem in self.__values:
            for val in elem:
                res = res + (val.giveVal(),)

        return res
        
    def checkSimilarData(self):
        '''
        Checks if all the items inside the list are of the same type.
        '''
        return all(isinstance(i, type(self.__values[0][0])) for i in elem for elem in self.__values)
    
    def writeOut(self, file, indent = 0):
        '''
        Writes the list to a file
        '''
        # TODO: Figure out a way to know when to write multiline lists
        # The format of printing in each list differs and is dependent of the keyword of the list. 
        # The basic structure of a list is to print elements vertically.
        # The syntax of each element depends of the keyword of the list.
        # If the syntax of every keyword is known, a method can be written to generate the files according to the syntax. 
        
        res = ""
        for elem in self.__values:
            for val in elem:
                res = res + f"{val.giveVal()} "
            res = res + "\n"
        file.write(res)
    
    def __eq__(self, other):
        return self.giveVal() == other.giveVal()
    
    def __ne__(self, other):
        return not self.__eq__(other)
            


