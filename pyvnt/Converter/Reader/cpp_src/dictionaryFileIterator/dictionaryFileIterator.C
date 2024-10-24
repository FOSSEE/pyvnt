
#include <stack>
#include <utility>

#include "fileName.H"
#include "IFstream.H"
#include "dictionary.H"
#include "token.H"

#include "dictionaryFile.H"
#include "dictionaryFileIterator.H"
#include "dictionaryFileIterator_PythonInterface.H"


inline DictionaryFileIterator* toDictionaryFileIteratorPtr(void* dictFileItr)
{
  return static_cast<DictionaryFileIterator*>(dictFileItr);
}

// ============================================================================
// Python Interface Functions
// ============================================================================
void* createIterator(void* dictFilePtr)
{
  DictionaryFile* dictFile = static_cast<DictionaryFile*>(dictFilePtr);
  DictionaryFileIterator* itr = new DictionaryFileIterator(dictFile);
  return itr;
}

void deleteIterator(void* dictFileItr)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr); 
  delete itr;
}

bool hasEntry(void* dictFileItr)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->hasEntry();
}

bool step(void* dictFileItr)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->step();
}

bool stepIn(void* dictFileItr)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->stepIn();
}

bool stepOut(void* dictFileItr)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->stepOut();
}

const char* getCurrentEntryKeyword(void* dictFileItr)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->getCurrentEntryKeyword();
}

bool isCurrentEntryDict(void* dictFileItr)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->isCurrentEntryDict();
}

bool isCurrentEntryList(void* dictFileItr)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->isCurrentEntryList();
}

int getCurrentEntryValueCount(void* dictFileItr)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->getCurrentEntryValueCount();
}

int getCurrentEntryValueTypeAt(void* dictFileItr, int index)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->getCurrentEntryValueTypeAt(index);
}

const char* getCurrentEntryValueAt_String(void* dictFileItr, int index)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->getCurrentEntryValueAt_String(index);
}

char getCurrentEntryValueAt_Character(void* dictFileItr, int index)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->getCurrentEntryValueAt_Character(index);
}

int getCurrentEntryValueAt_Integer(void* dictFileItr, int index)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->getCurrentEntryValueAt_Integer(index);
}

float getCurrentEntryValueAt_Float(void* dictFileItr, int index)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->getCurrentEntryValueAt_Float(index);
}

double getCurrentEntryValueAt_Double(void* dictFileItr, int index)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->getCurrentEntryValueAt_Double(index);
}

long double getCurrentEntryValueAt_LongDouble(void* dictFileItr, int index)
{
  DictionaryFileIterator* itr = toDictionaryFileIteratorPtr(dictFileItr);
  return itr->getCurrentEntryValueAt_LongDouble(index);
}




// ============================================================================
// DictionaryFileIterator Functions
// ============================================================================

DictionaryFileIterator::DictionaryFileIterator(DictionaryFile* dictFile)
{
  mDictFilePtr = dictFile;

  Foam::dictionary* dictPtr = dictFile->mDictPtr;
  mDictStack.push(std::make_pair(dictPtr, dictPtr->begin()));
}

DictionaryFileIterator::~DictionaryFileIterator()
{
  mDictFilePtr = nullptr;
}

const Foam::token& DictionaryFileIterator::getCurrentEntryTokenAt(int index)
{
  if( index < 0 or mDictStack.empty() )
    return UNDEFINED_TOKEN;

  dictInfo& top = mDictStack.top();
  Foam::dictionary* currDictPtr = top.first;
  Foam::dictionary::iterator& currIter = top.second;

  if( currIter == currDictPtr->end() )
    return UNDEFINED_TOKEN;

  if( currIter().isDict() )
    return UNDEFINED_TOKEN;

  if( index >= currIter().stream().size() )
    return UNDEFINED_TOKEN;

  Foam::tokenList& tokens = currIter().stream();
  return tokens[index];
}

bool DictionaryFileIterator::hasEntry()
{
  if( mDictStack.empty() )
    return false;

  dictInfo& top = mDictStack.top();
  Foam::dictionary* currDictPtr = top.first;
  Foam::dictionary::iterator& currIter = top.second;

  return (currIter != currDictPtr->end());
}

bool DictionaryFileIterator::step()
{
  if( mDictStack.empty() )
    return false;

  dictInfo& top = mDictStack.top();
  Foam::dictionary* currDictPtr = top.first;
  Foam::dictionary::iterator& currIter = top.second;

  if( currIter == currDictPtr->end() )
    return false;

  ++currIter;

  if( currIter == currDictPtr->end() )
    return false;

  return true;
}

bool DictionaryFileIterator::stepIn()
{
  if( mDictStack.empty() )
    return false;

  dictInfo& top = mDictStack.top();
  Foam::dictionary* currDictPtr = top.first;
  Foam::dictionary::iterator& currIter = top.second;

  if( currIter == currDictPtr->end() )
    return false;

  if( not currIter().isDict() )
    return false;

  Foam::dictionary* subDictPtr = currDictPtr->subDictPtr(currIter().keyword());
  mDictStack.push(std::make_pair(subDictPtr, subDictPtr->begin()));
  return true;
}

bool DictionaryFileIterator::stepOut()
{
  if( mDictStack.empty() )
    return false;

  // to disallow stepping out of root dictionary.
  if( mDictStack.size() == 1 )
    return false;

  mDictStack.pop();

  return true;
}

const char* DictionaryFileIterator::getCurrentEntryKeyword()
{
  if( mDictStack.empty() )
    return EMPTY_STRING;

  dictInfo& top = mDictStack.top();
  Foam::dictionary* currDictPtr = top.first;
  Foam::dictionary::iterator& currIter = top.second;

  if( currIter == currDictPtr->end() )
    return EMPTY_STRING;

  return currIter().keyword().c_str();
}

bool DictionaryFileIterator::isCurrentEntryDict()
{
  if( mDictStack.empty() )
    return false;

  dictInfo& top = mDictStack.top();
  Foam::dictionary* currDictPtr = top.first;
  Foam::dictionary::iterator& currIter = top.second;

  if( currIter == currDictPtr->end() )
    return false;

  return currIter().isDict();
}

bool DictionaryFileIterator::isCurrentEntryList()
{
  if( mDictStack.empty() )
    return false;

  dictInfo& top = mDictStack.top();
  Foam::dictionary* currDictPtr = top.first;
  Foam::dictionary::iterator& currIter = top.second;

  if( currIter == currDictPtr->end() )
    return false;

  return currIter().isDict();
}

int DictionaryFileIterator::getCurrentEntryValueCount()
{
  if( mDictStack.empty() )
    return 0;

  dictInfo& top = mDictStack.top();
  Foam::dictionary* currDictPtr = top.first;
  Foam::dictionary::iterator& currIter = top.second;

  if( currIter == currDictPtr->end() )
    return 0;

  if( currIter().isDict() )
    return 0;

  return currIter().stream().size();
}

int DictionaryFileIterator::getCurrentEntryValueTypeAt(int index)
{
  const Foam::token& tkn = getCurrentEntryTokenAt(index);
  int type = UNDEFINED;

  switch( tkn.type() )
  {
    case Foam::token::tokenType::WORD:
      type = STRING;
      break;

    case Foam::token::tokenType::STRING:
      type = STRING;
      break;
 
    case Foam::token::tokenType::VERBATIMSTRING:
      type = STRING;
      break;

    case Foam::token::tokenType::FUNCTIONNAME:
      type = STRING;
      break;

    case Foam::token::tokenType::VARIABLE:
      type = STRING;
      break;

    case Foam::token::tokenType::LABEL:
      type = INTEGER;
      break;

    case Foam::token::tokenType::FLOAT_SCALAR:
      type = FLOAT;
      break;

    case Foam::token::tokenType::DOUBLE_SCALAR:
      type = DOUBLE;
      break;

    case Foam::token::tokenType::LONG_DOUBLE_SCALAR:
      type = LONG_DOUBLE;
      break;

    case Foam::token::tokenType::PUNCTUATION:
      type = PUNCTUATION;
      break;

    case Foam::token::tokenType::UNDEFINED:
      type = UNDEFINED;
      break;

    case Foam::token::tokenType::ERROR:
      type = UNDEFINED;
      break;

    case Foam::token::tokenType::COMPOUND:
      type = UNDEFINED;
      break;
  }

  return type;
}

const char* DictionaryFileIterator::getCurrentEntryValueAt_String(int index)
{
  const Foam::token& tkn = getCurrentEntryTokenAt(index);
  return tkn.anyStringToken().c_str();
}

char DictionaryFileIterator::getCurrentEntryValueAt_Character(int index)
{
  const Foam::token& tkn = getCurrentEntryTokenAt(index);
  return tkn.pToken();
}

int DictionaryFileIterator::getCurrentEntryValueAt_Integer(int index)
{
  const Foam::token& tkn = getCurrentEntryTokenAt(index);
  return tkn.labelToken();
}

float DictionaryFileIterator::getCurrentEntryValueAt_Float(int index)
{
  const Foam::token& tkn = getCurrentEntryTokenAt(index);
  return tkn.floatScalarToken();
}

double DictionaryFileIterator::getCurrentEntryValueAt_Double(int index)
{
  const Foam::token& tkn = getCurrentEntryTokenAt(index);
  return tkn.doubleScalarToken();
}

long double DictionaryFileIterator::getCurrentEntryValueAt_LongDouble(int index)
{
  const Foam::token& tkn = getCurrentEntryTokenAt(index);
  return tkn.doubleScalarToken();
}

