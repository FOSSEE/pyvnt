from pyvnt import *

blockMeshDict = Node_C("blockMeshDict")
cM = Key_C("convertToMeters", Flt_P("convertToMeters", 0.1))

blockMeshDict.add_data(cM)

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

v_elem = []

for i in range(len(v)):
    v_elem.append([List_CP(f"v{i}", elems=[[Flt_P('x', v[i][0]), Flt_P('y', v[i][1]), Flt_P('z', v[i][2])]])])

vertices = List_CP("vertices", elems=v_elem)

verts = Key_C("vertices", vertices)

blockMeshDict.add_data(verts)

e1 = [
    Enm_P("type", {"hex"}, "hex"),
    List_CP("faces", elems=[[
        Int_P("v0", 0),
        Int_P("v1", 1),
        Int_P("v2", 2),
        Int_P("v3", 3),
        Int_P("v4", 4),
        Int_P("v5", 5),
        Int_P("v6", 6),
        Int_P("v7", 7)
    ]]),
    List_CP("res", elems=[[
        Int_P("nx", 20),
        Int_P("ny", 20),
        Int_P("nz", 1)
    ]]),
    Enm_P("grading", {"simpleGrading"}, "simpleGrading"),
    List_CP("simpleGrading", elems=[[
        Int_P("x", 1),
        Int_P("y", 1),
        Int_P("z", 1)
    ]])
]

blocks = List_CP("blocks", elems=[e1])

blks = Key_C("blocks", blocks)

blockMeshDict.add_data(blks)

edges = List_CP("edges", elems=[[]])

edgs = Key_C("edges", edges)

blockMeshDict.add_data(edgs)

typ = Key_C("type", Enm_P("type", {"wall", "empty"}, "wall"))

faces_1 = List_CP("faces", elems=[
    [List_CP("f0", elems=[[
    Int_P("v0", 3),
    Int_P("v1", 7),
    Int_P("v2", 6),
    Int_P("v3", 2)
    ]])]
])

fcs1 = Key_C("faces", faces_1)

mWall = Node_C("movingWall", None, [], typ, fcs1)

fcs2 = Key_C("faces", List_CP("faces", elems=[
    [List_CP("f0", elems=[
    [
        Int_P("v0", 0),
        Int_P("v1", 4),
        Int_P("v2", 7),
        Int_P("v3", 3)
    ]])], [List_CP("f1", elems=[
    [
        Int_P("v0", 2),
        Int_P("v1", 6),
        Int_P("v2", 5),
        Int_P("v3", 1)
    ]])], [List_CP("f2", elems=[
    [
        Int_P("v0", 1),
        Int_P("v1", 5),
        Int_P("v2", 4),
        Int_P("v3", 0)
    ]])],

]))

fwall = Node_C("fixedWalls", None, [], typ, fcs2)

fcs3 = Key_C("faces", List_CP("faces", elems=[
    [List_CP("f0", elems=[[
        Int_P("v0", 0),
        Int_P("v1", 3),
        Int_P("v2", 2),
        Int_P("v3", 1)
    ]])], 
    [List_CP("f1", elems=[[
        Int_P("v0", 4),
        Int_P("v1", 5),
        Int_P("v2", 6),
        Int_P("v3", 7)
    ]])]

]))

typ2 = Key_C("type", Enm_P("type", {"wall", "empty"}, "empty"))

fnb = Node_C("frontAndBack", None, [], typ2 , fcs3)

bnd = List_CP("boundary", values=[mWall, fwall, fnb], isNode=True)

blockMeshDict.add_child(bnd)

mergePatchPairs = List_CP("mergePatchPairs", elems=[[]])

mpp = Key_C("mergePatchPairs", mergePatchPairs)

blockMeshDict.add_data(mpp)

writeTo(blockMeshDict, "Demo_case_files/")
