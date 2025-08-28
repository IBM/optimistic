import operator
from abc import ABCMeta
from copy import copy
from functools import wraps, reduce
from itertools import chain, repeat
from numbers import Number
from typing import Union, Mapping, Tuple

from codegen.abstract_rep import CodeVisitor, FunctionDefinition, CodeFragment, FunctionApplExpr, parenthesize, \
    BooleanExpr, ComparisonExpr, CellsExpr, VariableAccess, LogicalExpr, SetExpr, AggregateExpr, \
    ComprehensionContainerCode, ComprehensionConditionCode, StreamExpr, AbstractClassDefinition, \
    AbstractFunctionDefinition, \
    AbstractTypeDeclaration, CompilationUnit, NegatedExpr, AttributeAccess, ConditionalExpr, SubscriptedExpr, RangeCode, \
    SequenceExpr, CastExpr, LambdaExpressionExpr, NamedConstant
from codegen.utils import decorate_method
from math_rep.constants import OR_SYMBOL, AND_SYMBOL, NOT_EQUALS_SYMBOL, GE_SYMBOL, LE_SYMBOL, IMPLIES_SYMBOL, \
    NOT_SYMBOL, ELEMENT_OF_SYMBOL, NOT_ELEMENT_OF_SYMBOL, FOR_ALL_SYMBOL
from math_rep.expr import Quantifier
from math_rep.expression_types import QualifiedName, NameTranslator, is_math_name
from math_rep.math_symbols import DIV_SYMBOL
from opl_repr.opl_builtins import is_opl_user_name
from opl_repr.opl_frame_constants import OPL_BUILTIN_FRAME_NAME, OPL_USER_FRAME_NAME
from scenoptic.xl_utils import column_to_index, index_to_column, cell_to_coords, normalize_cell, xl_range_elements
from validator2solver.python.python_to_expr import METHOD_CALL_INDICATOR

CONSTANTS = dict(epsilon='epsilon')

ASSOCIATIVE_OPL_OPERATORS = {'+', '*', '&&', '||'}

OPL_FUNCTION_TRANSLATIONS = {AND_SYMBOL: '&&', OR_SYMBOL: '||', IMPLIES_SYMBOL: '=>', 'max': 'maxl', 'min': 'minl',
                             NOT_SYMBOL: '!', ELEMENT_OF_SYMBOL: 'in', NOT_ELEMENT_OF_SYMBOL: 'not in',
                             LE_SYMBOL: '<=', GE_SYMBOL: '>=', NOT_EQUALS_SYMBOL: '!=',
                             '=': '==', '<': '<', '>': '>', '<=': '<=', '>=': '>=',
                             '+': '+', '-': '-', '*': '*', '/': '/', DIV_SYMBOL: '/',
                             'next': 'first', 'ceil': 'ceil'}

AGGREGATIVE_FUNCTIONS = {'all', 'sum', 'max', 'min', 'union', 'prod', 'inter'}

OPL_COMP_OPS = {'=': '==', NOT_EQUALS_SYMBOL: '!=', '>': '>', GE_SYMBOL: '>=', '<': '<', LE_SYMBOL: '<='}

OPL_PRIMITIVES = {'+': 160, '-': 160, '*': 170, '/': 170, '|': 153, '&': 156, '==': 140, '<': 140, '<=': 140,
                  '=': 140, '>=': 140, '>': 140, '!=': 140, '&&': 110, '||': 100, 'not': 158, '=>': 90,
                  'in': 150, 'not in': 150}

# See https://www.ibm.com/support/knowledgecenter/SSSA5P_12.10.0/ilog.odms.ide.help/OPL_Studio/opllang_quickref/topics/opl_grammar.html

#   90           | "if" '(' Expression ')' Constraint "else" Constraint
#   91           | "if" '(' Expression ')' Constraint
#   92           | "forall" '(' Qualifiers ')' Constraint
#   93           | "forall" '(' Qualifiers ')' ArraySlotExpression "="

#   166 AggregateExpression: "sum" '(' Qualifiers ')' Expression
#   167                    | "min" '(' Qualifiers ')' Expression
#   168                    | "max" '(' Qualifiers ')' Expression
#   169                    | "prod" '(' Qualifiers ')' Expression
#   170                    | "or" '(' Qualifiers ')' Expression
#   171                    | "and" '(' Qualifiers ')' Expression
#   172                    | "union" '(' Qualifiers ')' Expression
#   173                    | "inter" '(' Qualifiers ')' Expression
#   174                    | AllExpression
#
#   175 AllExpression: "all" AllRange_opt '(' Qualifiers ')' Expression

OPL_AGGREGATE_FUNCS = {'+': 'sum', '*': 'prod', 'SET': ('{', '}')}

# FIXME: add operators and translations
OPL_AGGREGATIVE_OPS = {'+': 'sum', 'SET': ('{', '}')}


def translate_function(appl, allow_undefined_vars) -> QualifiedName:
    func = appl.function
    if is_math_name(func):
        return QualifiedName(OPL_FUNCTION_TRANSLATIONS[func.name.lower()], lexical_path=OPL_BUILTIN_FRAME_NAME)
    if is_opl_user_name(func):
        return func
    if func.is_lexically_scoped():
        # FIXME!!! use translation table for known functions
        return func.with_path((OPL_USER_FRAME_NAME,), override=True)
    if allow_undefined_vars and func.lexical_path == (METHOD_CALL_INDICATOR,):
        return func
    # FIXME: remove this, just workaround for debugging
    if not func.lexical_path:
        return func.with_path((OPL_USER_FRAME_NAME,), override=True)
    raise Exception(f'Unknown OPL function {func}')


class OplNameTranslator(NameTranslator):
    def __init__(self, name_tranlations: Mapping[QualifiedName, QualifiedName] = None):
        self.name_tranlations = name_tranlations or {}

    def translate(self, name: QualifiedName):
        if is_opl_user_name(name):
            return name
        translated = self.name_tranlations.get(name)
        if translated:
            return translated
        if name.is_lexically_scoped():
            return name.with_path((OPL_USER_FRAME_NAME,), override=True)
        # FIXME: remove this, just workaround for debugging
        if not name.lexical_path:
            return name.with_path((OPL_USER_FRAME_NAME,), override=True)
        raise Exception(f'Unknown name {name}')


def print_type(method):
    @wraps(method)
    def printer(self, arg1, *args, **kwargs):
        result = method(self, arg1, *args, **kwargs)
        print(f'=== {arg1.doc_string}')
        print(f'--- {arg1.type}')
        return result

    return printer


class RangeFragment(CodeFragment):
    def __init__(self, start_cell, end_cell):
        self.start_row, self.start_col = cell_to_coords(start_cell)
        self.end_row, self.end_col = cell_to_coords(end_cell)
        super().__init__(f'!!Range {start_cell}:{end_cell}!!',
                         free_vars=frozenset(self.__iter__()))

    def __iter__(self):
        return xl_range_elements(self.start_col, self.start_row, self.end_col, self.end_row)

    def dims(self):
        return self.end_row - self.start_row + 1, self.end_col - self.start_col + 1

    def size(self):
        return reduce(operator.mul, self.dims())


OPL_LOGICAL_OPS = {AND_SYMBOL, OR_SYMBOL, IMPLIES_SYMBOL}

LIFT_ARGS = {'if': (0, 1), AND_SYMBOL: (0, 1), IMPLIES_SYMBOL: (1,)}


class OplVisitor(CodeVisitor, metaclass=decorate_method((print_type, 'Xvisit_*'), supermetaclass=ABCMeta)):
    def __init__(self, epsilon=1e-10, base_name: str = None,
                 variables_by_role: Mapping[Tuple[str, ...], str] = None, variable_translations=None,
                 allow_undefined_vars=False,
                 indentation=4):
        super().__init__(base_name)
        self.epsilon = epsilon
        self.variables_by_role = variables_by_role or {}
        self.allow_undefined_vars = allow_undefined_vars
        self.name_translator = OplNameTranslator(variable_translations)
        self.indentation = ' ' * indentation
        self.named_constants = set()
        self.already_transformed = False

    def update_variables(self, variables_by_role):
        self.variables_by_role = variables_by_role

    def pretty_function_def(self, helper: FunctionDefinition) -> str:
        pass

    def visit_attribute_access(self, attr: AttributeAccess):
        container_code = self.visit(attr.container)
        return CodeFragment(f'{parenthesize(190, container_code)}.{attr.attribute.name.to_c_identifier()}',
                            free_vars=attr.prog_free_vars,
                            precedence=190)

    def visit_variable_access(self, var: VariableAccess):
        # Pass errors without change, so will cause OPL errors
        identifier = (var.name if isinstance(var.name.name, str) and var.name.name.startswith('*** E')
                      else var.name.to_c_identifier())
        return CodeFragment(self.name_translator.translate(
            QualifiedName(identifier, lexical_path=var.name.lexical_path)).name)

    def visit_cells(self, cells: CellsExpr):
        # FIXME: Add usage of sheet information, maybe as Qualified Names
        # Note: the following code is never used, no CellsExpr is created in
        #     expr.Cell.to_code_rep() or expr.Cells.to_code_rep()
        if cells.end_cell:
            return RangeFragment(cells.start_cell, cells.end_cell)
        cell = normalize_cell(cells.start_cell)
        return CodeFragment(cell, free_vars=cells.prog_free_vars)

    def visit_comparison_expr(self, comp: ComparisonExpr):
        op = comp.op
        lhs = comp.lhs
        rhs = comp.rhs
        trans = FunctionApplExpr(OPL_COMP_OPS.get(op, op), [lhs, rhs])
        trans.type = comp.type
        trans.doc_string = comp.doc_string
        trans.prog_free_vars = comp.prog_free_vars
        return trans.accept(self)

    def visit_number(self, num):
        return CodeFragment(str(num.value))

    def visit_named_constant(self, const: NamedConstant):
        value = CONSTANTS[const.name]
        if not isinstance(value, Number):
            self.named_constants.add(value)
        return CodeFragment(value)

    def visit_string(self, s):
        # FIXME: add other escape sequences (see help topic "Identifiers" in opl)
        str_contents = s.value.replace('"', '\"')
        return CodeFragment(f'"{str_contents}"')

    def visit_set_expr(self, setexpr: SetExpr):
        elements = [self.visit(e) for e in setexpr.set]
        return CodeFragment(f'{{{", ".join(e.value for e in elements)}}}', free_vars=setexpr.prog_free_vars)

    def visit_sequence_expr(self, seqexpr: SequenceExpr):
        elements = [self.visit(e) for e in seqexpr.elements]
        return CodeFragment(f'[{", ".join(e.value for e in elements)}]', free_vars=seqexpr.prog_free_vars)

    def visit_set_membership(self, expr):
        pass

    def visit_quantifier(self, quant: Quantifier):
        expr_fragment = self.visit(quant.formula)
        container_fragment = self.visit(quant.container)
        bound_vars = container_fragment.bound_vars
        # TODO: split lines, add indentation
        if quant.kind != FOR_ALL_SYMBOL:
            # FIXME: Add support for existential, perhaps as sum of booleans?
            raise Exception('Existentials not yet supported for OPL')
        result = CodeFragment(f'forall ({container_fragment.value}) {expr_fragment.value}',
                              free_vars=quant.prog_free_vars)
        result.bound_vars = bound_vars
        return result

    def visit_negation(self, expr: NegatedExpr):
        expr_code = self.visit(expr.expr)
        result = CodeFragment(f'!{parenthesize(158, expr_code)}')
        result.free_vars = expr.prog_free_vars
        return result

    def visit_loop_in(self, loop):
        pass

    def visit_concatenation(self, conc):
        pass

    def visit_comprehension_container_code(self, compr: ComprehensionContainerCode):
        if (rest := compr.rest) is not None:
            rest_fragment = self.visit(rest)
            rest_code = (', ' if isinstance(rest, ComprehensionContainerCode) else ' : ') + rest_fragment.value
        else:
            rest_code = ''
        if isinstance(container := compr.container, VariableAccess) and container.name.name == 'solution':
            # FIXME!! need to do the same for method variables, but this is called during the process of defining them
            sol_var = self.variables_by_role.get(('solution',))
            ref = sol_var.domain_reference()
            container_code = CodeFragment(ref, free_vars=container.prog_free_vars)
        else:
            container_code = self.visit(container)
        bound_vars = set(compr.vars)
        result = CodeFragment(f'{", ".join(var.name for var in compr.vars)} in {container_code.value}{rest_code}',
                              free_vars=compr.prog_free_vars)
        result.bound_vars = bound_vars
        return result

    def visit_comprehension_condition_code(self, compr: ComprehensionConditionCode):
        if (rest := compr.rest) is not None:
            rest_fragment = self.visit(rest)
            rest_code = (', ' if isinstance(rest, ComprehensionContainerCode) else ' : ') + rest_fragment.value
        else:
            rest_code = ''
        condition_fragment = self.visit(compr.condition)
        return CodeFragment(f'{condition_fragment.value}{rest_code}',
                            free_vars=compr.prog_free_vars)

    def visit_aggregate_expr(self, aggregate: AggregateExpr):
        term = aggregate.term.accept(self)
        if isinstance(term, RangeFragment):
            # FIXME: translate operator for OPL
            # function = OPL_AGGREGATIVE_OPS.get(aggregate.operator)
            function = aggregate.operator
            if function is None:
                raise Exception('Unrecognized aggregative operator for OPL conversion: ' + aggregate.operator)
            vars = list(term)
            precedence = OPL_PRIMITIVES.get(function)
            return CodeFragment(f' {function} '.join(vars), precedence=precedence, free_vars=aggregate.prog_free_vars)
        # not a range parameter
        # Set example: {float} S3 = {x^y | x in 1..4 : x>2, y in 1..3 : x != y};
        container_fragment = aggregate.container.accept(self)
        term_code = aggregate.term.accept(self)
        bound_vars = container_fragment.bound_vars
        operator = OPL_AGGREGATE_FUNCS[aggregate.operator]
        inside = f'{term_code.value} | {container_fragment.value}'
        if isinstance(operator, (list, tuple)):
            return CodeFragment(f'{operator[0]}{inside}{operator[1]}', free_vars=aggregate.prog_free_vars)
        return CodeFragment(f'{operator} ({parenthesize(165, container_fragment)}) {term_code.value}',
                            free_vars=aggregate.prog_free_vars,
                            precedence=165)

    def visit_between(self, between):
        pass

    def substitute(self, appl: Union[FunctionApplExpr, ComparisonExpr], to_be_trans_idx: int) -> FunctionApplExpr:
        """
        Substitute a function application inside an expression.  For example, translate v < IF(p, a, b) into
        IF(p, v<a, v<b).

        :param appl: function application object
        :param to_be_trans_idx: index of argument of `appl` that is of type ExpressionAsCondition
        :return: New expression
        """
        if isinstance(appl, FunctionApplExpr):
            args = copy(appl.args)
        else:
            args = [appl.lhs, appl.rhs]
        to_be_trans = args[to_be_trans_idx]
        args[to_be_trans_idx] = None
        to_lift = to_be_trans.lifted_args
        to_be_trans = to_be_trans.expr
        new_args = [appl.with_arg(targ, to_be_trans_idx) if i in to_lift else targ
                    for i, targ in enumerate(to_be_trans.args)]
        return to_be_trans.with_args(new_args)

    def visit_function_appl_expr(self, appl: FunctionApplExpr):
        # if not self.already_transformed:
        function = translate_function(appl, self.allow_undefined_vars).name
        precedence = OPL_PRIMITIVES.get(function)
        args_code = self.function_appl_args_code(appl.args)
        arg_bindings = (repeat(precedence) if function in ASSOCIATIVE_OPL_OPERATORS
                        else chain([precedence], repeat((precedence or 0) + 1)))
        args_text = [parenthesize(arg_precedence, ac) for ac, arg_precedence in zip(args_code, arg_bindings)]
        if precedence:
            if len(args_text) > 1:
                return CodeFragment(f' {function} '.join(args_text), precedence=precedence,
                                    free_vars=appl.prog_free_vars)
            else:
                return CodeFragment(f'{function}{" " if function[-1].isalnum() else ""}{args_text[0]}',
                                    precedence=precedence, free_vars=appl.prog_free_vars)
        if function in OPL_FUNCTION_TRANSLATIONS.values():
            arglist = ', '.join(args_text)
            return CodeFragment(f'{function}({arglist})', free_vars=appl.prog_free_vars)
        # translate function call to variable reference
        opl_var = self.find_opl_var(function)
        if opl_var:
            ref = opl_var.opl_reference(*args_text)
        elif self.allow_undefined_vars:
            arglist = ''.join(f'[{arg}]' for arg in args_text)
            ref = f'{function}{arglist}'
        else:
            raise Exception(f'No information for translating function {function}')
        return CodeFragment(ref, free_vars=appl.prog_free_vars)

    def find_opl_var(self, function: str):
        opl_var = self.variables_by_role.get(('method', function))
        if not opl_var:
            sol_var = self.variables_by_role.get(('solution',))
            if not sol_var:
                return None
            if sol_var.name == function:
                opl_var = sol_var
        return opl_var

    def function_appl_args_code(self, args):
        # self.already_transformed = True
        args_code = [(a.as_set() if isinstance(a, StreamExpr) else a).accept(self) for a in args]
        # self.already_transformed = False
        i = 0
        for ac in list(args_code):  # copy list to protect from changes in loop
            if isinstance(ac, RangeFragment):
                args_code[i:i + 1] = [CodeFragment(v, free_vars=v.prog_free_vars) for v in ac]
                i += ac.size() + 1
            else:
                i += 1
        return args_code

    def visit_period(self, period):
        pass

    def visit_time(self, time):
        pass

    def visit_dummy_var(self, dummy_var):
        pass

    def visit_logical_expr(self, expr: LogicalExpr):
        # FIXME: treat logical expressions here instead of changing to function applications
        as_appl = FunctionApplExpr(expr.op, expr.elements)
        as_appl.prog_free_vars = expr.prog_free_vars
        return self.visit_function_appl_expr(as_appl)

    def visit_predicate_appl(self, appl):
        pass

    def visit_identifier(self, identifier):
        pass

    def visit_temporal_expr(self, temporal):
        pass

    def visit_boolean(self, value: BooleanExpr):
        return CodeFragment('1' if value.value else '0')

    def visit_stream_expr(self, stream: StreamExpr):
        term_code = self.visit(stream.term)
        container_fragment = self.visit(stream.container)
        bound_vars = container_fragment.bound_vars
        result = CodeFragment(f'{term_code.value} | {container_fragment.value}', free_vars=stream.prog_free_vars)
        result.bound_vars = container_fragment.bound_vars
        return result

    def visit_abstract_class_definition(self, cls: AbstractClassDefinition):
        raise Exception('No direct translation of classes to OPL')

    def visit_abstract_function_definition(self, func: AbstractFunctionDefinition):
        raise Exception('No direct translation of function definitions to OPL')

    def visit_abstrat_type_declaration(self, decl: AbstractTypeDeclaration):
        raise Exception('No direct translation of variable declarations to OPL')

    def visit_named_arg(self, arg):
        raise Exception('No direct translation of named parameters to OPL')

    def visit_compilation_unit(self, cu: CompilationUnit):
        if len(cu.stmts) == 1:
            return self.visit(cu.stmts[0])
        else:
            raise Exception('No translation for more than one expression')

    def visit_conditional_expr(self, cond: ConditionalExpr):
        return CodeFragment(f'{parenthesize(50, self.visit(cond.cond))} ? '
                            f'{parenthesize(50, self.visit(cond.pos))} : '
                            f'{parenthesize(50, self.visit(cond.neg))}',
                            precedence=50)

    def visit_subscripted_expr(self, sub: SubscriptedExpr):
        obj_code = self.visit(sub.obj)
        subs_code = [self.visit(s) for s in sub.subscripts]
        subs_str = ''.join(f'[{s.value}]' for s in subs_code)
        return CodeFragment(f'{parenthesize(200, obj_code)}{subs_str}',
                            precedence=200,
                            free_vars=sub.prog_free_vars)

    def visit_range_code(self, r: RangeCode):
        return CodeFragment(f'{r.start}..{r.stop - 1}')

    def visit_assignment(self, assign):
        raise Exception('Assignment not supported for OPL')

    def visit_statements(self, seq):
        raise Exception('Assignment not supported for OPL')

    def visit_return_statement(self, ret):
        raise Exception('Return statement not supported for OPL')

    def visit_data_constant(self, const):
        raise Exception('Data constants not supported for OPL')

    def visit_cast(self, cast: CastExpr):
        return self.visit(cast.term)

    def visit_lambda_expression_expr(self, lfunc: LambdaExpressionExpr):
        raise Exception('Lambda not supported')


if __name__ == '__main__':
    print(column_to_index('AA'))
    print(index_to_column(27))
    print(list(RangeFragment('A3', 'AB5')))
