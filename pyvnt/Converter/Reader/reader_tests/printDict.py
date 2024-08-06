
import os
import sys
from pyvnt import read


dictFilesFolder = os.path.join(os.path.dirname(__file__), 'dicts')
dictFile = os.path.join(dictFilesFolder, 'simpleDict')


if len(sys.argv) > 1:
  dictFile = os.path.join(dictFilesFolder, sys.argv[1])

tree = dw.read(dictFile)
tree.dispTree()