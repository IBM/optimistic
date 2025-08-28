# from test.test_python_to_expr import python_string_to_expr
from math_rep.expr import *
from rewriting.patterns import *
from validator2solver.optimistic_factory import python_string_to_expr

# e1 = Atom('int', ('foo',))


def test_pattern(pattern, expr):
    result = list(pattern_match(pattern, expr))
    if not result:
        print('Match failed!')
    else:
        for match in result:
            print(match)


def test_pat1():
    """
    >>> print(FormalContent[Let(PatternVariable('x'), Atom), Negation[PatternVariable('x')]])
    FormalContent[?x=Atom, Negation[?x]]
    >>> print(FormalContent[Let('x', Atom), Negation['x']])
    FormalContent[?x=Atom, Negation[?x]]
    >>> print(FormalContent[let(x=Atom), Negation['x']])
    FormalContent[?x=Atom, Negation[?x]]
    """


def test_match1():
    r"""
    >>> test_pattern(MathModule[FunctionApplication], python_string_to_expr('a+b/2\n'))
    {}
    >>> test_pattern(MathModule[FunctionApplication['+']], python_string_to_expr('a+b/2\n'))
    {}
    >>> test_pattern(MathModule[FunctionApplication['/']], python_string_to_expr('a+b/2\n'))
    Match failed!
    >>> test_pattern(MathModule[FunctionApplication['+', 'var', FunctionApplication['/']]], python_string_to_expr('a+b/2\n'))
    {?var=$a}
    >>> test_pattern(MathModule[FunctionApplication['+', 'var', FunctionApplication['*']]], python_string_to_expr('a+b/2\n'))
    Match failed!
    >>> test_pattern(MathModule[FunctionApplication['+', 'var', let(y=FunctionApplication['/'])]], python_string_to_expr('a+b/2\n'))
    {?var=$a, ?y=$b / 2}
    >>> test_pattern(MathModule[let(x=FunctionApplication['+', 'var', let(y=FunctionApplication['/'])])], python_string_to_expr('a+b/2\n'))
    {?var=$a, ?x=$a + $b / 2, ?y=$b / 2}
    >>> test_pattern(MathModule[let(x=FunctionApplication['+', 'var', let(y=FunctionApplication['/', 'left', 'right'])])], python_string_to_expr('a+b/2\n'))
    {?left=$b, ?right=2, ?var=$a, ?x=$a + $b / 2, ?y=$b / 2}
    >>> test_pattern(MathModule[let(x=FunctionApplication['+', 'var', let(y=FunctionApplication['/', 'var', 'right'])])], python_string_to_expr('a+b/2\n'))
    Match failed!
    >>> test_pattern(MathModule[Comparison], python_string_to_expr('a+b/2\n'))
    Match failed!
    >>> test_pattern(MathModule[let(x=FunctionApplication['+'])], python_string_to_expr('a+b/2\n'))
    {?x=$a + $b / 2}
    >>> test_pattern(MathModule[let(x=FunctionApplication['+', 'var', 'var'])], python_string_to_expr('a+a\n'))
    {?var=$a, ?x=$a + $a}
    >>> test_pattern(MathModule[let(x=FunctionApplication['+', 'var', 'var'])], python_string_to_expr('a+b\n'))
    Match failed!
    >>> test_pattern(MathModule[let(x=FunctionApplication['+', 'var', 'var'])], python_string_to_expr('a/2+a/2\n'))
    {?var=$a / 2, ?x=$a / 2 + $a / 2}
    >>> test_pattern(MathModule[let(x=IFTE['cond', 'then', 'else'])],
    ...                          python_string_to_expr('0 if p else 1\n'))
    {?cond=$p, ?else=1, ?then=0, ?x=$p ? 0 : 1}
    >>> test_pattern(MathModule[let(x=IFTE['cond', 'then'])],
    ...                          python_string_to_expr('0 if p else 1\n'))
    {?cond=$p, ?then=0, ?x=$p ? 0 : 1}
    >>> test_pattern(MathModule[let(x=IFTE['cond', 'then', let(e=PatternVariable('else')), let(d='dummy')])],
    ...                          python_string_to_expr('0 if p else 1\n'))
    Match failed!
    >>> test_pattern(MathModule[let(x=IFTE['cond', 'then', let(e='else'), let(d='dummy')])],
    ...                          python_string_to_expr('0 if p else 1\n'))
    Match failed!
    """


def test_ellipsis1():
    r"""
    >>> test_pattern(MathModule[IFTE[..., let(c=Comparison)]],
    ...              python_string_to_expr('0 if a<b else c<d\n'))
    {?c=$a < $b}
    {?c=$c < $d}
    >>> test_pattern(MathModule[IFTE[..., let(c=Comparison)]], python_string_to_expr('x>y if a<b else z>=w\n'))
    {?c=$a < $b}
    {?c=$x > $y}
    {?c=$z ≥ $w}
    >>> test_pattern(MathModule[IFTE[..., let(c=Comparison), ...]], python_string_to_expr('x>y if a<b else z>=w\n'))
    {?c=$a < $b}
    {?c=$x > $y}
    {?c=$z ≥ $w}
    >>> test_pattern(MathModule[IFTE[let(pre=...), let(c=Comparison), let(post=...)]],
    ...              python_string_to_expr('x>y if a<b else z>=w\n'))
    {?c=$a < $b, ?post=[$x > $y, $z ≥ $w], ?pre=[]}
    {?c=$x > $y, ?post=$z ≥ $w, ?pre=$a < $b}
    {?c=$z ≥ $w, ?post=[], ?pre=[$a < $b, $x > $y]}
    >>> test_pattern(MathModule[IFTE[let(pre2=let(pre=...)), let(c=Comparison), let(post=...)]],
    ...              python_string_to_expr('x>y if a<b else z>=w\n'))
    {?c=$a < $b, ?post=[$x > $y, $z ≥ $w], ?pre=[], ?pre2=[]}
    {?c=$x > $y, ?post=$z ≥ $w, ?pre=$a < $b, ?pre2=$a < $b}
    {?c=$z ≥ $w, ?post=[], ?pre=[$a < $b, $x > $y], ?pre2=[$a < $b, $x > $y]}
    >>> test_pattern(MathModule[FunctionApplication['f', let(pre=...), let(e=0), let(post=...)]],
    ...              python_string_to_expr('f(a+b, c and d, e/f)\n'))
    {?e=$a + $b, ?post=[$c ∧ $d, $e / $f], ?pre=[]}
    {?e=$c ∧ $d, ?post=$e / $f, ?pre=$a + $b}
    {?e=$e / $f, ?post=[], ?pre=[$a + $b, $c ∧ $d]}
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    # test_pattern(MathModule[let(x=IFTE['cond', 'then', let(e=PatternVariable('else')), let(d='dummy')])],
    #              python_string_to_expr('0 if p else 1\n'))
    # test_pattern(MathModule[IFTE[let(initial=...), let(c=Comparison)]], python_string_to_expr('0 if a<b else c<d\n'))
    # test_pattern(MathModule[IFTE[..., let(c=Comparison), ...]], python_string_to_expr('x>y if a<b else z>=w\n'))
