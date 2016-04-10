#include    <iostream>
#include    <fstream>
#include    <cctype>
#include    "token.h"
#include    "functions.h"

extern ifstream ifs;                        // input file stream to read from
extern SymTab   symtab;                     // global symbol table
extern string outputFileName;

static int lineno = 1;                      // static var to remember line no.

bool isOperatorOrSymbol(int t) {
	const char symbs[] = { '+', '-', '=', ';'};
	for (char c : symbs) {
		if (c == t) return true;
	}
	return false;
}

Token lexan( )                              // lexical analyzer
{
    int     t;
    string  tokstr;

    while( 1 )
    {
        t = ifs.get( );                     // get next character

        if( t == '#' )                      // beginning of a comment
        {
            while( ifs.get( ) != '\n' )
            {                               // comment until \n
            }
        }
        else if( t == ' '  ||  t == '\t' )
        {                                   // discard white space
        }
        else if( t == '\n' )                // new line
        {
            ++lineno;
        }
        else if( isalpha( t ) || isOperatorOrSymbol(t))             // t is a letter
        {
            tokstr = "";                    // empty tokstr
            while( isalnum( t ) || isOperatorOrSymbol(t))           // while it is an alpha numeric char
            {
                tokstr.push_back( t );
                t = ifs.get( );             // get the next character
            }

            ifs.putback( t );               // went one char too far
			if (tokstr.length() > 1 && tokstr[tokstr.length() - 1] == ';') {
				ifs.putback(';');
				tokstr = tokstr.substr(0, tokstr.length() - 1);
			}

            int p = symtab.lookup( tokstr );

            if( p < 0 )
            {                               // add an "undefined ID" to symtab
                p = symtab.insert( tokstr, UID );
            }
            return Token( tokstr, symtab.toktype( p ), p, lineno );
        }
        else if( t == EOF )
        {
            return Token( "", DONE, 0, lineno );
        }
        else
        {
            tokstr.push_back( t );
            return Token( tokstr, t, NONE, lineno );
        }
    }
}


void init_kws( )                            // init keywords/ids in symtab
{
    symtab.insert( "begin", KW );
    symtab.insert( "end",   KW );
    symtab.insert( "A",     ID );
    symtab.insert( "B",     ID );
    symtab.insert( "C",     ID );
	symtab.insert( "+",		OP );
	symtab.insert( "-",		OP );
	symtab.insert( "=",  	AS );
	symtab.insert( ";",		SC );
}

string getRootPath() {
	string filePath = __FILE__;
	int length = filePath.length();
	for (int i = length - 1; i >= 0; i--) {
		if (filePath[i] == '\\') {
			return filePath.substr(0, i + 1);
		}
	}
	return filePath;
}

string generateOutputFileName(string &inputFileName) {
	int length = inputFileName.length();
	for (int i = length-1; i >= 0; i--) {
		if (inputFileName[i] == '-') {
			return "out" + inputFileName.substr(i, length-i);
		}
	}
	return "output.txt";
}

ifstream get_ifs( )                         // get input file stream
{
    string filename;                        // input file name

    cout << "Enter input file name: ";
    cin  >> filename;
	string fullPath = getRootPath() + filename;
	ifstream ifs(fullPath);

    if( ! ifs )                             // cannot open file infilen
    {
		throw domain_error("Cannot open input file: " + fullPath);
    }
	cout << "Successfully read input file: " + fullPath << endl << endl;
	outputFileName = generateOutputFileName(filename);
    return ifs;                             // return input file stream
}
