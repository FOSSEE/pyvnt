# todo : tests for all methods for dictionaryFileIterator

import os
import unittest

from pyvnt import PropertyString, PropertyInt, PropertyFloat

import dictionarywrapper.exceptions as dwexception
from dictionarywrapper.dictionaryFileIterator import DictionaryFileIterator
from dictionarywrapper.dictionaryFile import DictionaryFile

DICT_FOLDER = os.path.join(os.path.dirname(__file__), 'dicts/')


class TestDictionaryFileIterator(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    filesToOpen = [
      'simpleDict',
      'emptyDict',
      'singlePrimitiveEntryDict',
      'twoPrimitiveEntryDict',
    ]
    cls.files = {}

    for file in filesToOpen:
      cls.files[file] = DictionaryFile(os.path.join(DICT_FOLDER, file))

  @classmethod
  def tearDownClass(cls):
    for file in cls.files.values():
      file.close()

  def test_init_on_closed_file(self):
    file = DictionaryFile(os.path.join(DICT_FOLDER, 'simpleDict'))
    file.close()
    with self.assertRaises(dwexception.ClosedDictionaryFileError):
      DictionaryFileIterator(file)

  def test_init_on_open_file(self):
    itr = DictionaryFileIterator(TestDictionaryFileIterator.files['simpleDict'])
    self.assertIsInstance(itr.file, DictionaryFile)
    self.assertIsInstance(itr._DictionaryFileIterator__iteratorPtr, int)
    self.assertNotEqual(itr._DictionaryFileIterator__iteratorPtr, 0)

  def test_private_checkValidity(self):
    # check for closed iterator
    itr1 = DictionaryFileIterator(TestDictionaryFileIterator.files['simpleDict'])
    itr1.close()
    with self.assertRaises(dwexception.ClosedDictionaryFileIteratorError):
      itr1._DictionaryFileIterator__checkValidity()

    # check for closed file
    file = DictionaryFile(os.path.join(DICT_FOLDER, 'simpleDict'))
    itr2 = DictionaryFileIterator(file)
    file.close()
    with self.assertRaises(dwexception.ClosedDictionaryFileError):
      itr2._DictionaryFileIterator__checkValidity()

    # check for valid case which is - open file and open iterator
    itr3 = DictionaryFileIterator(TestDictionaryFileIterator.files['simpleDict'])
    self.assertEqual(itr3._DictionaryFileIterator__checkValidity(), None)

  def test_isOpen(self):
    itr = DictionaryFileIterator(TestDictionaryFileIterator.files['simpleDict'])
    self.assertIsInstance(itr.isOpen(), bool)
    self.assertTrue(itr.isOpen())
    itr.close()
    self.assertIsInstance(itr.isOpen(), bool)
    self.assertFalse(itr.isOpen())

  def test_close(self):
    itr = DictionaryFileIterator(TestDictionaryFileIterator.files['simpleDict'])
    itr.close()
    self.assertFalse(itr.isOpen())
    with self.assertRaises(dwexception.ClosedDictionaryFileIteratorError):
      itr.close()

  def test_hasEntry(self):
    pass
    


if __name__ == '__main__':
  unittest.main()