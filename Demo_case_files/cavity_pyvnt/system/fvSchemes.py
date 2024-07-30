from pyvnt import *

fvSchemes = Node_C("fvSchemes")

ddtSchemes = Node_C(
    "ddtSchemes", fvSchemes, [],
    Key_C(
        "default",
        Enm_P("default", {"Euler", "CrankNicolson"}, "Euler")
    )
)

gradSchemes = Node_C(
    "gradSchemes", fvSchemes, [],
    Key_C(
        "default",
        Enm_P("def1", {"Gauss", "CrankNicolson", "none"}, "Gauss"),
        Enm_P("def2", {"linear", "limitedlinear", "limitedCubic"}, "linear")
    ),
    Key_C(
        "grad(p)",
        Enm_P("gradp1", {"Gauss", "CrankNicolson", "none"}, "Gauss"),
        Enm_P("gradp2", {"linear", "limitedlinear", "limitedCubic"}, "linear")
    )
)

divSchemes = Node_C(
    "divSchemes", fvSchemes, [],
    Key_C(
        "default",
        Enm_P("def1", {"Gauss", "CrankNicolson", "none"}, "none"),
    ),
    Key_C(
        "div(phi,U)",
        Enm_P("divphi1", {"Gauss", "CrankNicolson", "none"}, "Gauss"),
        Enm_P("divphi2", {"linear", "limitedLinear", "limitedCubic"}, "linear")
    )
)

laplacianSchemes = Node_C(
    "laplacianSchemes", fvSchemes, [],
    Key_C(
        "default",
        Enm_P("def1", {"Gauss", "CrankNicolson", "none"}, "Gauss"),
        Enm_P("def2", {"linear", "limitedLinear", "limitedCubic"}, "linear"),
        Enm_P("def3", {"hexagonal", "orthogonal", "skew", "symmetric"}, "orthogonal")
    )
)

interpolationSchemes = Node_C(
    "interpolationSchemes", fvSchemes, [],
    Key_C(
        "default",
        Enm_P("def1", {"linear", "linearUpwind", "linearLimited", "linearV", "linearVUpwind", "linearVLimited"}, "linear")
    )
)

snGradSchemes = Node_C(
    "snGradSchemes", fvSchemes, [],
    Key_C(
        "default",
        Enm_P("def1", {"hexagonal", "orthogonal", "skew", "symmetric"}, "orthogonal")
    )
)

writeTo(fvSchemes, "Demo_case_files/")