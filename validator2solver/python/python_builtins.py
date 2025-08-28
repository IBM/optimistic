from math_rep.expression_types import QualifiedName
from validator2solver.python.python_frame_constants import PYTHON_UNKNOWN_FRAME_NAME
from validator2solver.python.profile_frame_constants import PROFILE_FRAME_NAME
from validator2solver.python.symbol_table import Frame, Variable, PYTHON_BUILTIN_FRAME_NAME, FrameKind

# Top-level Python frame

PYTHON_BUILTIN_FUNCTIONS = ('abs all any ascii bin bool breakpoint bytearray bytes callable chr classmethod '
                            'compile complex delattr dict dir divmod enumerate eval exec filter float format '
                            'frozenset getattr globals hasattr hash help hex id input int isinstance issubclass '
                            'iter len list locals map max memoryview min next object oct open ord pow print '
                            'property range repr reversed round set setattr slice sorted staticmethod str sum '
                            'super tuple type vars zip').split()
PYTHON_BUILTIN_TYPES = 'int float complex str bool list tuple range set frozenset dict bytes bytearray'.split()
PYTHON_BUILTIN_NAMES = PYTHON_BUILTIN_FUNCTIONS + PYTHON_BUILTIN_TYPES

PYTHON_BUILTIN_FRAME = Frame(name=PYTHON_BUILTIN_FRAME_NAME, kind=FrameKind.BUILTIN,
                             variables={Variable(name) for name in PYTHON_BUILTIN_NAMES})

# DEBUG
PYTHON_UNKNOWN_FRAME = Frame(PYTHON_UNKNOWN_FRAME_NAME, kind=FrameKind.UNKNOWN, parent=PYTHON_BUILTIN_FRAME)

PYTHON_OPERATOR_NAMES = '+ - * / // ** % < > == != <= >= & | ~ >> << and or not in notin is isnot'.split()
PYTHON_LOGICAL_OPERATORS = 'and or not'.split()
PYTHON_OPERATOR_FRAME_NAME = '*python-operators*'
PYTHON_OPERATORS = {func: QualifiedName(func, lexical_path=(PYTHON_OPERATOR_FRAME_NAME,)) for func in
                    PYTHON_OPERATOR_NAMES}


# OPERATOR_FRAME = Frame(name='*python-operators*', variables={Variable(name) for name in PYTHON_OPERATORS})


def create_builtin_frame():
    return Frame(name=PYTHON_BUILTIN_FRAME_NAME, kind=FrameKind.BUILTIN,
                 variables={Variable(name) for name in PYTHON_BUILTIN_NAMES})


def is_python_name(qname: QualifiedName):
    path = qname.lexical_path
    return path and path[-1] == PYTHON_BUILTIN_FRAME_NAME


def is_python_builtin(qname: QualifiedName):
    return (qname.lexical_path in ((PYTHON_BUILTIN_FRAME_NAME,), ('math', PYTHON_BUILTIN_FRAME_NAME)) or
            # FIXME! this is a workaround for the case when there is no lexical information, assuming builtin
            qname.lexical_path == ())


def is_python_operator(qname: QualifiedName):
    return qname.lexical_path == (PYTHON_OPERATOR_FRAME_NAME,)


def is_profile_name(qname: QualifiedName):
    return qname.lexical_path == (PROFILE_FRAME_NAME,)


# def is_relative_name(qname: QualifiedName):
#     return qname.lexical_path == (RELATIVE_FRAME_NAME,)


QualifiedName.add_lexical_scope_predicate(is_python_name)
QualifiedName.add_lexical_scope_predicate(is_profile_name)
