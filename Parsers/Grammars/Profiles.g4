grammar Profiles;

//@header { package com.ibm.hrl.eco.abstractions; }

profile: condition EOF;

condition:
	condition ','? 'and' condition												# Conjunction
	| condition ','? 'or' condition												# Disjunction
	| expr to_be negate = 'not'? ('equal' 'to')? atomic_expr					# IsConstant
	| expr predicate expr														# PredicateAppl
	| expr unary_predicate														# UnaryPredAppl
	| expr comparison_operator expr												# Comparison
	| expr temporal_operator expr 'in' expr										# TemporalOp
	| value = expr to_be 'between' lower_bound = expr 'and' upper_bound = expr	# Between
	| expr to_be negate = 'not'? 'in' general_set								# In
	| 'not' condition															# Negation
	| existential																# ExistentialCond
	| universal																	# UniversalCond
	| binding_existential_with_diff												# BindingExistentialWithDiff
	| binding_existential_with_unique											# BindingExistentialWithUnique
	| binding_existential_unique												# BindingExistentialUnique
	| '(' condition ')'															# ParenCond;

/** FIXME: should be verb_phrase */
predicate:
	phrase												# AtomicPred
	| '(' phrase (',' phrase)* (','? 'and' phrase) ')'	# ConjunctivePred
	| '(' phrase (',' phrase)* (','? 'or' phrase) ')'	# DisjunctivePred;

// removed more specific art = ('a' | 'an') WORD+
unary_predicate: to_be negate = 'not'? phrase;

function:
	// Note: doesn't capture unary functions, these will become attributes
	function_name ('of' | 'between') expr (
		(',' expr)* ( ','? 'and' expr)
	) # FunctionApp
	//	| unary_function_name 'of' expr	# UnaryFunctionApp
	| PERCENT 'of' expr # PercentOf;

function_name:
	'the'? op = (
		'intersection'
		| 'union'
		| 'sum'
		| 'product'
		| 'difference'
		| 'quotient'
	);

existential:
	'there' to_be (diff = 'different' | article)? type_name VARIABLE (
		( ',' | 'and') VARIABLE
	)* ('in' expr)? such_that?;

binding_existential_with_diff:
	expr 'has' (
		(diff = 'different'? | article?) type_name mvars += VARIABLE (
			( ',' | 'and') mvars += VARIABLE
		)* such_that
	);

binding_existential_with_unique:
	binding_existential_with_unique1 (
		'and' binding_existential_with_unique1
	)* such_that;

binding_existential_with_unique1:
	expr 'has' unique = 'one'? type_name VARIABLE;

binding_existential_unique: expr 'has' 'one' type_name VARIABLE;

universal:
	'for' ('all' | 'each') (diff = 'different' | article)? type_name? VARIABLE (
		( ',' | 'and') VARIABLE
	)* ('in' expr)? such_that? ',' condition # ForAll
	| 'every' type_name VARIABLE (
		'of' of_expr = expr
		| 'in' in_set = general_set
	) 'is' predicate (','? 'and' condition)? # Every;

aggregate:
	article? op = ('sum' | 'product') 'of' term = expr 'for' 'all' type_name v = VARIABLE 'in'
		collection = expr such_that?;

such_that: 'such' 'that' condition;

attribute:
	'(' (cnp = conjunction_of_np | dnp = disjunction_of_np) ')' 'of' expr	# MultipleAttributes
	| noun_phrase 'of' expr													# SingleAttribute;

to_be: 'is' | 'are';

comparison_operator:
	to_be negate = ('not' | 'no')? (
		(gr = greater | sm = smaller) 'than' (
			'or' or_eq = 'equal' 'to'
		)?
	)											# ComparisonOp1
	| to_be 'at' (gr = 'least' | sm = 'most')	# ComparisonOp2
	| eq_not_eq									# ComparisonOp3
	| to_be 'different' 'from'					# ComparisonOp4;

eq_not_eq: to_be negate = 'not'? 'equal' 'to';

temporal_operator:
	(immed = 'immediately'? order = ( 'precedes' | 'follows'))	# TemporalOrder
	| 'overlaps'												# TemporalOverlap
	| to_be 'disjoint' 'with'									# TemporalDisjoint;

greater: 'greater' | 'more';

smaller: 'smaller' | 'less';

quantity: NUMBER;

general_set: '{' expr ( ',' expr)* '}';

conjunction_of_np:
	noun_phrase (',' noun_phrase)* (','? 'and' noun_phrase);

disjunction_of_np:
	noun_phrase (',' noun_phrase)* (','? 'or' noun_phrase);

//list_of_expr: expr | expr ( ',' expr)* ( ','? 'and' expr);

expr:
	function			# FunctionExpr
	| attribute			# AttributeExpr
	| expr 'and' expr	# ConjunctionExpr
	| expr 'or' expr	# DisjunctionExpr
	| noun_phrase		# PhraseExpr
	| aggregate			# AggregateExpr
	| atomic_expr		# AtomicExpr
	| general_set		# SetExpr
	| '(' expr ')'		# ParenExpr;

atomic_expr:
	quantity	# QuantityExpr
	| STRING	# StringExpr
	| VARIABLE	# VariableExpr
	| TIME		# TimeExpr
	| period	# PeriodExpr;

period: TIME '-' TIME;

phrase: noun_phrase | verb_phrase;

noun_phrase: article? WORD+;

/** FIXME: Will never be recognized, overridden by noun_phrase, need lists of nouns/verbs */
verb_phrase: WORD+;

type_name: article? WORD;

article: 'the' | 'a' | 'an';

VARIABLE: LETTER ( LETTER | DIGIT)* DIGIT ( LETTER | DIGIT)*;

fragment DIGIT: [0-9];

fragment LETTER: [a-zA-Z];

NUMBER: DIGIT+ ( '.' DIGIT*)?;

PERCENT: NUMBER '%';

TIME:
	DIGIT DIGIT? ':' DIGIT DIGIT (':' DIGIT DIGIT ( '.' DIGIT+))?;

WORD: [a-zA-Z'\-]+;

STRING: '"' ~["]*? '"';

WS: [ \t\r\n] -> channel(HIDDEN);