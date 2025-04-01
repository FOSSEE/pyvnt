from pyvnt.Container.node import *
from pyvnt.Container.key import *
from pyvnt.Container.list import *
from pyvnt.Reference.basic import *
from pyvnt.Reference.error_classes import *
from pyvnt.Reference.dimension_set import *
from pyvnt.Reference.vector import *
from pyvnt.Reference.tensor import *
from pyvnt.utils.make_indent import make_indent
import re

def writeTo(root, path,fileType='txt'):
    '''
    Function to write the dictionary object to the file

    The root node becomes the filename, and the content of the nodes are then written in the file by traversing through the contents of the node recursively. 

    Parameters:
        Node_C: Dictionary object to be written
        path: Path to the file where the dictionary object is to be written

    '''
    file_name = root.name

    if fileType=='txt':
        ptt = r"$.txt"
        if re.search(ptt, file_name):
            raise ValueError("File name cannot have .txt extension")

        with open(path + f"\\{file_name}.txt", "w") as file: # Creates a file with the same name as the root node
            print(path )
            for d in root.get_data():
                write_out(d, file)
            
            for child in root.children:
                write_out(child, file)
                file.write("\n")
    elif fileType=='yaml':
        ptt = r"$.yaml"
        if re.search(ptt, file_name):
            raise ValueError("File name cannot have .txt extension")

        with open(path + f"\\{file_name}.yaml", "w") as file: # Creates a file with the same name as the root node

            for d in root.get_data():
                write_out_Yaml(d, file)
            
            for child in root.children:
                write_out_Yaml(child, file)
                file.write("\n")

def write_out(obj, file, indent = 0, list_in_key = False):
    '''
    Function to write the current object to the file

    Parameters:
        file: File object to write the object to
        indent: Required indentation needed for the object to be written

    '''

    if type(obj) == Node_C: # If object is a node
        make_indent(file, indent)
        file.write(f"{obj.name}\n")
        make_indent(file, indent)
        file.write("{\n")

        for d in obj.get_data():
            write_out(d, file, indent+1)
        
        for child in obj.children:
            write_out(child, file, indent+1)
            file.write("\n")

        make_indent(file, indent)
        file.write("}\n")
    
    elif type(obj) == Key_C: # If object is a key
        col_width = 16
        last_elem = list(obj.get_keys())[-1]

        make_indent(file, indent)

        if len(list(obj.get_keys())) == 1 and type(list(obj.get_items())[0][1]) == List_CP:
            file.write(f"{obj.name}\n")
            for key, val in obj.get_items():
                write_out(val, file, indent, True)
        else:
            if len(obj.name) >= col_width:
                file.write(f"{obj.name} ")
            else:
                file.write(f"{obj.name.ljust(col_width)}")
            for key, val in obj.get_items():
                write_out(val, file)
                if key != last_elem:
                    file.write(" ")

        file.write(";\n")

    elif type(obj) == List_CP: # If object is a list
        if obj.is_a_node():
            make_indent(file, indent)
            file.write(f"{obj.name}\n")

            make_indent(file, indent)
            file.write("(\n")

            for child in obj.children:
                write_out(child, file, indent+1)
                file.write("\n")

            make_indent(file, indent)
            file.write(")\n")

        elif list_in_key:
            make_indent(file, indent)
            file.write("(\n")
            for elem in obj.get_elems():
                make_indent(file, indent+1)
                for val in elem:
                    write_out(val, file)
                    file.write(" ")
                file.write("\n")
            make_indent(file, indent)
            file.write(")")
            
        else:
            res = "( "
            for elem in obj.get_elems():
                for val in elem:
                    res = res + f"{val.give_val()} "
            res += ")"
            file.write(res)
    
    elif type(obj) == Int_P or type(obj) == Flt_P or type(obj) ==  Enm_P or type(obj) == Vector_P or type(obj) == Tensor_P : # If object is a property
        file.write(f"{obj.give_val()}")
    
    elif type(obj) == Dim_Set_P: # special case for dimension set
        file.write(" ".join(i for i in str(obj.give_val()).split(",")))
    
    else:
        raise ValueError(f"Object of type {type(obj)} not supported for writing out to file")

def write_out_Yaml(obj, file, indent = 0, list_in_key = False,parent_list_node=False):
    '''
    Function to write the current object to the file

    Parameters:
        file: File object to write the object to
        indent: Required indentation needed for the object to be written

    '''
    def make_indent(file, level):
        """Helper function to add indentation."""
        file.write("  " * level)

    if type(obj) == Node_C: # If object is a node
        make_indent(file, indent)
        if parent_list_node:
            file.write('- ')
            indent+=1
        file.write(f"{obj.name}:\n")
        for d in obj.get_data():
            write_out_Yaml(d, file, indent+1)
        
        for child in obj.children:
            write_out_Yaml(child, file, indent+1)

        file.write("\n")
    
    elif type(obj) == Key_C: # If object is a key
        last_elem = list(obj.get_keys())[-1]
        # print(str(indent)+"     "+str(obj.name))
        make_indent(file, indent)
        if len(list(obj.get_keys())) == 1 and type(list(obj.get_items())[0][1]) == List_CP:
            file.write(f"{obj.name}: ")
            for key, val in obj.get_items():
                write_out_Yaml(val, file, indent, True)
        else:
            file.write(f"{obj.name}: ")
            for key, val in obj.get_items():
                write_out_Yaml(val, file)
                if key != last_elem:
                    file.write(" ")
        file.write("\n")

    elif type(obj) == List_CP: # If object is a list
        if obj.is_a_node():
            make_indent(file, indent)
            file.write(f"{obj.name}:\n")

            for child in obj.children:
                write_out_Yaml(child, file, indent+1,parent_list_node=True)


        elif list_in_key:
            for elem in obj.get_elems():
                if not elem:
                    file.write("[]")
                    continue
                file.write('\n')
                for val in elem:
                    make_indent(file,indent+1)
                    file.write('- ')
                    write_out_Yaml(val, file)
                    file.write('\n')
            make_indent(file, indent)
            
        else:
            res = "[ "
            for elem in obj.get_elems():
                i=0
                for val in elem:
                    if i==1:
                        res+=','
                    res = res + f"{val.give_val()} "
                    i=1
            res += "]"
            file.write(res)
    
    elif type(obj) == Int_P or type(obj) == Flt_P or type(obj) ==  Enm_P or type(obj) == Vector_P or type(obj) == Tensor_P : # If object is a property
        file.write(f"{obj.give_val()}")
    
    elif type(obj) == Dim_Set_P: # special case for dimension set
        file.write(" ".join(i for i in str(obj.give_val()).split(",")))
    
    else:
        raise ValueError(f"Object of type {type(obj)} not supported for writing out to file")
