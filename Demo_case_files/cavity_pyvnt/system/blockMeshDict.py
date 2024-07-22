from pyvnt import *

blockMeshDict = Node_C("blockMeshDict")
cM = Key_C("convertToMeters", "1.0")

blockMeshDict.add_data(cM)

vertices = List_CP("vertices")

v = [
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 0.1],
    [1, 0, 0.1],
    [1, 1, 0.1],
    [0, 1, 0.1]
]

for i in range(len(v)):
    vertices.append_elem(List_CP(name=f'v_{i+1}', elems=[[Flt_P('x', i[0]), Flt_P('y', i[1]), Flt_P('z', i[2])]]))

verts = Key_C("vertices", vertices)

blockMeshDict.add_data(verts)

blocks = List_CP("blocks")

