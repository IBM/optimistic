from __future__ import annotations

from typing import Optional, Union

from codegen.utils import disown, visitor_for
from validator2solver.domain_analysis import AddDomainInfo, AddDomainInfoSuper, DomainTable, DomainBuilder
from math_rep.expr import intern_expr, MathVariable, Term, FormalContent
from math_rep.expression_types import M_ANY, QualifiedName, MType, MCollectionType, type_intersection
from scenoptic.excel_symbols import worksheet_path
from scenoptic.scenoptic_frame_constants import M_RANGE
from scenoptic.xl_utils import cell_as_str, cell_to_coords, get_sheet_in_cell_qn_as_string, get_cell_qn_as_excel_string, \
    range_to_cells


@intern_expr
class Cell(MathVariable):
    """
    A single cell in a spreadsheet
    """
    has_operator = False

    @disown('row', 'col', 'sheet', 'ctype')
    def __init__(self, row: int, col: int, sheet: Optional[str] = None, ctype=M_ANY):
        self.row = row
        self.col = col
        self.sheet = sheet
        super().__init__(QualifiedName(self.as_str(), ctype,
                                       lexical_path=worksheet_path(self.sheet or '*current-sheet*')))

    def as_str(self, with_sheet: bool = True):
        return cell_as_str(self.row, self.col, self.sheet if with_sheet else None)

    @classmethod
    def from_name(cls, cell: str, sheet: str = None):
        return cls(*cell_to_coords(cell), sheet)

    @classmethod
    def from_name_qn(cls, cell: QualifiedName, sheet: str = None):
        sheet = get_sheet_in_cell_qn_as_string(cell) or sheet
        name = get_cell_qn_as_excel_string(cell)
        return cls(*cell_to_coords(name), sheet, ctype=cell.type)

    def describe(self, parent_binding=None):
        return self.parenthesize(f'#{self.as_str(with_sheet=True)}', parent_binding)

    def is_eq(self, other):
        return type(other) == Cell and self.row == other.row and self.col == other.col and self.sheet == other.sheet

    def with_sheet(self, sheet: str):
        return Cell(self.row, self.col, sheet, self.type)

    def with_sheet_and_type(self, sheet: str, ctype: MType = M_ANY):
        return Cell(self.row, self.col, sheet, ctype)


@intern_expr
class CellsRange(Term):
    has_operator = False

    # FIXME!! add cell_type (see Cells)
    def __init__(self, start_cell: Term, end_cell: Term):
        super().__init__(M_RANGE)
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.free_vars = frozenset(x.name for x in (self.start_cell, self.end_cell) if isinstance(x, MathVariable))

    def to_code_rep(self):
        raise Exception('CellsRange cannot be translated directly')

    def describe(self, parent_binding=None):
        return f'CellsRange({self.start_cell.describe()}:{self.end_cell.describe()})'

    def arguments(self):
        return self.start_cell, self.end_cell

    def with_argument(self, index, arg):
        if index == 0:
            return CellsRange(arg, self.end_cell)
        if index == 1:
            return CellsRange(self.start_cell, arg)
        raise IndexError('Index for CellRange must be 0 or 1')


@intern_expr(key=lambda start_cell, end_cell, cell_type=None: (min(start_cell.row, end_cell.row),
                                                               max(start_cell.row, end_cell.row),
                                                               min(start_cell.col, end_cell.col),
                                                               max(start_cell.col, end_cell.col),
                                                               start_cell.sheet,
                                                               cell_type))
class Cells(Term):
    """
    A range of cells in a spreadsheet
    """
    has_operator = False

    # FIXME! generalize to expressions instead of specific cells
    @disown('start_cell', 'end_cell', 'cell_type')
    def __init__(self, start_cell: Cell, end_cell: Cell, cell_type: Optional[MType] = None):
        """
        Create a range.

        :param start_cell: the first cell
        :param end_cell: the last cell
        :param cell_type: optional type of cells in range; if not given, the intersection of the types of the start and
            end cells will be used as an approximation
        """
        if start_cell.sheet != end_cell.sheet:
            raise Exception(f'Range must belong to a single sheet: '
                            f'{start_cell.as_str(with_sheet=True)}:{end_cell.as_str(with_sheet=True)}')
        super().__init__(MCollectionType(cell_type if cell_type is not None
                                         else type_intersection(start_cell.type, end_cell.type)))
        self.sheet = start_cell.sheet
        self.start_row = min(start_cell.row, end_cell.row)
        self.end_row = max(start_cell.row, end_cell.row)
        self.start_col = min(start_cell.col, end_cell.col)
        self.end_col = max(start_cell.col, end_cell.col)
        self.free_vars = frozenset(cell.name for cell in self)

    def __iter__(self):
        return (Cell(r, c, self.sheet)
                for r in range(self.start_row, self.end_row + 1)
                for c in range(self.start_col, self.end_col + 1))

    def key(self):
        return self.sheet, self.start_row, self.end_row, self.start_col, self.end_col

    def is_eq(self, other):
        return (isinstance(other, Cells) and self.sheet == other.sheet
                and self.start_row == other.start_row and self.end_row == other.end_row
                and self.start_col == other.start_col and self.end_col == other.end_col)

    def to_code_rep(self):
        raise Exception('Cells cannot be translated directly')

    def describe(self, parent_binding=None):
        return self.parenthesize(
            f'#{cell_as_str(self.start_row, self.start_col, self.sheet)}:'
            f'{cell_as_str(self.end_row, self.end_col, self.sheet)}',
            parent_binding)

    def arguments(self):
        return ()

    def with_argument(self, index, arg):
        raise IndexError('Cells has no arguments')


# FIXME!!!!! add ctype
def cell_to_expr(spec: str, sheet: str = None) -> Union[Cell, Cells]:
    spec1, spec2, sheet = range_to_cells(spec, sheet)
    cell1 = Cell(*cell_to_coords(spec1), sheet)
    if spec2 is None:
        return cell1
    return Cells(cell1, Cell(*cell_to_coords(spec2), sheet))


@visitor_for(FormalContent, add_call_to='add_domain_info', collect_results=False)
class AddDomainInfoSuperForScenoptic(AddDomainInfoSuper):
    pass


class AddDomainInfoForScenoptic(AddDomainInfoSuperForScenoptic, AddDomainInfo):
    pass


class DomainTableForScenoptic(DomainTable):
    def __init__(self):
        super().__init__(domain_builder_class=DomainBuilderForScenoptic,
                         domain_adder_class=AddDomainInfoSuperForScenoptic)


class DomainBuilderForScenoptic(DomainBuilder):
    def visit_cell(self, obj: Cell):
        pass

    def visit_cells(self, obj: Cells):
        pass

    def visit_cells_range(self, obj: CellsRange):
        pass
