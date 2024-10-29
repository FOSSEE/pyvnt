
extern "C"
{

enum ValueType{
  STRING = 0,
  INTEGER,
  FLOAT,
  DOUBLE,
  LONG_DOUBLE,
  PUNCTUATION,
  UNDEFINED,
};

void* createIterator(void* dictFilePtr);
void deleteIterator(void* dictFileItr);

bool hasEntry(void* dictFileItr);
bool step(void* dictFileItr);
bool stepIn(void* dictFileItr);
bool stepOut(void* dictFileItr);

const char* getCurrentEntryKeyword(void* dictFileItr);
bool isCurrentEntryDict(void* dictFileItr);
bool isCurrentEntryList(void* dictFileItr);
int getCurrentEntryValueCount(void* dictFileItr);
int getCurrentEntryValueTypeAt(void* dictFileItr, int index);

const char* getCurrentEntryValueAt_String(void* dictFileItr, int index);
char getCurrentEntryValueAt_Character(void* dictFileItr, int index);
int getCurrentEntryValueAt_Integer(void* dictFileItr, int index);
float getCurrentEntryValueAt_Float(void* dictFileItr, int index);
double getCurrentEntryValueAt_Double(void* dictFileItr, int index);
long double getCurrentEntryValueAt_LongDouble(void* dictFileItr, int index);

}