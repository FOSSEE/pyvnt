from pyvnt.DictionaryElement.foamDS import Foam
from pyvnt.DictionaryElement.keyData import KeyData

def obj_constructor(name: str, parent = None, children: [] = None, *args):
    '''
    Function to create a new node object with the given name

    Parameter:
        name: Name of the Node that is to be created
        parent: Parent Node of the current Node (Optional)
        children: List of the children node(s) of the current Node (Optional)
    '''

    if children != None and args != None:
        raise Exception("Both children and args cannot be given at the same time")
    elif args == None:
        return Foam(name, parent, children)
    elif children == None:
        return KeyData(name, parent, *args)
    else:
        raise Exception("Invalid arguments given")

obj = obj_constructor("test_head")
print(obj)