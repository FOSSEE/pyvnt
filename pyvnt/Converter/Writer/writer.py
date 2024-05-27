from pyvnt.DictionaryElement import *

def writeTo(root, path):
    '''
    Function to write the dictionary object to the file

    Parameters:
        Foam: Dictionary object to be written
        path: Path to the file where the dictionary object is to be written

    '''
    with open(path, "w") as file:
        root.writeOut(file)