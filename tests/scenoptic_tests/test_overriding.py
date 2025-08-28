from math_rep.expression_types import QualifiedName, M_NUMBER
from math_rep.expr import MathVariable, Quantity, Comparison

e1 = Quantity(10)
e2 = MathVariable(QualifiedName('e2', M_NUMBER))
e3 = Quantity(20)
c1 = Comparison(e1, '=', e2)
c2 = Comparison(e1 + 2, '>', 1 + e2)


def test_term():
    """
    >>> e1
    10
    >>> e2
    $e2
    >>> e1 + e2
    10 + $e2
    >>> e2 + e1
    $e2 + 10
    >>> sum([e1, e2, e3])
    10 + $e2 + 20
    >>> sum([-30, e2, e3])
    -30 + $e2 + 20
    >>> 0 + e2
    $e2
    >>> e2 + 0
    $e2
    >>> 0 + e1
    10
    """


def test_condition():
    """
    >>> c1 & c2
    10 = $e2 ∧ 12 > 1 + $e2
    >>> True & c1
    10 = $e2
    >>> False & c2
    False*Boolean*
    >>> c1 & True
    10 = $e2
    """


def test_comparison():
    """
    >>> e1.eq(e2)
    10 = $e2
    >>> e1.ne(e2)
    10 ≠ $e2
    >>> e1 == e2
    10 = $e2
    >>> e1 != e2
    10 ≠ $e2
    >>> e1 < e2
    10 < $e2
    >>> e1 <= e2
    10 ≤ $e2
    >>> e1 > e2
    10 > $e2
    >>> e1 >= e2
    10 ≥ $e2
    >>> e2 > 1
    $e2 > 1
    >>> 1 > e2
    $e2 < 1
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
