import re
from more_itertools import partition
from numbers import Number
from typing import Optional

from codegen.utils import selective_combine, spread
from math_rep.constants import NOT_EQUALS_SYMBOL, LE_SYMBOL, GE_SYMBOL
from math_rep.expr import FunctionApplication, IFTE, Aggregate, AGGREGATE_TO_FUNCTION_QN_MAP, Term, \
    LambdaExpression, StringTerm, FormalContent, Comparison, Quantity, MathVariable, ComprehensionContainer, \
    ZERO_AS_QUANTITY, ComprehensionCondition, apply_lambda, LogicalOperator
from scenoptic.scenoptic_expr import CellsRange, Cells
from math_rep.expression_types import QualifiedName
from math_rep.math_symbols import PLUS_QN, ZIP_QN, AND_QN, DIV_QN, TIMES_QN, MINUS_QN, MAX_QN, MIN_QN, EQ_QN
from math_rep.math_frame import MATH_FRAME_NAME
from rewriting.patterns import Bindings, MATCH_ANY, let, one_of, ClassPattern, Span
from rewriting.rules import RewriteRule
from scenoptic.excel_symbols import EXCEL_IF_QN, EXCEL_AUX_V_QN, EXCEL_CONCATENATE_QN, \
    EXCEL_RE_MATCH_QN, EXCEL_SUMIF_LAMBDA_QN, EXCEL_SUM_QN, EXCEL_AUX_CELL_QN, \
    EXCEL_COUNTIF_LAMBDA_QN, EXCEL_COND_CELL_QN, EXCEL_SUMIFS_LAMBDA_QN, EXCEL_AUX_FRAME, \
    EXCEL_COUNTIFS_LAMBDA_QN, as_excel_name, EXCEL_INTERNAL_FRAME
from scenoptic.excel_to_math import EXCEL_OPERATORS

EXCEL_TO_MATH_MAP = {'+': PLUS_QN,
                     '-': MINUS_QN,
                     '*': TIMES_QN,
                     '/': DIV_QN,
                     'max': MAX_QN,
                     'min': MIN_QN}


def to_math(name):
    return EXCEL_TO_MATH_MAP.get(name, QualifiedName(name, lexical_path=(MATH_FRAME_NAME,)))


EXCEL_AS_MATH = {'+', '-', '*', '/', 'max', 'min'}
EXCEL_TO_MATH = {s: to_math(s) for s in EXCEL_AS_MATH}


class ExcelIfRule(RewriteRule):
    pattern = FunctionApplication[EXCEL_IF_QN, 'cond', 'then', 'else']

    def transform_single(self, obj, bindings: Bindings):
        cond = bindings['cond']
        pos = bindings['then']
        neg = bindings['else']
        return IFTE(cond, pos, neg)


class ConvertExcelFunctions(RewriteRule):
    pattern = ClassPattern(FunctionApplication)

    def condition(self, obj: FunctionApplication, bindings: Bindings) -> bool:
        return obj.function.lexical_path != (MATH_FRAME_NAME,) and obj.function.name.lower() in EXCEL_TO_MATH

    def transform_single(self, obj: FunctionApplication, bindings: Bindings):
        return obj.with_function(EXCEL_TO_MATH[obj.function.name.lower()])


def criteria_function_to_internal_name(func: QualifiedName) -> QualifiedName:
    return QualifiedName(f'{func.name}-lambda', func.type, lexical_path=EXCEL_INTERNAL_FRAME)


CRITERIA_ARGUMENTS = {as_excel_name(op): info.criteria_arguments
                      for op, info in EXCEL_OPERATORS.items()
                      if info.criteria_arguments}
CRITERIA_OPERATOR_MAP = {'=': '=', '<>': NOT_EQUALS_SYMBOL, '<': '<', '>': '>', '<=': LE_SYMBOL, '>=': GE_SYMBOL}
CRITERIA_INTERNAL_FUNCTIONS = [criteria_function_to_internal_name(as_excel_name(op))
                               for op, info in EXCEL_OPERATORS.items()
                               if info.criteria_arguments]

CRITERIA_COMP_RE = re.compile(r'(=|<>|<|>|<=|>=)(.*)')
CRITERIA_REGEX_RE = re.compile(r'(?:^[*?])|(?:[^~][*?])')


def coerce(s: str, target) -> Optional[Number]:
    try:
        return target(s)
    except ValueError:
        return None


def str_to_expr(s: str):
    result = coerce(s, int)
    if result is not None:
        return Quantity(result)
    result = coerce(s, float)
    if result is not None:
        return Quantity(result)
    return StringTerm(s)


def criteria_to_lambda(criteria: Term) -> LambdaExpression:
    param = FormalContent.fresh_name(EXCEL_AUX_V_QN, 'lambda')
    var = MathVariable(param)
    if isinstance(criteria, StringTerm):
        spec = criteria.contents
        m = CRITERIA_COMP_RE.fullmatch(spec)
        if m is not None:
            body = Comparison(var, CRITERIA_OPERATOR_MAP[m.group(1)], str_to_expr(m.group(2)))
        else:
            mre = CRITERIA_REGEX_RE.search(spec)
            if mre is not None:
                # FIXME!! implement semantics of match-excel-re
                body = FunctionApplication(EXCEL_RE_MATCH_QN, [var, criteria])
            else:
                body = var == str_to_expr(spec)
    elif (isinstance(criteria, FunctionApplication)
          and criteria.function == EXCEL_CONCATENATE_QN
          and len(criteria.args) == 2
          and isinstance(op := criteria.args[0], StringTerm)
          and op.contents in CRITERIA_OPERATOR_MAP.keys()):
        body = Comparison(var, CRITERIA_OPERATOR_MAP[op.contents], criteria.args[1])
    else:
        body = var == criteria
    return LambdaExpression([param], body)


class ExcelCriteriaRule(RewriteRule):
    pattern = FunctionApplication[let(func=one_of(*CRITERIA_ARGUMENTS.keys())), let(args=...)]

    def transform_single(self, obj, bindings: Bindings):
        # FIXME! treat as array formula if any criteria arg is an array
        func = bindings['func']
        args = bindings['args']
        criteria_indexes = CRITERIA_ARGUMENTS.get(func)
        return FunctionApplication(criteria_function_to_internal_name(func),
                                   list(selective_combine(spread(criteria_indexes,
                                                                 (criteria_to_lambda(args[i])
                                                                  for i in criteria_indexes)),
                                                          args)))


def is_equality_criterion(crit_func: LambdaExpression) -> bool:
    body = crit_func.body
    assert isinstance(body, Comparison)
    return body.op == EQ_QN


def is_static_criterion(crit_func: LambdaExpression) -> bool:
    body = crit_func.body
    assert isinstance(body, Comparison)
    args = (body.lhs, body.rhs)
    scalar = args[1] if type(args[0]) == MathVariable else args[0]
    return not scalar.appl_info.is_dvar()


class ExcelConditionalSummingRule(RewriteRule):
    pattern = FunctionApplication[let(func=one_of(*CRITERIA_INTERNAL_FUNCTIONS)), let(args=...)]

    def transform_single(self, obj, bindings: Bindings):
        args = bindings['args']
        p1 = partition(lambda pair: is_equality_criterion(pair[1]),
                       ((index, arg) for index, arg in enumerate(args) if
                        isinstance(arg, LambdaExpression)))
        equalities = sorted(((args[index - 1], func) for index, func in p1[1]),
                            key=lambda p: p[0].key())
        p2 = partition(lambda pair: is_static_criterion(pair[1]), p1[0])
        static = sorted(((args[index - 1], func) for index, func in p2[1]),
                        key=lambda p: p[0].key())
        dynamic = tuple((args[index - 1], func) for index, func in p2[0])
        print(f'{equalities=}, {static=}, {dynamic=}')
        return obj


class ExpandExcelSumMultipleArgs(RewriteRule):
    pattern = FunctionApplication[EXCEL_SUM_QN, 'arg1', 'arg2']

    def _transform_one_arg(self, obj: Term):
        """
        Transform SUM(x)

        :param obj: single parameter of SUM
        :return: transformed SUM(x); can be original obj, but never None
        """
        if isinstance(obj, (Cells, CellsRange)):
            return FunctionApplication(EXCEL_SUM_QN, [obj])
        return obj

    def transform_single(self, obj: FunctionApplication, bindings: Bindings):
        args = obj.args
        return FunctionApplication(PLUS_QN, [self._transform_one_arg(arg) for arg in args])


class ExpandExcelSumOneArg(RewriteRule):
    pattern = FunctionApplication[EXCEL_SUM_QN]

    def condition(self, obj: FunctionApplication, bindings: Bindings) -> bool:
        return len(obj.args) <= 1

    # FIXME!! remove this, replace by incremental computation
    def transform_single(self, obj: FunctionApplication, bindings: Bindings):
        if not obj.args:
            return ZERO_AS_QUANTITY
        var = FormalContent.fresh_name(EXCEL_AUX_CELL_QN, 'cell')
        return Aggregate('+', MathVariable(var), ComprehensionContainer([var], obj.args[0]))


class TranslateExcelSumif(RewriteRule):
    # FIXME!!! generalize
    pattern = FunctionApplication[EXCEL_SUMIF_LAMBDA_QN, 'range', 'criteria', let(sum_range=...)]

    def transform_single(self, obj, bindings: Bindings):
        range = bindings['range']
        criteria = bindings['criteria']
        sum_range = bindings['sum_range']
        var = FormalContent.fresh_name(EXCEL_AUX_CELL_QN, 'cell')
        mvar = MathVariable(var)
        if isinstance(sum_range, Span):
            if len(sum_range) == 0:
                return Aggregate('+',
                                 mvar,
                                 ComprehensionContainer([var],
                                                        range,
                                                        ComprehensionCondition(apply_lambda(criteria, mvar))))
            else:
                raise Exception(f'Too many arguments for SUMIF: {obj}')
        cvar = FormalContent.fresh_name(EXCEL_COND_CELL_QN, 'cond')
        return Aggregate('+',
                         mvar,
                         ComprehensionContainer([var, cvar],
                                                FunctionApplication(ZIP_QN, [sum_range, range]),
                                                ComprehensionCondition(apply_lambda(criteria, MathVariable(cvar)))))


class TranslateExcelSumifs(RewriteRule):
    # TODO: generalize
    pattern = FunctionApplication[EXCEL_SUMIFS_LAMBDA_QN, 'sum-range']

    def transform_single(self, obj, bindings: Bindings):
        sum_range = bindings['sum-range']
        criteria_list = obj.args[1:]
        var = FormalContent.fresh_name(EXCEL_AUX_CELL_QN, 'cell')
        mvar = MathVariable(var)
        cvars = [FormalContent.fresh_name(QualifiedName(f'cell{i}', lexical_path=EXCEL_AUX_FRAME), f'cell{i}')
                 for i in range(len(criteria_list) // 2)]
        condition = LogicalOperator(AND_QN,
                                    [apply_lambda(criteria, MathVariable(cvar))
                                     for criteria, cvar in zip(criteria_list[1::2], cvars)])
        return Aggregate('+',
                         mvar,
                         ComprehensionContainer([var, *cvars],
                                                FunctionApplication(ZIP_QN, [sum_range, *criteria_list[::2]]),
                                                ComprehensionCondition(condition)))


class TranslateExcelCountif(RewriteRule):
    pattern = FunctionApplication[EXCEL_COUNTIF_LAMBDA_QN, 'range', 'criteria']

    def transform_single(self, obj, bindings: Bindings):
        range = bindings['range']
        criteria = bindings['criteria']
        var = FormalContent.fresh_name(EXCEL_AUX_CELL_QN, 'cell')
        mvar = MathVariable(var)
        return Aggregate('+',
                         Quantity(1),
                         ComprehensionContainer([var],
                                                range,
                                                ComprehensionCondition(apply_lambda(criteria, mvar))))


class TranslateExcelCountifs(RewriteRule):
    # TODO: combine with ExpandExcelSumifs
    pattern = FunctionApplication[EXCEL_COUNTIFS_LAMBDA_QN]

    def transform_single(self, obj, bindings: Bindings):
        criteria_list = obj.args
        n_criteria = len(criteria_list) // 2
        cvars = [FormalContent.fresh_name(QualifiedName(f'cell{i}', lexical_path=EXCEL_AUX_FRAME), f'cell{i}')
                 for i in range(n_criteria)]
        condition = LogicalOperator(AND_QN,
                                    [apply_lambda(criteria, MathVariable(cvar))
                                     for criteria, cvar in zip(criteria_list[1::2], cvars)])
        return Aggregate('+',
                         Quantity(1),
                         ComprehensionContainer([*cvars],
                                                ZIP_QN(*criteria_list[::2]) if n_criteria > 1 else criteria_list[0],
                                                ComprehensionCondition(condition)))


class AggregateCellsRule(RewriteRule):
    pattern = Aggregate[
        let(op=MATCH_ANY), 'term', let(container=ComprehensionContainer[let(cells=ClassPattern(Cells))])]

    def transform_single(self, obj: Aggregate, bindings: Bindings):
        op = bindings['op']
        container = bindings['container']
        var = container.vars[0]
        if (rest := container.rest) is None:
            return FunctionApplication(AGGREGATE_TO_FUNCTION_QN_MAP[op],
                                       [obj.term.substitute({var: cell})
                                        for cell in bindings['cells']])
        # FIXME!!!!! take into account possible ComprehensionContainer as rest, make into Aggregate args (also rec.)
        if isinstance(rest, ComprehensionCondition):
            conditions = [rest.condition]
            rest2 = rest.rest
            while rest2 is not None and isinstance(rest2, ComprehensionCondition):
                conditions.append(rest2.condition)
                rest2 = rest2.rest
            condition = LogicalOperator(AND_QN, conditions)
            # TODO!! use let to avoid recomputation of cell
            return FunctionApplication(AGGREGATE_TO_FUNCTION_QN_MAP[obj.op],
                                       [IFTE(condition.substitute({var: cell}),
                                             obj.term.substitute({var: cell}),
                                             Quantity(Aggregate.units[op]))
                                        for cell in bindings['cells']])
        return obj


class AggregateZipCellsRule(RewriteRule):
    pattern = Aggregate[let(op=MATCH_ANY),
                        'term',
                        let(container=ComprehensionContainer[let(zip=FunctionApplication[ZIP_QN, let(args=...)])])]

    def condition(self, obj, bindings: Bindings) -> bool:
        # Supporting zip with only one arg
        args = bindings['args']
        return isinstance(args, Cells) or len(args) > 0 and all(isinstance(arg, Cells) for arg in args)

    def transform_single(self, obj, bindings: Bindings):
        container = bindings['container']
        var = container.vars[0]
        bargs = bindings['args']
        args = list(bargs) if isinstance(bargs, Span) else [bargs]
        if (rest := container.rest) is None:
            return FunctionApplication(AGGREGATE_TO_FUNCTION_QN_MAP[obj.op],
                                       [obj.term.substitute({var: val for var, val in zip(container.vars, arglist)})
                                        for arglist in zip(*(iter(arg) for arg in args))])
        # FIXME!!!!! take into account possible ComprehensionContainer as rest, make into Aggregate args (also rec.)
        if isinstance(rest, ComprehensionCondition):
            conditions = [rest.condition]
            rest2 = rest.rest
            while rest2 is not None and isinstance(rest2, ComprehensionCondition):
                conditions.append(rest2.condition)
                rest2 = rest2.rest
            condition = LogicalOperator(AND_QN, conditions)
            return FunctionApplication(AGGREGATE_TO_FUNCTION_QN_MAP[obj.op],
                                       [IFTE(condition.substitute(
                                           {var: val for var, val in zip(container.vars, arglist)}),
                                           obj.term.substitute(
                                               {var: val for var, val in zip(container.vars, arglist)}),
                                           Quantity(Aggregate.units[obj.op]))
                                           for arglist in zip(*(iter(arg) for arg in args))])
        return obj
