from pyvnt.Container import *

def writeTo(root, path):
    '''
    Function to write the dictionary object to the file

    Parameters:
        Node_C: Dictionary object to be written
        path: Path to the file where the dictionary object is to be written

    '''
    with open(path, "w") as file:
        root.write_out(file)