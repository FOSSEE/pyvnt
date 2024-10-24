
import os
from pyvnt.Container.node import Node_C
from .dictionaryFileIterator import DictionaryFileIterator
from .dictionaryFile import DictionaryFile


def read(filepath : str, verifyFile: bool = True) -> Node_C:
  '''
  Reads dictionary file from the given filepath and returns a node tree 
  representation of it.
  '''  
  file = DictionaryFile(filepath, verifyFile)
  itr = DictionaryFileIterator(file)

  path = file.filepath

  root_name = path.split('/')[-1]
  # print(root_name)

  root = _createTree(root_name, itr)
  itr.close()
  file.close()

  return root


def _createTree(parentName: str, itr: DictionaryFileIterator) -> Node_C:
  '''
  Recursively traverse the openfoam's dictionary data structure and create the
  node-tree structure.
  '''
  data = {}
  while itr.hasEntry():
    key = itr.getCurrentEntryKeyword()
    value = None

    # print(f"{key}, {itr.isCurrentEntryList()}")

    if itr.isCurrentEntryDict():
      # print(key)
      itr.stepIn()
      value = _createTree(key, itr)
      itr.stepOut()
    else:
      value = itr.getKeyData()
      # print(value)

    print(key)
    # print(f"{key}, {type(value)}")
    data[key] = value
    itr.step()

  # create node
  children = [] 
  itms = []

  for key, val in data.items():
    if isinstance(val,Node_C):
      children.append(val)
    else:
      itms.append(val)

  node = Node_C(parentName, None, children, *itms)

  return node


