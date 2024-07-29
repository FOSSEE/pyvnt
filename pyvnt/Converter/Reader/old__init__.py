
import os
from pyvnt.DictionaryElement.foamDS import Foam
from .dictionaryFileIterator import DictionaryFileIterator
from .dictionaryFile import DictionaryFile


def read(filepath : str, verifyFile: bool = True) -> Foam:
  '''
  Reads dictionary file from the given filepath and returns a node tree 
  representation of it.
  '''  
  file = DictionaryFile(filepath, verifyFile)
  itr = DictionaryFileIterator(file)
  root = _createTree(file.filepath, itr)
  itr.close()
  file.close()

  return root


def _createTree(parentName: str, itr: DictionaryFileIterator) -> Foam:
  '''
  Recursively traverse the openfoam's dictionary data structure and create the
  node-tree structure.
  '''
  data = {}
  while itr.hasEntry():
    key = itr.getCurrentEntryKeyword()
    value = None

    if itr.isCurrentEntryDict():
      itr.stepIn()
      value = _createTree(key, itr)
      itr.stepOut()
    else:
      value = itr.getKeyData()

    data[key] = value
    itr.step()

  # create node
  children = [val for val in data.values() if isinstance(val,Foam)]
  
  for key in list(data.keys()):
    val = data[key]
    if isinstance(val,Foam):
      del data[key]

  node = Foam(parentName, children=children, *data.values())

  return node


