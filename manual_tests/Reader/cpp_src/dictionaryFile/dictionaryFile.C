
#include "fileName.H"
#include "IFstream.H"
#include "dictionary.H"

#include "dictionaryFile.H"
#include "dictionaryFile_PythonInterface.H"


DictionaryFile::DictionaryFile(const char* filepath)
{
  Foam::fileName dictPath(filepath);
  Foam::IFstream dictFileStream(dictPath);
  mDictPtr = new Foam::dictionary(dictFileStream);
}

DictionaryFile::~DictionaryFile()
{
  delete mDictPtr;
}

// void DictionaryFile::printEntry(const char* key)
// {
//   Foam::word keyname(key);
//   std::cout 
//     << "dictionaryName : " << mDictPtr->name().toAbsolute() << " "
//     << mDictPtr->lookupEntry(keyname, false, false).keyword() 
//     << std::endl;
// }

// API FUNCTIONS===============================================================
void* openDictionaryFile(const char* filepath)
{
  DictionaryFile* dictFile = new DictionaryFile(filepath);  
  return dictFile;
}

void closeDictionaryFile(void* dictionaryFile)
{
  DictionaryFile* dictFile = static_cast<DictionaryFile*>(dictionaryFile);
  delete dictFile;
}

// void printDictionary(void* dictionaryFile)
// {
//   DictionaryFile* dictFile = static_cast<DictionaryFile*>(dictionaryFile);
//   dictFile->printEntry("key1");
// }