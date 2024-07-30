from pyvnt import *

fvSolution = Node_C("fvSolution")

solvers = Node_C("solvers", fvSolution, [])

p = Node_C(
    "p", solvers, [],
    Key_C(
        "solver", Enm_P("solver", {"PCG", "smoothSolver", "GAMG"}, "PCG")
    ),
    Key_C(
        "preconditioner", Enm_P("preconditioner", {"DIC", "DILU"}, "DIC")
    ),
    Key_C(
        "tolerance", Flt_P("tolerance", 1e-06)
    ),
    Key_C(
        "relTol", Flt_P("relTol", 0.05)
    )
)

pFinal = Node_C(
    "pFinal", solvers, [],
    Key_C(
        "solver", Enm_P("solver", {"PCG", "smoothSolver", "GAMG"}, "PCG")
    ),
    Key_C(
        "preconditioner", Enm_P("preconditioner", {"DIC", "DILU"}, "DIC")
    ),
    Key_C(
        "tolerance", Flt_P("tolerance", 1e-06)
    ),
    Key_C(
        "relTol", Flt_P("relTol", 0)
    )
)

u = Node_C(
    "U", solvers, [],
    Key_C(
        "solver", Enm_P("solver", {"PCG", "smoothSolver", "GAMG"}, "smoothSolver")
    ),
    Key_C(
        "smoother", Enm_P("smoother", {"GaussSeidel", "symGaussSeidel"}, "symGaussSeidel")
    ),
    Key_C(
        "tolerance", Flt_P("tolerance", 1e-05)
    ),
    Key_C(
        "relTol", Flt_P("relTol", 0)
    )
)

piso = Node_C(
    "PISO", fvSolution, [],
    Key_C(
        "nCorrectors", Int_P("nCorrectors", 2)
    ),
    Key_C(
        "nNonOrthogonalCorrectors", Int_P("nNonOrthogonalCorrectors", 0)
    ),
    Key_C(
        "pRefCell", Int_P("pRefCell", 0)
    ),
    Key_C(
        "pRefValue", Flt_P("pRefValue", 0)
    )
)

writeTo(fvSolution, "Demo_case_files/")