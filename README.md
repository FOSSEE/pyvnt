
# PyVNT : Python Venturial Node Trees

PyVNT is a library to control [Venturial's](https://github.com/FOSSEE/venturial) Node-Tree based data structure using Python. Primarily, PyVNT serves as a dependency to Venturial but it can also be used independently. PyVNT contains classes that define the Node-tree data structure and modules for manipulating it. 

## Features

The main features of PyVNT are: 
1. Make Node trees that mimic the structure of OpenFOAM Dictionaries.
2. Provide tools for conveniently manipulating trees with simple Python scripts. 
3. Generate serialised data for dynamically generating graphical representation of trees. 
4. Parse YAML files and traditional OpenFOAM dictionary files into PyVNT node trees.


## Installation

1. Clone the repository.
```bash
$ git clone https://github.com/FOSSEE/pyvnt.git
```
2. Create a python virtual environment in which you want to install the python package

3. Run the `setup.py` script inside a python virtual environment to build the python package from the source files

```bash
$ python setup.py sdist bdist_wheel
```

4. Install the python package from the build files using `setup.py`

```bash
$ python setup.py install
```


5. import `pyvnt` in your script to use it. 



## Venturial Node-Trees

There are different classes in the package for different kinds of data in OpenFOAM: 

- `Value_P` class is used to represent basic values. There are three children classes under `Value_P`:
    - `Enm_P` class is used to represent string values. The reason for it being an enum is that the fields that have string values usually have a few options for the string values, and a enum helps to reinforce those options and prevent the user from entering incorrect values.
    - `IntProperty` class is used to represent Integer values.
    - `FloatProperty` class is used to represent Floating point values

- `Key_C` class is used to store keys for the OpenFOAM dictionary data types

- `Node_C` class is used to represent the OpenFOAM dictionary data type.

Here is a detailed comparisions of a OpenFOAM dictionary and a pyvnt Node tree: 

The example OpenFOAM dictionary is written on the left, and the Node created in pyvnt is displayed in the right, with the object type mentioned in brackets beside the name of the value. 

<table border="0">
 <tr>
    <th><b>OpenFOAM dictionary</b></th>
    <th><b>PyVnt Node Tree</b></th>
 </tr>
 <tr>
    <td>
<pre>
solvers
{
    p
    { 
        solver          PCG, BNR;
        preconditioner  DIC;
        tolerance       1e-06;
        relTol          0.05;
    }
}
</pre>
    </td>
    <td>
<pre>
solvers(Node_C)
└── p(Node_C)
    {   
       solver(Key_C) : PCG(Enm_P), BNR(Enm_P)
       preconditioner(Key_C) : DIC(Enm_P), 
       tolerance(Key_C) : 1e-06(FloatProperty), 
       relTol(Key_C) : 0.05(FloatProperty), 
    }
</pre>
    </td>
 </tr>
</table>

As shown above, the `Node_C` and `Key_C` classes are used to represent the basic elements of the OpenFOAM Dictionary data structure. While the `Value_P` classe and its children classes are used to represent the basic property values in OpenFOAM. 

## Sample Use Case

Here is an example OpenFOAM use case file that we will use as a reference.

```text
fvSolutions.txt

FoamFile
{
    version 2.0;
    class   dictionary;
    format  ascii;
}

solvers
{
    p
    { 
        solver          PCG, BNR;
        preconditioner  DIC;
        tolerance       1e-06;
        relTol          0.05;
    }

    pFinal
    {
        relTol          0;
    }

    U
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-05;
        relTol          0;
    }
}

PISO
{
    nCorrectors     2;
    nNonOrthogonalCorrectors 0;
    pRefCell        0;
    pRefValue       0;
}
```



Here is how a sample code would look like that would build this file inside pyvnt:

```py
# testfile.py

from pyvnt import *

head = Node_C('fvSolutions')

sl = Node_C('solvers', parent = head)

s = Key_C('solver', Enm_P('val1', items={'PCG', 'PBiCG', 'PBiCGStab'}, default='PCG'))
pc = Key_C('preconditioner', Enm_P('val1', items={'DIC', 'DILU', 'FDIC'}, default='DIC'))
tol = Key_C('tolerance', Flt_P('val1', minimum=0, maximum=1000, default=1e-06))
rt = Key_C('relTol', Flt_P('val1', minimum=0, maximum=100, default=0.05))

p = Node_C('p', sl, None, pc, s,  tol, rt)

relTol2 = Key_C('relTol', Flt_P('val1', minimum=0, maximum=100, default=0))

pf = Node_C('pFinal', sl, None, relTol2)

sol2 = Key_C('solver', Enm_P('val1', items={'smoothSolver'}, default='smoothSolver'))
sm = Key_C('smoother', Enm_P('val1', items={'symGaussSeidel', 'gaussSeidel'}, default = 'symGaussSeidel'))
tol2 = Key_C('tolerance', Flt_P('val1', minimum=0, maximum=1000, default=1e-05))
relTol3 = Key_C('relTol', Flt_P('val1', minimum=0, maximum=100, default=0))

u = Node_C('U', sl, None, sol2, sm,
         tol2, relTol3)

ncorr = Key_C('nCorrectors', Int_P('int_prop_1', minimum=0, maximum=100, default=2))
nnoc = Key_C('nNonOrthogonalCorrectors', Int_P('int_prop_2', minimum=0, maximum=100, default=0))
prc = Key_C('pRefCell', Int_P('int_prop_3', minimum=0, maximum=100, default=0))
prv = Key_C('pRefValue', Int_P('int_prop_4', minimum=0, maximum=100, default=0))


piso = Node_C('PISO', head, None, ncorr,
           nnoc, prc, prv)

show_tree(head)

```

The resultant tree generated using the above code will look like the following:

```bash
$ python testfile.py

fvSolutions
├── solvers
│   ├── p
│   │   { 
│   │      preconditioner : DIC, 
│   │      solver : PCG, 
│   │      tolerance : 1e-06, 
│   │      relTol : 0.05, 
│   │   }
│   ├── pFinal
│   │   { 
│   │      relTol : 0, 
│   │   }
│   └── U
│       { 
│          solver : smoothSolver, 
│          smoother : symGaussSeidel, 
│          tolerance : 1e-05, 
│          relTol : 0, 
│       }
└── PISO
    { 
       nCorrectors : 2, 
       nNonOrthogonalCorrectors : 0, 
       pRefCell : 0, 
       pRefValue : 0, 
    }
```


## Controlling Element Order in Node_C for File Output

Node_C objects internally maintain an ordered list of their direct data elements (Key_C instances) and direct child nodes (nested Node_C instances). This ordering is critical for the writeTo function when generating files (especially in the traditional OpenFOAM .txt format), as it ensures that dictionaries are written with a consistent and predictable layout. Display utilities like show_tree also respect this order.

The writeTo(root, path, fileType='txt') function, when fileType is 'txt', iterates through root.get_ordered_items() to write the top-level elements (data and children) of the root node. This process is recursive for child Node_C objects, ensuring the entire tree is written according to the defined or default order at each level.

### set_order(names_list: list)

This method allows you to define the specific order of direct Key_Cs and child Node_Cs within a Node_C. This order will be directly used by writeTo (for .txt) when serializing the node.

### get_ordered_items() -> list

This method returns the items in the order that writeTo (for .txt) will use for iterating and writing the Node_C's contents.

### Example: Impact of set_order on writeTo Output

```py
from  pyvnt  import  Node_C, Key_C, Enm_P, List_CP, writeTo, show_tree
import  os
import  shutil

# Create a directory for output
output_dir  =  "pyvnt_output_example"

if  os.path.exists(output_dir):
	shutil.rmtree(output_dir) # Clean previous run
os.makedirs(output_dir)

  
root_node  =  Node_C("myConfig") # Filename will be myConfig.txt

key_c  =  Key_C("C_setting", Enm_P("val_c", {"val_c"}, default="val_c"))
key_a  =  Key_C("A_setting", Enm_P("val_a", {"val_a"}, default="val_a"))
child_b_node  =  Node_C("B_child_node",parent=root_node)
key_d  =  Key_C("D_setting", Enm_P("val_d", {"val_d"}, default="val_d"))

list_key  =  Key_C("E_list_key")
list_cp_val  =  List_CP("my_list_data", elems=[[Enm_P("item1", {"item1"},default="item1")],[Enm_P("item2", {"item2"}, default="item2")]])

list_key.append_val(list_cp_val._Value_P__name,list_cp_val)
# Add in an order different from desired final output
root_node.add_data(key_c)
root_node.add_data(key_a)
root_node.add_data(key_d)
root_node.add_data(list_key)

# --- Write to file BEFORE setting a specific order ---
print(f"--- Writing to {root_node.name}.txt (default order) ---")
writeTo(root_node, output_dir, fileType='txt')
show_tree(root_node)

# --- Set a specific order for root_node's items ---
desired_output_order  = ["A_setting", "B_child_node", "C_setting", "E_list_key", "D_setting"]
root_node.set_order(desired_output_order)

print(f"\\n--- Writing to {root_node.name}_ordered.txt (custom order) ---")
# To avoid overwriting, let's change the root_node name for the new file
original_name  =  root_node.name
root_node.name  =  original_name  +  "_ordered"
show_tree(root_node)
writeTo(root_node, output_dir, fileType='txt')

```

<table border="0">
 <tr>
    <th><b>Before</b></th>
    <th><b>After</b></th>
 </tr>
 <tr>
    <td>
<pre>
B_child_node
{
}
C_setting       val_c;
A_setting       val_a;
D_setting       val_d;
E_list_key
(
	item1 
	item2 
);
</pre>
    </td>
    <td>
<pre>
A_setting       val_a;
B_child_node
{
}
C_setting       val_c;
E_list_key
(
	item1 
	item2 
);
D_setting       val_d;
</pre>
    </td>
 </tr>
</table>


The writeTo function, by utilizing get_ordered_items for its .txt output routine, ensures that the generated files accurately reflect the intended structure and sequence, which is essential for OpenFOAM and other tools that rely on specific file layouts.

## Serializing PyVNT Trees to Files (writeTo)

PyVNT provides a writeTo(root_node, path, fileType='txt') function to serialize a node tree into a file.

-   **root_node**: The top-level Node_C object to be written. The name of this root_node is used as the base for the output filename (e.g., root_node.name = 'controlDict' results in controlDict.txt).
    
-   **path**: The directory where the file will be saved.
    
-   **fileType**: Specifies the output format.
    
    -   'txt' (default): Generates a file in the traditional OpenFOAM dictionary format. This process uses get_ordered_items() to iterate through Node_C contents, thus respecting any order defined by set_order() or the default addition order.
        
    -   'yaml': Generates a YAML representation of the tree. The provided writeTo snippet suggests separate iteration for data and children for YAML, relying on the YAML library to handle dictionary key order (often preserved from Python dicts) and the inherent order of List_CP.
        

This function is the primary means of converting an in-memory PyVNT tree back into a persistent file format that can be used by Venturial, OpenFOAM, or other compatible tools.

## Parsing OpenFOAM Data Files ( Dictionary and YAML)

PyVNT includes an OpenFoamParser class to convert OpenFOAM dictionary files (traditional format) and OpenFOAM-compatible YAML files into PyVNT Node-Trees.

 ### Parser Usage

The OpenFoamParser has two main methods for parsing:

-   parse_file(text: str = None, fileType: str = 'txt', path: str = None): Parses a single file.
    
    -   If path is provided, it reads the file from the path. The file extension (.yaml, .txt, or no extension for dictionary files) helps determine the parser type.
        
    -   If text is provided, it parses the string content. fileType must be specified as 'txt' (for dictionary format) or 'yaml'.
        
-   parse_case(path: str): Recursively parses an entire OpenFOAM case directory. It attempts to parse files it recognizes (dictionaries, YAML files) and builds a hierarchical tree of the case.

### Parsing OpenFOAM-like YAML Files

YAML is increasingly used for its readability. PyVNT can handle YAML structured similarly to OpenFOAM dictionaries.

#### Sample YAML Input

Consider the following YAML data, mimicking an OpenFOAM blockMeshDict:

```
FoamFile:                            # Dictionary
  format: "ascii"                    # key Entry
  class: "dictionary"
  object: "blockMeshDict"

convertToMeters: "0.1"               # key Entry

vertices:                            # key list
  - [ 0, 0, 0 ]
  - [ 1, 0, 0 ]
  - [ 1, 1, 0 ]
  - [ 0, 1, 0 ]
  - [ 0, 0, 0.1 ]
  - [ 1, 0, 0.1 ]
  - [ 1, 1, 0.1 ]
  - [ 0, 1, 0.1 ]

blocks:                            # key list
  - hex
  - [ 0, 1, 2, 3, 4, 5, 6, 7 ]
  - [ 20, 20, 1 ]
  - simpleGrading
  - [ 1, 1, 1 ]

edges:                             # key -> list (mixed custom structure)
  - arc
  - 0
  - 1
  - [ 0.5, 0.1, 0 ]
  - spline
  - 4
  - 5
  - [ [4.1, 4.2, 4.3], [4.5, 4.6, 4.7], [4.9, 5.0, 5.1] ]
  - polyLine
  - 6
  - 7
  - [ [6.1, 6.2, 6.3], [6.5, 6.6, 6.7] ]

boundary:                          # List Node 
  - movingWall:
      type: "wall"
      faces:
        - [ 3, 7, 6, 2 ]

  - fixedWalls:
      type: "wall"
      faces:
        - [ 0, 4, 7, 3 ]
        - [ 2, 6, 5, 1 ]
        - [ 1, 5, 4, 0 ]

  - frontAndBack:
      type: "empty"
      faces:
        - [ 0, 3, 2, 1 ]
        - [ 4, 5, 6, 7 ]

mergePatchPairs:                   # key -> list 
  - [ patch_0, patch_1 ]
  - [ patch_2, patch_3 ]


```
```py
# parse_yaml_example.py
from pyvnt import OpenFoamParser, Node_C, show_tree # Assuming these are top-level imports

# Sample YAML content (can also be read from a file)
yaml_content = """Yamle Example shown above"""

# Initialize the parser
parser = OpenFoamParser()

# Parse the YAML string
# For a file: tree = parser.parse_file(path="path/to/your/blockMeshDict.yaml")
tree = parser.parse_file(text=yaml_content, fileType='yaml')

# If parsed from text, the root node might be named 'root' by default.
# You can rename it for clarity:
if tree and tree.name == "root": # Default name from parser for text input
    tree.name = "blockMeshDict_from_yaml"

# Display the generated tree
if tree:
    show_tree(tree)
else:
    print("Failed to parse YAML content.")
```


#### Expected Tree Output (Conceptual)

The show_tree(tree) command for the parsed YAML would produce a structure conceptually similar to this:

```
blockMeshDict
{ 
   convertToMeters : 0.1
   vertices : ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0.1), (1, 0, 0.1), (1, 1, 0.1), (0, 1, 0.1))
   blocks : ('hex', (0, 1, 2, 3, 4, 5, 6, 7), (20, 20, 1), 'simpleGrading', (1, 1, 1))
   edges : ('arc', 0, 1, (0.5, 0.1, 0), 'spline', 4, 5, ((4.1, 4.2, 4.3), (4.5, 4.6, 4.7), (4.9, 5.0, 5.1)), 'polyLine', 6, 7, ((6.1, 6.2, 6.3), (6.5, 6.6, 6.7)))        
   mergePatchPairs : (('patch_0', 'patch_1'), ('patch_2', 'patch_3'))
}
├── FoamFile
│   {
│      format : ascii
│      class : dictionary
│      object : blockMeshDict
│   }
└── boundary
    ├── movingWall
    │   {
    │      type : wall
    │      faces : ((3, 7, 6, 2),)
    │   }
    ├── fixedWalls
    │   {
    │      type : wall
    │      faces : ((0, 4, 7, 3), (2, 6, 5, 1), (1, 5, 4, 0))
    │   }
    └── frontAndBack
        {
           type : empty
           faces : ((0, 3, 2, 1), (4, 5, 6, 7))
        }
```


### Parsing Traditional OpenFOAM Dictionary Files

The parser can also handle the standard OpenFOAM dictionary format:

```py
from  pyvnt  import  *

parser  =  OpenFoamParser()

# Parse from file path
# tree_from_dict_file  =  parser.parse_file(path="system/controlDict")
# if  tree_from_dict_file: 
# show_tree(tree_from_dict_file)

# Parse from text string

dict_content  =  """
application simpleFoam;
startFrom latestTime;
startTime 0;
stopAt endTime;
endTime 1000;
"""

tree_from_dict_text  =  parser.parse_file(text=dict_content, fileType='txt')
if  tree_from_dict_text:
	if  tree_from_dict_text.name  ==  "root": # Default for text input
		tree_from_dict_text.name  =  "controlDict_from_text"
	show_tree(tree_from_dict_text)
```


### Parsing Entire Case Directories

The parse_case(path) method is useful for loading an entire OpenFOAM case:

```py
parser = OpenFoamParser()
case_tree = parser.parse_case("/path/to/your/OpenFOAM_case_directory")
if case_tree:
    show_tree(case_tree)
```


This will create a master Node_C for the case, with child nodes for subdirectories and parsed files.

### Retrieving Values from a Parsed Tree

Once a tree is parsed (or manually constructed), use the get_value(node: Node_C, *keys) method of the OpenFoamParser instance (or a similar standalone utility if available) to navigate and retrieve specific elements:

```py
from pyvnt import *

parser  =  OpenFoamParser()

tree  =  parser.parse_file(path=r"\cavity\system\blockMeshDict")

foam_file_node  =  parser.get_value(tree, "FoamFile")
if  foam_file_node:
	show_tree(foam_file_node)
   

# Get the 'class' Key_C from within 'FoamFile' Node_C
class_key_obj  =  parser.get_value(tree, "FoamFile", "class")
if  class_key_obj:
	print(f"Retrieved Key: {class_key_obj.name}")

  
# Get vertices data (which would be a Key_C holding a List_CP)
vertices_key  =  parser.get_value(tree, "vertices")
if  vertices_key  and  isinstance(vertices_key, Key_C):
	list_cp_data  =  list(vertices_key.get_items())[0][1]
	if  isinstance(list_cp_data, List_CP):
		print(f"Vertices List Name: {list_cp_data._Value_P__name}")
```


This provides a versatile way to load, inspect, and interact with OpenFOAM configurations, whether they are in the traditional dictionary format or the more modern YAML format.