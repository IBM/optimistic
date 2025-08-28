import json
import sys
from pathlib import Path
from queue import SimpleQueue
from typing import Sequence, Optional

from validator2solver.codegen.opl.opl_generator import OplVisitor
from validator2solver.domain_analysis import DomainTable
from math_rep.expr import Comparison, Quantity, StringTerm, FormalContent
from scenoptic.scenoptic_expr import Cell, DomainTableForScenoptic
from math_rep.expression_types import QualifiedName
from validator2solver.optimistic_rules import CountToSum, NotToEqZero, BooleanToIntEquationInLogicalExpression, \
    QuantifiedBooleanToIntEquation, EquatedCeil, MoveSumConditionToTerm, IfToImplications, \
    EliminateNegationOfComparison, LiftLeftImplicationOverComparison, LiftRightImplicationOverComparison, \
    LiftRightLogicalOperatorOverComparison, LiftLeftLogicalOperatorOverComparison, \
    LiftImplicationOverFunctionApplication, LiftLogicalOperatorOverFunctionApplication, ReplaceStrictInequality
from rewriting.rules import RuleSet, OrderedRuleSets, exhaustively_apply_rules
from scenoptic.excel_data import BooleanCell, IntegerCell, FloatCell, StringCell, CellTypeFactory
from scenoptic.excel_rules import ExcelIfRule, ExcelCriteriaRule, ConvertExcelFunctions, ExpandExcelSumMultipleArgs, \
    AggregateCellsRule, TranslateExcelSumif, TranslateExcelCountif, AggregateZipCellsRule, ExpandExcelSumOneArg, \
    TranslateExcelSumifs, TranslateExcelCountifs
from scenoptic.excel_to_math import Scenario, OptimizationDirection, Constant, CELL_COLLECTOR, Constraint, \
    AbstractConstraint
from scenoptic.parse_excel import parse_formula
from scenoptic.xl_utils import get_sheet_in_cell_qn_as_string, xl_cell_or_range_elements_qn

EXCEL_TO_OPL_RULES1 = OrderedRuleSets(RuleSet(ConvertExcelFunctions()),
                                      RuleSet(ExcelIfRule()),
                                      RuleSet(ExcelCriteriaRule()),
                                      RuleSet(ExpandExcelSumMultipleArgs(),
                                              ExpandExcelSumOneArg(),
                                              TranslateExcelSumif(),
                                              TranslateExcelSumifs(),
                                              TranslateExcelCountif(),
                                              TranslateExcelCountifs()),
                                      RuleSet(AggregateCellsRule(),
                                              AggregateZipCellsRule()),
                                      RuleSet(CountToSum(),
                                              # GlobalizeCeil(self.om),
                                              NotToEqZero(),
                                              BooleanToIntEquationInLogicalExpression(),
                                              QuantifiedBooleanToIntEquation(),
                                              EquatedCeil(),
                                              MoveSumConditionToTerm(),
                                              # ReduceDomainTautologies()  # circular!
                                              ),
                                      # RuleSet(GlobalizeCeil(self.om)),
                                      RuleSet(IfToImplications()),
                                      RuleSet(EliminateNegationOfComparison()),
                                      RuleSet(LiftLeftImplicationOverComparison(),
                                              LiftRightImplicationOverComparison(),
                                              LiftRightLogicalOperatorOverComparison(),
                                              LiftLeftLogicalOperatorOverComparison(),
                                              LiftImplicationOverFunctionApplication(),
                                              LiftLogicalOperatorOverFunctionApplication()),
                                      RuleSet(ExpandExcelSumMultipleArgs()))
EXCEL_TO_OPL_RULES2 = OrderedRuleSets(RuleSet(ReplaceStrictInequality()))


def const_to_opl(const):
    # Hack; OPL uses the same syntax for constants as JSON
    return json.dumps(const)


class OplType:
    def __init__(self, name):
        self.name = name


OPL_POS_RANGE_TYPES = {'int': 'maxint', 'float': 'infinity'}
OPL_POS_TYPES = {'int': 'int+', 'float': 'float+'}

CELL_TYPES_FOR_OPL = dict(int=IntegerCell, float=FloatCell, bool=BooleanCell, string=StringCell)


def convert_excel_expr_to_opl(excel_expr):
    opl_visitor = OplVisitor(allow_undefined_vars=True)  # FIXME!!! should be False
    abstract_model = excel_expr.to_code_rep()
    code = abstract_model.accept(opl_visitor)
    return code, opl_visitor


class ScenarioForOPL(Scenario):
    def __init__(self, excel_file, sheet: str = None, default_type=FloatCell()):
        super().__init__(excel_file, sheet, default_type, CellTypeFactory(CELL_TYPES_FOR_OPL))
        self.use_epsilon = False
        self.epsilon = 1e-10
        self.constants = None
        self.initialized = None
        self.dvars = None
        self.constraints = None

    def cell_to_constraint(self, cell: QualifiedName, contents, domain_table: DomainTable = None
                           ) -> Optional[AbstractConstraint]:
        if not contents:
            return None
        current_sheet = get_sheet_in_cell_qn_as_string(cell)
        expr = parse_formula(contents, self, current_sheet)
        if domain_table is not None:
            domain_table.build(expr)
        if isinstance(expr, (Quantity, StringTerm)):
            return Constant(expr.to_code_rep().value)
        constraint_term = Comparison(Cell.from_name_qn(cell), '=', expr)
        if domain_table is not None:
            domain_table.build(constraint_term)
        cell_map = {cell.name: cell for cell in CELL_COLLECTOR.collect(constraint_term) if
                    cell is not None}
        cells = [cell_map[name] for name in (sorted(cell_map.keys()))]
        abs_rep1 = exhaustively_apply_rules(EXCEL_TO_OPL_RULES1, constraint_term, domain_table)
        code = exhaustively_apply_rules(EXCEL_TO_OPL_RULES2, abs_rep1, domain_table)
        result = Constraint(code, cells)
        return result

    def convert_to_language(self, expression: FormalContent):
        code, visitor = convert_excel_expr_to_opl(expression)
        self.use_epsilon = 'epsilon' in visitor.named_constants or self.use_epsilon
        return code

    def validate_initialization(self):
        if (self.parameters is None or self.types is None
                or self.objectives is None):
            raise Exception(f'Scenario not initialized properly')

    def build(self):
        # TODO: support named ranges
        self.find_translation_arguments()
        self.validate_initialization()
        domain_table = DomainTableForScenoptic()
        constraints = {}
        constants = {}
        analyzed_names = set(cell
                             for o in self.objectives.keys()
                             for cell in xl_cell_or_range_elements_qn(o, self.specification_sheet_name()))
        parameters = frozenset(self.parameters)
        for p in parameters:
            pcell = Cell.from_name_qn(p, self.ws.title)
            domain_table.build(pcell)
            pcell.appl_info.set_dvar(domain_table)
        domain_table.propagate()
        agenda = SimpleQueue()
        for cell in sorted(analyzed_names):
            agenda.put(cell)
        while not agenda.empty():
            cell = agenda.get()
            contents = self.cell_qn_value(cell)
            # print(f'Cell {cell}: {contents}')
            constraint = self.cell_to_constraint(cell, contents, domain_table)
            if not constraint:
                self.warn(f'Fail to parse cell <{cell}> with contents <{contents}>')
                continue
            if isinstance(constraint, Constant):
                constants[cell] = constraint.value
            else:
                assert isinstance(constraint, Constraint)
                constraints[cell] = constraint.code
                analyzed_cells = constraint.predecessors
                set_of_analyzed_cells_qn = set(cell.name for cell in analyzed_cells)
                for free in sorted(set_of_analyzed_cells_qn - analyzed_names - parameters):
                    agenda.put(free)
                analyzed_names |= set_of_analyzed_cells_qn
        dvars = sorted((analyzed_names | set(self.parameters)) - set(constants.keys()))
        self.constants = constants
        self.constraints = constraints
        self.dvars = dvars

    def _handle_objectives(self) -> Sequence[FormalContent]:
        """
        TODO: convert to expression FunctionApplication...
        """
        pass

    def to_opl(self, opl_file: str):
        constraints = []
        for cell, c in self.constraints.items():
            constraints.append(self.convert_to_language(c))

        with open(opl_file, 'w') as f:
            if self.use_epsilon:
                print(f'float epsilon = {self.epsilon};\n', file=f)
            for var in sorted(self.constants.keys()):
                t = self.types[var]
                print(f'{t.mtype.for_opl()} {var.to_c_identifier()} = {const_to_opl(self.constants[var])};', file=f)
            for var in self.dvars:
                t = self.types[var]
                stype = t.mtype.for_opl()
                range = ""
                if isinstance(t, (IntegerCell, FloatCell)):
                    if not t.upper_bound and t.lower_bound == 0:
                        # range = f'{t.lower_bound}..{OPL_POS_RANGE_TYPES.get(stype)}'
                        stype = OPL_POS_TYPES.get(stype)
                    elif t.upper_bound:
                        range = f'{t.lower_bound}..{t.upper_bound}'
                print(f'dvar {stype} {var.to_c_identifier()}{f" in {range}" if range else ""};', file=f)

            # FIXME!!!!!! cells here are strings, not QNs, fix!
            final_objectives = {cell: data
                                for cells_spec, data in self.objectives.items()
                                for cell in xl_cell_or_range_elements_qn(cells_spec, self.specification_sheet_name())}
            pos_objective = (f'{cell.to_c_identifier()}'
                             for cell, (level, direction) in final_objectives.items() if
                             direction == OptimizationDirection.MINIMIZE and level < 1)
            neg_objective = list(f'{cell.to_c_identifier()}'
                                 for cell, (level, direction) in final_objectives.items() if
                                 direction == OptimizationDirection.MAXIMIZE and level < 1)
            print(
                f'\nminimize {" + ".join(pos_objective)}{" - " if len(neg_objective) > 0 else ""}{" - ".join(neg_objective)};',
                file=f)

            print('', file=f)
            print('subject to {', file=f)
            for c in constraints:
                # print('  ' + c + ';', file=f)
                print(f'  {c.value};', file=f)
            print('}', file=f)


default_excel_file = (
    str(Path(__file__).joinpath(
        r'../../scenoptic_examples/user_stories/Supply-chain-for-OptaPlanner-OPL.xlsx'))
)
default_mod_file = Path(__file__).parent.parent / 'test-output/scenoptic/actual/gen-opl.mod'
default_sheet = 'S>s bool self-contained V2'
default_ref_file = Path(__file__).parent.parent / 'test-output/scenoptic/expected/gen-opl.mod'


def run_excel_test(excel_file, mod_file, sheet=default_sheet):
    s = ScenarioForOPL(excel_file, sheet=sheet)
    s.build()
    s.to_opl(mod_file)


if __name__ == '__main__':
    excel_file = str(Path(__file__).joinpath(sys.argv[1]).resolve()) if len(sys.argv) > 1 else default_excel_file
    if not Path(excel_file).exists():
        raise Exception(f'Excel file {excel_file} does not exist')
    sheet = sys.argv[2] if len(sys.argv) > 2 else default_sheet
    mod_file = str(Path(__file__).parent.joinpath(sys.argv[3]).resolve()) if len(sys.argv) > 3 else default_mod_file
    run_excel_test(excel_file, mod_file, sheet)
