from math_rep.expr import MathVariableArray, Quantity, DomainDim, MathVariable, RangeExpr
from math_rep.expression_types import QualifiedName, M_ANY
from validator2solver.domain_analysis import AddDomainInfo, DomainBuilder, DomainTable, InputValue

INT_1 = Quantity(1)
INT_3 = Quantity(3)
STR_A = Quantity('a')


def qn(name, type=M_ANY):
    return QualifiedName(name, type)


def infer(*terms):
    di_adder = AddDomainInfo(dt)
    builder = DomainBuilder(dt)
    for term in terms:
        di_adder.visit(term)
        builder.visit(term)
    dt.propagate()


def test_mva_range1():
    """
    >>> mva_range_expr1[1]
    $$x[1]
    >>> mva_range_expr1[INT_1]
    $$x[1]
    >>> mva_range_expr1[3]
    Traceback (most recent call last):
    IndexError: Index 3 out of range 1..2 for 1st index of $$x
    >>> mva_range_expr1[INT_3]
    Traceback (most recent call last):
    IndexError: Index 3 out of range 1..2 for 1st index of $$x
    >>> mva_range_expr1[-3]
    Traceback (most recent call last):
    IndexError: Index -3 (i.e., 0) out of range 1..2 for 1st index of $$x
    >>> mva_range_expr1[STR_A]
    Traceback (most recent call last):
    IndexError: String index a for numeric dimension Range(1, 3)
    """


def test_mva_2dim():
    """
    >>> mva_a2[1,3]
    $$a2[1, 3]
    >>> mva_a2[RangeExpr(1, 3), 3]
    [$$a2[1, 3], $$a2[2, 3]]
    >>> mva_a2[RangeExpr(1, 3), RangeExpr(3, 5)]
    [$$a2[1, 3], $$a2[1, 4], $$a2[2, 3], $$a2[2, 4]]
    >>> mva_a2[RangeExpr(1, 3), RangeExpr(3, 6)]
    Traceback (most recent call last):
    IndexError: Index 5 out of range 3..4 for 2nd index of $$a2
    >>> mva_a2[range(1, 3), 3]
    [$$a2[1, 3], $$a2[2, 3]]
    >>> mva_a2[range(1, 3), range(3, 5)]
    [$$a2[1, 3], $$a2[1, 4], $$a2[2, 3], $$a2[2, 4]]
    >>> mva_a2[range(1, 3), range(3, 6)]
    Traceback (most recent call last):
    IndexError: Index 5 out of range 3..4 for 2nd index of $$a2
    """


def setup_imv_str():
    domain_var = MathVariable(qn('domain'))
    dd1 = qn('dd')
    dd1_mvar = MathVariable(dd1)
    mva_dd1 = MathVariableArray(qn('d'), DomainDim(dd1_mvar))
    mva_dd_a = mva_dd1[STR_A]
    infer(dd1_mvar)
    infer(domain_var)
    domain_var.appl_info.update_value(InputValue(('Foo', 'bar')), dt)
    dd1_mvar.appl_info.update_domain(domain_var, dt)
    infer(mva_dd1)
    infer(mva_dd_a)
    return mva_dd_a  # mva_dd1.dims[0].domain_info.value


def test_mva_dd1():
    """
    >>> setup_imv_str().owner.dims[0].appl_info.value
    InputValue('Foo', 'bar')
    """


mva_range_expr1 = MathVariableArray(qn('x'), RangeExpr(1, 3))
mva_a2 = MathVariableArray(qn('a2'), RangeExpr(1, 3), RangeExpr(3, 5))
dt = DomainTable()

if __name__ == '__main__':
    import doctest

    doctest.testmod()
    # mvar1_a = mva_range1[STR_A]
    # infer(mvar1_a)
    # print(mvar1_a)
