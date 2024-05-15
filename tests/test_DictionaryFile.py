
import os
import unittest
import dictionarywrapper.exceptions as dwexception
from dictionarywrapper.dictionaryFile import DictionaryFile


DICT_FOLDER = os.path.join(os.path.dirname(__file__), 'dicts/')


class TestDictionaryFile(unittest.TestCase):

  def test_init_for_non_existing_file(self):
    filepath = ''
    with self.assertRaises(FileNotFoundError):
      DictionaryFile(filepath)

  def test_init_for_invalid_dictionary_file(self):
    filepath = os.path.join(DICT_FOLDER, 'invalidDict')
    with self.assertRaises(dwexception.InvalidDictionaryFileError):
      DictionaryFile(filepath)

  def test_init_for_warning_dictionary_file(self):
    filepath = os.path.join(DICT_FOLDER, 'warnDict')
    with self.assertRaises(dwexception.InvalidDictionaryFileError):
      DictionaryFile(filepath)

  def test_isOpen(self):
    filepath = os.path.join(DICT_FOLDER, 'simpleDict')
    file = DictionaryFile(filepath)
    self.assertIsInstance(file.isOpen(), bool)
    self.assertTrue(file.isOpen())
    file.close()
    self.assertIsInstance(file.isOpen(), bool)
    self.assertFalse(file.isOpen())

  def test_close(self):
    filepath = os.path.join(DICT_FOLDER, 'simpleDict')
    file = DictionaryFile(filepath)
    file.close()
    self.assertFalse(file.isOpen())
    with self.assertRaises(dwexception.ClosedDictionaryFileError):
      file.close()
    
  def test_getFilePointer(self):
    filepath = os.path.join(DICT_FOLDER, 'simpleDict')
    file = DictionaryFile(filepath)
    self.assertIsInstance(file.getFilePointer(), int)
    self.assertNotEqual(0, file.getFilePointer())
    file.close()
    with self.assertRaises(dwexception.ClosedDictionaryFileError):
      file.getFilePointer()

if __name__ == '__main__':
  unittest.main()