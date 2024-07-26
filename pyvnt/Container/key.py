from abc import ABC, abstractmethod
from collections import OrderedDict
from anytree import NodeMixin
from pyvnt.Reference.basic import *
from pyvnt.utils.make_indent import make_indent


'''
Criteria for classes:
1. any attributes should be added to the class only through the constructor or edit function, and not through the object
2. the attributes should be editable only through the object
3. the attributed should not be accesible through . operator -- done by name mangling(__var)
'''

class Key_Parent(ABC):
    '''
    Abstract class to make sure that attributes cannot be inserted into the child class directly
    Do not make objects of this class
    '''

    def __init__(self, name: str = "Parent"):
        self.__dict__['name'] = name

    @abstractmethod
    def instance_restricted(self):
        pass

# TODO: prevent access of attributes from outside the class  -- done
# Currently the attributes can be edited from outside the class, which should not be possible
# TODO: Modify such that constructor takes in no attribute by default. After making the constructor, use a method to insert attributes -- done
class Key_C(Key_Parent):

    def instance_restricted(self):
        pass
        
    # def old__init__(self, name=None, **kwargs: Value_P): # old init method, 
    #     super(Key_C, self).__init__(name)
    #     self.__dict__.update(kwargs)
    #     # self.__toggle_freeze()

    def __init__(self, name: str = None, *args: Value_P):
        super(Key_C, self).__init__(name)

        tmp = {}
        for e in args:
            tmp[e._Value_P__name] = e
        
        self._privateDict = OrderedDict(tmp)


    def __getattr__(self, key):
        """
        Prevents access to attributes which are not in _privateDict
        """
        if key in self._privateDict.keys():
            return self._privateDict[key]
        else:
            raise AttributeError(key) 

    def __setattr__(self, key, value):
        """
        Prevents Creation of new attributes but allows editing existing ones -- commented code

        Prevents setting of attributes except _privateDict
        """
        
        if( key == '_privateDict'):
            super().__setattr__(key,value)
        else :
            raise AttributeError(key)

    def append_val(self, key: "str", val: Value_P):
        self._privateDict[key] = val

    '''
    # TODO: Take input of the object to be replaced or the obejct name instead of the variable name as the string. -- done in replace_val2
    This piece of code is here to remind devs about what not to do

    def replace_val(self, oldKey: str, newKey: str, newVal: Value_P):

        if oldKey == newKey:
            self.__dict__[newKey] = newVal
        else:
            if newKey != oldKey and newKey in self.__dict__.keys():
                raise KeyRepeatError(newKey)
            else:
                replacement = {oldKey: newKey}
                for k, v in list(self.__dict__.items()):
                    self.__dict__[replacement.get(k, k)] = self.__dict__.pop(k)
                self.__dict__[newKey] = newVal
    

    def replace_val2(self, old: Value_P | str, new: Value_P):
        if type(old) == str:
            oldKey = old
        else:
            oldKey = old._Value_P__name
        
        newKey = new._Value_P__name

        if oldKey == newKey:
            self.__dict__[newKey] = new
        else:
            if newKey != oldKey and newKey in self.__dict__.keys():
                raise KeyRepeatError(newKey)
            else:
                replacement = {oldKey: newKey}
                for k, v in list(self.__dict__.items()):
                    self.__dict__[replacement.get(k, k)] = self.__dict__.pop(k)
                self.__dict__[newKey] = new
    '''

    def replace_val(self, old: Value_P or str, new: Value_P): # uses orderedDict instead of regular Dictionary
        '''
        Function to insert and edit values in the class object once it is created

        Parameters:
            old: object or name of object to be replaced
            new: object of the new Data that is to be added
        
        Returns:
            None

        '''
        if type(old) == str:
            oldKey = old
        else:
            oldKey = old._Value_P__name
        
        newKey = new._Value_P__name

        if oldKey == newKey:
            # self.__dict__[newKey] = new
            self._privateDict[newKey] = new
        else:
            if newKey != oldKey and newKey in self._privateDict.keys():
                raise KeyRepeatError(newKey)
            else:
                self._privateDict = OrderedDict([(newKey, new) if k == oldKey else (k, v) for k, v in self._privateDict.items()])

    def delete_val(self, key: str):
        '''
        Function to delete a given key from the object

        Parameters: 
            key: name of the key to be deleted
        '''
        del self._privateDict[key]

    def __repr__(self):
        last_elem = list(self._privateDict.keys())[-1]
        res_str = f"Key_C("
        for key, val in self._privateDict.items():
            res_str = res_str + f"{key} : {val}"
            if key != last_elem:
                res_str = res_str + ", "
        res_str = res_str + ")"

        return res_str
    
    def give_val(self):
        '''
        Function to get all the keys and values stored in the object in a text format
        '''
        last_elem = list(self._privateDict.keys())[-1]

        res = f"{self.name} : "
        for key, val in self._privateDict.items():
            if key == 'name':
                continue
            else:
                res = res + f"{val.give_val()}"
                if key != last_elem:
                    res = res + ", "
        
        return res

    def get_items(self):
        '''
        Function to get all the items stored in the object
        '''
        return self._privateDict.items()
    
    def get_keys(self):
        '''
        Function to get all the keys stored in the object
        '''
        return self._privateDict.keys()
    
    def write_out(self, file, indent = 0):
        '''
        Function to write the object to a file
        '''
        col_width = 16
        last_elem = list(self._privateDict.keys())[-1]

        make_indent(file, indent)

        if len(self._privateDict.values()) == 1 :
            try:
                file.write(f"{self.name}\n")
                for key, val in self._privateDict.items():
                    val.write_out(file, indent, True)
            except e:
                file.write(f"{self.name.ljust(col_width)}")
                for key, val in self._privateDict.items():
                    val.write_out(file)
                    if key != last_elem:
                        file.write(" ")
        else:
            file.write(f"{self.name.ljust(col_width)}")
            for key, val in self._privateDict.items():
                val.write_out(file)
                if key != last_elem:
                    file.write(" ")

        file.write(";\n")