from __future__ import annotations

from codegen.abstract_rep import TimeExpr, PeriodExpr, Import, CodeFragment, QuantifierExpr
from validator2solver.python.python_generator import PythonFunctionNameTranslator, PythonVisitor
from codegen.utils import disown
from math_rep.expr import intern_expr, Term, TEMPORAL_BEFORE, TEMPORAL_AFTER, TEMPORAL_MEETS, TEMPORAL_MEETS_INV, \
    TEMPORAL_DISJOINT, TEMPORAL_OVERLAPS
from math_rep.expression_types import MClassType, QualifiedName
from validator2solver.python.python_builtins import is_profile_name
from eco_profiles.profile_frame_constants import profile_name


@intern_expr
class Time(Term):
    has_operator = False

    @disown('time')
    def __init__(self, time):
        super().__init__(M_TIME)
        self.time = time

    def to_code_rep(self):
        return TimeExpr(self.time)

    def describe(self, parent_binding=None):
        return self.time

    def arguments(self):
        return ()

    def with_argument(self, index, arg):
        raise IndexError('Time has no arguments')


@intern_expr
class Period(Term):
    has_operator = False

    def __init__(self, start, end):
        super().__init__(M_PERIOD)
        self.start = start
        self.end = end

    def to_code_rep(self):
        return PeriodExpr(self.start.to_code_rep(), self.end.to_code_rep())

    def describe(self, parent_binding=None):
        return f'[{self.start.describe()}-{self.end.describe()}]'

    def arguments(self):
        return ()

    def with_argument(self, index, arg):
        raise IndexError('Period has no arguments')


M_TIME = MClassType(profile_name('Time'))
M_PERIOD = MClassType(profile_name('Period'))

ECO_ABST_MODULE = 'optimistic_rt'
ECO_TEMPORAL_MODULE = f'{ECO_ABST_MODULE}.temporal'
ECO_UTIL_MODULE = f'{ECO_ABST_MODULE}.util'
ECO_FUNCTIONS = {TEMPORAL_BEFORE: Import('t_before', ECO_TEMPORAL_MODULE),
                 TEMPORAL_AFTER: Import('t_after', ECO_TEMPORAL_MODULE),
                 TEMPORAL_MEETS: Import('t_meets', ECO_TEMPORAL_MODULE),
                 TEMPORAL_MEETS_INV: Import('t_meets_inv', ECO_TEMPORAL_MODULE),
                 TEMPORAL_DISJOINT: Import('t_disjoint', ECO_TEMPORAL_MODULE),
                 TEMPORAL_OVERLAPS: Import('t_overlaps', ECO_TEMPORAL_MODULE),
                 '*different*': Import('different', ECO_UTIL_MODULE),
                 '*period-length*': Import('period_length', ECO_UTIL_MODULE),
                 'intersection': Import('period_intersection', ECO_UTIL_MODULE),
                 'len': Import('period_length', ECO_UTIL_MODULE)}


class PythonFunctionNameTranslatorForProfiles(PythonFunctionNameTranslator):
    def _translate_additions(self, name: QualifiedName) -> QualifiedName:
        if is_profile_name(name):
            import_name = ECO_FUNCTIONS.get(name)
            if import_name:
                return QualifiedName(import_name.name, lexical_path=tuple(reversed(import_name.module.split('.'))))
            return name


class PythonVisitorForProfiles(PythonVisitor):
    def visit_time(self, time):
        self.add_import(Import('Time', ECO_ABST_MODULE))
        return CodeFragment(f'Time({repr(time.time)})')

    def visit_period(self, period: PeriodExpr):
        self.add_import(Import('Period', ECO_ABST_MODULE))
        start_code = period.start.accept(self)
        end_code = period.end.accept(self)
        return CodeFragment(f'Period({start_code.value}, {end_code.value})',
                            free_vars=start_code.free_vars | end_code.free_vars)

    def _get_import(self, name: QualifiedName | str) -> Import | None:
        return ECO_FUNCTIONS.get(name.name if isinstance(name, QualifiedName) else name,
                                 super()._get_import(name))

    def _handle_unique_existential(self, quantifier: QuantifierExpr, bound_vars, container_code, formula_code,
                                   free_vars, checkpoint):
        self.add_import(Import('unique_element', ECO_UTIL_MODULE))
        if len(bound_vars) != 1:
            raise Exception('Only one variable supported for unique existential')
        bound_var = next(iter(bound_vars))
        bound_ident = bound_var.to_c_identifier()
        body = f'{bound_ident} = unique_element({container_code.container_code.value})'
        # FIXME: create value expression, then visit to translate properly and add return
        value = f'{bound_ident} is not None'
        if formula_code:
            value += f' and {formula_code.value}'
        return self.encapsulate(CodeFragment(f'return {value}', body=body, free_vars=free_vars,
                                             doc_string=quantifier.doc_string),
                                checkpoint=checkpoint)

