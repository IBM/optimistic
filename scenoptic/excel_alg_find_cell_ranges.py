from typing import Sequence, TypedDict, Tuple, Set, Callable, Any

import more_itertools

from scenoptic.excel_to_math import CellSpec


class RangeSpec(TypedDict):
    sheet: str
    start_row: int
    start_col: int
    end_row: int
    end_col: int


class FindCellRanges:
    """
    Implements algorithm for identifying rectangular continuous cell ranges.
    This algorithm expects a matrix data input, where cells with value 1  represent a cell with value
    that should be allocated, if possible, to a rectangular range with other cells with value 1.
    Cells with value 0, are not part of a range.

    The algorithm gives precedence to column wize continuous range.
    for instance:

    # 0 1 2 3 4 5 6 7  col/row

      0 0 1 1 1 1 0 0    #0
      0 0 1 1 1 1 0 0    #1
      0 0 0 0 1 0 0 0    #2
      0 0 0 0 0 0 0 0    #3

    The algorithm will identify ranges: (top_left_cell(start_row,start_col), bottom right cell(end_row,end_col)):
      range1=(0,2, 1,3)  range2=(0,4, 2,4)  range3=(0,5,  1,5)

     in the above example, the cell at (2,4) breaks the column wise range (0,2, 1,5) into the above ranges.
    """

    def __init__(self,
                 sheet: str,
                 matrix: Sequence[Sequence[int]] = None,
                 n_columns: int = None,
                 n_rows: int = None):
        self.sheet = sheet
        self.matrix = matrix
        self.number_of_columns = n_columns or len(self.matrix[0])
        self.number_of_rows = n_rows or len(self.matrix)
        self.total_expected_cells_area = 0
        self.ranges = []
        self.cur_range_area = 0

    def _build(self):
        # Compute total expected rectangle area
        for i in range(self.number_of_columns):
            for j in range(self.number_of_rows):
                self.total_expected_cells_area += 1 if (self.matrix[j][i] > 0) else 0

    def analyze(self,
                verbose: bool = False) -> Sequence[RangeSpec]:
        self._build()

        while self.cur_range_area < self.total_expected_cells_area:
            rect = self._find_next_range()
            self.ranges.append(rect)
            self._mark_range_as_found(rect['start_col'], rect['start_row'], rect['end_col'], rect['end_row'])
            self.cur_range_area += (rect['end_col'] - rect['start_col'] + 1) * (rect['end_row'] - rect['start_row'] + 1)

        if verbose:
            print(self.ranges)
        return self.ranges

    def _mark_range_as_found(self, start_col: int, start_row: int, end_col: int, end_row: int):
        for i in range(start_col, end_col + 1):
            for j in range(start_row, end_row + 1):
                self.matrix[j][i] = 2

    def _is_cell_active(self, row: int, col: int) -> bool:
        return self.matrix[row][col] == 1

    def _find_next_range(self) -> RangeSpec:
        # find top left corner
        found_top_left_corner = False
        candidate = dict(sheet=self.sheet,
                         start_row=0,
                         start_col=0,
                         end_row=self.number_of_rows - 1,
                         end_col=self.number_of_columns - 1)
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                if self._is_cell_active(i, j):
                    candidate['start_col'] = j
                    candidate['start_row'] = i
                    found_top_left_corner = True
                    break

            if found_top_left_corner:
                break

        for i in range(candidate['start_row'], candidate['end_row'] + 1):
            if not self._is_cell_active(i, candidate['start_col']):
                candidate['end_row'] = i - 1
                for k in range(candidate['start_col'], candidate['end_col'] + 1):
                    if self._is_cell_active(i, k):
                        candidate['end_col'] = k - 1
                        return candidate
                return candidate
            for j in range(candidate['start_col'], candidate['end_col'] + 1):
                if not self._is_cell_active(i, j):
                    candidate['end_col'] = j - 1
                    break
        return candidate


class FindCellRangesByTuples(FindCellRanges):
    """
    The same algorithm as above, only the expected input is the sparse matrix, defined as unique set
    of tuples each with the (row, col) value of the cells with value 1 above.

    The above matrix

    # 0 1 2 3 4 5 6 7  col/row

      0 0 1 1 1 1 0 0    #0
      0 0 1 1 1 1 0 0    #1
      0 0 0 0 1 0 0 0    #2
      0 0 0 0 0 0 0 0    #3

    will be represented as :
    data = ( (0,2) (0,3) (0,4) (0,5) (1,2) (1,3) (1,4) (1,5) (2,4))

    """

    def __init__(self,
                 sheet: str,
                 data: Set[Tuple[int, int]]):
        super().__init__(sheet=sheet,
                         n_columns=max(data, key=lambda tup: tup[1])[1] + 1,
                         n_rows=max(data, key=lambda tup: tup[0])[0] + 1)
        self.data = data

    def _build(self):
        self.total_expected_cells_area = len(self.data)

    def _mark_range_as_found(self, start_col: int, start_row: int, end_col: int, end_row: int):
        drop_marked = set()
        for i in range(start_col, end_col + 1):
            for j in range(start_row, end_row + 1):
                drop_marked.add((j, i))

        self.data = self.data - drop_marked

    def _is_cell_active(self, row: int, col: int) -> bool:
        return (row, col) in self.data


class AnalyzeCellRanges:
    """
    Wrapper handler for analyzing cell ranges,
    The expected input is a unique set of tuples, with the following elements:
    ( sheet_name, row_index, col_index) :  Tuple[str, int, int]

    The analysis traverse the set of tuples, group them by:
    1. Sheet names.
    2. if each cell apply to all predicates provided during initialization

    A predicate is a function that should accept a cell tuple, and return True/False
    True value indicates that the cell should participate in the range analysis
      def predicate(cell: Tuple[str, int, int]) -> bool
    """

    def __init__(self, *predicates):
        self.predicates = predicates

    @staticmethod
    def is_same_sheet(cell: Tuple[str, int, int], sheet: str):
        return cell[0] == sheet

    def _is_ok(self, cell: Tuple[str, int, int]):
        return all(p(cell) for p in self.predicates)

    def analyze_by_category(self,
                            candidates: Set[Tuple[str, int, int]],
                            # Accepts CellRef, and returns a category consisting of tuple of any number of objects
                            category_func: Callable[[Tuple[str, int, int]], Tuple[Any, ...]]
                            ) -> \
            Tuple[Sequence[Tuple[CellSpec, Tuple[Any, ...]]], Sequence[Tuple[RangeSpec, Tuple[Any, ...]]]]:
        unique_sheets = {e[0] for e in candidates}
        unique_categories = {category_func(e) for e in candidates}
        ranges = []
        cells = []
        for u_sheet in unique_sheets:
            for category in unique_categories:
                sheet_candidates = {cell[1:3] for cell in candidates if
                                    self.is_same_sheet(cell, u_sheet) and category == category_func(cell)}

                if not sheet_candidates:
                    continue

                find = FindCellRangesByTuples(sheet=u_sheet,
                                              data=sheet_candidates)
                result = find.analyze()
                only_ranges, only_cells = more_itertools.partition(
                    lambda r: r['start_row'] == r['end_row'] and r['start_col'] == r['end_col'],
                    result)

                only_cells = tuple(dict(sheet=u_sheet, row=r['start_row'], col=r['start_col']) for r in only_cells)
                if only_cells:
                    cells = [*cells, (only_cells, category)]
                only_ranges = tuple(only_ranges)
                if only_ranges:
                    ranges = [*ranges, (only_ranges, category)]
        return cells, ranges

    def analyze_by_predicate(self, candidates: Set[Tuple[str, int, int]]) -> Tuple[
        Sequence[CellSpec], Sequence[RangeSpec]]:
        unique_sheets = {e[0] for e in candidates}
        ranges = []
        cells = []
        for u_sheet in unique_sheets:
            sheet_candidates = {cell[1:3] for cell in candidates if
                                self.is_same_sheet(cell, u_sheet) and self._is_ok(cell)}
            find = FindCellRangesByTuples(sheet=u_sheet,
                                          data=sheet_candidates)
            result = find.analyze()
            only_ranges, only_cells = more_itertools.partition(
                lambda r: r['start_row'] == r['end_row'] and r['start_col'] == r['end_col'],
                result)
            cells = [*cells, *(dict(sheet=u_sheet, row=r['start_row'], col=r['start_col']) for r in only_cells)]
            ranges = [*ranges, *only_ranges]
            # only_cells = [dict(sheet=u_sheet, row=r['start_row'], col=r['start_col']) for r in result if
            #               r['start_row'] == r['end_row'] and r['start_col'] == r['end_col']]
            # cells = [*cells, *only_cells]
            # ranges = [*ranges, *(r for r in result if r['start_row'] != r['end_row'] or r['start_col'] != r['end_col'])]

        return cells, ranges
