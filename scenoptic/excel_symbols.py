from typing import Tuple

from math_rep.expression_types import QualifiedName, M_ANY
from scenoptic.scenoptic_frame_constants import EXCEL_FRAME_NAME, EXCEL_AUX_NAME, EXCEL_ADDITIONS_NAME, \
    EXCEL_INTERNAL_NAME, EXCEL_VAR_NAME, WORKSHEET_FRAME_NAME

EXCEL_FRAME_PATH = (EXCEL_FRAME_NAME,)
WORKSHEET_FRAME_PATH = (WORKSHEET_FRAME_NAME,)
EXCEL_AUX_FRAME = (EXCEL_AUX_NAME,)
EXCEL_INTERNAL_FRAME = (EXCEL_INTERNAL_NAME,)
EXCEL_ADDITIONS_FRAME = (EXCEL_ADDITIONS_NAME,)


def as_excel_name(name, mtype=M_ANY):
    """
    Return the uppercased name, with the Excel lexical path
    """
    return QualifiedName(name.upper(), lexical_path=EXCEL_FRAME_PATH, type=mtype)


def as_excel_internal_name(name, mtype=M_ANY):
    """
    Return the name (as-is) with the internal Excel lexical path
    :param name:
    :return:
    """
    return QualifiedName(name, lexical_path=EXCEL_INTERNAL_FRAME, type=mtype)


def is_excel_name(qname: QualifiedName):
    path = qname.lexical_path
    return path and path[-1] in (EXCEL_FRAME_NAME, EXCEL_ADDITIONS_NAME, EXCEL_INTERNAL_NAME)


def worksheet_path(sheet_name: str) -> Tuple[str, ...]:
    return sheet_name, WORKSHEET_FRAME_NAME


def excel_var_path(origin_cell_name: str):
    return origin_cell_name, EXCEL_VAR_NAME


EXCEL_CONCATENATE_QN = as_excel_name('*concatenate-string*')

EXCEL_IF_QN = as_excel_name('IF')
EXCEL_SUM_QN = as_excel_name('SUM')
EXCEL_SUMIF_QN = as_excel_name('SUMIF')
EXCEL_SUMIFS_QN = as_excel_name('SUMIFS')
EXCEL_COUNT_QN = as_excel_name('COUNT')
EXCEL_COUNTIF_QN = as_excel_name('COUNTIF')
EXCEL_COUNTIFS_QN = as_excel_name('COUNTIFS')
EXCEL_XLOOKUP_QN = as_excel_name('XLOOKUP')

EXCEL_SUM_LAMBDA_QN = as_excel_internal_name('SUM-lambda')
EXCEL_SUMIF_LAMBDA_QN = as_excel_internal_name('SUMIF-lambda')
EXCEL_SUMIFS_LAMBDA_QN = as_excel_internal_name('SUMIFS-lambda')
EXCEL_COUNT_LAMBDA_QN = as_excel_internal_name('COUNT-lambda')
EXCEL_COUNTIF_LAMBDA_QN = as_excel_internal_name('COUNTIF-lambda')
EXCEL_COUNTIFS_LAMBDA_QN = as_excel_internal_name('COUNTIFS-lambda')

EXCEL_AUX_V_QN = QualifiedName('v', lexical_path=EXCEL_AUX_FRAME)
EXCEL_AUX_CELL_QN = QualifiedName('cell', lexical_path=EXCEL_AUX_FRAME)
EXCEL_COND_CELL_QN = QualifiedName('cond', lexical_path=EXCEL_AUX_FRAME)

EXCEL_RE_MATCH_QN = QualifiedName('match-excel-re', lexical_path=EXCEL_INTERNAL_FRAME)
