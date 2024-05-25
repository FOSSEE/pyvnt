from anytree import Node, RenderTree, AsciiStyle, NodeMixin
from anytree.search import find_by_attr
from typing import Any, Type
from pyvnt.DictionaryElement.keyData import KeyData
from pyvnt.Reference.errorClasses import *
from pyvnt.utils.makeIndent import makeIndent

'''
Criteria for classes:
1. any attributes should be added to the class only through the constructor, and not through the object
2. the attributes should be accessible only through the object
3. the attributed should not be accesible through . operator -- done by name mangling(__var)
'''

class Foam(NodeMixin):
    """
    Class to define nodes of the tree

    Contructor Parameters:
        name: Name of the Node object
        parent: Parent Node of the current Node (Optional)
        children: List of the children node(s) of the current Node (Optional)
    """

    # __slots__ = ('name', 'parent', 'children', 'data')

    def __init__(self, name: str, parent = None, children: [] = None, *args: KeyData):

        super(Foam, self).__init__()
        # self._privateDict = kwargs
        self.name = name

        self.data = list(args)
        
        if parent == None or parent.data == []:
            self.parent = parent
        else:
            raise LeafNodeError(self)

        if children:
            self.children = children
    
    
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
    

    def addChild(self, node):
        '''
        Function to add a child node to the current node

        Parameter:
            node: Node object to be added as a child
        '''
        self.children += (node, )
    

    def setParent(self, node):
        '''
        Function to set the parent node to the current node

        Parameter:
            node: Node object to be added as a child
        '''
        self.parent = node
    
    def __repr__(self):
        res_str = f"Foam("
        for key, val in self.__dict__.items():
            res_str = res_str + f"{key} : {val}, "
        res_str = res_str + ")"
        return res_str
    
    def getChild(self, val: str):
        '''
        Function to find a child node with the given attribute

        Parameter:
            val: Name of the Node that is bein searched for
        '''
        return find_by_attr(self, val, maxlevel = 2)

    def addData(self, data: KeyData, pos: int = None):
        '''
        Function to add KeyData attributes to the existing Node
        '''

        if pos != None:
            self.data.insert(pos, data)
        else:
            self.data.append(data)
    
    def removeData(self, data: KeyData):
        '''
        Function to remove a keydata attribute from the node
        '''

        try: 
            self.data.remove(data)
        except:
            raise AttributeError(f"{data.name} does not exist in this node")
    
    def reorderData(self, data: KeyData, pos: int):
        '''
        Function to reorder the data in the node
        '''

        try:
            self.data.remove(data)
            self.data.insert(data, pos)
        except:
            raise AttributeError(f"{data.name} does not exist in this node")
    
    def writeOut(self, file, indent = 0):
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
                d.writeOut(file)
            file.write("}\n")
        '''

        makeIndent(file, indent)
        file.write(f"{self.name}\n")

        makeIndent(file, indent)
        file.write("{\n")

        for d in self.data:
            d.writeOut(file, indent+1)

        # makeIndent(file, indent)

        for child in self.children:
            child.writeOut(file, indent+1)
            file.write("\n")

        makeIndent(file, indent)
        file.write("}\n")


