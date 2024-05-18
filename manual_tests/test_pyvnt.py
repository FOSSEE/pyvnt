from pyvnt import *
from anytree import RenderTree, AsciiStyle


prop1 = EnumProp('val1', items={'PCG', 'PBiCG', 'PBiCGStab'}, default='PCG')
prop2 = EnumProp('val2', items={'PCG', 'PBiCG', 'PBiCGStab'}, default='PBiCG')


# set up automated tests for CI/CD in github

# test for KeyData and Foam classes

key1 = KeyData('solver', prop1, prop2)
print(key1.giveVal())
head = Foam("test_head",None, None)

# head.appendDict(args)

child1 = Foam('test_child', head, None)
child2 = Foam('test_child2', child1, None, key1)
child3 = Foam('test_child3', child1, None, key1)


# Display tests

# print(head)
# showTree(head)
# print(RenderTree(child1).by_attr())


# Test for Keydata class singularily

# key1 = KeyData('solver', prop1)
# print(key1)

writeTo(head, 'testFile.txt')



