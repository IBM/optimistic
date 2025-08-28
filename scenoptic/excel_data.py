from __future__ import annotations

from abc import ABC, abstractmethod
from functools import total_ordering
from typing import Optional, Mapping, Type, Sequence, Union

from codegen.utils import intern
from scenoptic.scenoptic_expr import Cell, Cells, cell_to_expr
from math_rep.expression_types import MType, M_BOOLEAN, M_INT, M_NUMBER, M_STRING, QualifiedName, MClassType
from scenoptic.xl_utils import index_to_column


class ExcelData(ABC):
    @abstractmethod
    def get_type(self, cell: str) -> Optional[CellType]:
        """
        Return the type associated with the given cell

        :param cell: a cell specification (A1 style)
        :return: corresponding cell type of given cell, None if not found
        """

    @abstractmethod
    def cell_value(self, row, col, req_type=None, sheet=None, cast_to=None, empty_values=()):
        """
        Get the value of the cell in the given row and column.  If ``req_type`` is supplied and the type of the value
        is not on ``req_type``, or if the value is on ``empty_values``, return None.
        
        :param sheet:
        :param row: row of cell
        :param col: column of cell
        :param req_type: sequence of types or None
        :param cast_to: type to cast the result to
        :param empty_values: sequence of values indicating empty cell
        :return: cell value or None
        """

    @abstractmethod
    def cell_qn_value(self, cell: QualifiedName, req_type=None, cast_to=None, empty_values=()):
        """
        Get the value of the QualifiedName cell .  If ``req_type`` is supplied and the type of the value
        is not on ``req_type``, or if the value is on ``empty_values``, return None.

        :param cell:QualifiedName cell
        :param req_type: sequence of types or None
        :param cast_to: type to cast the result to
        :param empty_values: sequence of values indicating empty cell
        :return: cell value or None
        """

    @abstractmethod
    def sheet_names(self) -> Sequence[str]:
        """
        Returns iterator over sheet names
        """

    @abstractmethod
    def is_named_range(self, named_range_candidate: str) -> bool:
        """
        Returns True if the specified is a named range, otherwise False

        :param named_range_candidate: str a name range string value
        """

    @abstractmethod
    def named_range_sheet(self, named_range_candidate: str) -> Union[str, None]:
        """
        If this is valid named range value, return the sheet name of this range

        :param named_range_candidate: str a name range string value
        """

    @abstractmethod
    def named_range_cells(self, named_range_candidate: str) -> Union[str, None]:
        """
        If this is valid named range value, return the cell or range string specification

        :param named_range_candidate: str a name range string value
        """

    @abstractmethod
    def named_range_value(self, named_range_candidate: str) -> Union[str, None]:
        """
        If this is valid named range value, return the sheet and cell or range string specification

        :param named_range_candidate: str a name range string value
        """

    @abstractmethod
    def warn(self, msg: str):
        """
        Add a warning
        """

    @abstractmethod
    def specification_sheet_name(self):
        """
        Return the name of the sheet containing the table with the specification of the optimization problem
        """


# FIXME!!!!! move optional indicator to MType, track there
class CellType:
    def __init__(self, mtype: MType, optional=False):
        self.mtype = mtype
        self.optional = optional

    def same_math_type(self, other: CellType) -> bool:
        return isinstance(other, CellType) and self.mtype == other.mtype


class CellTypeParser(ABC):
    @staticmethod
    @abstractmethod
    def parse_type_args(row: int, col: int, scenario: ExcelData, cell_type_factory: CellTypeFactory, optional: bool
                        ) -> Optional[CellType]:
        """
        Parse the arguments to this type and return a completed type object

        :param optional:
        :param row: row containing type specification
        :param col: first column containing type specification
        :param scenario: the ``ExcelData`` object containing spreadsheet data
        :param cell_type_factory: factory that creates cell types
        :param optional: is this an optional type
        :return: a ``CellType`` object or ``None`` to indicate failure
        """


@intern
class BooleanCell(CellType, CellTypeParser):
    """
    A boolean cell type.
    """

    def __init__(self, optional=False):
        super().__init__(M_BOOLEAN, optional=optional)

    def __repr__(self):
        optional_str = 'Optional ' if self.optional else ''
        return f'<{optional_str}BooleanCell>'

    @staticmethod
    def parse_type_args(row: int, col: int, scenario: ExcelData, cell_type_factory: CellTypeFactory, optional
                        ) -> Optional[CellType]:
        return cell_type_factory.generate_cell_type('bool', optional=optional)


@intern
class IntegerCell(CellType, CellTypeParser):
    """
    An integer cell type with optional bounds.  A missing bound is indicated by ``None``.  Bounds are inclusive.
    """

    def __init__(self, lower_bound: Optional[int] = None, upper_bound: Optional[int] = None, optional=False):
        super().__init__(M_INT, optional=optional)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __repr__(self):
        optional_str = 'Optional ' if self.optional else ''
        return f'<{optional_str}IntegerCell({self.lower_bound}, {self.upper_bound})>'

    @staticmethod
    def parse_type_args(row: int, col: int, scenario: ExcelData, cell_type_factory: CellTypeFactory, optional
                        ) -> Optional[CellType]:
        lower_bound = scenario.cell_value(row, col + 1, int, empty_values='-')
        upper_bound = scenario.cell_value(row, col + 2, int, empty_values='-')
        return cell_type_factory.generate_cell_type('int', lower_bound, upper_bound, optional=optional)


class NonNegIntParser(CellTypeParser):
    @staticmethod
    def parse_type_args(row: int, col: int, scenario: ExcelData, cell_type_factory: CellTypeFactory, optional
                        ) -> Optional[CellType]:
        return cell_type_factory.generate_cell_type('int', 0, optional=optional)


@intern
class FloatCell(CellType, CellTypeParser):
    """
    A floating-point cell type with optional bounds.  A missing bound is indicated by ``None``.  Bounds are inclusive.
    """

    def __init__(self, lower_bound: Optional[float] = None, upper_bound: Optional[float] = None, optional=False):
        super().__init__(M_NUMBER, optional=optional)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __repr__(self):
        optional_str = 'Optional ' if self.optional else ''
        return f'<{optional_str}FloatCell({self.lower_bound}, {self.upper_bound})>'

    @staticmethod
    def parse_type_args(row: int, col: int, scenario: ExcelData, cell_type_factory: CellTypeFactory, optional
                        ) -> Optional[CellType]:
        lower_bound = scenario.cell_value(row, col + 1, (float, int), cast_to=float, empty_values='-')
        upper_bound = scenario.cell_value(row, col + 2, (float, int), cast_to=float, empty_values='-')
        return cell_type_factory.generate_cell_type('float', lower_bound, upper_bound, optional=optional)


class NonNegFloatParser(CellTypeParser):
    @staticmethod
    def parse_type_args(row: int, col: int, scenario: ExcelData, cell_type_factory: CellTypeFactory, optional
                        ) -> Optional[CellType]:
        return cell_type_factory.generate_cell_type('float', 0.0, optional=optional)


class StringCell(CellType, CellTypeParser):
    """
    A string cell type with an optional domain.  The domain is defined by a range of cells.
    """

    def __init__(self, domain: Optional[Cells] = None, optional=False):
        super().__init__(M_STRING, optional=optional)
        self.domain = domain

    def __eq__(self, other):
        return isinstance(other, StringCell) and self.domain == other.domain

    def __hash__(self):
        if self.domain is None:
            return 2284624
        return (3 * hash(self.domain.start_row) + 5 * hash(self.domain.end_row) +
                7 * hash(self.domain.start_col) + 11 * hash(self.domain.end_col))

    def __repr__(self):
        optional_str = 'Optional ' if self.optional else ''
        return f'<{optional_str}StringCell({self.domain})'

    @staticmethod
    def parse_type_args(row: int, col: int, scenario: ExcelData, cell_type_factory: CellTypeFactory, optional
                        ) -> Optional[CellType]:
        sources = scenario.cell_value(row, col + 1, str)
        if sources:
            source_cells = cell_to_expr(sources, scenario.specification_sheet_name())
            if isinstance(source_cells, Cell):
                source_cells = Cells(source_cells, source_cells)
        else:
            source_cells = None
        return cell_type_factory.generate_cell_type('string', source_cells, optional=optional)


class ClassCellType(CellType):
    """
    A cell type whose contents is a data structure, used for intermediates such as summing cells
    """

    def __init__(self, class_name: QualifiedName):
        super().__init__(MClassType(class_name), optional=False)


BOOLEAN_CELL_TYPE = BooleanCell()
INTEGER_CELL_TYPE = IntegerCell()


class CellTypeFactory:
    def __init__(self, cell_type_dict: Mapping[str, Type[CellType]]):
        self.cell_type_dict = cell_type_dict

    def generate_cell_type(self, type_name: str, *args, **kwargs) -> Optional[CellType]:
        """
        Return a new cell type based on the given arguments.  Override this to create more specific types.

        :param type_name: a string specifying a type, one of the keys of CELL_TYPES
        """
        constructor = self.cell_type_dict.get(type_name)
        if constructor is None:
            return None
        return constructor(*args, **kwargs)


@total_ordering
class CellReference:
    def __init__(self, row: int,
                 is_row_fixed: bool,
                 col: int,
                 is_col_fixed: bool,
                 sheet: str):
        self.row = row
        self.col = col
        self.is_row_fixed = is_row_fixed
        self.is_col_fixed = is_col_fixed
        self.sheet = sheet

    def _as_str(self, row, col) -> str:
        return f'{self.sheet}!' \
               f'{"$" if self.is_col_fixed else ""}{index_to_column(col)}' \
               f'{"$" if self.is_row_fixed else ""}{row}'

    def __eq__(self, o: object) -> bool:
        return isinstance(o, CellReference) and \
            (self.sheet, self.col, self.row, self.is_col_fixed, self.is_row_fixed) == (
                o.sheet, o.col, o.row, o.is_col_fixed, o.is_row_fixed)

    def __lt__(self, o: object) -> bool:
        if isinstance(o, CellReference):
            return isinstance(o, CellReference) and \
                (self.sheet, self.col, self.row, self.is_col_fixed, self.is_row_fixed) < (
                    o.sheet, o.col, o.row, o.is_col_fixed, o.is_row_fixed)

    def __hash__(self) -> int:
        return 7 * hash((self.sheet, self.row, self.col, self.is_col_fixed, self.is_row_fixed))

    def describe(self):
        return self._as_str(self.row, self.col)

    def __repr__(self) -> str:
        return self.describe()

    def __str__(self) -> str:
        return self.describe()

    def move(self, row, col) -> CellReference:
        new_row = self.row if self.is_row_fixed else row + self.row
        new_col = self.col if self.is_col_fixed else col + self.col
        return CellReference(new_row, self.is_row_fixed, new_col, self.is_col_fixed, self.sheet)
