from pyvnt.Container.Node_C import Foam
from pyvnt.Container.Key_C import Key_C

# Function no longer needed
# It is not available to use outside the package and the code is here just for future reference if needed

def obj_constructor(name: str, parent = None, children: [] = None, *args):
    '''
    Function to create a new node object with the given name 

    Parameter:
        name: Name of the Node that is to be created
        parent: Parent Node of the current Node (Optional)
        children: List of the children node(s) of the current Node (Optional)
    '''

    tmp = list(args)

    if children != None and tmp != []:
        raise Exception("Both children and args cannot be given at the same time")
    elif tmp == [] and children == None:
        return Foam(name, parent, children)
    elif children == None:
        return Key_C(name, parent, *args)
    else:
        raise Exception("Invalid arguments given")