

class InvalidDictionaryFileError(Exception):
  '''
  Invalid syntax in Dictionary File.
  '''
  def __init__(self, filepath: str, openfoamErrorMessage: str):
    self.filepath = filepath
    self.openfoamErrorMessage = openfoamErrorMessage

  def __str__(self):
    return f"Error occured while parsing the file : {self.filepath}\n {self.openfoamErrorMessage}"


class InvalidTraversalOperation(Exception):
  '''
  Generic Invalid Traversal Operation.
  '''
  def __init__(self, msg: str):
    self.msg = msg

  def __str__(self):
    return self.msg


class ClosedDictionaryFileError(Exception):
  '''
  Dictionary File closed.
  '''
  def __init__(self, filepath: str):
    self.filepath = filepath

  def __str__(self):
    return f"Cannot operate on a closed file : {self.filepath}"


class ClosedDictionaryFileIteratorError(Exception):
  '''
  DictionaryFileIterator closed.
  '''
  def __str__(self):
    return f"Cannot operate with a closed iterator"


class IteratorOutOfRange(Exception):
  '''
  DictionaryFileIterator is out of range.
  '''
  def __str__(self):
    return f"Iterator has moved beyond last entry in current dictionary"


class InvalidPrimitiveEntryOperation(Exception):
  '''
  Invalid operation for a primitive entry.
  '''
  def __str__(self):
    return f"Invalid operation for primitive entry"


class InvalidDictionaryEntryOperation(Exception):
  '''
  Invalid operation for a dictionary entry.
  '''
  def __str__(self):
    return "Invalid operation for dictionary entry"