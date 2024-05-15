
import os
import subprocess as sp


EXECUTABLE_PATH = os.path.join(
  os.path.dirname(__file__),
  'cpp_src/dictionaryFileChecker/bin/dictionaryFileChecker'
)


def verifyDictionaryFile(filepath : str) -> tuple[bool, str]:
  '''
  Checks if the given file follows the syntax of OpenFOAM's dictionary files. 
  Uses the custom utility 'dictionaryFileChecker' in a subprocess. The call to
  this function is blocking as it waits for the subprocess to exit.
  '''
  args = (EXECUTABLE_PATH, filepath)
  res = sp.run(args, stdout=sp.PIPE, stderr=sp.STDOUT)
  isValid = (res.returncode == 0) and (len(res.stdout) == 0)
  output = str(res.stdout, encoding='ascii')
  return (isValid, output)
