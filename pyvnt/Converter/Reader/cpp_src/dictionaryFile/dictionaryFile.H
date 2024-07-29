
#pragma once


class DictionaryFile
{
public:
  Foam::dictionary* mDictPtr;

  DictionaryFile(const char* filepath);
  ~DictionaryFile();
  // void* getIterator();
  // void printEntry(const char* key);
};

