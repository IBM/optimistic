from math_rep.expression_types import QualifiedName, MFunctionType, MStreamType, M_ANY, M_INT
from math_rep.math_frame import MATH_FRAME_NAME
from validator2solver.python.python_builtins import PYTHON_BUILTIN_NAMES
from validator2solver.python.symbol_table import PYTHON_BUILTIN_FRAME_NAME

# FIXME: change to correct path once paths are fixed
# MODULE_LEXICAL_PATH = (TOP_LEVEL_FRAME_NAME, PYTHON_BUILTIN_FRAME_NAME)
#
# BUILTIN QN
#
BUILTIN_QN = {name: QualifiedName(name, lexical_path=(PYTHON_BUILTIN_FRAME_NAME,)) for name in PYTHON_BUILTIN_NAMES}

#
# Python Main Libraries QN >= Python 3.8
#
STATICMETHOD_QN = QualifiedName('staticmethod', lexical_path=(PYTHON_BUILTIN_FRAME_NAME,))
CLASSMETHOD_QN = QualifiedName('classmethod', lexical_path=(PYTHON_BUILTIN_FRAME_NAME,))
DATACLASS_QN = QualifiedName('dataclass', lexical_path=('dataclasses', PYTHON_BUILTIN_FRAME_NAME))
NEW_TYPE_QN = QualifiedName('NewType', lexical_path=('typing', PYTHON_BUILTIN_FRAME_NAME))

RECORD_QN = QualifiedName('record', lexical_path=('utils', 'meta', 'optimistic_client', PYTHON_BUILTIN_FRAME_NAME))
METADATA_QN = QualifiedName('metadata', lexical_path=('utils', 'meta', 'optimistic_client', PYTHON_BUILTIN_FRAME_NAME))
SOLUTION_VARIABLE_QN = QualifiedName('solution_variable',
                                     lexical_path=('utils', 'meta', 'optimistic_client', PYTHON_BUILTIN_FRAME_NAME))
TOTAL_MAPPING_QN = QualifiedName('TotalMapping',
                                 lexical_path=('optimization', 'optimistic_client', PYTHON_BUILTIN_FRAME_NAME))

NEXT_QN = QualifiedName('next', lexical_path=(MATH_FRAME_NAME,))

DATA_RECORD_QN_GROUP = {DATACLASS_QN, RECORD_QN}

#
# Python Main Libraries QN >= Python 3.9
#
TUPLE_QN = QualifiedName('tuple', lexical_path=(PYTHON_BUILTIN_FRAME_NAME,))
MAPPING_QN = QualifiedName('Mapping', lexical_path=(PYTHON_BUILTIN_FRAME_NAME,))

#
# Optimistic Libraries  QN
#
OPTIMIZATION_PROBLEM_QN = QualifiedName('OptimizationProblem',
                                        lexical_path=('optimization', 'optimistic_client', PYTHON_BUILTIN_FRAME_NAME))
CONSTRAINT_QN = QualifiedName('constraint',
                              lexical_path=('utils', 'meta', 'optimistic_client', PYTHON_BUILTIN_FRAME_NAME))
MAXIMIZE_QN = QualifiedName('maximize', lexical_path=('utils', 'meta', 'optimistic_client', PYTHON_BUILTIN_FRAME_NAME))
MINIMIZE_QN = QualifiedName('minimize', lexical_path=('utils', 'meta', 'optimistic_client', PYTHON_BUILTIN_FRAME_NAME))
UNIQUE_ASSIGNMENT_CLASS_QN = QualifiedName('UniqueAssignment',
                                           lexical_path=('unique_assignment', 'optimistic_client',
                                                         PYTHON_BUILTIN_FRAME_NAME))
UNIQUE_ASSIGNMENT_METHOD_QN = QualifiedName('unique_assignment',
                                            lexical_path=('Class UniqueAssignment', 'unique_assignment',
                                                          'optimistic_client', PYTHON_BUILTIN_FRAME_NAME))
COUNT_QN = QualifiedName('count', MFunctionType([MStreamType(M_ANY)], M_INT),
                         lexical_path=('utils', 'meta', 'optimistic_client', PYTHON_BUILTIN_FRAME_NAME))
