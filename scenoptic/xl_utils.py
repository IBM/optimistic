import numbers
import re
import string
from functools import reduce
from typing import Tuple, Optional, Generator, Iterable

from math_rep.expression_types import QualifiedName, M_ANY
from scenoptic.scenoptic_frame_constants import WORKSHEET_FRAME_NAME
from scenoptic.excel_symbols import worksheet_path


def normalize_sheet_special_characters(sheet_name: str) -> str:
    """
    The following functions handle special characters in sheet names
    as part of the parameters column, specified as string by a user
    Background:

        In Excel, a sheet name may contain a single quotes only in the middle of string,
        never at the beginning or end of the name
        When referenced inside a cell excel transforms it to double quote:
        i.e   sheet_name =  Do'nt Produce
        when referencing it inside a cell it will turn it into:
                      =Filter(..., 'Do''nt Produce'!C2:C5, ...)
            here you can see, adding single quotes in the beginning and end
             and also doubling the middle single quotes to double single quotes !!

    Since users tend to mistakenly remove single quotes at the beginning or end of the sheet name
    we apply less strict conformance to excel format, dropping the need for a quote at the beginning or end

    """
    #  The following code is strictly compliant with excel format
    #
    # sheet = sheet_name.strip()
    # if sheet.startswith("'") and sheet.endswith("'"):
    #     sheet = sheet[1:-1]
    # return sheet
    sheet = sheet_name.strip()
    if sheet.startswith("'"):
        sheet = sheet[1:]
    if sheet.endswith("'"):
        sheet = sheet[:-1]
    return sheet


def cell_as_str(row: int, col: int, sheet: Optional[str]) -> str:
    sheet_spec = f'{sheet}!' if sheet else ''
    return f'{sheet_spec}{coords_to_cell(row, col)}'


def get_cell_qn_as_excel_string(cell: QualifiedName) -> str:
    # FIXME!!!! get rid of this function
    cell1, _, _ = range_to_cells(cell.name)
    return cell1


def get_sheet_in_cell_qn_as_string(cell: QualifiedName) -> Optional[str]:
    if cell.lexical_path[-1] == WORKSHEET_FRAME_NAME and len(cell.lexical_path) > 1:
        return cell.lexical_path[0]
    return None


def as_cell_qn(row: int, col: int, sheet: str, ctype=M_ANY) -> QualifiedName:
    return QualifiedName(cell_as_str(row, col, sheet),
                         type=ctype,
                         lexical_path=worksheet_path(sheet))


def column_to_index(col) -> int:
    """Translate a numeric or character column name into a 1-based index"""
    if isinstance(col, numbers.Number):
        return col
    try:
        num = int(col)
        return num
    except ValueError:
        return reduce(lambda res, digit: res * 26 + digit,
                      (ord(ch.upper()) - ord('A') + 1 for ch in col))


def index_to_column(index: int) -> str:
    """Translate a 1-based column index to a character column name"""
    letters = string.ascii_uppercase
    result = ''
    while index:
        mod = (index - 1) % 26
        result = letters[mod] + result
        index = (index - mod) // 26
    return result


CELL_REF_PATTERN = r'[$]?([a-zA-Z]+)[$]?(\d+)'
CELL_REF_PATTERN_NO_GROUPS = r'[$]?(?:[a-zA-Z]+)[$]?(?:\d+)'
CELL_REF_RE = re.compile(CELL_REF_PATTERN)
SHEET_CELL_RE = re.compile(rf'(?:(.*)!)?\s*({CELL_REF_PATTERN_NO_GROUPS})\s*')
SHEET_RANGE_RE = re.compile(
    rf'(?:(.*)!)?\s*({CELL_REF_PATTERN_NO_GROUPS})\s*(?::\s*({CELL_REF_PATTERN_NO_GROUPS})\s*)?')


def cell_name_to_components(cell_name: str, sheet: str = None) -> Tuple[int, int, str]:
    m = SHEET_CELL_RE.fullmatch(cell_name)
    if m is None:
        raise Exception(f'Bad cell specification: {cell_name}')
    sheet = normalize_sheet_special_characters(m.group(1)) if m.group(1) else sheet
    coords = cell_to_coords(m.group(2))
    return *coords, sheet


def cell_qn_to_components(qn: QualifiedName, sheet: str = None) -> Tuple[int, int, str]:
    return cell_name_to_components(qn.name, sheet)


def range_to_cells(spec: str, sheet: str = None) -> Tuple[int, Optional[int], Optional[str]]:
    m = SHEET_RANGE_RE.fullmatch(spec)
    if m is None:
        raise Exception(f'Bad range specification: {spec}')
    # sheet = m.group(1).strip().strip("'") if m.group(1) else sheet
    sheet = normalize_sheet_special_characters(m.group(1)) if m.group(1) else sheet
    cells = (m.group(index).upper() if m.group(index) else None for index in range(2, 4))
    return *cells, sheet


def cell_to_coords(cell: str) -> Tuple[int, int]:
    m1 = CELL_REF_RE.fullmatch(cell.upper())
    # FIXME!! indicate matching error as exception or None
    col = column_to_index(m1.group(1))
    row = int(m1.group(2))
    return row, col


def coords_to_cell(row, col) -> str:
    return f'{index_to_column(col)}{row}'


# TODO: add support for named cells and ranges
def normalize_cell(spec) -> str:
    row, col = cell_to_coords(spec)
    return coords_to_cell(row, col)


def normalize_cell_qn(spec, sheet: str) -> QualifiedName:
    row, col = cell_to_coords(spec)
    return as_cell_qn(row, col, sheet)


def xl_range_elements(start_col, start_row, end_col, end_row) -> Generator[str, None, None]:
    """
    Return a generator for the individual cells that are members of the given range; all elements are normalized
    """
    return (coords_to_cell(i, j)
            for i in range(start_row, end_row + 1)
            for j in range(start_col, end_col + 1))


def xl_range_element_qn(start_col, start_row, end_col, end_row, sheet: str) -> Generator[QualifiedName, None, None]:
    """
    Return a generator for the qualified names of the individual cells that are members of the given range;
    all elements are normalized
    """
    return (as_cell_qn(i, j, sheet)
            for i in range(start_row, end_row + 1)
            for j in range(start_col, end_col + 1))


def xl_cell_or_range_elements_qn(xl_range: str, sheet: str = None) -> Iterable[QualifiedName]:
    """
    Return a generator for the individual cells that are members of the given range.

    :param xl_range: an Excel specification of a cell or range
    :param sheet: current sheet title
    :return: a generator for the elements of the range; all elements are normalized qualified names
    """
    cell1, cell2, sheet = range_to_cells(xl_range, sheet)
    if cell2:
        start_row, start_col = cell_to_coords(cell1)
        end_row, end_col = cell_to_coords(cell2)
        return xl_range_element_qn(start_col, start_row, end_col, end_row, sheet)
    else:
        return normalize_cell_qn(cell1, sheet),


RANGE_EXPR = r"""
(?P<min_col_fix>[$])?(?P<min_col>[A-Za-z]{1,3})?
(?P<min_row_fix>[$])?(?P<min_row>\d+)?
(:(?P<max_col_fix>[$])?(?P<max_col>[A-Za-z]{1,3})?
(?P<max_row_fix>[$])?(?P<max_row>\d+)?)?
"""
RANGE_RE = re.compile(RANGE_EXPR, re.VERBOSE)

SHEET_TITLE = r"""
(('(?P<quoted>([^']|'')*)')|(?P<notquoted>[^'^ ^!]*))!"""
SHEETRANGE_EXPR = f'{SHEET_TITLE}(?P<cells>{RANGE_EXPR})(?=,?)'
SHEETRANGE_RE = re.compile(SHEETRANGE_EXPR, re.VERBOSE)

CELL_EXPR = r"""
(?P<col_fix>[$])?(?P<col>[A-Za-z]{1,3})?
(?P<row_fix>[$])?(?P<row>\d+)?
"""
CELL_RE = re.compile(CELL_EXPR, re.VERBOSE)


def get_cell_re_dict(cell):
    m = CELL_RE.match(cell)
    return m.groupdict()


def get_full_sheet_re_dict(cell):
    m = SHEETRANGE_RE.match(cell)
    return m.groupdict()
