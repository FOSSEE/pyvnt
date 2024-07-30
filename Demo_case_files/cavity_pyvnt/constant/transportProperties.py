from pyvnt import *

transportProperties = Node_C("transportProperties")

nu = Key_C("nu", 
    Dim_Set_P("nu_dim", [0, 2, -1, 0, 0, 0, 0]),
    Flt_P("nu_val", 0.01)
)

transportProperties.add_data(nu)

writeTo(transportProperties, "Demo_case_files/")