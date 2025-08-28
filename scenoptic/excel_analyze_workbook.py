from dataclasses import dataclass

from typing import Sequence

from math_rep.expression_types import QualifiedName
from scenoptic.excel_analyze import check_compatible_formula
from scenoptic.excel_analyze_variability import VariabilityTree
from scenoptic.excel_data import CellReference
from scenoptic.excel_to_math import Scenario
from scenoptic.xl_utils import as_cell_qn


@dataclass
class CompatibleCells:
    origin: QualifiedName
    compatible_cells: Sequence[QualifiedName]
    variability: VariabilityTree
    cell_references: Sequence[CellReference]


class AnalyzeWorkbook:
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
        self.registry = dict()
        self.variability: VariabilityTree = None
        self.compatible_cells: Sequence[QualifiedName] = []
        self.cell_references: Sequence[CellReference] = None

    def describe(self):
        msg = ''
        nl = "\n"
        for key, value in self.registry.items():
            msg = msg + f'Origin Cell "{key}":{nl}' \
                        f'  Compatible Cells: {value.compatible_cells}{nl}' \
                        f'  Variability: {value.variability}{nl}' \
                        f'  Referenced Cells: {value.cell_references}{nl}'

        return msg

    def __repr__(self):
        return self.describe()

    def __str__(self):
        return self.describe()

    def _xl_column_range_elements(self, start_col, start_row, end_col, end_row, sheet):
        return ((i, j, as_cell_qn(i, j, sheet))
                for j in range(start_col, end_col + 1)
                for i in range(start_row, end_row + 1))

    def _store_origin(self,
                      origin_cell_qn: QualifiedName,
                      compatible_cells: Sequence[QualifiedName],
                      variability: VariabilityTree,
                      cell_references: Sequence[CellReference],
                      verbose=False):
        if origin_cell_qn is None or variability is None:
            return
        if self.registry.get(origin_cell_qn) is not None:
            raise AttributeError(f"Origin element {origin_cell_qn} already exists")
        self.registry[origin_cell_qn] = CompatibleCells(origin_cell_qn,
                                                        compatible_cells,
                                                        variability,
                                                        cell_references)
        if verbose:
            print(f'Compatible Cells : {self.registry[origin_cell_qn]}')
        self.variability = None
        self.cell_references = None
        self.compatible_cells = []

    def analyze(self, verbose=False):
        for sheet_name in self.scenario.wb.sheetnames:
            if verbose:
                print(f'Analyze sheet {sheet_name}')
            ws = self.scenario.wb[sheet_name]
            origin_qn = None
            for row, col, cur_cell_qn in self._xl_column_range_elements(1, 1, ws.max_column, ws.max_row, sheet_name):
                if verbose:
                    print(f'Cur Cell {cur_cell_qn}  Origin {origin_qn}')
                if self.scenario.get_type(cur_cell_qn) is None:
                    # The current cell is not registered as valid typed cell
                    self._store_origin(origin_qn, self.compatible_cells, self.variability, self.cell_references,
                                       verbose=verbose)
                    origin_qn = None
                    continue
                cur_value = self.scenario.cell_value(row, col, sheet=sheet_name)
                if cur_value is None:
                    # Empty cell, with no value is skipped.
                    self._store_origin(origin_qn, self.compatible_cells, self.variability, self.cell_references,
                                       verbose=verbose)
                    origin_qn = None
                    continue
                if origin_qn is None:
                    origin_qn = cur_cell_qn
                    continue
                if self.scenario.get_type(cur_cell_qn).same_math_type(self.scenario.get_type(origin_qn)):
                    result = check_compatible_formula(origin_qn.name,
                                                      cur_cell_qn.name,
                                                      self.scenario,
                                                      verbose=verbose)
                    if result is False:
                        # The formula are not compatible, set current cell as new origin
                        self._store_origin(origin_qn, self.compatible_cells, self.variability, self.cell_references,
                                           verbose=verbose)
                        origin_qn = cur_cell_qn
                        continue

                    self.variability, self.cell_references = result
                    self.compatible_cells.append(cur_cell_qn)
                else:
                    self._store_origin(origin_qn, self.compatible_cells, self.variability, self.cell_references,
                                       verbose=verbose)
                    origin_qn = cur_cell_qn

            self._store_origin(origin_qn, self.compatible_cells, self.variability, self.cell_references,
                               verbose=verbose)
