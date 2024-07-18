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

- `Value_P` class is used to represent basic values. There are three children classes under `Value_P`:
    - `Enm_P` class is used to represent string values. The reason for it being an enum is that the fields that have string values usually have a vew options for the string values, and a enum helps to reinforce those options and prevent the user from entering incorrect values.
    - `IntProperty` class is used to represent Integer values.
    - `FloatProperty` class is used to represent Floating point values

- `Key_C` class is used to store keys for the OpenFOAM distionary data types

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
       solver(Key_C) : PCG(Enm_P), BNR(Enm_P)
       preconditioner(Key_C) : DIC(Enm_P), 
       tolerance(Key_C) : 1e-06(FloatProperty), 
       relTol(Key_C) : 0.05(FloatProperty), 
    }
</pre>
    </td>
 </tr>
</table>

As shown above, the `Foam` and `Key_C` classes are used to represent the basic elements of the OpenFOAM Dictionary data structure. While the `Value_P` classe and its children classes are used to represent the basic property values in OpenFOAM. 

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

s = Key_C('solver', Enm_P('val1', items={'PCG', 'PBiCG', 'PBiCGStab'}, default='PCG'))
pc = Key_C('preconditioner', Enm_P('val1', items={'DIC', 'DILU', 'FDIC'}, default='DIC'))
tol = Key_C('tolerance', Flt_P('val1', minimum=0, maximum=1000, default=1e-06))
rt = Key_C('relTol', Flt_P('val1', minimum=0, maximum=100, default=0.05))

p = Foam('p', sl, None, pc, s,  tol, rt)

relTol2 = Key_C('relTol', Flt_P('val1', minimum=0, maximum=100, default=0))

pf = Foam('pFinal', sl, None, relTol2)

sol2 = Key_C('solver', Enm_P('val1', items={'smoothSolver'}, default='smoothSolver'))
sm = Key_C('smoother', Enm_P('val1', items={'symGaussSeidel', 'gaussSeidel'}, default = 'symGaussSeidel'))
tol2 = Key_C('tolerance', Flt_P('val1', minimum=0, maximum=1000, default=1e-05))
relTol3 = Key_C('relTol', Flt_P('val1', minimum=0, maximum=100, default=0))

u = Foam('U', sl, None, sol2, sm,
         tol2, relTol3)

ncorr = Key_C('nCorrectors', Int_P('int_prop_1', minimum=0, maximum=100, default=2))
nnoc = Key_C('nNonOrthogonalCorrectors', Int_P('int_prop_2', minimum=0, maximum=100, default=0))
prc = Key_C('pRefCell', Int_P('int_prop_3', minimum=0, maximum=100, default=0))
prv = Key_C('pRefValue', Int_P('int_prop_4', minimum=0, maximum=100, default=0))


piso = Foam('PISO', head, None, ncorr,
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

 
