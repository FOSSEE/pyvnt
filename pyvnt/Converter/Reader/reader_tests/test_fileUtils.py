
import os
import unittest
import dictionarywrapper.fileUtils as fileUtils

DICT_FOLDER = os.path.join(os.path.dirname(__file__), 'dicts/')


class TestFileUtils(unittest.TestCase):

  def test_invalid_dictionary_file(self):
    filepath = os.path.join(DICT_FOLDER, 'invalidDict')
    res = fileUtils.verifyDictionaryFile(filepath)
    self.assertIsInstance(res, tuple)
    isValid, error = res
    self.assertIsInstance(isValid, bool)
    self.assertFalse(isValid)
    self.assertIsInstance(error, str)
    self.assertNotEqual(len(error), 0)

  def test_warning_dictionary_file(self):
    filepath = os.path.join(DICT_FOLDER, 'warnDict')
    res = fileUtils.verifyDictionaryFile(filepath)
    self.assertIsInstance(res, tuple)
    isValid, error = res
    self.assertIsInstance(isValid, bool)
    self.assertFalse(isValid)
    self.assertIsInstance(error, str)
    self.assertNotEqual(len(error), 0)

  def test_valid_dictionary_file(self):
    filepath = os.path.join(DICT_FOLDER, 'simpleDict')
    res = fileUtils.verifyDictionaryFile(filepath)
    self.assertIsInstance(res, tuple)
    isValid, error = res
    self.assertIsInstance(isValid, bool)
    self.assertTrue(isValid)
    self.assertIsInstance(error, str)
    self.assertEqual(len(error), 0)


if __name__ == '__main__':
  unittest.main()