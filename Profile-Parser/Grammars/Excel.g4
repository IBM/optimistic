grammar Excel;

start: (constant | '=' formula | array_formula) EOF;

array_formula: '{' '=' formula '}';

formula:
	constant														# ConstantFormula
	| reference														# ReferenceFormula
	| function_call													# FunctionCall
	| op = ('+' | '-') formula										# UnaryOp
	| formula '%'													# Percent
	| formula op = '^' formula										# Expon
	| formula op = ('*' | '/') formula								# MultiplicativeOp
	| formula op = ('+' | '-') formula								# AdditiveOp
	| formula op = '&' formula										# Concat
	| formula op = ('<' | '>' | '<=' | '>=' | '=' | '<>') formula	# Comparison
	| '(' formula ')'												# ParenFormula
	| RESERVED_NAME													# ReservedName;

constant: INT | DECIMAL | STRING | BOOL | ERROR;

function_call: function '(' arguments ')';

arguments: formula? (',' formula?)*;

prefixed_function: FUNCTION_PREFIX function;

// ID may be too general
function: FUNCTION | ID | prefixed_function;

// add others
reference:
	reference_item            # SimpleRef
	// | CELL ':' CELL			  # Range
	| reference ':' reference # Range
	| '(' reference ')'		  # ParenRef
	| prefix reference_item	  # PrefixedRef;

reference_item:
	CELL									# CellRef
	| named_range							# NamedRange
	| REFERENCE_FUNCTION '(' arguments ')'	# RefFunction
	| VERTICAL_RANGE						# VertRange
	| HORIZONTAL_RANGE						# HorizRange
	| ERROR_REF								# ErrorRef;

// add others
prefix: FILE? SHEET | FILE '!';

// These allow a period as well?
named_range: ID;

INT: [0-9]+;

BOOL: 'TRUE' | 'FALSE';

CELL: '$'? [A-Za-z]+ '$'? INT;

HORIZONTAL_RANGE: '$'? [A-Za-z]+ ':' '$'? [A-Za-z]+;

VERTICAL_RANGE: '$'? INT ':' '$'? INT;

//COL: '$'? [A-Za-z]+; ROW: '$'? INT;

ERROR:
	'#' (
		'NULL!'
		| 'DIV/0!'
		| 'VALUE!'
		| 'NAME?'
		| 'NUM!'
		| 'N/A'
	);

ERROR_REF: '#REF!';

// add others
FUNCTION: 'SUM';

REFERENCE_FUNCTION: 'INDEX' | 'OFFSET' | 'INDIRECT';

FUNCTION_PREFIX: '_xlfn.' | '_xlws.';

// changed from paper
ID: [A-Za-z_][A-Za-z0-9_]+;

RESERVED_NAME: '_xlnm' [_A-Za-z]+;

FILE: '[' INT ']';

SHEET: (
		[0-9A-Za-z_.]+
		| '\'' ([0-9A-Za-z_ !@#$%^&*()+=|:;<>,./?\\"-] | '\'\'')+ '\''
	) '!';

DECIMAL: (INT? '.' INT | INT '.' INT?) ([Ee] INT)?;

STRING: '"' (~('\r' | '\n' | '"') | '""')* '"';

WS: [ \t\r\n] -> channel(HIDDEN);

