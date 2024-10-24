
from enum import Enum
from pyvnt import (
  Key_C, 
  Int_P, 
  Flt_P, 
  Str_P, 
  Enm_P,
  Dim_Set_P,
  List_CP,
  Value_P
)

from .exceptions import (
  InvalidTraversalOperation,
  ClosedDictionaryFileError,
  ClosedDictionaryFileIteratorError,
  IteratorOutOfRange,
  InvalidPrimitiveEntryOperation,
  InvalidDictionaryEntryOperation,
)
from .sharedLibs import DictionaryFileIteratorLib
from .dictionaryFile import DictionaryFile


INT_MIN = -99999999
INT_MAX =  99999999
CODEC = 'ascii'


class ValueType(Enum):
  STRING = 0
  INTEGER = 1
  FLOAT = 2
  DOUBLE = 3
  LONG_DOUBLE = 4
  PUNCTUATION = 5
  UNDEFINED = 6


class DictionaryFileIterator:
  '''
  A uni-directional, read-only iterator to recursively traverse the OpenFOAM's
  dictionary structure. It traverses the structure entry by entry. Dictionary 
  entries can be stepped in and stepped out of and primitive entries(non 
  dictionary entries) can be read.
  '''
  def __init__(self, file: DictionaryFile):
    self.file = file
    if not file.isOpen():
      raise ClosedDictionaryFileError(self.file.filepath)
    self.__iteratorPtr = DictionaryFileIteratorLib.createIterator(
      self.file.getFilePointer()
    )

  def __checkValidity(self):
    '''
    Checks if the iterator and file are open or not.
    '''
    if not self.file.isOpen():
      raise ClosedDictionaryFileError(self.file.filepath)
    if not self.isOpen():
      raise ClosedDictionaryFileIteratorError

  def close(self):
    '''
    Closes the iterator.
    '''
    if self.__iteratorPtr is None:
      raise ClosedDictionaryFileIteratorError
    DictionaryFileIteratorLib.deleteIterator(self.__iteratorPtr)
    self.__iteratorPtr = None

  def isOpen(self) -> bool:
    '''
    Checks if iterator is open or not.
    '''
    return self.__iteratorPtr is not None

  def hasEntry(self) -> bool:
    '''
    Checks if the iterator is currently pointing to an entry or not.
    '''
    self.__checkValidity()
    return DictionaryFileIteratorLib.hasEntry(self.__iteratorPtr)

  def step(self):
    '''
    Moves the iterator to the next entry in current dictionary. For the last 
    entry in a dictionary moves the iterator out of range.
    Raises an error if called when iterator is out of range.
    '''
    self.__checkValidity()
    if not self.hasEntry():
      raise IteratorOutOfRange
    DictionaryFileIteratorLib.step(self.__iteratorPtr)

  def stepIn(self):
    '''
    Steps into a dictionary entry and moves the iterator to first entry in it.
    Raises an error if iterator is out of range.
    Raises an error if current entry is not a dictionary entry.
    '''
    self.__checkValidity()
    if not self.hasEntry():
      raise IteratorOutOfRange

    if not self.isCurrentEntryDict():
      raise InvalidPrimitiveEntryOperation

    DictionaryFileIteratorLib.stepIn(self.__iteratorPtr)

  def stepOut(self):
    '''
    Steps out from current dictionary and moves the iterator to the entry in 
    parent dictionary from where step in occured.
    Raises an error when stepping out of root dictionary.
    '''
    self.__checkValidity()
    stepOutOccured = DictionaryFileIteratorLib.stepOut(self.__iteratorPtr)

    if not stepOutOccured:
      raise InvalidTraversalOperation(
        'Cannot step out of root dictionary.'
      )

  def getCurrentEntryKeyword(self) -> str:
    '''
    Returns a string representing the name of the key of current entry.
    Raises an error if the iterator is out of range.
    '''
    self.__checkValidity()

    if not self.hasEntry():
      raise IteratorOutOfRange

    keyword = str(
      DictionaryFileIteratorLib.getCurrentEntryKeyword(self.__iteratorPtr), 
      CODEC
    )

    return keyword

  def isCurrentEntryDict(self) -> bool:
    '''
    Checks if current entry is a 'dictionary entry' or a 'primitive entry(non 
    dictionary entry).'
    Raises an error if iterator is out of range.
    '''
    self.__checkValidity()

    if not self.hasEntry():
      raise IteratorOutOfRange

    return DictionaryFileIteratorLib.isCurrentEntryDict(self.__iteratorPtr)
  
  def isCurrentEntryList(self) -> bool:
    '''
    Checks if current entry is a 'list entry' or a 'primitive entry(non 
    dictionary entry).'
    Raises an error if iterator is out of range.
    '''
    self.__checkValidity()

    if not self.hasEntry():
      raise IteratorOutOfRange

    return DictionaryFileIteratorLib.isCurrentEntryList(self.__iteratorPtr)

  def getValues(self) -> list[Value_P]:
    '''
    Returns a list of 'Value_P' objects for the values in current entry.
    Raises an error if iterator is out of range.
    Raises an error if current entry is not primitive entry.
    '''
    self.__checkValidity()

    if not self.hasEntry():
      raise IteratorOutOfRange

    if self.isCurrentEntryDict():
      raise InvalidDictionaryEntryOperation

    stack = [[]]

    for index in range(self.__getCurrentEntryValueCount()):
      val = self.__getValueAt(index)
      if val == '(' or val == '[':
        stack.append([])
      elif val == ')':
        popped = stack.pop()
        prop = List_CP(f'val{index+1}', elems=[popped])
        stack[-1].append(prop)
      elif val == ']':
        popped = tuple(stack.pop())
        prop = Dim_Set_P(f'val{index+1}', popped)
        stack[-1].append(prop)
      # elif val == '{':
      #   stack.append([]) # TODO: Figure out to iterate thtough dictionaries nested inside a list
      # elif val == '}':
      #   popped = tuple(stack.pop())
      #   prop = Enm_P(f'val{index+1}', popped)
      #   stack[-1].append(prop)
      elif val == ',':
        pass
      else:
        prop = self.__getValuePropertyAt(index)
        stack[-1].append(prop)
    # print(stack)

    return stack[0]

  def getRawValues(self) -> list:
    '''
    Return list of raw python objects for the values in current entry.
    '''
    self.__checkValidity()
    return [val.giveVal() for val in self.getValues()]

  def getKeyData(self) -> Key_C:
    '''
    Returns 'Key_C' object for the current entry.
    Raises an error if iterator is out of range.
    Raises an error if current entry is not primitive entry.
    '''
    self.__checkValidity()

    if not self.hasEntry():
      raise IteratorOutOfRange

    if self.isCurrentEntryDict():
      raise InvalidDictionaryEntryOperation

    key = self.getCurrentEntryKeyword()
    values = self.getValues()
    
    # print(f"key: {key}, values: {values}")
    return Key_C(key, *values)

  def __getCurrentEntryValueCount(self) -> int:
    '''
    Returns the number of value tokens in the current entry. The tokens also
    includes characters like comma(,) and brackets((),[]).
    '''
    return DictionaryFileIteratorLib.getCurrentEntryValueCount(self.__iteratorPtr)

  def __getCurrentEntryValueTypeAt(self, index: int) -> ValueType:
    '''
    Returns the ValueType of token at a given index in values of an entry.
    '''
    valType = ValueType(
      DictionaryFileIteratorLib.getCurrentEntryValueTypeAt(
        self.__iteratorPtr, 
        index
      )
    )
    return valType

  def __getCurrentEntryValueAt_String(self, index : int) -> str:
    '''
    Get token at given index as a 'str'. 
    The ValueType of this token should be of type 'str'.
    '''
    val = DictionaryFileIteratorLib.getCurrentEntryValueAt_String(
      self.__iteratorPtr, 
      index
    )

    return str(val, CODEC)

  def __getCurrentEntryValueAt_Character(self, index : int) -> str:
    '''
    Get token at given index as a 'character'. 
    The ValueType of this token should be of type 'character'.
    '''
    val = DictionaryFileIteratorLib.getCurrentEntryValueAt_Character(
      self.__iteratorPtr, 
      index
    )
    return str(val, CODEC)

  def __getCurrentEntryValueAt_Integer(self, index : int) -> int:
    '''
    Get token at given index as a 'integer'. 
    The ValueType of this token should be of type 'integer'
    '''
    return DictionaryFileIteratorLib.getCurrentEntryValueAt_Integer(
      self.__iteratorPtr,
      index
    )

  def __getCurrentEntryValueAt_Float(self, index : int) -> float:
    '''
    Get token at given index as a 'float'. 
    The ValueType of this token should be of type 'float'
    '''
    return DictionaryFileIteratorLib.getCurrentEntryValueAt_Float(
      self.__iteratorPtr,
      index
    )

  def __getCurrentEntryValueAt_Double(self, index : int) -> float:
    '''
    Get token at given index as a 'float'. 
    The ValueType of this token should be of type 'float'
    '''
    return DictionaryFileIteratorLib.getCurrentEntryValueAt_Double(
      self.__iteratorPtr,
      index
    )

  def __getCurrentEntryValueAt_LongDouble(self, index : int) -> float:
    '''
    Get token at given index as a 'float'. 
    The ValueType of this token should be of type 'float'
    '''
    return DictionaryFileIteratorLib.getCurrentEntryValueAt_LongDouble(
      self.__iteratorPtr,
      index
    )

  def __getValueAt(self, index : int, valType: ValueType = None):
    '''
    Returns a python object for value at the given index.
    '''
    if valType is None:
      valType = self.__getCurrentEntryValueTypeAt(index)
    value = None

    if valType == ValueType.STRING:
      value = self.__getCurrentEntryValueAt_String(index)
    elif valType == ValueType.PUNCTUATION:
      value = self.__getCurrentEntryValueAt_Character(index)
      # print(f"Punctuation 1 here: {value}")
    elif valType == ValueType.INTEGER:
      value = self.__getCurrentEntryValueAt_Integer(index)
    elif valType == ValueType.FLOAT:
      value = self.__getCurrentEntryValueAt_Float(index)
    elif valType == ValueType.DOUBLE:
      value = self.__getCurrentEntryValueAt_Double(index)
    elif valType == ValueType.LONG_DOUBLE:
      value = self.__getCurrentEntryValueAt_LongDouble(index)
    
    # print(value)

    return value

  def __getValuePropertyAt(self, index : int) -> Value_P:
    '''
    Returns a Value_P object for value at the given index.
    '''
    valType = self.__getCurrentEntryValueTypeAt(index)
    val = self.__getValueAt(index, valType)

    if valType == ValueType.INTEGER:
      return Int_P(f'val{index+1}', val, INT_MIN, INT_MAX)

    if valType == ValueType.FLOAT or \
        valType == ValueType.DOUBLE or \
        valType == ValueType.LONG_DOUBLE:
      return Flt_P(f'val{index+1}', val, float('-inf'), float('inf'))

    if valType == ValueType.STRING:
      return Enm_P(f'val{index+1}', {val}, val)

    return Str_P(f'val{index+1}', 'Invalid')
