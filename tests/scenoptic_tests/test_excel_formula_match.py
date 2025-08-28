from argparse import ArgumentParser
from pathlib import Path
from typing import Tuple, Set

from math_rep.domain_analysis import DomainTable
from math_rep.expr import FormalContent
from rewriting.rules import exhaustively_apply_rules
from scenoptic.excel_analyze import check_compatible_formula, bind_cell_variability, get_cell, get_content
from scenoptic.excel_to_math import Scenario, Constraint
from scenoptic import EXCEL_RULES0A, EXCEL_RULES0B
from scenoptic.parse_excel import parse_formula_with_variability
from scenoptic.xl_utils import as_cell_qn


class ScenarioTest(Scenario):

    def __init__(self, excel_file, sheet: str = None):
        super().__init__(excel_file, sheet)

    def validate_initialization(self):
        pass

    def cell_to_constraint(self, cell: str, contents: str, domain_table: DomainTable = None) -> Tuple[Constraint, Set]:
        pass

    def convert_to_language(self, expression: FormalContent):
        pass


default_excel_file = (
    (Path(__file__).joinpath(
        r'../../scenoptic_examples/user_stories/formula-experiments.xlsx')))
default_sheet = "Spec"

default_scenario = ScenarioTest(default_excel_file, default_sheet)

NUM_TEST = 30
index = (i for i in range(NUM_TEST))
last_index = -1

candidates = {
    # OK
    0: dict(root="Problem!K2", second="Problem!K3"),
    # Cell H2 does not contain a formula
    1: dict(root="Problem!G2", second="Problem!H2"),
    # Exception: Child[0] has different parser context CellRefContext vs NamedRangeContext
    2: dict(root="Problem!G2", second="Problem!I2"),
    # Exception: Cells are not compatible "$B$2@34:37" and "$B$3@34:37"
    3: dict(root="Problem!L2", second="Problem!L6"),
    # Exception: Nodes of "PrefixContext" have different values "location_params!@18:33" and "inventory!@18:27"
    4: dict(root="Problem!L2", second="Problem!L3"),
    # Exception: Nodes of "FunctionContext" have different values "SUMIF@1:5" and "COUNIFS@1:7"
    5: dict(root="inventory!C2", second="inventory!C5"),
    # Exception: Nodes of "Named_rangeContext" have different values "Inventory@30:38" and "Inventories@30:40"
    6: dict(root="inventory!F2", second="inventory!F6"),
    # Exception: Nodes of "ConstantContext" have different values "" <> 1"@17:21" and "" > 2"@17:20"
    7: dict(root="inventory!G2", second="inventory!G4"),
    # Exception: Nodes of "AdditiveOpContext" have different values "+@12:12" and "-@12:12"
    8: dict(root="Problem!Q5", second="Problem!Q6"),
    # OK, do not include fixed cells
    9: dict(root="inventory!C2", second="inventory!C3"),
    # OK,
    10: dict(root="inventory!K2", second="inventory!K3"),
    # OK, Cells are in sibling columns,
    11: dict(root="inventory!K2", second="inventory!L2"),
    # OK, Cells are in sibling columns, diagonal
    12: dict(root="inventory!K2", second="inventory!L3"),
    # OK, Cells are in sibling columns, reverse diagonal
    13: dict(root="inventory!K3", second="inventory!L2"),
    # OK, Cells are in sibling columns, 2 rows diagonal
    14: dict(root="inventory!K2", second="inventory!L4"),
    # Exception: Cells are not compatible "H2@5:6" and "I6@5:6"
    # Reason, input distance (row, colum)= (1, 3) while row 6-2 = 4(Fail) , column I-H = 1(OK)
    15: dict(root="inventory!K2", second="inventory!L5"),
    # Exception: Cells are not compatible "H2@5:6" and "H6@5:6"
    # Reason, input distance (row, colum)= (1, 4) while row 6-2 = 4(OK) , column H-H = 0(FAIL)
    16: dict(root="inventory!K2", second="inventory!L6"),
    # OK, cells are fixed and identical, empty ledger
    17: dict(root="inventory!M2", second="inventory!M3"),
    # OK, cells 1 row apart, first operand column is fixed, second operand row is fixed
    18: dict(root="inventory!N2", second="inventory!N3"),
    # OK, cells 2 rows apart, first operand column is fixed, second operand row is fixed
    19: dict(root="inventory!N2", second="inventory!N4"),
    # OK, cells 1 col apart, first operand column is fixed, second operand row is fixed
    20: dict(root="inventory!N2", second="inventory!O2"),
    # OK, cells 1 col 1 rows apart, first operand column is fixed, second operand row is fixed
    21: dict(root="inventory!N2", second="inventory!O3"),
    # OK, Range have partial fixed cell
    22: dict(root="inventory!G12", second="inventory!G13"),
    # OK, cells 1 col 1 rows apart, Single range cell have partial fixed cell
    23: dict(root="inventory!G12", second="inventory!H13"),
    # OK, cells 1 col 1 rows apart, both Range cells have partial fixed cell
    24: dict(root="inventory!I12", second="inventory!J13"),
    # OK, cells 0 col 1 rows apart, both Range cells have partial fixed cell
    25: dict(root="inventory!I12", second="inventory!I13"),
}


def run_all_formula_match(scenario: Scenario):
    global index, last_index
    index = (i for i in range(NUM_TEST))
    last_index = -1
    for t in candidates.keys():
        variability = formula_compatibility(candidates[t]['root'],
                                            candidates[t]['second'],
                                            scenario or default_scenario,
                                            verbose=True)

        if variability is not False:
            binding = bind_cell_variability(candidates[t]['root'],
                                            variability,
                                            scenario or default_scenario,
                                            verbose=True)
            print(f'binding: {binding}')


def run_all_formula_expr(scenario: Scenario, *, indexes=None, verbose=True):
    for t in indexes or candidates.keys():
        print(formula_expression(t, scenario, verbose=verbose))


def formula_expression(t: int, scenario: Scenario, verbose=True):
    variability = formula_compatibility(candidates[t]['root'],
                                        candidates[t]['second'],
                                        scenario or default_scenario,
                                        verbose=verbose,
                                        index=t)

    origin_cell_spec = get_cell(candidates[t]['root'])
    origin_qn = as_cell_qn(origin_cell_spec['row'], origin_cell_spec['col'], origin_cell_spec['sheet'])
    origin_content = get_content(origin_cell_spec, scenario)
    expr0 = parse_formula_with_variability(formula=origin_content,
                                           scenario=scenario,
                                           current_sheet_name=origin_cell_spec['sheet'],
                                           origin_cell_qn=origin_qn,
                                           variability=variability)
    domain_table = None
    # FIXME!!!! add this
    # subexpression_splitter = IncrementalsSplitter(expr0, cell.name)
    # expr1 = exhaustively_apply_rules(subexpression_splitter, expr0, domain_table)
    expr1 = expr0
    expr2 = exhaustively_apply_rules(EXCEL_RULES0A, expr1, domain_table)
    expr3 = exhaustively_apply_rules(EXCEL_RULES0B, expr2, domain_table)
    if verbose:
        print(f'Cell-expr0 "{origin_qn}" :: {expr0}')
        print(f'Cell-expr2 "{origin_qn}" :: {expr3}')
    return expr3


def formula_compatibility(root, second, scenario, index: int = -1, verbose=True):
    if verbose:
        print(f'Test {index}:')
    result = check_compatible_formula(root, second, scenario, verbose=verbose)
    if result is False or result is True:
        return result
    return result[0]


def formula_helper(candidate: int, verbose=False):
    result = check_compatible_formula(*candidates.get(candidate).values(),
                                      default_scenario,
                                      verbose=verbose)
    if result is False or result is True:
        pass
    else:
        result = result[0]
    return candidates.get(candidate)['root'], result


def test_formula_compatibility():
    """
    >>> formula_compatibility(*candidates.get(0).values(), scenario=default_scenario, index=0, verbose=True)
    Test 0:
    Cell{'sheet': 'Problem', 'row': 2, 'col': 11}  =IF(C2<E2,E2-C2,0)
    Cell{'sheet': 'Problem', 'row': 3, 'col': 11}  =IF(C3<E3,E3-C3,0)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): Problem!C2, (1, 0, 2, 0, 2, 0, 0, 0): Problem!E2, (1, 0, 2, 2, 0, 0, 0, 0): Problem!E2, (1, 0, 2, 2, 2, 0, 0, 0): Problem!C2}
    variability = {(1, 0, 2, 2, 0, 0, 0, 0), (1, 0, 2, 0, 2, 0, 0, 0), (1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 2, 2, 0, 0, 0)}
    Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (Problem!C2) -> ()))),2 -> (0 -> (0 -> (0: (Problem!E2) -> ())))),2 -> (0 -> (0 -> (0 -> (0: (Problem!E2) -> ()))),2 -> (0 -> (0 -> (0: (Problem!C2) -> ()))))))))
    >>> formula_compatibility(*candidates.get(1).values(), scenario=default_scenario, index=1, verbose=True)
    Test 1:
    Cell{'sheet': 'Problem', 'row': 2, 'col': 7}  =C2
    False
    >>> formula_compatibility(*candidates.get(2).values(), scenario=default_scenario, index=2, verbose=True)
    Test 2:
    Cell{'sheet': 'Problem', 'row': 2, 'col': 7}  =C2
    Cell{'sheet': 'Problem', 'row': 2, 'col': 9}  =namrang
    FormulaMatchException: RuleNode with different parser context CellRefContext vs NamedRangeContext
    False
    >>> formula_compatibility(*candidates.get(3).values(), scenario=default_scenario, index=3, verbose=True)
    Test 3:
    Cell{'sheet': 'Problem', 'row': 2, 'col': 12}  =IF(C2<E2,(E2-C2)*location_params!$B$2,0)
    Cell{'sheet': 'Problem', 'row': 6, 'col': 12}  =IF(C6<E6,(E6-C6)*location_params!$B$3,0)
    FormulaMatchException: Cells are not compatible "$B$2@34:37" and "$B$3@34:37"
    False
    >>> formula_compatibility(*candidates.get(4).values(), scenario=default_scenario, index=4, verbose=True)
    Test 4:
    Cell{'sheet': 'Problem', 'row': 2, 'col': 12}  =IF(C2<E2,(E2-C2)*location_params!$B$2,0)
    Cell{'sheet': 'Problem', 'row': 3, 'col': 12}  =IF(C3<E3,(E3-C3)*inventory!$B$2,0)
    FormulaMatchException: Nodes of "PrefixContext" have different values "location_params!@18:33" and "inventory!@18:27"
    False
    >>> formula_compatibility(*candidates.get(5).values(), scenario=default_scenario, index=5, verbose=True)
    Test 5:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 3}  =SUMIF(Problem!$B$2:$B$6,inventory!A2, Problem!$C$2:$C$6)
    Cell{'sheet': 'inventory', 'row': 5, 'col': 3}  =COUNIFS(Problem!$B$2:$B$6,inventory!A5, Problem!$C$2:$C$6)
    FormulaMatchException: Nodes of "FunctionContext" have different values "SUMIF@1:5" and "COUNIFS@1:7"
    False
    >>> formula_compatibility(*candidates.get(6).values(), scenario=default_scenario, index=6, verbose=True)
    Test 6:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 6}  =SUMIF(products,inventory!A2, Inventory)
    Cell{'sheet': 'inventory', 'row': 6, 'col': 6}  =SUMIF(products,inventory!A6, Inventories)
    FormulaMatchException: Nodes of "Named_rangeContext" have different values "Inventory@30:38" and "Inventories@30:40"
    False
    >>> formula_compatibility(*candidates.get(7).values(), scenario=default_scenario, index=7, verbose=True)
    Test 7:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 7}  =SUMIF($B$2:$B$6,"<>1",$C$2)
    Cell{'sheet': 'inventory', 'row': 4, 'col': 7}  =SUMIF($B$2:$B$6,">2",$C$2)
    FormulaMatchException: Nodes of "ConstantContext" have different values ""<>1"@17:21" and "">2"@17:20"
    False
    >>> formula_compatibility(*candidates.get(8).values(), scenario=default_scenario, index=8, verbose=True)
    Test 8:
    Cell{'sheet': 'Problem', 'row': 5, 'col': 17}  =SUM(J5:J6) + K5*D5
    Cell{'sheet': 'Problem', 'row': 6, 'col': 17}  =SUM(J6:J7) - K6*D6
    FormulaMatchException: Nodes of "AdditiveOpContext" have different values "+@12:12" and "-@12:12"
    False
    >>> formula_compatibility(*candidates.get(9).values(), scenario=default_scenario, index=9, verbose=True)
    Test 9:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 3}  =SUMIF(Problem!$B$2:$B$6,inventory!A2, Problem!$C$2:$C$6)
    Cell{'sheet': 'inventory', 'row': 3, 'col': 3}  =SUMIF(Problem!$B$2:$B$6,inventory!A3, Problem!$C$2:$C$6)
    Results = {(1, 0, 2, 2, 0, 1, 0): inventory!A2}
    variability = {(1, 0, 2, 2, 0, 1, 0)}
    Start -> (1 -> (0 -> (2 -> (2 -> (0 -> (1 -> (0: (inventory!A2) -> ())))))))
    >>> formula_compatibility(*candidates.get(10).values(), scenario=default_scenario, index=10, verbose=True)
    Test 10:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 3, 'col': 11}  =SUM(H3:I3)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!H2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!I2}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (inventory!H2) -> ())),2 -> (0 -> (0: (inventory!I2) -> ()))))))))
    >>> formula_compatibility(*candidates.get(11).values(), scenario=default_scenario, index=11, verbose=True)
    Test 11:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 2, 'col': 12}  =SUM(I2:J2)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!H2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!I2}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (inventory!H2) -> ())),2 -> (0 -> (0: (inventory!I2) -> ()))))))))
    >>> formula_compatibility(*candidates.get(12).values(), scenario=default_scenario, index=12, verbose=True)
    Test 12:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 3, 'col': 12}  =SUM(I3:J3)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!H2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!I2}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (inventory!H2) -> ())),2 -> (0 -> (0: (inventory!I2) -> ()))))))))
    >>> formula_compatibility(*candidates.get(13).values(), scenario=default_scenario, index=13, verbose=True)
    Test 13:
    Cell{'sheet': 'inventory', 'row': 3, 'col': 11}  =SUM(H3:I3)
    Cell{'sheet': 'inventory', 'row': 2, 'col': 12}  =SUM(I2:J2)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!H3, (1, 0, 2, 0, 0, 2, 0, 0): inventory!I3}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (inventory!H3) -> ())),2 -> (0 -> (0: (inventory!I3) -> ()))))))))
    >>> formula_compatibility(*candidates.get(14).values(), scenario=default_scenario, index=14, verbose=True)
    Test 14:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 4, 'col': 12}  =SUM(I4:J4)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!H2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!I2}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (inventory!H2) -> ())),2 -> (0 -> (0: (inventory!I2) -> ()))))))))
    >>> formula_compatibility(*candidates.get(15).values(), scenario=default_scenario, index=15, verbose=True)
    Test 15:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 5, 'col': 12}  =SUM(I6:J6)
    FormulaMatchException: Cells are not compatible "H2@5:6" and "I6@5:6"
    False
    >>> formula_compatibility(*candidates.get(16).values(), scenario=default_scenario, index=16, verbose=True)
    Test 16:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 6, 'col': 12}  =SUM(H6:I6)
    FormulaMatchException: Cells are not compatible "H2@5:6" and "H6@5:6"
    False
    >>> formula_compatibility(*candidates.get(17).values(), scenario=default_scenario, index=17, verbose=True)
    Test 17:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 13}  =SUM($H$2+$I$2)
    Cell{'sheet': 'inventory', 'row': 3, 'col': 13}  =SUM($H$2+$I$2)
    Results = {}
    variability = set()
    Start -> ()
    >>> formula_compatibility(*candidates.get(18).values(), scenario=default_scenario, index=18, verbose=True)
    Test 18:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 14}  =$H2+I$4
    Cell{'sheet': 'inventory', 'row': 3, 'col': 14}  =$H3+I$4
    Results = {(1, 0, 0, 0, 0): inventory!$H2, (1, 2, 0, 0, 0): inventory!I$4}
    variability = {(1, 0, 0, 0, 0), (1, 2, 0, 0, 0)}
    Start -> (1 -> (0 -> (0 -> (0 -> (0: (inventory!$H2) -> ()))),2 -> (0 -> (0 -> (0: (inventory!I$4) -> ())))))
    >>> formula_compatibility(*candidates.get(19).values(), scenario=default_scenario, index=19, verbose=True)
    Test 19:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 14}  =$H2+I$4
    Cell{'sheet': 'inventory', 'row': 4, 'col': 14}  =$H4+I$4
    Results = {(1, 0, 0, 0, 0): inventory!$H2, (1, 2, 0, 0, 0): inventory!I$4}
    variability = {(1, 0, 0, 0, 0), (1, 2, 0, 0, 0)}
    Start -> (1 -> (0 -> (0 -> (0 -> (0: (inventory!$H2) -> ()))),2 -> (0 -> (0 -> (0: (inventory!I$4) -> ())))))
    >>> formula_compatibility(*candidates.get(20).values(), scenario=default_scenario, index=20, verbose=True)
    Test 20:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 14}  =$H2+I$4
    Cell{'sheet': 'inventory', 'row': 2, 'col': 15}  =$H2+J$4
    Results = {(1, 0, 0, 0, 0): inventory!$H2, (1, 2, 0, 0, 0): inventory!I$4}
    variability = {(1, 0, 0, 0, 0), (1, 2, 0, 0, 0)}
    Start -> (1 -> (0 -> (0 -> (0 -> (0: (inventory!$H2) -> ()))),2 -> (0 -> (0 -> (0: (inventory!I$4) -> ())))))
    >>> formula_compatibility(*candidates.get(21).values(), scenario=default_scenario, index=21, verbose=True)
    Test 21:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 14}  =$H2+I$4
    Cell{'sheet': 'inventory', 'row': 3, 'col': 15}  =$H3+J$4
    Results = {(1, 0, 0, 0, 0): inventory!$H2, (1, 2, 0, 0, 0): inventory!I$4}
    variability = {(1, 0, 0, 0, 0), (1, 2, 0, 0, 0)}
    Start -> (1 -> (0 -> (0 -> (0 -> (0: (inventory!$H2) -> ()))),2 -> (0 -> (0 -> (0: (inventory!I$4) -> ())))))
    >>> formula_compatibility(*candidates.get(22).values(), scenario=default_scenario, index=22, verbose=True)
    Test 22:
    Cell{'sheet': 'inventory', 'row': 12, 'col': 7}  =SUM(B$2:C3)
    Cell{'sheet': 'inventory', 'row': 13, 'col': 7}  =SUM(B$2:C4)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!B$2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!C3}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (inventory!B$2) -> ())),2 -> (0 -> (0: (inventory!C3) -> ()))))))))
    >>> formula_compatibility(*candidates.get(23).values(), scenario=default_scenario, index=23, verbose=True)
    Test 23:
    Cell{'sheet': 'inventory', 'row': 12, 'col': 7}  =SUM(B$2:C3)
    Cell{'sheet': 'inventory', 'row': 13, 'col': 8}  =SUM(C$2:D4)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!B$2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!C3}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (inventory!B$2) -> ())),2 -> (0 -> (0: (inventory!C3) -> ()))))))))
    >>> formula_compatibility(*candidates.get(24).values(), scenario=default_scenario, index=24, verbose=True)
    Test 24:
    Cell{'sheet': 'inventory', 'row': 12, 'col': 9}  =SUM(C$2:D$3)
    Cell{'sheet': 'inventory', 'row': 13, 'col': 10}  =SUM(D$2:E$3)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!C$2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!D$3}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (inventory!C$2) -> ())),2 -> (0 -> (0: (inventory!D$3) -> ()))))))))
    >>> formula_compatibility(*candidates.get(25).values(), scenario=default_scenario, index=25, verbose=True)
    Test 25:
    Cell{'sheet': 'inventory', 'row': 12, 'col': 9}  =SUM(C$2:D$3)
    Cell{'sheet': 'inventory', 'row': 13, 'col': 9}  =SUM(C$2:D$3)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!C$2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!D$3}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (inventory!C$2) -> ())),2 -> (0 -> (0: (inventory!D$3) -> ()))))))))
    """


def test_binding_cell_variability():
    """
    >>> print(bind_cell_variability(*formula_helper(0), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(1), scenario=default_scenario, verbose=False) is False)
    True
    >>> print(bind_cell_variability(*formula_helper(2), scenario=default_scenario, verbose=False) is False)
    True
    >>> print(bind_cell_variability(*formula_helper(3), scenario=default_scenario, verbose=False) is False)
    True
    >>> print(bind_cell_variability(*formula_helper(4), scenario=default_scenario, verbose=False) is False)
    True
    >>> print(bind_cell_variability(*formula_helper(5), scenario=default_scenario, verbose=False) is False)
    True
    >>> print(bind_cell_variability(*formula_helper(6), scenario=default_scenario, verbose=False) is False)
    True
    >>> print(bind_cell_variability(*formula_helper(7), scenario=default_scenario, verbose=False) is False)
    True
    >>> print(bind_cell_variability(*formula_helper(8), scenario=default_scenario, verbose=False) is False)
    True
    >>> print(bind_cell_variability(*formula_helper(9), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(10), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(11), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(12), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(13), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(14), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(15), scenario=default_scenario, verbose=False) is False)
    True
    >>> print(bind_cell_variability(*formula_helper(16), scenario=default_scenario, verbose=False) is False)
    True
    >>> print(bind_cell_variability(*formula_helper(17), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(18), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(19), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(20), scenario=default_scenario, verbose=False) is False)
    False
    >>> print(bind_cell_variability(*formula_helper(21), scenario=default_scenario, verbose=False) is False)
    False
    """


def test_formula_expression():
    """
    >>> formula_expression(0, scenario=default_scenario, verbose=True)
    Test 0:
    Cell{'sheet': 'Problem', 'row': 2, 'col': 11}  =IF(C2<E2,E2-C2,0)
    Cell{'sheet': 'Problem', 'row': 3, 'col': 11}  =IF(C3<E3,E3-C3,0)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): Problem!C2, (1, 0, 2, 0, 2, 0, 0, 0): Problem!E2, (1, 0, 2, 2, 0, 0, 0, 0): Problem!E2, (1, 0, 2, 2, 2, 0, 0, 0): Problem!C2}
    variability = {(1, 0, 2, 2, 0, 0, 0, 0), (1, 0, 2, 0, 2, 0, 0, 0), (1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 2, 2, 0, 0, 0)}
    Cell-expr0 "*worksheet*.Problem.Problem!K2" :: (v1, v2) -> IF($v1 < $v2, -($v2, $v1), 0)
    Cell-expr2 "*worksheet*.Problem.Problem!K2" :: (v1, v2) -> $v1 < $v2 ? $v2 - $v1 : 0
    (v1, v2) -> $v1 < $v2 ? $v2 - $v1 : 0
    >>> formula_expression(1, scenario=default_scenario, verbose=True)
    Test 1:
    Cell{'sheet': 'Problem', 'row': 2, 'col': 7}  =C2
    Cell-expr0 "*worksheet*.Problem.Problem!G2" :: #Problem!C2
    Cell-expr2 "*worksheet*.Problem.Problem!G2" :: #Problem!C2
    #Problem!C2
    >>> formula_expression(2, scenario=default_scenario, verbose=True)
    Test 2:
    Cell{'sheet': 'Problem', 'row': 2, 'col': 7}  =C2
    Cell{'sheet': 'Problem', 'row': 2, 'col': 9}  =namrang
    FormulaMatchException: RuleNode with different parser context CellRefContext vs NamedRangeContext
    Cell-expr0 "*worksheet*.Problem.Problem!G2" :: #Problem!C2
    Cell-expr2 "*worksheet*.Problem.Problem!G2" :: #Problem!C2
    #Problem!C2
    >>> formula_expression(3, scenario=default_scenario, verbose=True)
    Test 3:
    Cell{'sheet': 'Problem', 'row': 2, 'col': 12}  =IF(C2<E2,(E2-C2)*location_params!$B$2,0)
    Cell{'sheet': 'Problem', 'row': 6, 'col': 12}  =IF(C6<E6,(E6-C6)*location_params!$B$3,0)
    FormulaMatchException: Cells are not compatible "$B$2@34:37" and "$B$3@34:37"
    Cell-expr0 "*worksheet*.Problem.Problem!L2" :: IF(#Problem!C2 < #Problem!E2, *(-(#Problem!E2, #Problem!C2), #location_params!B2), 0)
    Cell-expr2 "*worksheet*.Problem.Problem!L2" :: #Problem!C2 < #Problem!E2 ? (#Problem!E2 - #Problem!C2) * #location_params!B2 : 0
    #Problem!C2 < #Problem!E2 ? (#Problem!E2 - #Problem!C2) * #location_params!B2 : 0
    >>> formula_expression(4, scenario=default_scenario, verbose=True)
    Test 4:
    Cell{'sheet': 'Problem', 'row': 2, 'col': 12}  =IF(C2<E2,(E2-C2)*location_params!$B$2,0)
    Cell{'sheet': 'Problem', 'row': 3, 'col': 12}  =IF(C3<E3,(E3-C3)*inventory!$B$2,0)
    FormulaMatchException: Nodes of "PrefixContext" have different values "location_params!@18:33" and "inventory!@18:27"
    Cell-expr0 "*worksheet*.Problem.Problem!L2" :: IF(#Problem!C2 < #Problem!E2, *(-(#Problem!E2, #Problem!C2), #location_params!B2), 0)
    Cell-expr2 "*worksheet*.Problem.Problem!L2" :: #Problem!C2 < #Problem!E2 ? (#Problem!E2 - #Problem!C2) * #location_params!B2 : 0
    #Problem!C2 < #Problem!E2 ? (#Problem!E2 - #Problem!C2) * #location_params!B2 : 0
    >>> formula_expression(5, scenario=default_scenario, verbose=True)
    Test 5:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 3}  =SUMIF(Problem!$B$2:$B$6,inventory!A2, Problem!$C$2:$C$6)
    Cell{'sheet': 'inventory', 'row': 5, 'col': 3}  =COUNIFS(Problem!$B$2:$B$6,inventory!A5, Problem!$C$2:$C$6)
    FormulaMatchException: Nodes of "FunctionContext" have different values "SUMIF@1:5" and "COUNIFS@1:7"
    Cell-expr0 "*worksheet*.inventory.inventory!C2" :: SUMIF(#Problem!B2:Problem!B6, #inventory!A2, #Problem!C2:Problem!C6)
    Cell-expr2 "*worksheet*.inventory.inventory!C2" :: Σ $cell FOR cell, cond IN zip(#Problem!C2:Problem!C6, #Problem!B2:Problem!B6) S.T. #inventory!A2 = $cond
    Σ $cell FOR cell, cond IN zip(#Problem!C2:Problem!C6, #Problem!B2:Problem!B6) S.T. #inventory!A2 = $cond
    >>> formula_expression(6, scenario=default_scenario, verbose=True)
    Test 6:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 6}  =SUMIF(products,inventory!A2, Inventory)
    Cell{'sheet': 'inventory', 'row': 6, 'col': 6}  =SUMIF(products,inventory!A6, Inventories)
    FormulaMatchException: Nodes of "Named_rangeContext" have different values "Inventory@30:38" and "Inventories@30:40"
    Cell-expr0 "*worksheet*.inventory.inventory!F2" :: SUMIF(#Problem!B2:Problem!B6, #inventory!A2, #Problem!C2:Problem!C6)
    Cell-expr2 "*worksheet*.inventory.inventory!F2" :: Σ $cell FOR cell, cond IN zip(#Problem!C2:Problem!C6, #Problem!B2:Problem!B6) S.T. #inventory!A2 = $cond
    Σ $cell FOR cell, cond IN zip(#Problem!C2:Problem!C6, #Problem!B2:Problem!B6) S.T. #inventory!A2 = $cond
    >>> formula_expression(7, scenario=default_scenario, verbose=True)
    Test 7:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 7}  =SUMIF($B$2:$B$6,"<>1",$C$2)
    Cell{'sheet': 'inventory', 'row': 4, 'col': 7}  =SUMIF($B$2:$B$6,">2",$C$2)
    FormulaMatchException: Nodes of "ConstantContext" have different values ""<>1"@17:21" and "">2"@17:20"
    Cell-expr0 "*worksheet*.inventory.inventory!G2" :: SUMIF(#inventory!B2:inventory!B6, "<>1", #inventory!C2)
    Cell-expr2 "*worksheet*.inventory.inventory!G2" :: Σ $cell FOR cell, cond IN zip(#inventory!C2, #inventory!B2:inventory!B6) S.T. $cond ≠ 1
    Σ $cell FOR cell, cond IN zip(#inventory!C2, #inventory!B2:inventory!B6) S.T. $cond ≠ 1
    >>> formula_expression(8, scenario=default_scenario, verbose=True)
    Test 8:
    Cell{'sheet': 'Problem', 'row': 5, 'col': 17}  =SUM(J5:J6) + K5*D5
    Cell{'sheet': 'Problem', 'row': 6, 'col': 17}  =SUM(J6:J7) - K6*D6
    FormulaMatchException: Nodes of "AdditiveOpContext" have different values "+@12:12" and "-@12:12"
    Cell-expr0 "*worksheet*.Problem.Problem!Q5" :: +(SUM(#Problem!J5:Problem!J6), *(#Problem!K5, #Problem!D5))
    Cell-expr2 "*worksheet*.Problem.Problem!Q5" :: (Σ $cell FOR cell IN #Problem!J5:Problem!J6) + #Problem!K5 * #Problem!D5
    (Σ $cell FOR cell IN #Problem!J5:Problem!J6) + #Problem!K5 * #Problem!D5
    >>> formula_expression(9, scenario=default_scenario, verbose=True)
    Test 9:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 3}  =SUMIF(Problem!$B$2:$B$6,inventory!A2, Problem!$C$2:$C$6)
    Cell{'sheet': 'inventory', 'row': 3, 'col': 3}  =SUMIF(Problem!$B$2:$B$6,inventory!A3, Problem!$C$2:$C$6)
    Results = {(1, 0, 2, 2, 0, 1, 0): inventory!A2}
    variability = {(1, 0, 2, 2, 0, 1, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!C2" :: (v1) -> SUMIF(#Problem!B2:Problem!B6, $v1, #Problem!C2:Problem!C6)
    Cell-expr2 "*worksheet*.inventory.inventory!C2" :: (v1) -> Σ $cell FOR cell, cond IN zip(#Problem!C2:Problem!C6, #Problem!B2:Problem!B6) S.T. $cond = $v1
    (v1) -> Σ $cell FOR cell, cond IN zip(#Problem!C2:Problem!C6, #Problem!B2:Problem!B6) S.T. $cond = $v1
    >>> formula_expression(10, scenario=default_scenario, verbose=True)
    Test 10:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 3, 'col': 11}  =SUM(H3:I3)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!H2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!I2}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!K2" :: (v1, v2) -> SUM(CellsRange($v1:$v2))
    Cell-expr2 "*worksheet*.inventory.inventory!K2" :: (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    >>> formula_expression(11, scenario=default_scenario, verbose=True)
    Test 11:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 2, 'col': 12}  =SUM(I2:J2)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!H2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!I2}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!K2" :: (v1, v2) -> SUM(CellsRange($v1:$v2))
    Cell-expr2 "*worksheet*.inventory.inventory!K2" :: (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    >>> formula_expression(12, scenario=default_scenario, verbose=True)
    Test 12:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 3, 'col': 12}  =SUM(I3:J3)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!H2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!I2}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!K2" :: (v1, v2) -> SUM(CellsRange($v1:$v2))
    Cell-expr2 "*worksheet*.inventory.inventory!K2" :: (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    >>> formula_expression(13, scenario=default_scenario, verbose=True)
    Test 13:
    Cell{'sheet': 'inventory', 'row': 3, 'col': 11}  =SUM(H3:I3)
    Cell{'sheet': 'inventory', 'row': 2, 'col': 12}  =SUM(I2:J2)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!H3, (1, 0, 2, 0, 0, 2, 0, 0): inventory!I3}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!K3" :: (v1, v2) -> SUM(CellsRange($v1:$v2))
    Cell-expr2 "*worksheet*.inventory.inventory!K3" :: (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    >>> formula_expression(14, scenario=default_scenario, verbose=True)
    Test 14:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 4, 'col': 12}  =SUM(I4:J4)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!H2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!I2}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!K2" :: (v1, v2) -> SUM(CellsRange($v1:$v2))
    Cell-expr2 "*worksheet*.inventory.inventory!K2" :: (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    >>> formula_expression(15, scenario=default_scenario, verbose=True)
    Test 15:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 5, 'col': 12}  =SUM(I6:J6)
    FormulaMatchException: Cells are not compatible "H2@5:6" and "I6@5:6"
    Cell-expr0 "*worksheet*.inventory.inventory!K2" :: SUM(#inventory!H2:inventory!I2)
    Cell-expr2 "*worksheet*.inventory.inventory!K2" :: Σ $cell FOR cell IN #inventory!H2:inventory!I2
    Σ $cell FOR cell IN #inventory!H2:inventory!I2
    >>> formula_expression(16, scenario=default_scenario, verbose=True)
    Test 16:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 11}  =SUM(H2:I2)
    Cell{'sheet': 'inventory', 'row': 6, 'col': 12}  =SUM(H6:I6)
    FormulaMatchException: Cells are not compatible "H2@5:6" and "H6@5:6"
    Cell-expr0 "*worksheet*.inventory.inventory!K2" :: SUM(#inventory!H2:inventory!I2)
    Cell-expr2 "*worksheet*.inventory.inventory!K2" :: Σ $cell FOR cell IN #inventory!H2:inventory!I2
    Σ $cell FOR cell IN #inventory!H2:inventory!I2
    >>> formula_expression(17, scenario=default_scenario, verbose=True)
    Test 17:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 13}  =SUM($H$2+$I$2)
    Cell{'sheet': 'inventory', 'row': 3, 'col': 13}  =SUM($H$2+$I$2)
    Results = {}
    variability = set()
    Cell-expr0 "*worksheet*.inventory.inventory!M2" :: SUM(+(#inventory!H2, #inventory!I2))
    Cell-expr2 "*worksheet*.inventory.inventory!M2" :: Σ $cell FOR cell IN #inventory!H2 + #inventory!I2
    Σ $cell FOR cell IN #inventory!H2 + #inventory!I2
    >>> formula_expression(18, scenario=default_scenario, verbose=True)
    Test 18:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 14}  =$H2+I$4
    Cell{'sheet': 'inventory', 'row': 3, 'col': 14}  =$H3+I$4
    Results = {(1, 0, 0, 0, 0): inventory!$H2, (1, 2, 0, 0, 0): inventory!I$4}
    variability = {(1, 0, 0, 0, 0), (1, 2, 0, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!N2" :: (v1, v2) -> +($v1, $v2)
    Cell-expr2 "*worksheet*.inventory.inventory!N2" :: (v1, v2) -> $v1 + $v2
    (v1, v2) -> $v1 + $v2
    >>> formula_expression(19, scenario=default_scenario, verbose=True)
    Test 19:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 14}  =$H2+I$4
    Cell{'sheet': 'inventory', 'row': 4, 'col': 14}  =$H4+I$4
    Results = {(1, 0, 0, 0, 0): inventory!$H2, (1, 2, 0, 0, 0): inventory!I$4}
    variability = {(1, 0, 0, 0, 0), (1, 2, 0, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!N2" :: (v1, v2) -> +($v1, $v2)
    Cell-expr2 "*worksheet*.inventory.inventory!N2" :: (v1, v2) -> $v1 + $v2
    (v1, v2) -> $v1 + $v2
    >>> formula_expression(20, scenario=default_scenario, verbose=True)
    Test 20:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 14}  =$H2+I$4
    Cell{'sheet': 'inventory', 'row': 2, 'col': 15}  =$H2+J$4
    Results = {(1, 0, 0, 0, 0): inventory!$H2, (1, 2, 0, 0, 0): inventory!I$4}
    variability = {(1, 0, 0, 0, 0), (1, 2, 0, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!N2" :: (v1, v2) -> +($v1, $v2)
    Cell-expr2 "*worksheet*.inventory.inventory!N2" :: (v1, v2) -> $v1 + $v2
    (v1, v2) -> $v1 + $v2
    >>> formula_expression(21, scenario=default_scenario, verbose=True)
    Test 21:
    Cell{'sheet': 'inventory', 'row': 2, 'col': 14}  =$H2+I$4
    Cell{'sheet': 'inventory', 'row': 3, 'col': 15}  =$H3+J$4
    Results = {(1, 0, 0, 0, 0): inventory!$H2, (1, 2, 0, 0, 0): inventory!I$4}
    variability = {(1, 0, 0, 0, 0), (1, 2, 0, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!N2" :: (v1, v2) -> +($v1, $v2)
    Cell-expr2 "*worksheet*.inventory.inventory!N2" :: (v1, v2) -> $v1 + $v2
    (v1, v2) -> $v1 + $v2
    >>> formula_expression(22, scenario=default_scenario, verbose=True)
    Test 22:
    Cell{'sheet': 'inventory', 'row': 12, 'col': 7}  =SUM(B$2:C3)
    Cell{'sheet': 'inventory', 'row': 13, 'col': 7}  =SUM(B$2:C4)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!B$2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!C3}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!G12" :: (v1, v2) -> SUM(CellsRange($v1:$v2))
    Cell-expr2 "*worksheet*.inventory.inventory!G12" :: (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    >>> formula_expression(23, scenario=default_scenario, verbose=True)
    Test 23:
    Cell{'sheet': 'inventory', 'row': 12, 'col': 7}  =SUM(B$2:C3)
    Cell{'sheet': 'inventory', 'row': 13, 'col': 8}  =SUM(C$2:D4)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!B$2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!C3}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!G12" :: (v1, v2) -> SUM(CellsRange($v1:$v2))
    Cell-expr2 "*worksheet*.inventory.inventory!G12" :: (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    >>> formula_expression(24, scenario=default_scenario, verbose=True)
    Test 24:
    Cell{'sheet': 'inventory', 'row': 12, 'col': 9}  =SUM(C$2:D$3)
    Cell{'sheet': 'inventory', 'row': 13, 'col': 10}  =SUM(D$2:E$3)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!C$2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!D$3}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!I12" :: (v1, v2) -> SUM(CellsRange($v1:$v2))
    Cell-expr2 "*worksheet*.inventory.inventory!I12" :: (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    >>> formula_expression(25, scenario=default_scenario, verbose=True)
    Test 25:
    Cell{'sheet': 'inventory', 'row': 12, 'col': 9}  =SUM(C$2:D$3)
    Cell{'sheet': 'inventory', 'row': 13, 'col': 9}  =SUM(C$2:D$3)
    Results = {(1, 0, 2, 0, 0, 0, 0, 0): inventory!C$2, (1, 0, 2, 0, 0, 2, 0, 0): inventory!D$3}
    variability = {(1, 0, 2, 0, 0, 0, 0, 0), (1, 0, 2, 0, 0, 2, 0, 0)}
    Cell-expr0 "*worksheet*.inventory.inventory!I12" :: (v1, v2) -> SUM(CellsRange($v1:$v2))
    Cell-expr2 "*worksheet*.inventory.inventory!I12" :: (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    (v1, v2) -> Σ $cell FOR cell IN CellsRange($v1:$v2)
    """


def parse_scenario_test_args(args=None):
    parser = ArgumentParser(description='Generate Java classes from spreadsheet')
    parser.add_argument('-i', '--input-file', type=Path, help='name of spreadsheet file containing problem description')
    parser.add_argument('-s', '--sheet', type=str, help='name of sheet to analyze')
    parsed = parser.parse_args(args)
    return parsed


if __name__ == '__main__':
    import doctest

    doctest.testmod()
