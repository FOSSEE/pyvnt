from pyvnt import *

prop1 = EnumProp('val1', items={'PCG', 'PBiCG', 'PBiCGStab'}, default='PCG')

key1 = KeyData('solver', prop1)

head = Foam("test_head", None, None, key1)

# head.dispTree()

showTree(head)