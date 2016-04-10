/*

    prog        ->  begin stmt_list end

    stmt_list   ->  stmt ; stmt_list
                 |  stmt
				 |	stmt;

    stmt        ->  var = expr

    var         ->  A | B | C

    expr        ->  var + expr
                 |  var - expr
                 |  var

*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stack>
#include "token.h"
#include "functions.h"


using namespace std;

ifstream ifs;                   // input file stream used by lexan
string outputFileName;
SymTab   symtab;                // global symbol table
Token    token;                 // global token
int      lookahead = 0;         // no look ahead token yet

int      dbg = 1;               // debug is ON





// your methods...
bool isSpace(char c) {
	return c == ' ' || c == '\t';
}

string inToPostFix(const string &infix) {
	/*Converts an infix expression to a postfix expression,
	e.g. A + B => AB+
	*/
	string postfix = "";
	stack<char> opstack;
	for (char c : infix) {
		if (isSpace(c)) {
			continue;
		}
		else if (c > 64) {
			postfix.push_back(c);
			postfix.push_back(' ');
		}
		else if (opstack.size()<2) {
			opstack.push(c);
		}
		else {
			postfix.push_back(opstack.top());
			postfix.push_back(' ');
			opstack.pop();
			opstack.push(c);
		}
	}
	while (!opstack.empty()) {
		postfix.push_back(opstack.top());
		postfix.push_back(' ');
		opstack.pop();
	}
	return postfix;
}

int waitForKey(int returnCode) {
	/*Helper function to leave console window open. Must press key AND hit enter.*/
	cout << "Enter any value to continue..." << endl;
	int x;
	cin >> x;
	return returnCode;
}


bool isValid(int validType) {
	return lookahead == validType;
}

string _getNextItem(int id, string errorString) {
	/*Returns the current token's tokstr and loads the next token*/
	string tokenString = token.tokstr();
	if (isValid(id)) {
		match(lookahead);
		return tokenString;
	}
	else {
		match(lookahead);
		throw domain_error(errorString + tokenString);
	}
}

bool endOfProgram() {
	return isValid(KW) && token.tokstr() == "end";
}

bool endOfStatement() {
	return isValid(SC) || endOfProgram();
}

string getNextKeyword() {
	return _getNextItem(KW, "Invalid keyword: ");
}

string As() {
	return _getNextItem(AS, "Invalid assignment operator: ");
}

string Op() {
	return _getNextItem(OP, "Invalid operator: ");
}

string Sc() {
	/*Handles the parsing of semicolons.*/
	string tokstring = token.tokstr();
	if (isValid(SC)) {
		match(lookahead);
		if (endOfProgram()) {
			throw domain_error("Invalid keyword: " + tokstring);
		}
		return tokstring;
	}
	else if (isValid(KW) || isValid(ID)) {
		return "";
	}
	else {
		throw domain_error("Invalid semicolon: " + tokstring);
	}
}

string Var() {
	return _getNextItem(ID, "Invalid variable: ");
}

string Expr() {
	string v = Var(), o = "", e = "";
	if (!endOfStatement()) {
		o = Op();
		e = Expr();
	}
	return v + o + e;
}

string Statement() {
	string v = Var();
	string assign = As();
	string expr = Expr();
	string sc = Sc();
	return inToPostFix(v + assign + expr) + sc;
}

vector<string> StatementList() {
	vector<string> result;
	while (!isValid(KW)) {
		result.push_back(Statement());
	}
	return result;
}

void run(string begin, vector<string> statements, string end) {
	/*
	Simulates 'running' the program after it has been compiled correctly.
	All this does is write to the output file.
	*/

	string fullPath = getRootPath() + outputFileName;
	ofstream os(fullPath);
	if (os.is_open()) {
		os << begin << endl;
		cout << begin << endl;
		for (string statement : statements) {
			os << statement << endl;
			cout << statement << endl;
		}
		os << end << endl;
		cout << end << endl << endl;
		os.close();
		cout << "Saved output to " + fullPath << endl;
	}
	else {
		throw domain_error("Cannot open output file: " + fullPath);
	}
}

void prog() {
	/* Parses the program file and "runs" it by generating an output file. */
	match(lookahead);
	string begin = getNextKeyword();
	vector<string> statements = StatementList();
	string end = getNextKeyword();
	run(begin, statements, end);
}


// utility methods
void emit( int t )
{
    switch( t )
    {
        case '+': case '-': case '=':
            cout << char( t ) << ' ';
            break;

        case ';':
            cout << ";\n";
            break;

        case '\n':
            cout << "\n";
            break;

        case ID:
        case KW:
        case UID:
            cout << symtab.tokstr( token.tokvalue( ) ) << ' ';
            break;

        default:
            cout << "'token " << t << ", tokvalue "
                 << token.tokvalue( ) << "' ";
            break;
    }
}

void error( int t, int expt, const string &str )
{
    cerr << "\nunexpected token '";
    if( lookahead == DONE )
    {
        cerr << "EOF";
    }
    else
    {
        cerr << token.tokstr( );
    }
    cerr << "' of type " << lookahead;

    switch( expt )
    {
        case 0:         // default value; nothing to do
            break;

        case ID:
            cout << " while looking for an ID";
            break;

        case KW:
            cout << " while looking for KW '" << str << "'";
            break;

        default:
            cout << " while looking for '" << char( expt ) << "'";
            break;
    }

    cerr << "\nsyntax error.\n";

    exit( waitForKey(1) );
}


void match( int t )
{
    if( lookahead == t )
    {
        token = lexan( );
		lookahead = token.toktype( );   // lookahead contains the tok type
    }
    else
    {
        error( t );
    }
}

int main()
{
	try {
		ifs = get_ifs();
		init_kws();
		prog();
		return waitForKey(0);
	}
	catch (domain_error &e) {
		cout << e.what() << endl;
		return waitForKey(-1);
	}
}
