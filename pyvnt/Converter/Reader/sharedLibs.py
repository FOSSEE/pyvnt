

import ctypes
import os


class DictionaryFileLib:
  _libFilePath = os.path.join(
    os.path.dirname(__file__),
    "cpp_src/dictionaryFile/lib/dictionaryFile.so"
  )
  _lib = ctypes.CDLL(_libFilePath)
  openDictionaryFile = _lib.openDictionaryFile
  closeDictionaryFile = _lib.closeDictionaryFile

#   _function_signature_dict = {
#     'openDictionaryFile' : (ctypes.c_char_p, ctypes.c_void_p),
#     'closeDictionaryFile' : (ctypes.c_void_p, None)
#   }


# _libs = [DictionaryFileLib]

# for lib in _libs:
#   func_names = [attr for attr in dir(lib) if not attr.startswith('_')]
#   print(func_names)
#   for func in func_names:
#     if func in lib._function_signature_dict:
#       argtypes, restype = lib._function_signature_dict[func]
#       lib.__dict__[func].argtypes = argtypes
#       lib.__dict__[func].restype = restype
      


DictionaryFileLib.openDictionaryFile.argtypes = [ctypes.c_char_p]
DictionaryFileLib.openDictionaryFile.restype = ctypes.c_void_p

DictionaryFileLib.closeDictionaryFile.argtypes = [ctypes.c_void_p]
DictionaryFileLib.closeDictionaryFile.restype = None



class DictionaryFileIteratorLib:
  _libFilePath = os.path.join(
    os.path.dirname(__file__),
    "cpp_src/dictionaryFileIterator/lib/dictionaryFileIterator.so"
  )
  _lib = ctypes.CDLL(_libFilePath)
  createIterator = _lib.createIterator
  deleteIterator = _lib.deleteIterator
  hasEntry = _lib.hasEntry
  step = _lib.step
  stepIn = _lib.stepIn
  stepOut = _lib.stepOut
  getCurrentEntryKeyword = _lib.getCurrentEntryKeyword
  isCurrentEntryDict = _lib.isCurrentEntryDict
  isCurrentEntryList = _lib.isCurrentEntryList
  getCurrentEntryValueCount = _lib.getCurrentEntryValueCount
  getCurrentEntryValueTypeAt = _lib.getCurrentEntryValueTypeAt
  getCurrentEntryValueAt_String = _lib.getCurrentEntryValueAt_String
  getCurrentEntryValueAt_Character = _lib.getCurrentEntryValueAt_Character
  getCurrentEntryValueAt_Integer = _lib.getCurrentEntryValueAt_Integer
  getCurrentEntryValueAt_Float = _lib.getCurrentEntryValueAt_Float
  getCurrentEntryValueAt_Double = _lib.getCurrentEntryValueAt_Double
  getCurrentEntryValueAt_LongDouble = _lib.getCurrentEntryValueAt_LongDouble


DictionaryFileIteratorLib.createIterator.argtypes = [ctypes.c_void_p]
DictionaryFileIteratorLib.createIterator.restype = ctypes.c_void_p

DictionaryFileIteratorLib.deleteIterator.argtypes = [ctypes.c_void_p]
DictionaryFileIteratorLib.deleteIterator.restype = None

DictionaryFileIteratorLib.hasEntry.argtypes = [ctypes.c_void_p]
DictionaryFileIteratorLib.hasEntry.restype = ctypes.c_bool

DictionaryFileIteratorLib.step.argtypes = [ctypes.c_void_p]
DictionaryFileIteratorLib.step.restype = ctypes.c_bool

DictionaryFileIteratorLib.stepIn.argtypes = [ctypes.c_void_p]
DictionaryFileIteratorLib.stepIn.restype = ctypes.c_bool

DictionaryFileIteratorLib.stepOut.argtypes = [ctypes.c_void_p]
DictionaryFileIteratorLib.stepOut.restype = ctypes.c_bool

DictionaryFileIteratorLib.getCurrentEntryKeyword.argtypes = [ctypes.c_void_p]
DictionaryFileIteratorLib.getCurrentEntryKeyword.restype = ctypes.c_char_p

DictionaryFileIteratorLib.isCurrentEntryDict.argtypes = [ctypes.c_void_p]
DictionaryFileIteratorLib.isCurrentEntryDict.restype = ctypes.c_bool

DictionaryFileIteratorLib.isCurrentEntryList.argtypes = [ctypes.c_void_p]
DictionaryFileIteratorLib.isCurrentEntryList.restype = ctypes.c_bool


DictionaryFileIteratorLib.getCurrentEntryValueCount.argtypes = [
  ctypes.c_void_p
]
DictionaryFileIteratorLib.getCurrentEntryValueCount.restype = ctypes.c_int


DictionaryFileIteratorLib.getCurrentEntryValueTypeAt.argtypes = [
  ctypes.c_void_p, 
  ctypes.c_int
]
DictionaryFileIteratorLib.getCurrentEntryValueTypeAt.restype = ctypes.c_int


DictionaryFileIteratorLib.getCurrentEntryValueAt_String.argtypes = [
  ctypes.c_void_p,
  ctypes.c_int
]
DictionaryFileIteratorLib.getCurrentEntryValueAt_String.restype \
  = ctypes.c_char_p


DictionaryFileIteratorLib.getCurrentEntryValueAt_Character.argtypes = [
  ctypes.c_void_p,
  ctypes.c_int
]
DictionaryFileIteratorLib.getCurrentEntryValueAt_Character.restype \
  = ctypes.c_char


DictionaryFileIteratorLib.getCurrentEntryValueAt_Integer.argtypes = [
  ctypes.c_void_p,
  ctypes.c_int
]
DictionaryFileIteratorLib.getCurrentEntryValueAt_Integer.restype \
  = ctypes.c_int


DictionaryFileIteratorLib.getCurrentEntryValueAt_Float.argtypes = [
  ctypes.c_void_p,
  ctypes.c_int
]
DictionaryFileIteratorLib.getCurrentEntryValueAt_Float.restype \
  = ctypes.c_float


DictionaryFileIteratorLib.getCurrentEntryValueAt_Double.argtypes = [
  ctypes.c_void_p,
  ctypes.c_int
]
DictionaryFileIteratorLib.getCurrentEntryValueAt_Double.restype \
  = ctypes.c_double


DictionaryFileIteratorLib.getCurrentEntryValueAt_LongDouble.argtypes = [
  ctypes.c_void_p,
  ctypes.c_int
]
DictionaryFileIteratorLib.getCurrentEntryValueAt_LongDouble.restype \
  = ctypes.c_longdouble
