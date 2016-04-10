
// productions

void		expr( );
void		prog( );
void		stmt( );
void		stmt_list( );
void		var( );


// helper functions

void		emit( int );
void		error( int, int = 0, const string & = "" );
ifstream 	get_ifs( );
void		init_kws( );
void		match( int );
string		getRootPath();


// lexical analyzer

Token		lexan( );

