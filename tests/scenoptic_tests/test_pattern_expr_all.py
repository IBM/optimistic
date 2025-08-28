from tests.scenoptic_tests.test_python_to_expr import python_string_to_expr
from math_rep.expr import *
from rewriting.patterns import *


def test_pattern(pattern, expr):
    result = list(pattern_match(pattern, expr))
    if not result:
        print('Match failed!')
    else:
        for match in result:
            print(match)


if __name__ == '__main__':
    test_pattern(MathModule[let(x=FunctionApplication['+', 'var', let(y=FunctionApplication['/', 'left', 'right'])])], python_string_to_expr('a+b/2\n'))
    # test_pattern(MathModule[FunctionApplication], python_string_to_expr('a+b/2\n'))
    # test_pattern(let(x='5'), python_string_to_expr('5'))
    # test_pattern(MathModule[FunctionApplication], python_string_to_expr('a+b/2\n'))
    # print(FormalContent[Let(PatternVariable('x'), Atom), Negation[PatternVariable('x')]])
