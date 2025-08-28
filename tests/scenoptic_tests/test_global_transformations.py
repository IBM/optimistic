from math_rep.expr import MathVariable
from math_rep.expression_types import QualifiedName
from rewriting.global_transformations import find_constants, substitute_globally

a = MathVariable(QualifiedName('a'))
b = MathVariable(QualifiedName('b'))
c = MathVariable(QualifiedName('c'))

ab = a + b
abc = ab + c

a10 = a == 10
b20 = b == 20
c30 = c == 30


def test_global_substitute():
    """
    >>> ab_sub = find_constants([a10, b20])
    >>> ab_sub
    {a: 10, b: 20}
    >>> substitute_globally([a, ab, abc], ab_sub)
    [10, 30, 30 + $c]
    >>> ac_sub = find_constants([a10, c30])
    >>> ac_sub
    {a: 10, c: 30}
    >>> substitute_globally([a, ab, abc], ac_sub)
    [10, 10 + $b, 10 + $b + 30]
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
