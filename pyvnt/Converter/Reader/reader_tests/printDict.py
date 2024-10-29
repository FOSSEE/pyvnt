
import os
import sys
<<<<<<< HEAD
from pyvnt import read, show_tree, writeTo
=======
from pyvnt import read
>>>>>>> acb2eb0 (fixed merge conflict)


dictFilesFolder = os.path.join(os.path.dirname(__file__), 'dicts')
dictFile = os.path.join(dictFilesFolder, 'simpleDict')


if len(sys.argv) > 1:
  dictFile = os.path.join(dictFilesFolder, sys.argv[1])

<<<<<<< HEAD
tree = read(dictFile)

show_tree(tree)
writeTo(tree, 'reader_test')
=======
tree = dw.read(dictFile)
tree.dispTree()
>>>>>>> acb2eb0 (fixed merge conflict)
