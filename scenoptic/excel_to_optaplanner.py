from __future__ import annotations

import itertools
import json
import re
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from inspect import isfunction
from operator import itemgetter
from pathlib import Path
from queue import SimpleQueue
from typing import Tuple, Mapping, Sequence, Set, Callable, Optional, Any, MutableMapping, Union

import inflection
from jinja2 import Environment, PackageLoader, select_autoescape
from more_itertools import partition

from codegen.java.java_generator import JavaVisitor, convert_to_java_string
from codegen.java.java_symbols import JAVA_LIST_OF_QN, THIS, static_method_to_class_transform
from codegen.utils import intern
from math_rep.expr import Quantity, StringTerm, LambdaExpression, FormalContent, MathVariable, \
    Cast, FunctionApplication, Stream, ComprehensionContainer, Aggregate, ComprehensionCondition, IFTE, \
    ZERO_AS_QUANTITY, Comparison, Term, LogicalOperator, ONE_AS_QUANTITY
from math_rep.expression_types import QualifiedName, M_INT, MClassType, MAtomicType, M_NUMBER, M_BOOLEAN, MArray, M_ANY, \
    MType, is_subtype, M_STRING, MCollectionType, type_intersection
from math_rep.math_frame import MATH_FRAME_NAME, MATH_VAR_FRAME_PATH
from math_rep.math_symbols import RANGE_QN, MAKE_STREAM_QN, MOD_QN, INT_DIV_QN, ZIP_QN, make_array_qn, EQ_QN, AND_QN
from rewriting.patterns import Bindings, one_of, let
from rewriting.rules import RuleSet, OrderedRuleSets, exhaustively_apply_rules, RewriteRule
from scenoptic.excel_alg_find_cell_ranges import AnalyzeCellRanges
from scenoptic.excel_data import CellType, BooleanCell, IntegerCell, FloatCell, CellTypeFactory, StringCell, ExcelData, \
    ClassCellType
from scenoptic.excel_rules import ExcelIfRule, to_math, ConvertExcelFunctions, ExpandExcelSumMultipleArgs, \
    AggregateCellsRule, \
    ExcelCriteriaRule, AggregateZipCellsRule, TranslateExcelSumif, TranslateExcelSumifs, TranslateExcelCountif, \
    TranslateExcelCountifs, ExpandExcelSumOneArg, ExcelConditionalSummingRule
from scenoptic.excel_symbols import as_excel_name, worksheet_path
from scenoptic.excel_to_math import Scenario, OptimizationDirection, Constraint, Constant, CELL_COLLECTOR, \
    extract_cell_components_to_dict, ExcelOperator, EXCEL_OPERATORS, EXCEL_AGGREGATE_OPERATORS, EXCEL_SUM_OPERATORS, \
    EXCEL_COUNT_OPERATORS, AbstractConstraint, extract_cell_components, CellSpec
from scenoptic.parse_excel import parse_formula
from scenoptic.scenoptic_expr import Cell, Cells, DomainTableForScenoptic
from scenoptic.scenoptic_rules import SubscriptedToGetMethodCall, ConvertJavaObjectComparisons
from scenoptic.scenoptic_symbols import GET_OPTIONAL_INT_QN, GET_OPTIONAL_DOUBLE_QN, GET_OPTIONAL_STRING_QN, \
    SCENOPTIC_JAVA_GET_VALUE_QN, SCENOPTIC_JAVA_CELL_KEY, VALUES_QN, PREVIOUS_VALUES_QN, NEW_VALUES_QN, CURRENT_QN, \
    SCENOPTIC_JAVA_GET_QN, ABSTRACT_CELL_KEY_QN, SCENOPTIC_JAVA_GET_INCREMENTAL_VALUE_QN, GET_OPTIONAL_FLOAT_QN, \
    PREVIOUS_SCALARS_QN, NEW_SCALARS_QN, SUMMING_CELL_GET_INT_QN, SUMMING_CELL_GET_DOUBLE_QN, ISUMMING_CELL_QN, \
    CELL_KEY_QN, SCENOPTIC_JAVA_SINGLE_INT_SUMMING_CREATOR_QN, COUNTING_SHADOW_CELL_CLASS_SUFFIX, SCENOPTIC_UTILS_PATH
from scenoptic.xl_utils import coords_to_cell, get_sheet_in_cell_qn_as_string, range_to_cells, normalize_cell_qn, \
    cell_to_coords, xl_cell_or_range_elements_qn, as_cell_qn, cell_qn_to_components, index_to_column
from streams.stream_tools import take
from validator2solver.domain_analysis import DomainTable

MAIN_PACKAGE_SUFFIX = 'main'
DOMAIN_PACKAGE_SUFFIX = 'domain'
SOLVER_PACKAGE_SUFFIX = 'solver'

JAVA_LIST_OF_OWNER = static_method_to_class_transform(JAVA_LIST_OF_QN)

SPECIAL_SHEET_SYMBOL = '\u203C'  # '‼'

BLANK_VALUE = Quantity(None)

CONSTRUCTING_FORMULA_PARAMS = (CELL_KEY_QN,)


@dataclass
class ExcelOperatorForOptaPlanner(ExcelOperator):
    incremental_computation: bool = False

    @classmethod
    def from_excel_operator(cls, generic: ExcelOperator,
                            incremental_computation: bool = False):
        return cls(scalar_result=generic.scalar_result,
                   can_be_used_as_array_formula=generic.can_be_used_as_array_formula,
                   argument_type=generic.argument_type,
                   blank_treatment=generic.blank_treatment,
                   one_to_one=generic.one_to_one,
                   output_size=generic.output_size,
                   criteria_arguments=generic.criteria_arguments,
                   ranges_must_match=generic.ranges_must_match,
                   incremental_computation=incremental_computation)


INCREMENTAL_OPERATORS = (*EXCEL_AGGREGATE_OPERATORS, *'XLOOKUP,UNIQUE'.split(','))
INCREMENTAL_OPERATOR_QNS = tuple(as_excel_name(op) for op in INCREMENTAL_OPERATORS)

EXCEL_OPERATORS_ADDITIONS = {**{op: dict(incremental_computation=True)
                                for op in EXCEL_COUNT_OPERATORS},
                             **{op: dict(incremental_computation=True)
                                for op in EXCEL_SUM_OPERATORS}}

EXCEL_OPERATORS_FOR_OPTAPLANNER: Mapping[str, ExcelOperatorForOptaPlanner] = {
    op: ExcelOperatorForOptaPlanner.from_excel_operator(desc, **EXCEL_OPERATORS_ADDITIONS.get(op, {}))
    for op, desc in EXCEL_OPERATORS.items()}


# Obsolete
class IncrementalComputation(ABC):
    @abstractmethod
    def incremental_formula(self, computation: FunctionApplication, source_cell: QualifiedName,
                            scenario: ScenarioForOptaPlanner) -> LambdaExpression:
        """
        Given a term ``computation`` that computes the value of an Excel formula with a top-level function belonging
        to this ``IncrementalComputation`` object, return a lambda expression suitable for an incremental computation

        Precondition: ``computation.function`` is an Excel operator whose semantics is defined by this object.
        """

    @abstractmethod
    def incremental_predecessors(self, computation: FunctionApplication, source_cell: QualifiedName
                                 ) -> Tuple[int, LambdaExpression]:
        """
        Given a term ``computation`` that computes the value of an Excel formula with a top-level function belonging
        to this ``IncrementalComputation`` object and the source cell containing the formula, return the number of
        incremental-predecessor lists, and a LambdaExpression that will be the body of the
        ``getIncrementalPredecessors(int index)`` method in Java

        Precondition: ``computation.function`` is an Excel operator whose semantics is defined by this object.
        """


def cells_to_key_stream(cells: Cells):
    """
    Return an expression that represents a stream of CellKey objects corresponding to the cells in the given ``cells``
    range
    """
    sheet_str = Quantity(cells.sheet)
    start_row = cells.start_row
    end_row = cells.end_row
    start_col = cells.start_col
    end_col = cells.end_col
    comprehension = None
    if start_col != end_col:
        col_var = FormalContent.fresh_name(QualifiedName('col', lexical_path=MATH_VAR_FRAME_PATH), 'v')
        col_expr = MathVariable(col_var)
        comprehension = ComprehensionContainer(
            [col_var], RANGE_QN(Quantity(start_col), Quantity(end_col + 1)))
    else:
        col_expr = Quantity(start_col)
    if start_row != end_row:
        row_var = FormalContent.fresh_name(QualifiedName('row', lexical_path=MATH_VAR_FRAME_PATH), 'v')
        row_expr = MathVariable(row_var)
        comprehension = ComprehensionContainer(
            [row_var], RANGE_QN(Quantity(start_row), Quantity(end_row + 1)), rest=comprehension)
    else:
        row_expr = Quantity(start_row)
    if comprehension is None:
        return MAKE_STREAM_QN(SCENOPTIC_JAVA_CELL_KEY(sheet_str, row_expr, col_expr, constructor=True))
    return LambdaExpression(
        (),
        Stream(SCENOPTIC_JAVA_CELL_KEY(sheet_str, row_expr, col_expr, constructor=True),
               comprehension))


ABSTRACT_CELL_KEY_TYPE = MClassType(ABSTRACT_CELL_KEY_QN)
MAKE_ABSTRACT_CELL_KEY_ARRAY_QN = make_array_qn(ABSTRACT_CELL_KEY_TYPE, None)


def row_and_col_exprs(range: Cells, nrows, index_var):
    start_row = range.start_row
    end_row = range.end_row
    start_col = range.start_col
    end_col = range.end_col
    nrows_expr = Quantity(nrows)
    start_row_expr = Quantity(start_row)
    start_col_expr = Quantity(start_col)
    row_expr = (start_row_expr + (MOD_QN(index_var, nrows_expr) if start_col != end_col else index_var)
                if start_row != end_row else start_row_expr)
    col_expr = (start_col_expr + (INT_DIV_QN(index_var, nrows_expr) if start_row != end_row else index_var)
                if start_col != end_col else start_col_expr)
    return row_expr, col_expr


def extend_package(package: str, extension: str) -> str:
    if not extension:
        return package
    return f'{package}.{extension}'


def package_to_path(package: str) -> Path:
    return Path('/'.join(package.split('.')))


EXCEL_RULES0A = OrderedRuleSets(RuleSet(ConvertExcelFunctions()),
                                RuleSet(ExcelIfRule()),
                                RuleSet(ExcelCriteriaRule()),
                                RuleSet(ExpandExcelSumMultipleArgs()),
                                RuleSet(ExpandExcelSumOneArg()))

EXCEL_RULES0B = OrderedRuleSets(RuleSet(TranslateExcelSumif()),
                                RuleSet(TranslateExcelSumifs()),
                                RuleSet(TranslateExcelCountif()),
                                RuleSet(TranslateExcelCountifs()))

EXCEL_SUMMING_CELL_RULES = OrderedRuleSets(ExcelConditionalSummingRule())

EXCEL_TO_JAVA_RULES1 = OrderedRuleSets(RuleSet(AggregateCellsRule()),
                                       RuleSet(AggregateZipCellsRule()))

EXCEL_TO_JAVA_RULES2 = OrderedRuleSets(RuleSet(SubscriptedToGetMethodCall()),
                                       RuleSet(ConvertJavaObjectComparisons()))


def as_java_list(p):
    return ', '.join(f'"{e}"' for e in p)


def math_qn(name: str):
    return QualifiedName(name, lexical_path=(MATH_FRAME_NAME,))


def convert_excel_expr_to_java(excel_expr):
    java_extractor = JavaVisitor('optimistic', lexical_paths_to_ignore=(SCENOPTIC_UTILS_PATH,))
    abstract_model = excel_expr.to_code_rep()
    code = java_extractor.full_code(abstract_model, '', encapsulate=False)
    return code


def invert_map(forward):
    """
    Invert a one-to-many mapping.  If ``y in forward[x]`` then ``x in result[y]``.
    """
    result = defaultdict(set)
    for current, values in forward.items():
        for value in values:
            result[value].add(current)
    return result


def transitive_closure(mapping: Mapping, roots: Sequence, reflexive=True) -> Set:
    """
    Return the transitive closure of the mapping starting from the roots; i.e., all elements accessible from the roots.
    """
    if reflexive:
        result = set(roots)
        excluded = set()
    else:
        result = set()
        excluded = set(roots)
    agenda = set(roots)
    while agenda:
        current = agenda.pop()
        elements = mapping.get(current)
        if elements is None:
            continue
        elements = set(elements)
        new_elements = elements - result - {current} - excluded
        result.update(new_elements)
        agenda.update(new_elements)
    return result


OPTAPLANNER_TYPES = dict(int='Integer', float='Double')  # 'BigDecimal'
OPTIONAL_TYPE_QNS = dict(int=GET_OPTIONAL_INT_QN,
                         float=GET_OPTIONAL_FLOAT_QN,
                         double=GET_OPTIONAL_DOUBLE_QN,
                         String=GET_OPTIONAL_STRING_QN)
UNKNOWN_QN = QualifiedName('*unknown*')
JAVA_WRAPPER_TYPES = {M_INT: MAtomicType('Wrapped Integer', java_type='Integer'),
                      M_NUMBER: MAtomicType('Wrapped Double', java_type='Double'),
                      M_BOOLEAN: MAtomicType('Wrapped Boolean', java_type='Boolean')}


class PlanningVarRange(CellType, ABC):
    has_constructor = True

    @abstractmethod
    def _range_as_camel_case(self) -> str:
        """
        Return a camel-case representation of this range.  The result may start with a number.
        """

    def java_class_name(self) -> str:
        java_type = self.mtype.for_java().name
        return f'{java_type[0].upper()}{java_type[1:]}{self._range_as_camel_case()}'

    def java_type_name(self) -> str:
        base_type = self.mtype.for_java()
        return OPTAPLANNER_TYPES.get(base_type.name, base_type.name)

    @abstractmethod
    def java_constructor(self) -> str:
        """
        Return Java code that generates a range object corresponding to this range
        """


class IntVarRange(IntegerCell, PlanningVarRange):
    def _range_as_camel_case(self) -> str:
        return (f'{"_" if self.lower_bound < 0 else ""}{abs(self.lower_bound)}'
                f'To{"_" if self.upper_bound < 0 else ""}{self.upper_bound}')

    def java_constructor(self) -> str:
        return f'ValueRangeFactory.createIntValueRange({self.lower_bound}, {self.upper_bound})'


class FloatVarRange(FloatCell, PlanningVarRange):
    @staticmethod
    def _float_to_str(num: float):
        return str(num).replace('.', 'p')

    def _range_as_camel_case(self) -> str:
        return (f'{"_" if self.lower_bound < 0 else ""}{self._float_to_str(abs(self.lower_bound))}'
                f'To{"_" if self.upper_bound < 0 else ""}{self._float_to_str(self.upper_bound)}')

    def java_constructor(self) -> str:
        return f'ValueRangeFactory.createBigDecimalValueRange({self.lower_bound}, {self.upper_bound})'


class BooleanVarRange(BooleanCell, PlanningVarRange):
    def _range_as_camel_case(self) -> str:
        return ''

    def java_constructor(self) -> str:
        return 'ValueRangeFactory.createBooleanValueRange()'


@intern(key=lambda cells, optional=False: (cells.key() if cells else None, optional))
class StringVarRange(StringCell, PlanningVarRange):
    has_constructor = False
    _instance_number = 0

    def __init__(self, domain: Optional[Cells] = None, optional=False):
        super().__init__(domain, optional=optional)
        StringVarRange._instance_number += 1
        self.id = StringVarRange._instance_number

    def _range_as_camel_case(self) -> str:
        return str(self.id)

    # FIXME!!!!!! this should work with constant fields, not classes!
    #  The entity class will have a @PlanningVariable(valueRangeProviderRefs = "String1") as usual
    #  Instead of a @ValueRangeProvider method, the solution class will have a field containing the list of values
    #  (also annotated with @ProblemFactCollectionProperty?)
    def java_constructor(self) -> str:
        raise NotImplementedError('StringVarRange supports a value list, not a constructor')

    def values(self, excel_data: ExcelData):
        values = ', '.join(f'"{excel_data.cell_value(cell.row, cell.col, sheet=cell.sheet, req_type=str)}"'
                           for cell in self.domain)
        return f'List.of({values})'


def name_to_identifier(name):
    if not name:
        name = 'C'
    elif name[0].isdigit():
        name = 'C' + name
    name = inflection.camelize(re.sub(r'\W+', '', name[0].upper() + name[1:]))
    return name


# FIXME! add string range (using ListValueRange)
CELL_TYPES_FOR_OPTAPLANNER = dict(int=IntVarRange, float=FloatVarRange, bool=BooleanVarRange, string=StringVarRange)


def const_to_java(const):
    # Hack; Java uses the same syntax for constants as JSON
    return json.dumps(const)


@dataclass
class IncrementalConstraint(AbstractConstraint):
    incremental_update_formula: LambdaExpression
    incremental_fresh_formula: LambdaExpression
    n_preds: int
    incremental_predecessors_formula: LambdaExpression
    element_type: MType
    all_inc_predecessors: Set[QualifiedName]
    predecessors: Sequence[QualifiedName]
    subexpression_cells: Set[QualifiedName]


@dataclass
class SummingConstraint(AbstractConstraint):
    constructor_expr: Term
    n_preds: int
    incremental_predecessors_formula: LambdaExpression
    all_inc_predecessors: Set[QualifiedName]
    predecessors: Sequence[QualifiedName] = ()

    def with_predecessors(self, predecessors):
        return SummingConstraint(self.constructor_expr, self.n_preds, self.incremental_predecessors_formula,
                                 self.all_inc_predecessors, predecessors)

    @property
    def code(self):
        return None

    @property
    def subexpression_cells(self):
        return set()


@dataclass
class OptaPlannerConstraint(Constraint):
    subexpression_cells: Set[QualifiedName]


@dataclass
class Phase01Constraint(OptaPlannerConstraint):
    original_cell: QualifiedName


@dataclass
class IncrementalPhase01Constraint(Phase01Constraint):
    all_inc_predecessors: Set[QualifiedName]

    def with_predecessors(self, predecessors):
        return IncrementalPhase01Constraint(self.code,
                                            predecessors,
                                            self.subexpression_cells,
                                            self.original_cell,
                                            self.all_inc_predecessors)


@dataclass
class OptaPhase01Constraint(Phase01Constraint):
    def with_predecessors(self, predecessors):
        return OptaPhase01Constraint(self.code,
                                     predecessors,
                                     self.subexpression_cells,
                                     self.original_cell)


class IncrementalsSplitter(RewriteRule):
    """
    This rule replaces incremental operators by new Cell variables.  It collects the new variables and the corresponding
    formulas.

    This rule must be applied bottom up, so that a replaced subexpression will not contain incremental subexpressions.

    **N.B. This rule must not be applied inside quantifiers or aggregations!**
    """
    pattern = FunctionApplication[let(op=one_of(*INCREMENTAL_OPERATOR_QNS))]

    def __init__(self, top_level_expr: FormalContent, original_cell_spec: str, domain_table):
        self.top_level_expr = top_level_expr
        self.original_cell_spec = original_cell_spec
        self.domain_table = domain_table
        self.new_variables = {}
        self.next_index = 1

    def condition(self, obj, bindings: Bindings) -> bool:
        return obj is not self.top_level_expr

    def transform_single(self, obj, bindings: Bindings):
        # FIXME!! compute type information using general type inference (to be implemented)
        op = bindings['op']
        if op.name in EXCEL_SUM_OPERATORS:
            args = obj.args
            criteria_args = EXCEL_OPERATORS_FOR_OPTAPLANNER[op.name].criteria_arguments
            limited_criteria_args = tuple(take(len(args), criteria_args))
            arg_types = tuple(arg.appl_info.type.element_type if isinstance(arg.appl_info.type, MCollectionType)
                              else arg.appl_info.type
                              for i, arg in enumerate(args) if i not in limited_criteria_args)
            ctype = type_intersection(*arg_types)
        elif op.name in EXCEL_COUNT_OPERATORS:
            ctype = M_INT
        else:
            ctype = obj.appl_info.type
        subexpr_cell = Cell(self.next_index, 22, f'subexpr!{self.original_cell_spec}', ctype=ctype)
        self.next_index += 1
        self.new_variables[subexpr_cell.name] = obj
        self.domain_table.build(subexpr_cell.defined_as(obj))
        return subexpr_cell


def mtype_to_cell_type(mtype: MType) -> CellType:
    if is_subtype(mtype, M_BOOLEAN):
        return BooleanCell()
    if is_subtype(mtype, M_INT):
        return IntegerCell()
    if is_subtype(mtype, M_NUMBER):
        return FloatCell()
    if is_subtype(mtype, M_STRING):
        return StringCell()
    raise Exception(f'No CellType equivalent for {mtype}')


def incremental_initializer_class(mtype: MType) -> str:
    if is_subtype(mtype, M_INT):
        return 'IntegerInitializer.SINGLETON'
    if is_subtype(mtype, M_NUMBER):
        return 'DoubleInitializer.SINGLETON'
    raise Exception(f'Type {mtype} not (yet) supported as element type for incremental operations')


PREFIX_TO_JAVA_TYPE = dict(CF='Formula',
                           IUF='IncrementalUpdateFormula',
                           IFF='IncrementalFreshFormula',
                           IPF='IncrementalPredecessorFormula<AbstractCellKey>',
                           SIF='ConstructingFormula<AbstractCellKey, ? extends ISummingCell<AbstractCellKey, ?>>')

CRITERION_TYPE = Sequence[Tuple[Cells, Term, Tuple[MathVariable, Term]]]
CRITERIA_INFO = Tuple[CRITERION_TYPE, CRITERION_TYPE, CRITERION_TYPE]


def summing_cell_info(term: Term) -> Optional[CRITERIA_INFO]:
    """
    Identify candidates for summing cells.  These are aggregations with either a single var, or multiple vars with a
    zip container, and a condition.  The ranges of the vars must be Cells objects.

    :param term: The term to be analyzed
    :return: sequences of (range, comparison, (var, scalar)) tuples for the conjuncts of the aggregate condition,
        divided into equalities, static, dynamic; or None if not a candidate for a summing cell
    """

    def get_ranges(agg: Aggregate):
        compr_container = agg.container
        vars = compr_container.vars
        container = compr_container.container
        if len(vars) == 1:
            ranges = [container]
        else:
            if not (isinstance(container, FunctionApplication) and container.function == ZIP_QN):
                return None, None
            ranges = container.args
        if not all(isinstance(r, Cells) for r in ranges):
            return None, None
        return vars, ranges

    def is_equality_criterion(body: Term) -> bool:
        return isinstance(body, Comparison) and body.op == EQ_QN

    def is_criterion(body: Term, vars: Sequence[MathVariable]) -> bool:
        if not isinstance(body, Comparison):
            return False
        args = (body.lhs, body.rhs)
        return any(isinstance(arg, MathVariable) and arg.name in vars for arg in args)

    def is_static_criterion(body: Term) -> bool:
        if not isinstance(body, Comparison):
            return False
        args = (body.lhs, body.rhs)
        scalar = args[1] if type(args[0]) == MathVariable else args[0]
        return not scalar.appl_info.is_dvar()

    def get_var_and_scalar(comp: Comparison, vars: Sequence[MathVariable]) -> Tuple[MathVariable, Term]:
        if isinstance(comp.lhs, MathVariable) and comp.lhs.name in vars:
            return comp.lhs, comp.rhs
        return comp.rhs, comp.lhs

    if not isinstance(term, Aggregate):
        return None
    comp_cond = term.container.rest
    if comp_cond is None or not isinstance(comp_cond, ComprehensionCondition) or comp_cond.rest is not None:
        return None
    vars, ranges = get_ranges(term)
    if vars is None:
        return None
    condition = comp_cond.condition
    if isinstance(condition, LogicalOperator) and condition.kind == AND_QN:
        conjuncts = condition.elements
    else:
        conjuncts = [condition]
    if not all(is_criterion(c, vars) for c in conjuncts):
        return None
    p1 = partition(lambda pair: is_equality_criterion(pair[1]),
                   zip(ranges, conjuncts, (get_var_and_scalar(c, vars) for c in conjuncts)))
    equalities = sorted(p1[1], key=lambda p: p[0].key())
    p2 = partition(lambda pair: is_static_criterion(pair[1]), p1[0])
    static = sorted(p2[1], key=lambda p: p[0].key())
    dynamic = tuple(p2[0])
    # print(f'{equalities=}, {static=}, {dynamic=}')
    return equalities, static, dynamic


class ScenarioForOptaPlanner(Scenario):
    def __init__(self, name: Optional[str], base_package, excel_file, sheet: str = None, default_type=FloatCell(),
                 incremental=True):
        super().__init__(excel_file, sheet, default_type, CellTypeFactory(CELL_TYPES_FOR_OPTAPLANNER))
        self.name = name_to_identifier(name) if name is not None else None
        self.base_package = base_package
        self.incremental = incremental
        self.constants = None
        self.initialized = None
        self.dvars = None
        self.constraints = None
        self.predecessors_cells = None
        self.predecessors_ranges = None
        self.parameter_classes = None
        self.incremental_vars = None
        self.var_names = defaultdict(int)
        self.var_to_code = {}
        self.code_to_var = {}
        self.final_objectives = {}
        self.phase01_constraints = {}
        self.summing_vars: MutableMapping[Sequence[Tuple[str, int, int, int, int]], QualifiedName] = {}
        self.domain_table = DomainTableForScenoptic()
        self.fresh_column_counter = defaultdict(int)
        self.this = MathVariable(THIS)

    def _fresh_name_by_col(self, sheet: str, col: Union[int, str]) -> QualifiedName:
        if isinstance(col, int):
            col = index_to_column(col)
        key = (sheet, col)
        row = self.fresh_column_counter[key] + 1
        self.fresh_column_counter[key] = row
        return QualifiedName(f'{sheet}!{col}{row}', lexical_path=worksheet_path(sheet))

    def _get_or_create_var(self, prefix: str, code: str) -> str:
        if (existing := self.code_to_var.get(code)) is not None:
            return existing
        index = self.var_names[prefix]
        index += 1
        result = f'{prefix}{index}'
        self.var_names[prefix] = index
        self.code_to_var[code] = result
        self.var_to_code[prefix, index] = code
        return result

    def _get_vars(self, prefixes: Sequence[str], constraints: Sequence[str]) -> Sequence[str]:
        return tuple(self._get_or_create_var(prefix, constraint)
                     for prefix, constraint in zip(prefixes, constraints))

    def _value_var_reference_for_cell(self, cell, values_var, index):
        ctype = self.get_type(cell)
        return self.value_var_reference_by_type(ctype, index, values_var)

    def value_var_reference_by_type(self, ctype: CellType, index, values_var, optional=False):
        # base_value = Subscripted(values_var, (Quantity(index),)) if index is not None else values_var
        base_value = (SCENOPTIC_JAVA_GET_QN(Quantity(index), method_target=values_var)
                      if index is not None
                      else values_var)
        if optional or ctype.optional:
            optional_qn = OPTIONAL_TYPE_QNS.get(ctype.mtype.for_java().name)
            if optional_qn is None:
                self.warn(f'Optional type {ctype.mtype} not supported')
                optional_qn = UNKNOWN_QN
            return FunctionApplication(optional_qn,
                                       [Cast(JAVA_WRAPPER_TYPES.get(ctype.mtype, ctype.mtype), base_value)])
        return Cast(ctype.mtype, base_value)

    # TODO: generalize for product
    def incremental_formulas_for_aggregate(self, source_cell: QualifiedName,
                                           scalar_preds: Sequence[QualifiedName], computation: Aggregate,
                                           domain_table: DomainTable) -> Tuple[LambdaExpression, LambdaExpression]:
        container = computation.container
        cells = container.container
        # FIXME!!!! currently only supporting Cells as a parameter of aggregates from SUM/COUNT/IF/S
        condition = container.rest
        vars = container.vars
        n_vars = len(vars)
        if n_vars > 1:
            if not (isinstance(cells, FunctionApplication) and cells.function == ZIP_QN):
                raise Exception(
                    f'Aggregation with multiple vars must have a zip container: {computation} in {source_cell}')
            args = cells.args
        else:
            args = (container.container,)
        if not all(isinstance(a, Cells) for a in args):
            raise Exception(f'Only Cells currently supported for aggregation: {computation} in {source_cell}')
        # FIXME!!! all cells in range must have the same type, except some may be optional and some not
        #  alt. use most general type (union, but doesn't exist)
        arg_types = [self.get_type(next(iter(a)).name) for a in args]
        scalar_types = [self.get_type(a) for a in scalar_preds]
        result_type = self.get_type(source_cell)
        # FIXME!! check that types are compatible, add cast if necessary
        current_qn = FormalContent.fresh_name(CURRENT_QN, 'lambda-').with_type(result_type.mtype)
        values_type = MArray(M_ANY, range(n_vars))
        prev_values_qn = FormalContent.fresh_name(PREVIOUS_VALUES_QN, 'lambda-').with_type(values_type)
        new_values_qn = FormalContent.fresh_name(NEW_VALUES_QN, 'lambda-').with_type(values_type)
        prev_scalars_qn = FormalContent.fresh_name(PREVIOUS_SCALARS_QN, 'lambda-').with_type(values_type)
        new_scalars_qn = FormalContent.fresh_name(NEW_SCALARS_QN, 'lambda-').with_type(values_type)

        current_value = self.value_var_reference_by_type(result_type, None, MathVariable(current_qn), optional=True)
        prev_var_values = [self.value_var_reference_by_type(arg_type, i, MathVariable(prev_values_qn), optional=True)
                           for i, arg_type in enumerate(arg_types)]
        new_var_values = [self.value_var_reference_by_type(arg_type, i, MathVariable(new_values_qn), optional=True)
                          for i, arg_type in enumerate(arg_types)]
        prev_scalar_values = [self.value_var_reference_by_type(arg_type, i, MathVariable(prev_scalars_qn),
                                                               optional=True)
                              for i, arg_type in enumerate(scalar_types)]
        new_scalar_values = [self.value_var_reference_by_type(arg_type, i, MathVariable(new_scalars_qn),
                                                              optional=True)
                             for i, arg_type in enumerate(scalar_types)]
        prev_substitutions = {var: value for var, value in zip(vars, prev_var_values)}
        prev_scalar_substitutions = {var: value for var, value in zip(scalar_preds, prev_scalar_values)}
        prev_substitutions.update(prev_scalar_substitutions)
        new_substitutions = {var: value for var, value in zip(vars, new_var_values)}
        new_scalar_substitutions = {var: value for var, value in zip(scalar_preds, new_scalar_values)}
        new_substitutions.update(new_scalar_substitutions)
        prev_term = computation.term.substitute(prev_substitutions)
        new_term = computation.term.substitute(new_substitutions)
        # FIXME!! not supporting nested comprehension containers or conditions
        if condition is not None:
            if not isinstance(condition, ComprehensionCondition):
                raise Exception(f'Comprehension can only have an associated condition: {computation} in {source_cell}')
            prev_term = IFTE(condition.condition.substitute(prev_substitutions), prev_term, ZERO_AS_QUANTITY)
            new_term = IFTE(condition.condition.substitute(new_substitutions), new_term, ZERO_AS_QUANTITY)
        update_expr = LambdaExpression([current_qn, prev_values_qn, new_values_qn, prev_scalars_qn, new_scalars_qn],
                                       current_value - prev_term + new_term)
        fresh_expr = LambdaExpression([current_qn, new_values_qn, new_scalars_qn],
                                      current_value + new_term)
        domain_table.build(update_expr)
        update_final = exhaustively_apply_rules(EXCEL_TO_JAVA_RULES2, update_expr, domain_table)
        domain_table.build(fresh_expr)
        fresh_final = exhaustively_apply_rules(EXCEL_TO_JAVA_RULES2, fresh_expr, domain_table)
        return update_final, fresh_final

    def incremental_predecessors_for_aggregate(self, computation: Aggregate, source_cell: QualifiedName) -> Tuple[
        int, LambdaExpression]:
        # FIXME!!!!! implement for dragged cells
        comp_container = computation.container
        container = comp_container.container
        vars = comp_container.vars
        n_vars = len(vars)
        if n_vars > 1:
            if not (isinstance(container, FunctionApplication) and container.function == ZIP_QN):
                raise Exception(
                    f'Aggregation with multiple vars must have a zip container: {computation} in {source_cell}')
            ranges = container.args
        else:
            ranges = (container,)
        if not all(isinstance(a, Cells) for a in ranges):
            raise Exception(f'Only Cells currently supported for aggregation: {computation} in {source_cell}')
        # FIXME!!!!!! currently only supporting Cells as parameters
        return self.incremental_predecessors_from_ranges(ranges)

    def incremental_predecessors_from_ranges(self, ranges):
        sheets = [StringTerm(a.sheet) for a in ranges]
        index_qn = QualifiedName('index', type=M_INT, lexical_path=MATH_VAR_FRAME_PATH)
        key_qn = QualifiedName('key', type=M_INT, lexical_path=MATH_VAR_FRAME_PATH)
        index_var = MathVariable(index_qn)
        # Note: Excel uses the size of the first argument for all others
        nrows = ranges[0].end_row - ranges[0].start_row + 1
        ncols = ranges[0].end_col - ranges[0].start_col + 1
        body = MAKE_ABSTRACT_CELL_KEY_ARRAY_QN(
            *[SCENOPTIC_JAVA_CELL_KEY(sheet, *row_and_col_exprs(ranges[i], nrows, index_var),
                                      constructor=True)
              for i, sheet in enumerate(sheets)],
            constructor=True)
        pred_func = LambdaExpression([key_qn, index_qn], body)
        self.domain_table.build(pred_func)
        exhaustively_apply_rules(EXCEL_TO_JAVA_RULES2, pred_func, self.domain_table)
        n_preds = nrows * ncols
        return n_preds, pred_func

    def non_incremental_predecessors_for_aggregate(self, computation: Aggregate) -> Sequence[QualifiedName]:
        # FIXME!!!!! implement for dragged cells
        preds = {cell.name for cell in CELL_COLLECTOR.collect(computation.term)
                 if cell is not None}
        comp_container = computation.container
        condition = comp_container.rest
        # FIXME!! not supporting nested comprehension containers or conditions
        if condition is not None:
            preds.update({cell.name for cell in CELL_COLLECTOR.collect(condition)
                          if cell is not None})
        return sorted(preds)

    def summing_constraint(self, cell_qn: QualifiedName, agg: Aggregate, info: CRITERIA_INFO
                           ) -> Optional[Tuple[Constraint, Sequence[Tuple[QualifiedName, AbstractConstraint]]]]:
        if agg.term != ONE_AS_QUANTITY:
            return None
        equalities, static, dynamic = info
        if not (equalities and not static and not dynamic):
            # FIXME!!! support static and dynamic conjuncts
            return None
        key = tuple(e[0].key() for e in equalities)
        cell_type = self.get_type(cell_qn)
        if (summing_qn := self.summing_vars.get(key)) is not None:
            pass
        else:
            summing_qn = self._fresh_name_by_col(f'summing!{cell_qn.name}', 'S').with_type(MClassType(ISUMMING_CELL_QN))
            self.set_type(summing_qn, ClassCellType(ISUMMING_CELL_QN))
            self.summing_vars[key] = summing_qn
        if isinstance(cell_type, IntegerCell):
            getter = SUMMING_CELL_GET_INT_QN
        elif isinstance(cell_type, FloatCell):
            getter = SUMMING_CELL_GET_DOUBLE_QN
        else:
            raise Exception(f'Unsupported type {cell_type} for summing {cell_qn}')
        scalars = [e[2][1] for e in equalities]
        fetch_code = getter(
            JAVA_LIST_OF_QN(*scalars,
                            method_target=MathVariable(JAVA_LIST_OF_OWNER)),
            method_target=MathVariable(summing_qn))
        predecessors = (cell
                        for scalar in scalars
                        for cell in CELL_COLLECTOR.collect(scalar)
                        if cell is not None)
        fetch_constraint = OptaPhase01Constraint(fetch_code, (summing_qn, *(p.name for p in predecessors)), set(),
                                                 cell_qn)
        ranges = [e[0] for e in equalities]
        n_preds, pred_func = self.incremental_predecessors_from_ranges(ranges)
        # FIXME!!!!!! add appropriate constructor arguments
        process_constructor_list = JAVA_LIST_OF_QN(
            SCENOPTIC_JAVA_SINGLE_INT_SUMMING_CREATOR_QN(constructor=True),
            method_target=MathVariable(JAVA_LIST_OF_OWNER))
        # FIXME!!!!!! add scalar predecessors
        scalar_predecessors = JAVA_LIST_OF_QN(
            method_target=MathVariable(JAVA_LIST_OF_OWNER))
        # FIXME!!!!!! use SUMMING_SHADOW_CELL_QN for sums; for sums need need a formula to compute the term, also
        #  a selector for the registerKey from the prev/newValues
        counting_shadow_cell_class = QualifiedName(self.class_name(COUNTING_SHADOW_CELL_CLASS_SUFFIX),
                                                   lexical_path=reversed(self.base_package.split('.')))
        constructor_expr = LambdaExpression(CONSTRUCTING_FORMULA_PARAMS,
                                            counting_shadow_cell_class(*map(MathVariable, CONSTRUCTING_FORMULA_PARAMS),
                                                                       scalar_predecessors,
                                                                       Quantity(n_preds),
                                                                       pred_func,
                                                                       process_constructor_list,
                                                                       constructor=True))
        all_cells = set(cell.name
                        for cell in itertools.chain.from_iterable(CELL_COLLECTOR.collect(cond[0])
                                                                  for cond in equalities)
                        if cell is not None)
        summing_constraint = SummingConstraint(constructor_expr, n_preds, pred_func, all_cells)
        # FIXME!!!!!! mark somehow to generate a SummingCellInfo rather than a ShadowCell
        self.dummy_cells[summing_qn] = constructor_expr
        return fetch_constraint, ((summing_qn, summing_constraint),)

    def cell_to_constraint_phase01(self, cell: QualifiedName, contents, domain_table: DomainTable = None):
        """
        This phase transforms the parsed formula into an equivalent form and collects predecessor information.

        Incremental subexpressions are extracted and returned for further processing.
        """
        if contents is None:
            # FIXME!!!!!! incompatible use of code (not FormalContent), fix classes
            return OptaPhase01Constraint(code=Constant(None), predecessors=[], subexpression_cells=set(),
                                         original_cell=cell), ()
        # contents can be an expression (FormalContent) for dummy cells
        expr0 = (contents if isinstance(contents, FormalContent)
                 else parse_formula(contents, self, get_sheet_in_cell_qn_as_string(cell)))
        if domain_table is not None:
            domain_table.build(expr0)
        # FIXME!!!!!! return code=expr0
        if isinstance(expr0, (Quantity, StringTerm)):
            return OptaPhase01Constraint(code=Constant(expr0.to_code_rep().value), predecessors=[],
                                         subexpression_cells=set(),
                                         original_cell=cell), ()
        subexpression_splitter = IncrementalsSplitter(expr0, cell.name, domain_table)
        expr1 = exhaustively_apply_rules(subexpression_splitter, expr0, domain_table)
        self.dummy_cells.update(subexpression_splitter.new_variables)
        for cell_qn, value in subexpression_splitter.new_variables.items():
            self.set_type(cell_qn, mtype_to_cell_type(value.appl_info.type))
        subexpression_cells = set(subexpression_splitter.new_variables.keys())
        expr2 = exhaustively_apply_rules(EXCEL_RULES0A, expr1, domain_table)
        expr3 = exhaustively_apply_rules(EXCEL_RULES0B, expr2, domain_table)
        if self.incremental and isinstance(expr3, Aggregate) and expr3.op == '+':
            # FIXME!!!!!! index info by the ranges of the equalities, reuse same summing cell (and add summing cell
            #  as predecessor to all count/sums that use it)
            if ((info := summing_cell_info(expr3)) is not None
                    and (summing_result := self.summing_constraint(cell, expr3, info)) is not None):
                contents = summing_result[0]
                additional_constraints = summing_result[1]
                return contents, additional_constraints
            non_inc_preds = self.non_incremental_predecessors_for_aggregate(expr3)
            all_inc_preds = {cell.name
                             for cell in CELL_COLLECTOR.collect(expr3.container.container)
                             if cell is not None}
            return IncrementalPhase01Constraint(expr3, non_inc_preds, subexpression_cells, cell, all_inc_preds), ()
        cells = {cell.name for cell in CELL_COLLECTOR.collect(expr3)
                 if cell is not None}
        return OptaPhase01Constraint(expr3, cells, subexpression_cells, cell), ()

    def cell_to_constraint_phase02(self, cell: QualifiedName, contents: Phase01Constraint,
                                   domain_table: DomainTable = None
                                   ) -> Tuple[AbstractConstraint, Sequence[Tuple[QualifiedName, AbstractConstraint]]]:
        """
        This phase creates Constraint objects, containing the code transformed for the Java framework; this includes
        the creation of the incremental fresh/update functions and incremental-predecessors function for incremental
        cells.
        """
        if isinstance(contents, SummingConstraint):
            return contents, ()
        if isinstance(contents.code, Constant):
            return contents.code, ()
        subexpression_cells = contents.subexpression_cells
        expr3 = contents.code
        if isinstance(contents, IncrementalPhase01Constraint):
            non_inc_preds = contents.predecessors
            all_inc_preds = contents.all_inc_predecessors
            incr_update_expr, incr_fresh_expr = self.incremental_formulas_for_aggregate(
                cell, non_inc_preds, expr3, domain_table)
            num, inc_preds_func = self.incremental_predecessors_for_aggregate(expr3, cell)
            return IncrementalConstraint(incr_update_expr, incr_fresh_expr, num, inc_preds_func,
                                         expr3.term.appl_info.type, all_inc_preds, non_inc_preds,
                                         subexpression_cells), ()
        cells = contents.predecessors
        values_qn = FormalContent.fresh_name(VALUES_QN, 'lambda-')
        values_var = MathVariable(values_qn)
        func0 = LambdaExpression((values_qn,), expr3)
        if domain_table is not None:
            domain_table.build(func0)
        func1 = exhaustively_apply_rules(EXCEL_TO_JAVA_RULES1, func0, domain_table)
        values_refs = [self._value_var_reference_for_cell(cell, values_var, index)
                       for index, cell in enumerate(cells)]
        substitutions = dict(zip(cells, values_refs))
        func2 = func1.substitute(substitutions)
        if domain_table is not None:
            domain_table.build(func2)
        code = exhaustively_apply_rules(EXCEL_TO_JAVA_RULES2, func2, domain_table)
        result = OptaPlannerConstraint(code, cells, subexpression_cells)
        return result, ()

    def convert_to_language(self, expression: FormalContent):
        return convert_excel_expr_to_java(expression)

    def _analyze_parameters(self):
        """
        Determine the required planning-var classes, depending on the types and ranges of parameters
        """
        parameter_classes = {param: self.get_type(param) for param in self.parameters}
        if None in parameter_classes.values():
            self.warn(
                f'Missing type for '
                f'{", ".join(str(param) for param in self.parameters if self.get_type(param) is None)}')
        if not all(isinstance(c, PlanningVarRange) for c in parameter_classes.values()):
            non_range_params = ", ".join(
                str(param) for param in self.parameters if
                not isinstance(self.get_type(param), PlanningVarRange))
            self.warn(f'Type for {non_range_params} is not a range')
        self.parameter_classes = parameter_classes

    def _parse_name(self, row, first_col):
        """
        Parse a name for the decision problem, which is a single string

        :param row: number of row containing the name
        :param first_col: number of column containing the name (one after header)
        """
        name = self.cell_value(row, first_col, str)
        if name is None:
            self.warn(f'Bad value for name argument: {name} in {coords_to_cell(row, first_col)}')
        else:
            if self.name is not None:
                self.warn(f'Overriding name to {name} (was {self.name})')
            self.name = name_to_identifier(name)

    def _parse_package(self, row, first_col):
        """
        Parse a package for the generated code, which is a single string

        :param row: number of row containing the package
        :param first_col: number of column containing the package (one after header)
        """
        package = self.cell_value(row, first_col, str)
        if package is None:
            self.warn(f'Bad value for package argument: {package} in {coords_to_cell(row, first_col)}')
        else:
            if self.base_package is not None:
                self.warn(f'Overriding package to {package} (was {self.base_package})')
            self.base_package = package

    def _block_parsers(self) -> Mapping[str, Callable[[Sequence[int], int], None]]:
        base = super()._block_parsers()
        name_parser = self._parse_name
        package_parser = self._parse_package
        return {**base, 'name': name_parser, 'package': package_parser}

    def validate_initialization(self):
        if (self.name is None or self.base_package is None or self.parameters is None or self.types is None
                or self.objectives is None):
            raise Exception(f'Scenario not initialized properly')

    def build(self):
        self.find_translation_arguments()
        self.validate_initialization()
        domain_table = self.domain_table
        all_predecessors = {}
        constraints = {}
        objective_cells = self.create_objective_cells(constraints)
        analyzed_names, constants = self.collect_constraints_phase01(objective_cells, domain_table)
        self.order_predecessors(verbose=False)

        for cell, constraint_phase01 in self.phase01_constraints.items():
            code, additional_constraints = self.cell_to_constraint_phase02(cell, constraint_phase01, domain_table)
            constraints.update(additional_constraints)
            if isinstance(code, Constant):
                continue
            assert isinstance(code, (OptaPlannerConstraint, IncrementalConstraint, SummingConstraint))
            constraints[cell] = code
            set_of_analyzed_cells = set(code.predecessors)
            if isinstance(code, IncrementalConstraint):
                set_of_analyzed_cells.update(code.all_inc_predecessors)
            all_predecessors[cell] = set_of_analyzed_cells

        dependents = invert_map(all_predecessors)
        dvars = transitive_closure(dependents, self.parameters, reflexive=False)
        summing_cells = {cell for cell, constraint in self.phase01_constraints.items()
                         if isinstance(constraint, SummingConstraint)}
        initialized = analyzed_names - set(constants.keys()) - dvars - set(self.parameters) - summing_cells
        self._analyze_parameters()
        self.constants = constants
        self.initialized = initialized
        self.dvars = dvars
        self.constraints = constraints
        self.incremental_vars = {inc for inc, constraint in self.constraints.items()
                                 if isinstance(constraint, IncrementalConstraint)}

    def create_objective_cells(self, constraints):
        specification_sheet_name = self.specification_sheet_name()
        serial = 0
        # Create Incremental Objective dummy cell
        objective_cells = set()
        for cell_spec, objective_specs in self.objectives.items():
            cell1, cell2, sheet = range_to_cells(cell_spec, specification_sheet_name)
            if cell2 is None:
                cell_qn = normalize_cell_qn(cell_spec, sheet)
                objective_cells.add(cell_qn)
                self.final_objectives[cell_qn] = objective_specs
            else:
                # create a new shadow cell to represent the sum of the objective range
                # check that all cells in range have the same type
                mtypes = {self.get_type(cell).mtype for cell in xl_cell_or_range_elements_qn(cell_spec, sheet)}
                if len(mtypes) != 1:
                    raise Exception(f'Different types for range {cell_spec}')
                cell1_qn = normalize_cell_qn(cell1, sheet)
                serial += 1
                cell1_type = self.get_type(cell1_qn).mtype
                obj_sheet = f'objectives!{cell_spec}'
                sum_qn = QualifiedName(f'{obj_sheet}!S{serial}', cell1_type,
                                       lexical_path=worksheet_path(obj_sheet))
                self.set_type(sum_qn, mtype_to_cell_type(cell1_type))
                sum_var = MathVariable(sum_qn)
                objective_value = Aggregate(
                    '+', sum_var,
                    ComprehensionContainer([sum_qn], Cells(Cell(*cell_to_coords(cell1), sheet),
                                                           Cell(*cell_to_coords(cell2), sheet))))
                self.dummy_cells[sum_qn] = objective_value
                self.domain_table.build(sum_var.defined_as(objective_value))
                objective_cells.add(sum_qn)
                constraints[sum_qn] = objective_value
                self.final_objectives[sum_qn] = objective_specs
        return objective_cells

    def collect_constraints_phase01(self, objective_cells, domain_table):
        analyzed_names = objective_cells
        constants = {}
        definitions = []
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
            if cell in self.phase01_constraints:
                continue
            contents = self.cell_qn_value(cell)
            # print(f'Cell {cell}: {contents}')
            code, additional_constraints = self.cell_to_constraint_phase01(cell, contents, domain_table)
            if not code:
                self.warn(f'Failed to parse cell <{cell}> with contents <{contents}>')
                continue
            for cell, code in itertools.chain([(cell, code)], additional_constraints):
                self.phase01_constraints[cell] = code
                if isinstance(code.code, Constant):
                    constants[cell] = code.code.value
                else:
                    if isinstance(code, (OptaPhase01Constraint, IncrementalPhase01Constraint)):
                        # but not SummingConstraint
                        definition = Cell(*cell_qn_to_components(cell)).defined_as(code.code)
                        domain_table.build(definition)
                        definitions.append(definition)
                    non_inc_preds = code.predecessors
                    set_of_analyzed_cells = set(non_inc_preds)
                    if isinstance(code, (IncrementalPhase01Constraint, SummingConstraint)):
                        set_of_analyzed_cells.update(code.all_inc_predecessors)
                    new_cells = code.subexpression_cells
                    for free in sorted((set_of_analyzed_cells | set(new_cells)) - analyzed_names - parameters):
                        agenda.put(free)
                    analyzed_names |= set_of_analyzed_cells
        domain_table.propagate()
        return analyzed_names, constants

    def order_predecessors(self, verbose=False):
        ordered_cells_by_column = sorted(self.phase01_constraints.keys(),
                                         key=lambda e: itemgetter(2, 1, 0)(cell_qn_to_components(e)))
        if verbose:
            print("Original Constraint Predecessors:")
            print("\n".join(
                f'{e.name}: predecessors[{self.phase01_constraints[e].predecessors}]' for e in ordered_cells_by_column))

        # Step 1: For each cell, split the constraint predecessors, into types,
        #         Identify fixed cell predecessors between successive column cells, label them as "fixed_cells"
        #         label "predecessors" the group of cells less the one's in the "fixed_cells"
        #         These two types, will be aggregated differently during category extraction during range collections
        #
        # """
        # We iterate through the ordered columns,
        # the step is done from start of a column to the end of that column, from column "A" until "ZZZ" if exists,
        # once the end of the column is reached the next step is the start of the next column.
        #
        # The "origin_qn" refers to the first introduced column cell,
        # the "current_qn" refers to the successive cells in the column.
        #
        # We discard the current "origin_qn" value, when the following criteria met:
        # 1. The current "fixed_cells" between "current_qn" and "origin_qn" is empty.
        #    in this case we should log the "origin_qn" with the last identified
        #    "intersections" and remove these to set the predecessors.
        #    note, since we step through down the column with the value of "current_qn"
        #    it is possible, that just before the last "current_qn" we did find an "fixed_cells"
        #    so we must log it for the last "origin_qn", before we switch to a new "origin_qn"
        #    Once, we logged, we set the "current_qn" to be the new "origin_qn"
        # 2. If the current "fixed_cells" exists and not empty, two options here:
        #    2a. If the "last fixed_cells" (with previous "current_qn") was empty
        #          (i.e. the "origin_qn" was set by the previous "current_qn" as in criteria 1,)
        #        OR
        #        if the "last fixed_cells" (with previous "current_qn") existed, AND it is
        #        identical to current "fixed_cells"
        #         if so:
        #            we log the "current_qn" with the this "fixed_cells".
        #            and update the "last_intersection" with current information.
        #     2b. If the "last fixed_cells" (with previous "current_qn") existed (not empty),
        #         AND
        #         the "last fixed_cells" is NOT identical to current "fixed_cells",
        #         if so:
        #           The "origin_qn" intersected with previous "current_qn" on different cells
        #           we can not consider it as a match with the current "current_qn".
        #           We set up the "current_qn" as the new "origin_qn"
        #           We reset the "last fixed_cells"

        predecessors_types = {}
        last_origin_predecessors = dict(predecessors=[], fixed_cells=[])
        origin_qn = None
        for current_qn in ordered_cells_by_column:
            if not origin_qn:
                origin_qn = current_qn
                origin_predecessors = set(sorted(self.phase01_constraints[origin_qn].predecessors))
                last_origin_predecessors = dict(predecessors=list(origin_predecessors), fixed_cells=[])
                continue
            origin_predecessors = set(sorted(self.phase01_constraints[origin_qn].predecessors))
            current_predecessors = set(sorted(self.phase01_constraints[current_qn].predecessors))
            fixed_cells = sorted(origin_predecessors & current_predecessors,
                                 key=lambda e: itemgetter(2, 1, 0)(cell_qn_to_components(e)))
            if verbose:
                print(f'origin: {origin_qn.name} -- cur: {current_qn.name} = {fixed_cells}')
            if not fixed_cells:
                # 1. The current "fixed_cells" between "current_qn" and "origin_qn" is empty. (criteria 1 above)
                predecessors_types[origin_qn] = dict(
                    predecessors=list(origin_predecessors - set(last_origin_predecessors.get('fixed_cells', []))),
                    fixed_cells=last_origin_predecessors.get('fixed_cells', []))
                origin_qn = current_qn
                last_origin_predecessors = dict(predecessors=list(current_predecessors), fixed_cells=[])
            elif not last_origin_predecessors.get('fixed_cells', []) or \
                    last_origin_predecessors['fixed_cells'] == fixed_cells:
                predecessors_types[current_qn] = dict(predecessors=list(current_predecessors - set(fixed_cells)),
                                                      fixed_cells=fixed_cells)
                last_origin_predecessors = dict(predecessors=list(origin_predecessors - set(fixed_cells)),
                                                fixed_cells=fixed_cells)
            else:
                origin_qn = current_qn
                last_origin_predecessors = dict(predecessors=list(current_predecessors), fixed_cells=[])
        predecessors_types[origin_qn] = last_origin_predecessors
        if verbose:
            print(f'\nSplit Predecessors by Type:')
            print("\n".join(f'{k.name}:{v}' for k, v in predecessors_types.items()))
            print()

        #
        # Step 2: Collect the constraints cells into groups,
        #         But, first, for each cell constraint ,
        #              1. we group it's "predecessors"
        #                 into regular "cells" and "ranges" (i.e successful grouping into successive range)
        #                 for either of them we extract category tuple components, based on distance from the original
        #                  cell constraint.
        #              2. We use the "fixed_cells" members as is using its qualified name, where the category
        #                  based on these qualified names is ordered by the column
        #
        #
        if verbose:
            print(f'Collecting Ranges and Cells:')
        cells, ranges = self._collect_ranges(
            [dict(cell=extract_cell_components_to_dict(cell.name),
                  **self.extract_predecessors_query_category(
                      extract_cell_components_to_dict(cell.name),
                      pred_type.get('predecessors', []), verbose=False),
                  fixed_cells=tuple(sorted((extract_cell_components(e.name) for e in pred_type['fixed_cells']),
                                           key=lambda e: itemgetter(0, 2, 1)(e))))
             for cell, pred_type in predecessors_types.items() if
             not isinstance(self.phase01_constraints[cell].code, Constant)],
            grouping_keys=('cells_category', 'range_category', 'fixed_cells'),
            verbose=verbose)

        #
        # Step 3: We expand,extract the above ordered predecessors, into ordered qualified names
        #         the order is:
        #          (fixed_columns_qn,  regular_cells_qn, cells_in_range_qn) each sub set ordered by column
        #
        def cell_spec_to_qn(row: int, col: int, sheet: str) -> QualifiedName:
            cell_qn = as_cell_qn(row, col, sheet)
            return cell_qn.with_type(self.get_type(cell_qn))

        def expand_cell_info(cell_key: CellSpec,
                             # sheet, row, col
                             fixed_cells: Tuple[Tuple[str, int, int], ...],
                             # sheet, row_distance, col_distance
                             cells_category: Tuple[Tuple[str, int, int], ...],
                             # sheet, first_row_dist, end_row_dist, first_col_dist, end_col_dis
                             range_category: Tuple[Tuple[str, int, int, int, int], ...]):
            cell_qn = cell_spec_to_qn(cell_key['row'], cell_key['col'], cell_key['sheet'])

            fixed_cells_qn = [cell_spec_to_qn(row, col, sheet)
                              for sheet, row, col in fixed_cells]

            cells_by_distance_qn = [
                cell_spec_to_qn(cell_key['row'] + distance[1],
                                cell_key['col'] + distance[2],
                                distance[0])
                for distance in cells_category]

            range_by_distance_qn = \
                [cell_spec_to_qn(row, col, sheet)
                 for sheet, first_row_dist, end_row_dist, first_col_dist, end_col_dist in range_category
                 for row in range(cell_key['row'] + first_row_dist, cell_key['row'] + end_row_dist + 1)
                 for col in range(cell_key['col'] + first_col_dist, cell_key['col'] + end_col_dist + 1)]
            return dict(cell=cell_qn, predecessors=[*fixed_cells_qn, *cells_by_distance_qn, *range_by_distance_qn])

        cells_predecessors_by_cell = [expand_cell_info(cell['cell'],
                                                       cell['fixed_cells'],
                                                       cell['cells_category'],
                                                       cell['range_category'])
                                      for cell in sorted(cells, key=lambda c: (c['key']))]

        cells_predecessors_by_range = [
            expand_cell_info(dict(sheet=arange['range']['sheet'], row=row, col=col),
                             arange['fixed_cells'],
                             arange['cells_category'],
                             arange['range_category'])
            for arange in sorted(ranges, key=lambda c: (c['key']))
            for col in range(arange['range']['start_col'], arange['range']['end_col'] + 1)
            for row in range(arange['range']['start_row'], arange['range']['end_row'] + 1)]

        #
        # Step 4: update the cell constraints with the updated ordered predecessors
        #
        if verbose:
            print('Ordered Predecessors:')
        for cell in itertools.chain(cells_predecessors_by_cell, cells_predecessors_by_range):
            if verbose:
                print(f'{cell}')
            self.phase01_constraints[cell['cell']] = \
                self.phase01_constraints[cell['cell']].with_predecessors(cell['predecessors'])

        #
        # Step 5: Keep the predecessors compression to ranges for java synthesis
        #
        self.predecessors_cells = cells
        self.predecessors_ranges = ranges

    def _score_expressions(self) -> Tuple[Sequence[FormalContent], Sequence[FormalContent]]:
        """
        Return the list of expressions for hard constraints and the list for soft constraints
        """
        solution_var_path = ('calculateScore',
                             f'{self.name}ScoreCalculator',
                             extend_package(self.base_package, SOLVER_PACKAGE_SUFFIX),
                             '*java-base*')
        solution_var = MathVariable(
            QualifiedName('solution',
                          type=MClassType(QualifiedName(solution_var_path[1], lexical_path=solution_var_path[2:])),
                          lexical_path=solution_var_path))

        def expression(cell, direction) -> FormalContent:
            components = extract_cell_components_to_dict(cell.name)
            key_expr = FunctionApplication(
                SCENOPTIC_JAVA_CELL_KEY,
                [StringTerm(components['sheet']), Quantity(components['row']), Quantity(components['col'])],
                constructor=True)
            expr = Cast(self.get_type(cell).mtype,
                        (SCENOPTIC_JAVA_GET_INCREMENTAL_VALUE_QN if cell in self.incremental_vars else
                         SCENOPTIC_JAVA_GET_VALUE_QN)(solution_var, key_expr, method_target=self.this))
            return expr if direction == OptimizationDirection.MAXIMIZE else FunctionApplication(to_math('-'), [expr])

        def level_expression(cells: Tuple[str, bool]):
            if len(cells) == 1:
                return expression(*cells[0])
            return FunctionApplication(to_math('+'), [expression(*cell) for cell in cells])

        level_info = defaultdict(list)
        for cell_qn, (level, direction) in self.final_objectives.items():
            level_info[level].append((cell_qn, direction))
        levels = sorted(level_info.keys(), reverse=True)
        hard_levels = []
        soft_levels = []
        # FIXME!!!!! create a new shadow cell for each level that has more than one element
        #  (must be called during build)
        for level in levels:
            (hard_levels if level > 0 else soft_levels).append(level_info[level])
        return [level_expression(info) for info in hard_levels], [level_expression(info) for info in soft_levels]

    def _compute_java_vars(self):
        for constraint in self.constraints.values():
            if isinstance(constraint, OptaPlannerConstraint):
                code = self.convert_to_language(constraint.code)
                vars = self._get_or_create_var('CF', code)
            elif isinstance(constraint, IncrementalConstraint):
                code = (self.convert_to_language(constraint.incremental_update_formula),
                        self.convert_to_language(constraint.incremental_fresh_formula),
                        self.convert_to_language(constraint.incremental_predecessors_formula))
                vars = self._get_vars(('IUF', 'IFF', 'IPF'), code)
            elif isinstance(constraint, SummingConstraint):
                code = self.convert_to_language(constraint.constructor_expr)
                vars = self._get_or_create_var('SIF', code)
            else:
                continue
            constraint.vars = vars

    def _collect_ranges(self,
                        info,
                        grouping_keys: Tuple[Any, ...] = (),
                        verbose: bool = False):
        """
        params:
        info: a list of dictionary each consists of following keys:
        a. Mandatory keys:
            - "cell" - holds set of cells with structure Tuple[str, int, int]
                        representing (sheet_name, row_index, col_index)
        b. optional keys, any number of keys to be used as aggregator keys grouping cells

        grouping_keys - tuple of keys to use to aggregate ranges by their values
        """
        if isinstance(info, list):
            # first_element = info[0]
            # grouping_keys = group_keys if group_keys else \
            #     {key for key in first_element.keys() if key != "cell" and key != "key"}
            #

            if grouping_keys:
                value_func = lambda e: itemgetter(*grouping_keys)(e) if len(grouping_keys) > 1 else (itemgetter(
                    *grouping_keys)(e),)

            else:
                value_func = lambda e: ()
            query_category = {tuple(element['cell'].values()): value_func(element) for element in info}
            if verbose:
                print(f'Categories: {query_category}')

            def get_category(cell):
                return query_category.get(cell, ())

            candidates = {tuple(element['cell'].values()) for element in info}

            find = AnalyzeCellRanges()
            cells, ranges = find.analyze_by_category(candidates, get_category)

            if verbose:
                print(f'Cells: {cells}')
                print(f'Ranges: {ranges}')

            the_cells = [{**{'cell': cell, 'key': itemgetter(0, 2, 1)(tuple(cell.values()))},
                          **{name: value for name, value in zip(grouping_keys, e[1])}}
                         for e in cells
                         for cell in e[0]]
            if verbose:
                print("\n".join(f'{r}' for r in the_cells))

            the_ranges = [{**{'range': arange, 'key': itemgetter(0, 2, 1)(tuple(arange.values()))},
                           **{name: value for name, value in zip(grouping_keys, e[1])}}
                          for e in ranges
                          for arange in e[0]]
            if verbose:
                print("\n".join(f'{r}' for r in the_ranges))
                print()

            return the_cells, the_ranges

    def extract_predecessors_query_category(self,
                                            key_cell: CellSpec,
                                            predecessors: Sequence[QualifiedName],
                                            verbose=False):
        cells, ranges = self._collect_ranges([dict(cell=extract_cell_components_to_dict(c.name))
                                              for c in sorted(predecessors)],
                                             verbose=verbose)

        cells_category = tuple((cell['cell']['sheet'],
                                cell['cell']['row'] - key_cell['row'],
                                cell['cell']['col'] - key_cell['col'])
                               for cell in sorted(cells, key=lambda c: (c['key'])))

        range_category = tuple((arange['range']['sheet'],
                                arange['range']['start_row'] - key_cell['row'],
                                arange['range']['end_row'] - key_cell['row'],
                                arange['range']['start_col'] - key_cell['col'],
                                arange['range']['end_col'] - key_cell['col'])
                               for arange in sorted(ranges, key=lambda c: (c['key'])))

        return dict(cells_category=cells_category, range_category=range_category)

    def to_java(self, java_base_folder):
        self._compute_java_vars()

        solver_package = extend_package(self.base_package, SOLVER_PACKAGE_SUFFIX)
        main_package = extend_package(self.base_package, MAIN_PACKAGE_SUFFIX)
        domain_package = extend_package(self.base_package, DOMAIN_PACKAGE_SUFFIX)

        env = Environment(loader=PackageLoader('scenoptic', 'templates'), trim_blocks=True,  # lstrip_blocks=True
                          autoescape=select_autoescape([]))
        top_folder = Path(java_base_folder) / package_to_path(self.base_package)
        top_folder.mkdir(parents=True, exist_ok=True)
        (top_folder / MAIN_PACKAGE_SUFFIX).mkdir(parents=True, exist_ok=True)
        (top_folder / DOMAIN_PACKAGE_SUFFIX).mkdir(parents=True, exist_ok=True)
        (top_folder / SOLVER_PACKAGE_SUFFIX).mkdir(parents=True, exist_ok=True)
        entity_classes = sorted({c.java_class_name() for c in self.parameter_classes.values()})
        main_template = env.get_template('main-template.java')
        main_template = template_functions.set_global_functions(main_template)
        # FIXME!!! add non_strict_cells
        # FIXME!!! add incremental_predecessors with fields name, pred_lists (list of cell names)
        # FIXME!!! add incremental_formulas
        # FIXME!!! add IncrementalCell subclass to entity_classes
        functions = [dict(name=f'{prefix}{index}',
                          code=self.var_to_code[prefix, index],
                          type=PREFIX_TO_JAVA_TYPE[prefix])
                     for prefix, index in sorted(self.var_to_code.keys())]
        with open(top_folder / MAIN_PACKAGE_SUFFIX / f'{self.name}Main.java',
                  'w', encoding='utf8') as f:
            decisions = self._collect_ranges([dict(cell=extract_cell_components_to_dict(param.name),
                                                   class_suffix=self.parameter_classes[param].java_class_name())
                                              for param in self.parameters],
                                             grouping_keys=('class_suffix',))
            dvars = self._collect_ranges([dict(cell=extract_cell_components_to_dict(d.name),
                                               formula=self.constraints[d].vars)
                                          for d in self.dvars - self.incremental_vars
                                          if isinstance(self.constraints[d], Constraint)],
                                         grouping_keys=('formula',))
            incremental = self._collect_ranges([dict(cell=extract_cell_components_to_dict(cell.name),
                                                     n_preds=c.n_preds,
                                                     update_formula=c.vars[0],
                                                     fresh_formula=c.vars[1],
                                                     formula=c.vars[2],
                                                     element_type=incremental_initializer_class(c.element_type))
                                                for cell, c in self.constraints.items()
                                                if isinstance(c, IncrementalConstraint)],
                                               grouping_keys=('n_preds', 'formula', 'element_type', 'update_formula',
                                                              'fresh_formula'))
            inputs = self._collect_ranges([dict(cell=extract_cell_components_to_dict(cell.name))
                                           for cell in self.initialized | self.constants.keys()])
            summing = self._collect_ranges([dict(cell=extract_cell_components_to_dict(cell.name),
                                                 creator=c.vars)
                                            for cell, c in self.constraints.items()
                                            if isinstance(c, SummingConstraint)],
                                           grouping_keys=('creator',))
            print(main_template.render(scenario_name=self.name,
                                       package=main_package,
                                       domain_package=domain_package,
                                       solver_package=solver_package,
                                       functions=functions,
                                       decisions=decisions,
                                       dvars=dvars,
                                       summing=summing,
                                       initialized=[],
                                       predecessors=(self.predecessors_cells, self.predecessors_ranges),
                                       incremental=incremental,
                                       inputs=inputs,
                                       entity_classes=entity_classes),
                  file=f)
        shadow_template = env.get_template('shadow-var-template.java')
        with open(top_folder / DOMAIN_PACKAGE_SUFFIX / f'{self.name}ShadowCell.java', 'w', encoding='utf8') as f:
            print(shadow_template.render(scenario_name=self.name,
                                         package=domain_package,
                                         shadow_cell_class='ShadowCell',
                                         planning_classes=entity_classes),
                  file=f)
        if summing[0]:
            # TODO: add SummingShadowCell when implemented
            summing_var_template = env.get_template('summing-var-template.java')
            with open(top_folder / DOMAIN_PACKAGE_SUFFIX / f'{self.name}CountingShadowCell.java',
                      'w', encoding='utf8') as f:
                print(summing_var_template.render(scenario_name=self.name,
                                                  package=domain_package,
                                                  superclass='CountingShadowCellImpl',
                                                  shadow_cell_class='CountingShadowCell',
                                                  planning_classes=entity_classes),
                      file=f)
        if False:
            # TODO: generate for dragged formulas!
            dragged_template = env.get_template('dragged-var-template.java')
            with open(top_folder / DOMAIN_PACKAGE_SUFFIX / f'{self.name}DraggedCell.java', 'w',
                      encoding='utf8') as f:
                print(dragged_template.render(scenario_name=self.name,
                                              package=domain_package,
                                              planning_classes=entity_classes),
                      file=f)
        incremental_template = env.get_template('incremental-var-template.java')
        with open(top_folder / DOMAIN_PACKAGE_SUFFIX / f'{self.name}IncrementalCell.java', 'w',
                  encoding='utf8') as f:
            print(incremental_template.render(scenario_name=self.name,
                                              package=domain_package,
                                              planning_classes=entity_classes),
                  file=f)
        if False:
            # TODO: generate for dragged formulas!
            dragged_incremental_template = env.get_template('dragged-incremental-var-template.java')
            with open(top_folder / DOMAIN_PACKAGE_SUFFIX / f'{self.name}DraggedIncrementalCell.java', 'w',
                      encoding='utf8') as f:
                print(dragged_incremental_template.render(scenario_name=self.name,
                                                          package=domain_package,
                                                          planning_classes=entity_classes),
                      file=f)
        # FIXME!!! create incremental vars
        planning_template = env.get_template('planning-var-template.java')
        for planning_class in self.parameter_classes.values():
            class_name = planning_class.java_class_name()
            with open(top_folder / DOMAIN_PACKAGE_SUFFIX / f'{self.name}{class_name}.java', 'w',
                      encoding='utf8') as f:
                print(planning_template.render(scenario_name=self.name,
                                               package=domain_package,
                                               planning_class=class_name,
                                               java_type=planning_class.mtype.for_java_boxed()),
                      file=f)
        hard_exprs, soft_exprs = self._score_expressions()
        solution_template = env.get_template('solution-template.java')
        solution_template = template_functions.set_global_functions(solution_template)
        with open(top_folder / SOLVER_PACKAGE_SUFFIX / f'{self.name}Solution.java', 'w', encoding='utf8') as f:
            planning_classes = [dict(name=cls.java_class_name(),
                                     type=cls.java_type_name(),
                                     constructor=cls.java_constructor())
                                if cls.has_constructor
                                else dict(name=cls.java_class_name(),
                                          type=cls.java_type_name(),
                                          value=cls.values(self))
                                for cls in set(self.parameter_classes.values())]
            print(solution_template.render(scenario_name=self.name,
                                           package=solver_package,
                                           n_hard=len(hard_exprs),
                                           n_soft=len(soft_exprs),
                                           planning_classes=planning_classes),
                  file=f)
        score_template = env.get_template('score-calculator-template.java')
        score_template = template_functions.set_global_functions(score_template)
        # FIXME!!! use getIncrementalValue when relevant
        with open(top_folder / SOLVER_PACKAGE_SUFFIX / f'{self.name}ScoreCalculator.java', 'w',
                  encoding='utf8') as f:
            print(score_template.render(scenario_name=self.name,
                                        package=solver_package,
                                        domain_package=domain_package,
                                        hard_exprs=[self.convert_to_language(e) for e in hard_exprs],
                                        soft_exprs=[self.convert_to_language(e) for e in soft_exprs]),
                  file=f)

    def class_name(self, suffix) -> str:
        return f'{self.name}{suffix}'


class CollectTemplatesGlobalFunctions:
    functions = {}

    def __call__(self, func):
        if isfunction(func) and not self.functions.get(func.__name__):
            self.functions[func.__name__] = func
            return func

    def set_global_functions(self, template):
        for func_name, function in self.functions.items():
            template.globals[func_name] = function
        return template


template_functions = CollectTemplatesGlobalFunctions()


@template_functions
def normalize_java_vars(var_name: str):
    return convert_to_java_string(var_name)


def run_excel_test(excel_file, java_base_path, sheet, base_name, base_package, incremental=True):
    s = ScenarioForOptaPlanner(base_name, base_package, excel_file, sheet=sheet, incremental=incremental)
    s.build()
    s.to_java(java_base_path)
