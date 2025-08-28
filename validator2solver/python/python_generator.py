import copy
from abc import ABCMeta, ABC, abstractmethod
from functools import wraps
from itertools import chain, groupby, repeat
from numbers import Number
from operator import attrgetter
from typing import List, Sequence, Union, Optional

from codegen.abstract_rep import CodeVisitor, AttributeAccess, VariableAccess, Expression, ComparisonExpr, NumberExpr, \
    Import, SetExpr, StringExpr, SetMembershipExpr, NegatedExpr, LoopIn, AggregateExpr, \
    BetweenExpr, FunctionApplExpr, DummyVariable, PredicateApplExpr, LogicalExpr, Identifier, \
    QuantifierExpr, TemporalExpr, CodeFragment, FunctionDefinition, CodeElement, BooleanExpr, parenthesize, \
    ComprehensionContainerCode, ComprehensionConditionCode, StreamExpr, AbstractFunctionDefinition, \
    AbstractClassDefinition, AbstractTypeDeclaration, AbstractNamedArg, CompilationUnit, SubscriptedExpr, SequenceExpr, \
    Assignment, Statements, add_return_if_needed, ReturnStatement, Imperative, CastExpr, LambdaExpressionExpr
from codegen.library import AttributeMappings
from codegen.parameters import ParameterDescriptor
from codegen.transformations import ArgRef, MultipleArgs, TransformToAttribute, SpliceArgs
from codegen.utils import decorate_method
from math_rep.constants import GE_SYMBOL, LE_SYMBOL, NOT_EQUALS_SYMBOL, AND_SYMBOL, OR_SYMBOL, IMPLIES_SYMBOL, \
    FOR_ALL_SYMBOL, ELEMENT_OF_SYMBOL, NOT_ELEMENT_OF_SYMBOL, INTERSECTION_SYMBOL, UNION_SYMBOL, NOT_SYMBOL
from math_rep.expr import function_type, BodyExpr, IFTE
from math_rep.expression_types import MType, M_NUMBER, M_ANY, QualifiedName, NameTranslator, as_math_name, \
    is_math_name
from validator2solver.python.python_builtins import is_python_builtin, is_python_name
from validator2solver.python.python_frame_constants import PYTHON_UNKNOWN_FRAME_NAME
from validator2solver.python.symbol_table import PYTHON_BUILTIN_FRAME_NAME

ASSOCIATIVE_PYTHON_OPERATORS = {'+', '*', 'and', 'or'}

# FIXME: add 'is', 'is not'
PYTHON_COMP_OPS = {'=': '==', NOT_EQUALS_SYMBOL: '!=', '>': '>', GE_SYMBOL: '>=', '<': '<', LE_SYMBOL: '<=',
                   ELEMENT_OF_SYMBOL: 'in', NOT_ELEMENT_OF_SYMBOL: 'not in'}
PYTHON_AGGREGATE_FUNCS = {'+': 'sum', '*': 'product', 'SET': ('{', '}')}

PYTHON_FUNCTION_TRANSLATIONS = {AND_SYMBOL: 'and', OR_SYMBOL: 'or', 'max': 'max', 'min': 'min', NOT_SYMBOL: 'not',
                                ELEMENT_OF_SYMBOL: 'in', NOT_ELEMENT_OF_SYMBOL: 'not in',
                                LE_SYMBOL: '<=', GE_SYMBOL: '>=', NOT_EQUALS_SYMBOL: '!=',
                                '=': '==', '+': '+', '*': '*', '-': '-', '/': '/', 'next': 'next'}


class PythonFunctionNameTranslator(NameTranslator):
    def _translate_additions(self, name: QualifiedName) -> QualifiedName:
        """
        Override this in subclasses to provide additional name translations; raises exception by default.

        Don't forget to call super when overriding!
        """
        raise Exception(f'Unknown Python function {name}')

    def translate(self, name: QualifiedName) -> QualifiedName:
        if is_math_name(name):
            return QualifiedName(PYTHON_FUNCTION_TRANSLATIONS[name.name.lower()],
                                 lexical_path=(PYTHON_BUILTIN_FRAME_NAME,))
        if is_python_builtin(name):
            return name
        if is_python_name(name):
            return name
        return self._translate_additions(name)


def translate_python_function(func):
    if is_math_name(func):
        return QualifiedName(PYTHON_FUNCTION_TRANSLATIONS[func.name.lower()], lexical_path=(PYTHON_BUILTIN_FRAME_NAME,))
    if is_python_builtin(func):
        return func
    if is_python_name(func):
        return func
    raise Exception(f'Unknown Python function {func}')


class ConditionalTransformation(ABC):
    @abstractmethod
    def condition(self, args):
        pass

    @abstractmethod
    def transformation(self):
        pass


class TransformDifferent(ConditionalTransformation):
    def condition(self, args):
        return len(args) == 2

    def transformation(self):
        return NOT_EQUALS_SYMBOL, ArgRef(0), ArgRef(1)


# FIXME: add all primitives
# FIXME!!!! add unary -,+
PYTHON_PRIMITIVES = {'+': 160, '-': 160, '*': 170, '/': 170, '|': 153, '&': 156, '==': 140, '<': 140, '<=': 140,
                     '=': 140, '>=': 140, '>': 140, '!=': 140, 'and': 110, 'or': 100, 'not': 130}

# Removed this: INTERSECTION_SYMBOL: 'period-intersection'
FUNCTION_TRANSLATIONS = {INTERSECTION_SYMBOL: '&', UNION_SYMBOL: '|', AND_SYMBOL: 'and',
                         OR_SYMBOL: 'or',
                         IMPLIES_SYMBOL: (OR_SYMBOL, (NOT_SYMBOL, ArgRef(0)), ArgRef(1)),
                         '%*': ('*', ('/', ArgRef(0), 100), ArgRef(1)),
                         '*different*': TransformDifferent(),
                         # TODO: this is part of profiles
                         # 'len': {M_PERIOD: '*period-length*'}
                         }


class PythonFunctionDefinition(FunctionDefinition):
    def __init__(self, name: QualifiedName, typed_parameters: Sequence[ParameterDescriptor], return_type: MType,
                 doc_string: Optional[str], body: str,
                 defs: Sequence[Union['PythonFunctionDefinition', 'PythonClassDefinition']] = (),
                 decorators: Sequence[Expression] = (), is_method=False):
        self.name = name
        self.typed_parameters = typed_parameters
        self.return_type = return_type
        self.doc_string = doc_string
        self.body = body
        self.defs = defs
        self.decorators = decorators
        self.is_method = is_method

    @staticmethod
    def from_abstract_function_definition(abst: AbstractFunctionDefinition,
                                          visitor: 'PythonVisitor') -> 'PythonFunctionDefinition':
        # FIXME: check this!
        pars = abst.typed_parameters
        if target := abst.method_target:
            pars = [target] + pars
        return PythonFunctionDefinition(abst.name, pars, abst.return_type, abst.func_doc_string,
                                        visitor.visit(add_return_if_needed(abst.body)).value, defs=abst.defs,
                                        decorators=abst.decorators, is_method=target is not None)


def apply_transformation(template, args: List[Expression], doc_string):
    if isinstance(template, Sequence):
        transformed_args = []
        for e in template[1:]:
            ta = apply_transformation(e, args, '???')
            if isinstance(ta, SpliceArgs):
                transformed_args.extend(ta.args)
            else:
                transformed_args.append(ta)
        func_name = as_math_name(template[0])
        result = FunctionApplExpr(func_name, transformed_args)
        result.type = function_type(func_name)
    elif isinstance(template, str):
        result = StringExpr(template)
    elif isinstance(template, Number):
        result = NumberExpr(template)
    elif isinstance(template, ArgRef):
        result = args[template.num]
    elif isinstance(template, ConditionalTransformation) and template.condition(args):
        return apply_transformation(template.transformation(), args, doc_string)
    elif isinstance(template, MultipleArgs):
        result = SpliceArgs(args[slice(template.start, template.stop)])
    elif isinstance(template, TransformToAttribute):
        assert len(args) == 1, 'Only one argument possible for attribute access'
        result = AttributeAccess(template.attribute, args[0])
    else:
        raise Exception(f'Unrecognized template element: {template}')
    result.doc_string = doc_string
    return result


def python_attribute_mappings():
    result = AttributeMappings()
    # len
    dv = DummyVariable()
    expr = FunctionApplExpr(QualifiedName('len', lexical_path=(PYTHON_BUILTIN_FRAME_NAME,)), [dv])
    expr.type = M_NUMBER
    result.add_mapping('length', expr, dv)
    return result


def functionize(method):
    @wraps(method)
    def with_func(self, *args, **kwargs):
        checkpoint = self.helper_checkpoint()
        result = method(self, *args, **kwargs)
        # FIXME!! need to add return statement to function
        return self.encapsulate(result, checkpoint=checkpoint, additional_doc=f'Return type: {str(args[0].type)}')

    return with_func


def transfer_doc_string(method):
    @wraps(method)
    def transferer(self, arg1, *args, **kwargs):
        result = method(self, arg1, *args, **kwargs)
        try:
            result.doc_string = arg1.doc_string
        except AttributeError:
            pass
        return result

    return transferer


def print_type(method):
    @wraps(method)
    def printer(self, arg1, *args, **kwargs):
        result = method(self, arg1, *args, **kwargs)
        print(f'=== {arg1.doc_string}')
        print(f'--- {arg1.type}')
        return result

    return printer


class PythonVisitor(CodeVisitor, metaclass=decorate_method((functionize, 'Xvisit_*'),
                                                           (print_type, 'Xvisit_*'),
                                                           (transfer_doc_string, 'visit_*'),
                                                           supermetaclass=ABCMeta)):
    def __init__(self, base_name, function_name_translator_class=PythonFunctionNameTranslator, indentation=4):
        super().__init__(base_name, attribute_mappings=python_attribute_mappings())
        self.function_name_translator = function_name_translator_class()
        self.indentation = ' ' * indentation

    def full_code(self, abs_rep: CodeElement, paraphrase, encapsulate=True):
        code = self.visit(add_return_if_needed(abs_rep))
        imports = []
        for module, contents in groupby(sorted(self.imports, key=attrgetter('module', 'name')), attrgetter('module')):
            imports.append(f'from {module} import {", ".join(map(attrgetter("name"), contents))}')
        body = (self.encapsulate(code, additional_doc=paraphrase, checkpoint=0) if encapsulate
                else code)
        helpers = self.pretty_helpers()
        return '\n'.join(imports) + ('\n\n\n' if imports else '') + helpers + ('\n\n\n' if helpers else '') + body.value

    def code_fragment_to_function_body(self, cf: CodeFragment):
        # retval = f'return {cf.value}'
        retval = cf.value
        if cf.body:
            return self.conc(cf.body, retval)
        else:
            return retval

    def indent(self, fragment: str):
        """
        Return an indented version of the given fragment.

        Convention: fragment is properly indented, doesn't start or end with a newline
        """
        return self.indentation + fragment.replace('\n', '\n' + self.indentation)

    def conc(self, *fragments):
        return '\n'.join(fragments)

    def loop(self, var, container, body):
        return f'for {var} in {container}:\n{self.indent(body)}'

    def conditional(self, condition, pos_code, neg_code=None):
        result = f'if {condition}:\n{self.indent(pos_code)}'
        if neg_code:
            result += f'else:\n{self.indent(neg_code)}'
        return result

    def pretty_function_def(self, func: PythonFunctionDefinition) -> str:
        doc = f'"""\n{func.doc_string.strip()}\n"""\n' if func.doc_string else ''
        # params = sorted(func.typed_parameters, key=attrgetter('name'))
        params = func.typed_parameters
        rtype = f' -> {t.for_python()}' if (t := func.return_type) is not None and t != M_ANY else ''
        defs = ''
        if internals := func.defs:
            defs = '\n' + '\n\n'.join(self.visit(d).value for d in internals) + '\n\n'
        dec = ((''.join('@' + self.visit(d).value + '\n' for d in decorators))
               if (decorators := func.decorators) else '')
        param_text = ', '.join(p.for_python(add_type=not (func.is_method and i == 0)) for i, p in enumerate(params))
        return (
            f'{dec}def {func.name.name}({param_text}){rtype}:\n'
            f'{self.indent(doc + defs + func.body)}')

    def encapsulate(self, cf: CodeFragment, checkpoint: int, additional_doc=None) -> CodeFragment:
        doc_string = cf.doc_string or ''
        if additional_doc:
            doc_string += '\n' + additional_doc
        args = cf.free_vars
        body = self.code_fragment_to_function_body(cf)
        fname = QualifiedName(self.fresh_func(), lexical_path=())
        fargs = sorted(arg.to_c_identifier() for arg in args)
        helpers = self.pretty_helpers(checkpoint)
        nl = '\n' if helpers else ''
        full_body = f'{helpers}{nl}{body}'
        self.clear_helpers(checkpoint)
        helper = PythonFunctionDefinition(fname,
                                          [ParameterDescriptor(arg.name, M_ANY)
                                           for arg in sorted(args, key=attrgetter('name'))],
                                          M_ANY, doc_string, full_body)
        self.add_helper_function(helper)
        return CodeFragment(f'{fname}({", ".join(fargs)})', doc_string=doc_string, free_vars=frozenset(args))

    def visit_dummy_var(self, dummy_var):
        if dummy_var not in self.dummy_vars:
            raise Exception('Undefined dummy variable')
        return self.dummy_vars[dummy_var].accept(self)

    def visit_identifier(self, identifier: Identifier):
        self._add_import_from_var(identifier.name)
        return CodeFragment(identifier.name.to_c_identifier())

    def visit_variable_access(self, variable: VariableAccess):
        var = variable.name
        self._add_import_from_var(var)
        return CodeFragment(var.to_c_identifier(), free_vars=frozenset([var]))

    def _add_import_from_var(self, var):
        # FIXME: implement this; ignore user vars and vars from current module (need to define in __init__)
        pass

    def visit_number(self, num: NumberExpr):
        return CodeFragment(str(num.value))

    def visit_boolean(self, value: BooleanExpr):
        return CodeFragment(str(bool(value.value)))

    def visit_string(self, s: StringExpr):
        return CodeFragment(repr(s.value))

    def visit_set_expr(self, s: SetExpr):
        elements = [e.accept(self) for e in s.set]
        return CodeFragment('{' + ', '.join(e.value for e in elements) + '}',
                            free_vars=frozenset(chain.from_iterable(e.free_vars for e in elements)))

    def visit_sequence_expr(self, s: SequenceExpr):
        elements = [e.accept(self) for e in s.elements]
        return CodeFragment('[' + ', '.join(e.value for e in elements) + ']',
                            free_vars=frozenset(chain.from_iterable(e.free_vars for e in elements)))

    def visit_attribute_access(self, attr: AttributeAccess):
        # FIXME: check type in next line
        attr_id = attr.attribute.name.to_c_identifier()
        trans = self.attribute_mappings.get_mapping(attr_id)
        if trans:
            dummy = trans.dummy
            dummy_type = dummy.type
            dummy.type = attr.container.type
            self.push_dummy_var(dummy, attr.container)
            new_expr = copy.copy(trans.expr)
            new_expr.doc_string = attr.doc_string
            result = new_expr.accept(self)
            self.pop_dummy_var(dummy)
            dummy.type = dummy_type

            return result
        container_code = attr.container.accept(self)
        container_str = parenthesize(190, container_code)
        return CodeFragment(f'{container_str}.{attr_id}', precedence=190, free_vars=container_code.free_vars)

    def visit_comparison_expr(self, comp: ComparisonExpr):
        lhs_code = comp.lhs.accept(self)
        lhs_str = parenthesize(140, lhs_code)
        rhs_code = comp.rhs.accept(self)
        rhs_str = parenthesize(140, rhs_code)
        py_op = PYTHON_COMP_OPS[comp.op.name]
        return CodeFragment(f'{lhs_str} {py_op} {rhs_str}', precedence=140,
                            free_vars=lhs_code.free_vars | rhs_code.free_vars)

    def visit_temporal_expr(self, temporal: TemporalExpr):
        # Translate into a function application
        funapp = FunctionApplExpr(temporal.op, [temporal.lhs, temporal.rhs, temporal.container])
        funapp.type = temporal.type
        funapp.doc_string = temporal.doc_string
        return funapp.accept(self)

    def visit_set_membership(self, expr: SetMembershipExpr):
        element_code = expr.element.accept(self)
        element = parenthesize(150, element_code)
        expr_code = expr.container.accept(self)
        container = parenthesize(150, expr_code)
        return CodeFragment(f'{element} in {container}', precedence=150,
                            free_vars=element_code.free_vars | expr_code.free_vars)

    def visit_negation(self, expr: NegatedExpr):
        expr_code = expr.expr.accept(self)
        precedence = PYTHON_PRIMITIVES.get('not')
        return CodeFragment('not ' + parenthesize(precedence, expr_code), precedence=precedence,
                            free_vars=expr_code.free_vars)

    def visit_between(self, between: BetweenExpr):
        lb_code = between.lb.accept(self)
        expr_code = between.expr.accept(self)
        ub_code = between.ub.accept(self)
        return CodeFragment((f'{parenthesize(140, lb_code)} '
                             f'<= {parenthesize(140, expr_code)} '
                             f'<= {parenthesize(140, ub_code)}'), precedence=140,
                            free_vars=lb_code.free_vars | expr_code.free_vars | ub_code.free_vars)

    def visit_function_appl_expr(self, appl: FunctionApplExpr):
        if not appl.method_target:
            return self._application_to_code(appl.function, appl.doc_string, appl.args, appl.named_args)
        target = parenthesize(190, self.visit(appl.method_target))
        args_code = [a.accept(self) for a in appl.args]
        free_vars = frozenset(chain.from_iterable(ac.free_vars for ac in args_code))
        # FIXME: add lexical path components as required based in imports
        return CodeFragment(f'{target}.{appl.function.name}({", ".join(a.value for a in args_code)})',
                            free_vars=free_vars)

    def _get_import(self, name: QualifiedName | str) -> Import | None:
        """
        Return an import for the given function name, or None if no import is necessary.

        Override in subclasses as appropriate, this implementation always returns None.
        """
        return None

    def _application_to_code(self, function_name, doc_string, args, named_args=None):
        function = function_name
        # FIXME! translation of function depends on lexical-path, function must be a QualifiedName
        template = FUNCTION_TRANSLATIONS.get(function.name if isinstance(function, QualifiedName) else function)
        while template:
            if isinstance(template, str):
                function = QualifiedName(template, lexical_path=(PYTHON_BUILTIN_FRAME_NAME,))
                break
            elif isinstance(template, dict):
                assert len(args) >= 1
                template = template.get(args[0].type) or template.get(None)
            else:
                transformed = apply_transformation(template, args, doc_string)
                return transformed.accept(self)
        external = self._get_import(function)
        if external:
            function = QualifiedName(external.name,
                                     lexical_path=tuple(
                                         reversed([PYTHON_BUILTIN_FRAME_NAME] + external.module.split('.'))))
            if external.module != '':
                self.add_import(external)
            precedence = None
            arg_bindings = repeat(None)
        else:
            # function = translate_python_function(function)
            function = self.function_name_translator.translate(function)
            precedence = PYTHON_PRIMITIVES.get(function.name)
            arg_bindings = (repeat(precedence) if function.name in ASSOCIATIVE_PYTHON_OPERATORS
                            else chain([precedence], repeat((precedence or 0) + 1)))

        args_code = [a.accept(self) for a in args]
        free_vars = frozenset(chain.from_iterable(ac.free_vars for ac in args_code))
        args_text = [parenthesize(arg_precedence, ac) for ac, arg_precedence in zip(args_code, arg_bindings)]
        if precedence:
            if len(args_text) > 1:
                return CodeFragment(f' {function} '.join(args_text), precedence=precedence, free_vars=free_vars)
            else:
                return CodeFragment(f'{function}{" " if function.name[-1].isalnum() else ""}{args_text[0]}',
                                    precedence=precedence, free_vars=free_vars)
        arglist = ', '.join(args_text)
        if named_args:
            arglist += ', ' + ', '.join(f'{name}={value.accept(self)[0]}' for name, value in named_args)
        return CodeFragment(f'{function.name}({arglist})', doc_string=doc_string, free_vars=free_vars)

    def code_from_rest(self, compr: Union[ComprehensionContainerCode, ComprehensionConditionCode]):
        if (rest := compr.rest) is not None:
            rest_code_fragment = self.visit(rest)
            rest_code = ' ' + rest_code_fragment.value
            rest_vars = rest_code_fragment.free_vars
            rest_bound_vars = rest_code_fragment.bound_vars
        else:
            rest_code = ''
            rest_vars = set()
            rest_bound_vars = set()
        return rest_code, rest_vars, rest_bound_vars

    def visit_comprehension_container_code(self, compr: ComprehensionContainerCode):
        rest_code, rest_vars, rest_bound_vars = self.code_from_rest(compr)
        container_code = self.visit(compr.container)
        bound_vars = set(compr.vars) | rest_bound_vars
        result = CodeFragment(f'for {", ".join(var.name for var in compr.vars)} in {container_code.value}{rest_code}',
                              free_vars=(rest_vars | container_code.free_vars) - bound_vars)
        result.bound_vars = bound_vars
        result.container_code = container_code
        return result

    def visit_comprehension_condition_code(self, compr: ComprehensionConditionCode):
        rest_code, rest_vars, rest_bound_vars = self.code_from_rest(compr)
        condition_code = self.visit(compr.condition)
        result = CodeFragment(f'if {condition_code.value}{rest_code}', free_vars=condition_code.free_vars | rest_vars)
        result.bound_vars = rest_bound_vars
        return result

    def visit_stream_expr(self, stream: StreamExpr):
        term_code = stream.term.accept(self)
        container_code = stream.container.accept(self)
        bound_vars = container_code.bound_vars
        free_vars = (container_code.free_vars | term_code.free_vars) - bound_vars
        return CodeFragment(f'({term_code.value} {container_code.value})', free_vars=free_vars)

    def visit_aggregate_expr(self, aggregate: AggregateExpr):
        # TODO: unify this code with the one in opl_generator.py
        term_code = aggregate.term.accept(self)
        container_code = aggregate.container.accept(self)
        bound_vars = container_code.bound_vars
        free_vars = (container_code.free_vars | term_code.free_vars) - bound_vars
        operator = PYTHON_AGGREGATE_FUNCS[aggregate.operator]
        inside = f'{term_code.value} {container_code.value}'
        if isinstance(operator, (tuple, list)):
            code = f'{operator[0]}{inside}{operator[1]}'
        else:
            code = f'{operator}({inside})'
        return CodeFragment(code, free_vars=free_vars)

    def visit_predicate_appl(self, appl: PredicateApplExpr):
        # FIXME! support predicate transformations, like functions; this is a hack
        # pred_name = appl.pred.accept(self).value
        pred_name = appl.pred.name.name
        if isinstance(pred_name, (tuple, list)):
            pred_name = '_'.join(pred_name)
        pred_id = QualifiedName(pred_name,
                                lexical_path=(PYTHON_UNKNOWN_FRAME_NAME, PYTHON_BUILTIN_FRAME_NAME))
        return self._application_to_code(pred_id, appl.doc_string, appl.args)

    def visit_logical_expr(self, expr: LogicalExpr):
        return self._application_to_code(expr.op, expr.doc_string, expr.elements)

    def visit_concatenation(self, conc):
        return self.conc(*conc.fragments)

    def visit_loop_in(self, loop: LoopIn):
        return self.loop(loop.var, loop.container, loop.body)

    def _handle_unique_existential(self, quantifier: QuantifierExpr, bound_vars, container_code, formula_code,
                                   free_vars, checkpoint):
        """
        Special handling for unique existential.  Raises exception by default.
        """
        raise Exception('Unique existential quantifiers not supported')

    def visit_quantifier(self, quantifier: QuantifierExpr):
        function = 'all' if quantifier.kind == FOR_ALL_SYMBOL else 'any'
        checkpoint = self.helper_checkpoint()
        if quantifier.formula:
            formula_code = quantifier.formula.accept(self)
            formula = formula_code.value
            formula_vars = formula_code.free_vars
        else:
            formula_code = None
            formula = True
            formula_vars = frozenset()
        container_code = quantifier.container.accept(self)
        bound_vars = container_code.bound_vars
        free_vars = (formula_vars | container_code.free_vars) - bound_vars
        if not quantifier.unique:
            return CodeFragment(f'{function}({formula} {container_code.value})', free_vars=free_vars)
        return self._handle_unique_existential(quantifier, bound_vars, container_code, formula_code,
                                               free_vars, checkpoint)

    def visit_cells(self, cells):
        raise Exception('Spreadsheet cells not supported in Python')

    def visit_subscripted_expr(self, sub: SubscriptedExpr):
        obj_cf = self.visit(sub.obj)
        subscripts_cf = [self.visit(s) for s in sub.subscripts]
        return CodeFragment(f'{parenthesize(180, obj_cf)}[{", ".join(s.value for s in subscripts_cf)}]',
                            precedence=180,
                            free_vars=obj_cf.free_vars | frozenset(
                                chain.from_iterable(s.free_vars for s in subscripts_cf)))

    def visit_conditional_expr(self, ifte: IFTE):
        cond_cf = self.visit(ifte.cond)
        pos_cf = self.visit(ifte.pos)
        neg_cf = self.visit(ifte.neg)
        return CodeFragment(f'{parenthesize(50, pos_cf)} '
                            f'if {parenthesize(50, cond_cf)} '
                            f'else {parenthesize(50, neg_cf)}',
                            precedence=50,
                            free_vars=frozenset(cond_cf.free_vars | pos_cf.free_vars | neg_cf.free_vars))

    def visit_abstract_function_definition(self, func_def: AbstractFunctionDefinition):
        return CodeFragment(
            self.pretty_function_def(PythonFunctionDefinition.from_abstract_function_definition(func_def, self)))

    def visit_body_expr(self, body: BodyExpr):
        raise Exception('BodyExpr should be handled as part of the containing function definition')

    def visit_abstract_class_definition(self, class_def: AbstractClassDefinition):
        defs_code = [self.visit(d) for d in class_def.defs]
        doc = f'"""\n{d.strip()}\n"""\n' if (d := class_def.class_doc_string) else ''
        defs = '\n\n'.join(d.value for d in defs_code) if defs_code else 'pass'
        dec = ((''.join('@' + self.visit(d).value + '\n' for d in decorators))
               if (decorators := class_def.decorators) else '')
        # FIXME! Add to QualifiedName a method to return the name for a given set of imports
        return CodeFragment(
            f'{dec}class {class_def.name.name}({", ".join(self.visit(sc).value for sc in class_def.superclasses)}):\n'
            f'{self.indent(doc + defs)}',
            doc_string=doc)

    def visit_abstrat_type_declaration(self, decl: AbstractTypeDeclaration):
        return CodeFragment(f'{decl.var}: {decl.type.for_python()}')
        # raise Exception('AbstractTypeDefinition should be handled by containing class')

    def visit_named_arg(self, arg: AbstractNamedArg):
        expr = self.visit(arg.expr)
        return CodeFragment(f'{arg.name}={expr.value}', free_vars=frozenset(arg.name) | expr.free_vars)

    def visit_compilation_unit(self, cu: CompilationUnit):
        stmts = [self.visit(s) for s in cu.stmts]
        return CodeFragment('\n'.join(s.value for s in stmts),
                            free_vars=frozenset(chain.from_iterable(s.free_vars for s in stmts)))

    def _add_comment(self, element: Imperative, code: str):
        comment = element.comment
        if comment is None:
            return code
        return f'# {comment}\n{code}'

    def visit_assignment(self, assign: Assignment):
        value = self.visit(assign.value)
        return CodeFragment(self._add_comment(assign, f'{assign.var_name.to_c_identifier()} = {value.value}'),
                            free_vars=value.free_vars)

    def visit_statements(self, seq: Statements):
        statements = [self.visit(s) for s in seq.statements]
        free_vars = frozenset(chain.from_iterable(s.free_vars for s in statements))
        # last_val = statements[-1]
        # if isinstance(last_val, Imperative):
        return CodeFragment(self._add_comment(seq, '\n'.join(s.value for s in statements)), free_vars=free_vars)
        # body = statements[:-1]
        # result = CodeFragment(last_val.value, free_vars=free_vars)
        # result.body = '\n'.join(s.value for s in body)
        # return result

    def visit_return_statement(self, ret: ReturnStatement):
        value = self.visit(ret.value)
        return CodeFragment(self._add_comment(ret, f'return {value.value}'), free_vars=value.free_vars)

    def visit_data_constant(self, const):
        return CodeFragment(str(const.value), free_vars=frozenset())

    def visit_cast(self, cast: CastExpr):
        return self.visit(cast.term)

    def visit_lambda_expression_expr(self, lfunc: LambdaExpressionExpr):
        raise Exception('Lambda not yet supported')

    def visit_named_constant(self, const):
        raise Exception(f'NumericConstant not supported in PythonVisitor: {const}')
