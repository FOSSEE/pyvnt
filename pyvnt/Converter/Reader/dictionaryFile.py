
import os, errno

from . import fileUtils
from .sharedLibs import DictionaryFileLib
from .exceptions import (
  InvalidDictionaryFileError,
  ClosedDictionaryFileError,
)


class DictionaryFile:
  def __init__(self, filepath: str, verifyFile: bool = True):
    self.filepath = os.path.abspath(filepath)
  
    if not os.path.isfile(self.filepath):
      raise FileNotFoundError(
        errno.ENOENT, 
        os.strerror(errno.ENOENT), 
        self.filepath
      )

    if verifyFile:
      isValid, error = fileUtils.verifyDictionaryFile(self.filepath)
      if not isValid:
        raise InvalidDictionaryFileError(self.filepath, error)

    self.__codec = 'ascii'
    self.__fileptr = DictionaryFileLib.openDictionaryFile(
      bytes(self.filepath, self.__codec)
    )

  def close(self):
    '''
    Closes the file by deleting the C++ DictionaryFile object from memory.
    '''
    if self.__fileptr is None:
      raise ClosedDictionaryFileError(self.filepath)

    DictionaryFileLib.closeDictionaryFile(self.__fileptr)
    self.__fileptr = None

  def isOpen(self) -> bool:
    '''
    Check if file is open or not.
    '''
    return self.__fileptr is not None

  def getFilePointer(self) -> int:
    '''
    Get the pointer to C++ DictionaryFile object.
    '''
    if not self.isOpen():
      raise ClosedDictionaryFileError(self.filepath)
    return self.__fileptr

