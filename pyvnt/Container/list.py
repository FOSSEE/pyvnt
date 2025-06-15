from pyvnt.Reference.basic import *
from pyvnt.Container.node import Node_C
from anytree import Node, RenderTree, AsciiStyle, NodeMixin
from pyvnt.Reference.error_classes import SizeError, NoPlaceholdersError, NoValueError, KeyRepeatError
from pyvnt.utils.make_indent import make_indent
import warnings
from pyvnt.Container.orderChildMixin import OrderedChildMixin

class List_CP(OrderedChildMixin,Value_P, NodeMixin):
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
        List_CP(name, size, values)
        List_CP(name, values)
        List_CP(name, size, default)

    '''

    __slots__ = ['_Value_P__name', '_List_CP__values', '_List_CP__isNode']

    def __init__(self, 
             name: int, 
             size: int = None, 
             values: [Node_C] = None,
             elems: [[Value_P]] = None,
             default: Value_P = None, 
             isNode: bool = False, 
             parent: Node_C = None):
    
        super(List_CP, self).__init__()
        # Value_P.__init__(self)
        # NodeMixin.__init__(self)
        self.__isNode = isNode

        if not self.__isNode:
            self.__values = [[]]
            if elems is None:
                elems = [[]]

            self.set_properties(name, size, elems, default)
        else:
            if values is not None:
                self.check_type(values=values)
            
            self.name = name
            self.__values = []
            self.data = []
            
            if parent:
                self.parent = parent

            self.children = values if values is not None else []
    
    def instance_restricted(self):
        pass
    
    def total_len(self, ar: [[Value_P]]= [[]]) -> int:
        res = 0
        for elem in ar:
            res += len(elem)
        return res
    
    def check_type(self, elems: [[Value_P]] = None, values: [Value_P] = None, value: Value_P = None):
        '''
        Checks if all the values are of the same type.
        '''
        if value:
            if self.__isNode:
                if not isinstance(value, Node_C):
                    raise TypeError("Value should be of type Node_C")
                else:
                    pass
            else:
                if not isinstance(value, Value_P):
                    raise TypeError("Value should be of type Value_P")
                else:
                    pass
        elif elems:
            if self.__isNode:
                for v in elems:
                    if not all(isinstance(i, Node_C) for i in v):
                        raise TypeError("All values should be of type Node_C")
                    else:
                        pass
            else:
                for v in elems:
                    if not all(isinstance(i, Value_P) for i in v):
                        raise TypeError("All values should be of type Value_P")
                    else:
                        pass
        elif values:
            if self.__isNode:
                if not all(isinstance(i, Node_C) for i in values):
                    raise TypeError("All values should be of type Node_C")
                else:
                    pass
            else:
                if not all(isinstance(i, Value_P) for i in values):
                    raise TypeError("All values should be of type Value_P")
                else:
                    pass
        else:
            raise NoValueError("No values given for type checking")
    
    def set_properties(self, name: int, size: int, values: [[Value_P]], default: Value_P = None):
        '''
        Sets the values of the list is it is not a node.

        values: it is the list of elements that are stored in the List class
        
        '''
        self._Value_P__name = name

        if values != [[]]:
            self.check_type(elems = values)
        
        if size and values != []:
            '''
            If both size and list of values are given
            '''
            if default:
                warnings.warn("Default value will be ignored")
            else:
                pass

            if size != self.total_len(values):
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
    
    def get_item(self, elem: int, index: int = None):
        '''
        Returns the value at the given index.

        Parameters: 
            elem: The index of the element.
            index: The index of the value in the element.(Optional)
        '''

        if index != None:
            return self.__values[elem][index]
        else:
            return self.__values[elem]
    
    def append_value(self, elem: int, val: Value_P):
        '''
        Appends a value to the list.
        
        Parameters:
            elem: The index of the element in which the value is to be appended.
            val: The value to be appended.
        '''
        self.check_type(value = val)

        self.__values[elem].append(val)
    
    def append_uniq_value(self, elem: int, val: Value_P):
        '''
        Appends a value to the element of the list if it is not already present.
        
        Parameters:
            elem: The index of the element in which the value is to be appended.
            val: The value to be appended.
        
        '''

        self.check_type(value = val)

        if val not in self.__values[elem]:
            self.__values[elem].append(val)
        else:
            raise KeyRepeatError(val)
    
    def append_elem(self, elem: [Value_P]):
        '''
        Appends an element to the list.

        Parameters:
            elem: The element to be appended.
        '''
        self.check_type(values = elem)
        if self.__values == [[]]:
            self.__values = [elem]
        else:
            self.__values.append(elem)
    
    def append_uniq_elem(self, elem: [Value_P]):
        '''
        Appends an element to the list if it is not already present.

        Parameters:
            elem: The element to be appended.
        '''
        self.check_type(values = elem)

        if self.__values == [[]]:
            self.__values = [elem]
            return


        if elem not in self.__values:
            self.__values.append(elem)
        else:
            raise KeyRepeatError(elem)
    

    def append_child(self, value:Node_C):
        '''
        Appends an child to the List Node.

        Parameters:
            value: The Node_C object to be appended as a child.
        '''
        # print("Appending child ::  "+str(value.name))
        self.children +=(value,)
        # print(self.children)

    def format_nested(self,obj, visited=set()):
        """Helper function to safely format nested structures without infinite recursion."""
        if id(obj) in visited:
            return "[...]"

        visited.add(id(obj))

        if isinstance(obj, tuple):  # Handle tuples
            return tuple(self.format_nested(item, visited) for item in obj)
        elif isinstance(obj, list):  # Handle lists
            return [self.format_nested(item, visited) for item in obj]
        elif hasattr(obj, "__repr__"):  
            return obj.__repr__()  
        else:
            return obj

    def __repr__(self):
        if not self.__isNode:
            tval = []
            for elem in self.__values:
                tval.append([val.give_val() for val in elem])
            return f"List_CP(name : {self._Value_P__name}, values : {tval})"
        else:
            formated_Children=self.format_nested(self.children)
            return f"List_CP(name : {self.name}, values : {formated_Children})"
        
    def size(self):
        '''
        Returns the size of the list.
        '''
        s = 0
        for elem in self.__values:
            s = s + len(elem)
        return s
    
    def is_a_node(self):
        '''
        Returns if the list is a list of nodes.
        '''
        return self.__isNode
    
    def give_val(self):
        '''
        Returns the list.
        '''
        res = tuple()

        for elem in self.__values:
            for val in elem:
                res = res + (val.give_val(),)
        return res
    
    def get_elems(self):
        '''
        Returns the elements of the list.
        '''
        return self.__values
        
    def check_similar_data(self):
        '''
        Checks if all the items inside the list are of the same type.
        '''
        return all(isinstance(i, type(self.__values[0][0])) for i in elem for elem in self.__values)
    
    def write_out(self, file, indent: int = 0, vert: bool = False):
        '''
        Writes the list to a file
        '''
        # TODO: Figure out a way to know when to write multiline lists
        # The format of printing in each list differs and is dependent of the keyword of the list. 
        # The basic structure of a list is to print elements vertically.
        # The syntax of each element depends of the keyword of the list.
        # If the syntax of every keyword is known, a method can be written to generate the files according to the syntax. 

        if self.__isNode:
            make_indent(file, indent)
            file.write(f"{self.name}\n")

            make_indent(file, indent)
            file.write("(\n")

            for child in self.children:
                child.write_out(file, indent+1)
                file.write("\n")

            make_indent(file, indent)
            file.write(")\n")
        elif vert:
            make_indent(file, indent)
            file.write("(\n")
            for elem in self.__values:
                make_indent(file, indent+1)
                for val in elem:
                    val.write_out(file)
                    file.write(" ")
                file.write("\n")
            make_indent(file, indent)
            file.write(")")
            
        else:
            
            file.write('(')
            for elem in self.__values:
                for val in elem:
                    val.write_out(file)
                    file.write(" ")
            # res += ")"
            file.write(')')
    
    def __eq__(self, other):
        return self.give_val() == other.give_val()
    
    def __ne__(self, other):
        return not self.__eq__(other)