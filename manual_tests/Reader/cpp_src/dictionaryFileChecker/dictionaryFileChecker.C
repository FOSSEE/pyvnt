
#include "fileName.H"
#include "IFstream.H"
#include "dictionary.H"


Foam::dictionary* dictPtr = nullptr;


bool openDictionary(const char* filepath);
void closeDictionary();


int main(int argc, char* argv[]){

  if( argc != 2 ){
    return 1;
  }

  bool isOpen = openDictionary(argv[1]);
  closeDictionary();

  return (isOpen ? 0 : 1);
}


bool openDictionary(const char* filepath)
{
  if( dictPtr != nullptr )
  {
    closeDictionary();
  }

  Foam::fileName dictPath(filepath);
  Foam::IFstream dictFileStream(dictPath);

  if( dictFileStream.closed() or dictFileStream.bad() )
  {
    return false;
  }

  dictPtr = new Foam::dictionary(dictFileStream);
  return true;
}


void closeDictionary()
{
  if( dictPtr != nullptr )
  {
    delete dictPtr;
    dictPtr = nullptr;
  }
}