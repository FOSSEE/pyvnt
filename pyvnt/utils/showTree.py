from anytree import Node, RenderTree, AsciiStyle, NodeMixin
from pyvnt.DictionaryElement.foamDS import Foam

def showTree(head: Foam):
    '''
    Function to output the entire tree in the terminal starting from the current node object

    Parameters:
        head: Head Node of the tree to be printed. Must be of typpe `Foam`
    
    Returns: 
        None
    '''
    for pre, fill, node in RenderTree(head):
        print( "%s%s" % (pre, node.name))
        attr = "%s{ \n" % (fill)
        for d in node.data:

            tmp_str = u"%s   %s" % (fill, d.giveVal())
            attr = attr + tmp_str + "\n"
        attr = attr + "%s}"%(fill)

        chk = "%s{ \n%s}" % (fill, fill) 
        if attr != chk:
            print(attr)
        
        

        
        