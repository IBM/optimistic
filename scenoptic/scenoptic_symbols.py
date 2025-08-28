from codegen.java.java_symbols import LAMBDA_PARAM_PATH
from math_rep.expression_types import QualifiedName, MFunctionType, M_NUMBER, M_INT, M_STRING

SCENOPTIC_JAVA_GET_VALUE_QN = QualifiedName(
    'getValue', lexical_path=tuple(reversed('com.ibm.hrl.scenoptic.solver.SpreadsheetScoreCalculator'.split('.'))))
SCENOPTIC_JAVA_GET_INCREMENTAL_VALUE_QN = QualifiedName(
    'getIncrementalValue',
    lexical_path=tuple(reversed('com.ibm.hrl.scenoptic.solver.SpreadsheetScoreCalculator'.split('.'))))
SCENOPTIC_JAVA_CELL_KEY = QualifiedName('CellKey',
                                        lexical_path=tuple(reversed('com.ibm.hrl.scenoptic.keys'.split('.'))))
SCENOPTIC_JAVA_GET_QN = QualifiedName('get', lexical_path=('*java-method*',))
ABSTRACT_CELL_KEY_QN = QualifiedName('AbstractCellKey',
                                     lexical_path=tuple(reversed('com.ibm.hrl.scenoptic.keys'.split('.'))))
SCENOPTIC_JAVA_SINGLE_INT_SUMMING_TERMINATOR_QN = QualifiedName(
    'SingleIntSummingTerminator',
    lexical_path=tuple(reversed('com.ibm.hrl.scenoptic.domain.processors'.split('.'))))
SCENOPTIC_JAVA_SINGLE_INT_SUMMING_CREATOR_QN = QualifiedName(
    'SingleIntSummingCreator',
    lexical_path=tuple(reversed('com.ibm.hrl.scenoptic.domain.processors'.split('.'))))

# FIXME: extend type system with optional values
SCENOPTIC_UTILS_PATH = tuple(reversed('com.ibm.hrl.scenoptic.utils'.split('.')))
GET_OPTIONAL_STRING_QN = QualifiedName('getOptionalString', type=MFunctionType([M_STRING], M_STRING),
                                       lexical_path=SCENOPTIC_UTILS_PATH)
GET_OPTIONAL_INT_QN = QualifiedName('getOptionalInt', type=MFunctionType([M_INT], M_INT),
                                    lexical_path=SCENOPTIC_UTILS_PATH)
GET_OPTIONAL_FLOAT_QN = QualifiedName('getOptionalString', type=MFunctionType([M_NUMBER], M_NUMBER),
                                      lexical_path=SCENOPTIC_UTILS_PATH)
GET_OPTIONAL_DOUBLE_QN = QualifiedName('getOptionalDouble', type=MFunctionType([M_NUMBER], M_NUMBER),
                                       lexical_path=SCENOPTIC_UTILS_PATH)

VALUES_QN = QualifiedName('values', lexical_path=LAMBDA_PARAM_PATH)
CELL_KEY_QN = QualifiedName('cellKey', lexical_path=LAMBDA_PARAM_PATH)
CURRENT_QN = QualifiedName('current', lexical_path=LAMBDA_PARAM_PATH)
PREVIOUS_VALUES_QN = QualifiedName('previousValues', lexical_path=LAMBDA_PARAM_PATH)
NEW_VALUES_QN = QualifiedName('newValues', lexical_path=LAMBDA_PARAM_PATH)
PREVIOUS_SCALARS_QN = QualifiedName('previousScalars', lexical_path=LAMBDA_PARAM_PATH)
NEW_SCALARS_QN = QualifiedName('newScalars', lexical_path=LAMBDA_PARAM_PATH)

SCENOPTIC_DOMAIN_PATH = tuple(reversed('com.ibm.hrl.scenoptic.domain'.split('.')))
ISUMMING_CELL_QN = QualifiedName('ISummingCell', lexical_path=SCENOPTIC_DOMAIN_PATH)
ISUMMING_CELL_PATH = ('ISummingCell', *SCENOPTIC_DOMAIN_PATH)
SUMMING_CELL_GET_INT_QN = QualifiedName('getInt', lexical_path=ISUMMING_CELL_PATH)
SUMMING_CELL_GET_DOUBLE_QN = QualifiedName('getDouble', lexical_path=ISUMMING_CELL_PATH)

COUNTING_SHADOW_CELL_CLASS_SUFFIX = 'CountingShadowCell'
COUNTING_SHADOW_CELL_QN = QualifiedName('CountingShadowCellImpl', lexical_path=SCENOPTIC_DOMAIN_PATH)
SUMMING_SHADOW_CELL_QN = QualifiedName('SummingShadowCellImpl', lexical_path=SCENOPTIC_DOMAIN_PATH)
