#pragma once


typedef std::pair<Foam::dictionary*,Foam::dictionary::iterator> dictInfo;
const char* EMPTY_STRING =     "";
Foam::token UNDEFINED_TOKEN =  Foam::token::undefinedToken;


class DictionaryFileIterator
{
public:
  DictionaryFileIterator(DictionaryFile* dictPtr);
  ~DictionaryFileIterator();

  bool hasEntry();
  bool step();
  bool stepIn();
  bool stepOut();

  const char* getCurrentEntryKeyword();
  bool isCurrentEntryDict();
  bool isCurrentEntryList();
  int getCurrentEntryValueCount();
  int getCurrentEntryValueTypeAt(int index);

  const char* getCurrentEntryValueAt_String(int index);
  char getCurrentEntryValueAt_Character(int index);
  int getCurrentEntryValueAt_Integer(int index);
  float getCurrentEntryValueAt_Float(int index);
  double getCurrentEntryValueAt_Double(int index);
  long double getCurrentEntryValueAt_LongDouble(int index);

private:
  DictionaryFile*       mDictFilePtr;
  std::stack<dictInfo>  mDictStack;

  const Foam::token& getCurrentEntryTokenAt(int index);
};

