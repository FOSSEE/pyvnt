from anytree import Node, RenderTree, AsciiStyle, NodeMixin
from anytree.search import find_by_attr
from typing import Any, Type
from pyvnt.Container.key import Key_C
from pyvnt.Reference.error_classes import *
from pyvnt.utils.make_indent import make_indent

'''
Criteria for classes:
1. any attributes should be added to the class only through the constructor, and not through the object
2. the attributes should be accessible only through the object
3. the attributed should not be accesible through . operator -- done by name mangling(__var)
'''

'''
Why we implement _ordered_items : In a node we can add key-value and dictionaries and the order can be anything as
                                  dictionaries then data. So only node is one where we are handling data and dictionaries 
                                  both .Whereas in other we can just chnage the sequence of data or child(in list node) as 
                                  way we add them .
'''

class Node_C(NodeMixin):
    """
    Class to define nodes of the tree

    Contructor Parameters:
        name: Name of the Node object
        parent: Parent Node of the current Node (Optional)
        children: List of the children node(s) of the current Node (Optional)
    """

    # __slots__ = ('name', 'parent', 'children', 'data')

    def __init__(self, name: str, parent = None, children: [] = None, *args: Key_C):

        super(Node_C, self).__init__()
        # self._privateDict = kwargs
        self.name = name

        self.data = list(args)
        
        if parent == None or parent.data == []:
            self.parent = parent
        else:
            raise LeafNodeError(self)

        if children:
            self.children = children

        # for Writing in order 
        self._ordered_items = []

        for item in self.data:
            if item not in self._ordered_items: # Avoid duplicates if init is complex
                self._ordered_items.append(item)
        for item in self.children:
            if item not in self._ordered_items:
                self._ordered_items.append(item)
    
    
    def __getattr__(self, key):
        """
        Prevents access to attributes which are not in _privateDict
        """
        accepted_keys = ['name', 'parent', 'children']
        if key in accepted_keys:
            return super().__getattr__(key)
        else:
            raise AttributeError(key) 


    # def __setattr__(self, key, value):
    #     super().__setattr__(key, value)
    

    # def dispTree(self):
    #     '''
    #     Function to output the entire tree in the terminal starting from the current node object
    #     '''
    #     for pre, fill, node in RenderTree(self):
    #         treestr = u"%s%s" % (pre, node.name)
    #         s = ""
            
            

            
    #         print(treestr.ljust(8), s)
    


    # helper Function for seting _ordered_items 
    def set_order(self, names_list):
        """Reorders _ordered_items based on a list of names."""
        new_ordered_items = []
        current_item_map = {}
        all_current_items = self.data + list(self.children)
        for item in all_current_items:
            name = getattr(item, 'name', None)
            if name is not None:
                 current_item_map[name] = item

        processed_items = set()
        for name in names_list:
            item_ref = current_item_map.get(name)
            if item_ref is not None:
                new_ordered_items.append(item_ref)
                processed_items.add(name)
            else:
                print(f"Warning: Name '{name}' in set_order not found in node '{self.name}'.")

        for item_ref in self._ordered_items:
             if getattr(item_ref, 'name', None) not in processed_items:
                 new_ordered_items.append(item_ref)

        self._ordered_items = new_ordered_items

    def get_ordered_items(self):
        """Returns an iterator over the items (references) in the desired order."""
        return list(self._ordered_items)





    def add_child(self, node):
        '''
        Function to add a child node to the current node

        Parameter:
            node: Node object to be added as a child
        '''
        self.children += (node, )
        self._ordered_items.append(node)
        
    
    def get_data(self):
        '''
        Function to get the attributes of the current node

        Parameter:
            None
        '''
        return self.data
    
    def set_Parent(self, node):
        '''
        Function to set the parent node to the current node

        Parameter:
            node: Node object to be added as a child
        '''
        self.parent = node
    
    def __repr__(self):
        res_str = f"Node_C("
        for key, val in self.__dict__.items():
            res_str = res_str + f"{key} : {val}, "
        res_str = res_str + ")"
        return res_str
    
    def get_child(self, val: str):
        '''
        Function to find a child node with the given attribute

        Parameter:
            val: Name of the Node that is bein searched for
        '''
        return find_by_attr(self, val, maxlevel = 2)

    def add_data(self, data: Key_C, pos: int = None):
        '''
        Function to add Key_C attributes to the existing Node
        '''

        if pos != None:
            self.data.insert(pos, data)
        else:
            self.data.append(data)
            
        self._ordered_items.append(data)
    
    def remove_data(self, data: Key_C):
        '''
        Function to remove a Key_C attribute from the node
        '''

        try: 
            self.data.remove(data)
        except:
            raise AttributeError(f"{data.name} does not exist in this node")
    
    def reorder_data(self, data: Key_C, pos: int):
        '''
        Function to reorder the data in the node
        '''

        try:
            self.data.remove(data)
            self.data.insert(data, pos)
        except:
            raise AttributeError(f"{data.name} does not exist in this node")
    
    def write_out(self, file, indent = 0):
        '''
        Function to write the current node to the file
        '''

        '''
        if self.parent == None:
            # TODO: Add the header to the file
            pass
        else:
            file.write(f"{self.name}\n")
            file.write("{\n")
            for d in self.data:
                file.write("\t")
                d.write_out(file)
            file.write("}\n")
        '''

        make_indent(file, indent)
        file.write(f"{self.name}\n")

        make_indent(file, indent)
        file.write("{\n")

        for d in self.data:
            d.write_out(file, indent+1)

        # make_indent(file, indent)

        for child in self.children:
            child.write_out(file, indent+1)
            file.write("\n")

        make_indent(file, indent)
        file.write("}\n")