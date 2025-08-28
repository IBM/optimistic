from opl_repr.opl_frame_constants import OPL_USER_FRAME_NAME
from validator2solver.codegen.opl.opl_generator import OplVisitor
from validator2solver.python.python_generator import PythonVisitor
from math_rep.expr import MathVariable
from math_rep.expression_types import QualifiedName


def qn(name: str) -> QualifiedName:
    return QualifiedName(name, lexical_path=(OPL_USER_FRAME_NAME,))


v1 = MathVariable(qn('v1'))
v2 = MathVariable(qn('v2'))
v3 = MathVariable(qn('v3'))
v4 = MathVariable(qn('v4'))

opl = OplVisitor()
py = PythonVisitor('test_prec')

def test_paren1():
    """
    >>> v1 + (1 + v2) + v3
    $v1 + 1 + $v2 + $v3
    >>> (v1 + 2) + (1 + v2) + v3
    $v1 + 2 + 1 + $v2 + $v3
    >>> m1 = v1 - (1 - v2) - v3
    >>> m1
    $v1 - (1 - $v2) - $v3
    >>> opl.visit(m1.to_code_rep()).value
    'v1 - (1 - v2) - v3'
    >>> py.visit(m1.to_code_rep()).value
    'v1 - (1 - v2) - v3'
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
