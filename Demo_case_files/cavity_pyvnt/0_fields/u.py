from pyvnt import *

u = Node_C("U")

dim = Key_C("dimensions",
    Dim_Set_P("dim_set", [0, 1, -1, 0, 0, 0, 0])
)

u.add_data(dim)

internalField = Key_C("internalField",
    Enm_P("type", {"uniform", "nonuniform"}, "uniform"),
    Vector_P("value", 0, 0, 0)
)

u.add_data(internalField)

bf = Node_C("boundaryField", u)

mWall = Node_C("mWall", bf, [], 
    Key_C("type",
        Enm_P("type", {"fixedValue", "zeroGradient", "noSlip", "empty"}, "fixedValue")
    ),
    Key_C("value", 
        Enm_P("type", {"uniform", "nonuniform"}, "uniform"),
        Vector_P("value", 1, 0, 0)  
    )
)

fWalls = Node_C("fWalls", bf, [],
    Key_C("type",
        Enm_P("type", {"fixedValue", "zeroGradient", "noSlip", "empty"}, "noSlip")
    )
)

fnb = Node_C("fnb", bf, [],
    Key_C("type",
        Enm_P("type", {"fixedValue", "zeroGradient", "noSlip", "empty"}, "empty")
    )
)

