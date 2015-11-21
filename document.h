#ifndef DOCUMENT_H
#define DOCUMENT_H

#include <string>
using namespace std;

class Document{

    string text;
    string filename;
    string directory;
    bool saved;

    public:

    Document(){
        filename = "Untitled.txt";
        saved = false;
    }

    string getFilename(){
        return filename;
    }

};

#endif // DOCUMENT_H
