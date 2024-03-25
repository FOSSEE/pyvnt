# PyVNT : Python Venturial Node Trees

PyVNT is a library to control [Venturial's](https://github.com/FOSSEE/venturial) Node-Tree based data structure using Python. Primarily, PyVNT serves as a dependency to Venturial but it can also be used independently. PyVNT contains classes that define the Node-tree data structure and modules for manipulating it. 

## Features

The main features of PyVNT are: 
1. Make Node trees that mimic the structure of OpenFOAM Dictionaries.
2. Provide tools for conveniently manipulating trees with simple Python scripts. 
3. Generate serialised data for dynamically generating graphical representation of trees. 


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

- `ValueProperty` class is used to represent basic values. There are three children classes under `ValueProperty`:
    - `EnumProp` class is used to represent string values. The reason for it being an enum is that the fields that have string values usually have a vew options for the string values, and a enum helps to reinforce those options and prevent the user from entering incorrect values.
    - `IntProperty` class is used to represent Integer values.
    - `FloatProperty` class is used to represent Floating point values

- `KeyData` class is used to store keys for the OpenFOAM distionary data types

- `Foam` class is used to represent the OpenFOAM dictionary data type.

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
solvers(Foam)
└── p(Foam)
    {   
       solver(KeyData) : PCG(EnumProp), BNR(EnumProp)
       preconditioner(KeyData) : DIC(EnumProp), 
       tolerance(KeyData) : 1e-06(FloatProperty), 
       relTol(KeyData) : 0.05(FloatProperty), 
    }
</pre>
    </td>
 </tr>
</table>

As shown above, the `Foam` and `KeyData` classes are used to represent the basic elements of the OpenFOAM Dictionary data structure. While the `ValueProperty` classe and its children classes are used to represent the basic property values in OpenFOAM. 

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
        $p;
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

head = Foam('fvSolutions')

sl = Foam('solvers', parent = head)

s = KeyData('solver', EnumProp('val1', items={'PCG', 'PBiCG', 'PBiCGStab'}, default='PCG'))
pc = KeyData('preconditioner', EnumProp('val1', items={'DIC', 'DILU', 'FDIC'}, default='DIC'))
tol = KeyData('tolerance', PropertyFloat('val1', minimum=0, maximum=1000, default=1e-06))
rt = KeyData('relTol', PropertyFloat('val1', minimum=0, maximum=100, default=0.05))

p = Foam('p', sl, None, pc, s,  tol, rt)

relTol2 = KeyData('relTol', PropertyFloat('val1', minimum=0, maximum=100, default=0))

pf = Foam('pFinal', sl, None, relTol2)

sol2 = KeyData('solver', EnumProp('val1', items={'smoothSolver'}, default='smoothSolver'))
sm = KeyData('smoother', EnumProp('val1', items={'symGaussSeidel', 'gaussSeidel'}, default = 'symGaussSeidel'))
tol2 = KeyData('tolerance', PropertyFloat('val1', minimum=0, maximum=1000, default=1e-05))
relTol3 = KeyData('relTol', PropertyFloat('val1', minimum=0, maximum=100, default=0))

u = Foam('U', sl, None, sol2, sm,
         tol2, relTol3)

ncorr = KeyData('nCorrectors', PropertyInt('int_prop_1', minimum=0, maximum=100, default=2))
nnoc = KeyData('nNonOrthogonalCorrectors', PropertyInt('int_prop_2', minimum=0, maximum=100, default=0))
prc = KeyData('pRefCell', PropertyInt('int_prop_3', minimum=0, maximum=100, default=0))
prv = KeyData('pRefValue', PropertyInt('int_prop_4', minimum=0, maximum=100, default=0))


piso = Foam('PISO', head, None, ncorr,
           nnoc, prc, prv)

showTree(head)

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

 
