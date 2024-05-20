
#pragma once


extern "C"
{

void* openDictionaryFile(const char* filepath);
void closeDictionaryFile(void* dictionaryFile);  
// void* getIterator(void* dictionaryFile);
// void printDictionary(void* dictionaryFile);
}


