from pyvnt import *

p = Node_C("P")

dim = Dim_Set_P("dimensions", [0, 2, -2, 0, 0, 0, 0])

p.add_data(dim)

internalField = Key_C("internalField",
    Enm_P("type", {"uniform", "nonuniform"}, "uniform"),
    Flt_P("value", 0)
)

p.add_data(internalField)

bf = Node_C("boundaryField", p)

mWall = Node_C("mWall", bf, [],
    Key_C("type",
        Enm_P("type", {"fixedValue", "zeroGradient", "noSlip", "empty"}, "zeroGradient")
    )
)

fWalls = Node_C("fWalls", bf, [],
    Key_C("type",
        Enm_P("type", {"fixedValue", "zeroGradient", "noSlip", "empty"}, "zeroGradient")
    )
)

fnb = Node_C("fnb", bf, [],
    Key_C("type",
        Enm_P("type", {"fixedValue", "zeroGradient", "noSlip", "empty"}, "empty")
    )
)