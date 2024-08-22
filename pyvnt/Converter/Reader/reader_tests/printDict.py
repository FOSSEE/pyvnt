
import os
import sys
from pyvnt import read, show_tree, writeTo


dictFilesFolder = os.path.join(os.path.dirname(__file__), 'dicts')
dictFile = os.path.join(dictFilesFolder, 'simpleDict')


if len(sys.argv) > 1:
  dictFile = os.path.join(dictFilesFolder, sys.argv[1])

tree = read(dictFile)

show_tree(tree)
writeTo(tree, 'reader_test')