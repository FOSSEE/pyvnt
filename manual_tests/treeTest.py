from .pyvnt.DictionaryElement.foamDS import *
from .pyvnt.DictionaryElement.keyData import *
from .pyvnt.Reference.basic import *

prop1 = EnumProp('val1', items={'PCG', 'PBiCG', 'PBiCGStab'}, default='PCG')

key1 = KeyData('solver', prop1)

head = Foam(name="test_head", children = [key1])

head.dispTree()