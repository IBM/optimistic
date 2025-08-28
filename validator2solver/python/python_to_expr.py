from abc import ABC, abstractmethod
from dataclasses import dataclass
from numbers import Number
from typing import Optional, Union

from codegen.abstract_rep import AbstractTypeDeclaration
from codegen.parameters import ParameterDescriptor, TARGET_PARM
from validator2solver.python.python_generator import PythonVisitor, PYTHON_COMP_OPS
from codegen.utils import visitor_for, disown
from math_rep.constants import AND_SYMBOL, ELEMENT_OF_SYMBOL, NOT_ELEMENT_OF_SYMBOL, OR_SYMBOL, NOT_SYMBOL, \
    NOT_EQUALS_SYMBOL, GE_SYMBOL, LE_SYMBOL, FOR_ALL_SYMBOL, EXISTS_SYMBOL
from math_rep.math_frame import MATH_FRAME_NAME
from math_rep.expr import MathVariable, FunctionApplication, Quantity, Comparison, LogicalOperator, \
    GeneralSet, Aggregate, ComprehensionContainer, ComprehensionCondition, Stream, FormalContent, Quantifier, \
    FunctionDefinitionExpr, Attribute, Atom, Term, BodyExpr, ClassDefinitionExpr, MathTypeDeclaration, NamedArgument, \
    MathModule, Subscripted, IFTE, InitializedVariable, TRUE_AS_QUANTITY, TypeAlias, GeneralSequence
from math_rep.expression_types import MFunctionType, M_ANY, MClassType, MAtomicType, QualifiedName, as_math_name
from validator2solver.python.python_rep import PythonElement, PythonVariable, PythonCall, PythonConstant, PythonOp, \
    PythonComparison, \
    PythonSetCons, PythonSetCompr, PythonForComprehension, PythonIfComprehension, PythonGenExpr, PythonFile, \
    Comprehension, PythonFuncDef, PythonAttribute, PythonStatements, PythonReturn, PythonExpressions, \
    python_type_to_abstract, PythonClass, PythonTypedExpr, PythonImport, PythonImportFrom, PythonImportAs, PythonPass, \
    PythonDecorated, PythonKeywordArg, PythonAssignment, PythonSubscripted, PythonIFTE, PythonListCons, PythonTupleCons
from validator2solver.python.python_builtins import PYTHON_OPERATORS, is_python_operator, is_python_builtin, \
    PYTHON_LOGICAL_OPERATORS
from validator2solver.python.symbol_default_modules import METADATA_QN, NEW_TYPE_QN, CLASSMETHOD_QN, \
    STATICMETHOD_QN, DATA_RECORD_QN_GROUP, SOLUTION_VARIABLE_QN
from validator2solver.python.symbol_table import environment_path_from_frame

METHOD_CALL_INDICATOR = '**method-call**'

PYTHON_COMP_OPS_REV1 = {v: k for k, v in PYTHON_COMP_OPS.items()}
PYTHON_COMP_OPS_REV = {**PYTHON_COMP_OPS_REV1, 'in': ELEMENT_OF_SYMBOL, 'notin': NOT_ELEMENT_OF_SYMBOL,
                       # N.B. no notion of object identity in mathematical representation!
                       'is': '=', 'isnot': NOT_EQUALS_SYMBOL}

PYTHON_OPERATOR_TRANSLATIONS = {'and': AND_SYMBOL, 'or': OR_SYMBOL, 'not': NOT_SYMBOL,
                                'in': ELEMENT_OF_SYMBOL, 'notin': NOT_ELEMENT_OF_SYMBOL, '<=': LE_SYMBOL,
                                '>=': GE_SYMBOL, '!=': NOT_EQUALS_SYMBOL, '==': '=',
                                '+': '+', '*': '*', '-': '-', '/': '/'}

PYTHON_AGGREGATIVE_FUNCTIONS = {as_math_name('sum'): '+'}


class PythonBuiltinTransformer(ABC):
    @abstractmethod
    def transform(self, expr: PythonCall, visitor: 'AbstractPythonElementVisitor') -> Optional[FormalContent]:
        pass


class PythonQuantifierTransformer(PythonBuiltinTransformer):
    def __init__(self, quantifier_symbol):
        self.quantifier_symbol = quantifier_symbol

    @staticmethod
    def extract_comprehension(arglist) -> Optional[Comprehension]:
        if len(arglist) != 1:
            return None
        arg = arglist[0]
        if isinstance(arg, Comprehension):
            return arg

    def transform(self, expr: PythonCall, visitor: PythonVisitor) -> Optional[FormalContent]:
        if (compr := self.extract_comprehension(expr.arglist)) is not None:
            return Quantifier(self.quantifier_symbol, visitor.visit(compr.expr), visitor.visit(compr.control))
        return IGNORE_ELEMENT


class PythonBuiltinIgnoredTransformer(PythonBuiltinTransformer):
    def __init__(self):
        self.symbol = PYTHON_BUILTIN_IGNORED_ELEMENT

    def transform(self, expr: PythonCall, visitor: PythonVisitor) -> Optional[FormalContent]:
        return IGNORE_ELEMENT


PYTHON_BUILTIN_IGNORED_ELEMENT = '**IGNORED**'
# FIXME: add bindings for all builtins
# FIXME: add support for more general transformations (e.g., to Quantifiers)
PYTHON_BUILTIN_TRANSLATION = {'all': PythonQuantifierTransformer(FOR_ALL_SYMBOL),
                              'any': PythonQuantifierTransformer(EXISTS_SYMBOL),
                              'next': 'next', 'set': 'set', 'abs': 'abs', 'pow': 'pow', 'sum': 'sum', 'ceil': 'ceil',
                              'min': 'min', 'max': 'max'}


def translate_python_operator(op):
    return QualifiedName(PYTHON_OPERATOR_TRANSLATIONS[op], lexical_path=(MATH_FRAME_NAME,))


def translate_python_builtin(func):
    trans = PYTHON_BUILTIN_TRANSLATION.get(func, PythonBuiltinIgnoredTransformer())
    if isinstance(trans, PythonBuiltinTransformer):
        return trans
    # FIXME!! differentiate paths, e.g., between +, -, etc. and sum, next, etc.
    return QualifiedName(trans, lexical_path=(MATH_FRAME_NAME,))


class PythonIntermediateExpr:
    """
    A representation for Python constructs that can only be translated into expressions in a certain context.

    For example, assignments and return statements only make sense as part of a body (PythonStatements).
    """


@dataclass
class PythonReturnExpr(PythonIntermediateExpr):
    retval: Term


@disown('var', 'context')
@dataclass
class PythonAssignmentExpr(FormalContent):
    var: Union[MathVariable, MathTypeDeclaration]
    value: Term
    context: str

    has_operator = True

    def describe(self, parent_binding=None):
        return f'{self.var.describe()} = {self.value.describe()}'

    def to_code_rep(self):
        if isinstance(var := self.var, MathTypeDeclaration):
            var_name = var.var
            vtype = var.type
        else:
            # MathVariable
            var_name = var.name
            vtype = M_ANY
        if self.context == 'class':
            return AbstractTypeDeclaration(var_name, vtype)
        raise Exception(f'Assignments not yet supported in {self.context}')

    def operator(self):
        return self.var

    def arguments(self):
        return [self.value]

    def with_argument(self, index, arg):
        if index != 0:
            raise IndexError('Index for Negate must be 0')
        return PythonAssignmentExpr(self.var, arg, self.context)


@visitor_for(PythonElement, collect_results=False)
class AbstractPythonElementVisitor:
    pass


class IgnoredElement:
    pass


IGNORE_ELEMENT = IgnoredElement()


# FIXME: add visit_tuple_cons
class PythonToExpr(AbstractPythonElementVisitor):
    def __init__(self, symbol_table_visitor):
        self.enclosing_context = []
        self.symbol_table_visitor = symbol_table_visitor

    def visit_python_file(self, file: PythonFile):
        self.enclosing_context.append('file')
        result = MathModule([val for arg in file.contents if (val := self.visit(arg)) is not IGNORE_ELEMENT])
        self.enclosing_context.pop()
        result.add_class_members(self.symbol_table_visitor.create_class_members())
        return result

    def visit_python_import(self, imp: PythonImport):
        return IGNORE_ELEMENT

    def visit_python_import_from(self, imp: PythonImportFrom):
        return IGNORE_ELEMENT

    def visit_python_import_as(self, imp: PythonImportAs):
        return IGNORE_ELEMENT

    def visit_python_pass(self, ps: PythonPass):
        return IGNORE_ELEMENT

    def visit_python_constant(self, const: PythonConstant):
        value = const.value
        if isinstance(value, bool):
            return Quantity(value, '*Boolean*')
        elif isinstance(value, Number):
            return Quantity(value)
        elif isinstance(value, str):
            return Quantity(value, '*String*')
        elif value is None:
            return Quantity(None, '*Nil*')
        else:
            # FIXME: add support for None, Ellipsis
            raise Exception('Other types not yet supported')

    def visit_python_tuple_cons(self, const: PythonTupleCons):
        return GeneralSequence([self.visit(c) for c in const.components])

    def visit_python_variable(self, var: PythonVariable):
        import_frame, alias = self.check_variable_is_import(var)
        if import_frame:
            if alias and import_frame.contains_variable(alias):
                # The alias is for the module imported `doit` -> `parse file`
                # e.g    from optimistic_symbol.symbol_explore import parse_file as doit
                #        doit('what ever file')
                pseudo = PythonVariable(alias)
                pseudo.frame = import_frame
                return MathVariable(
                    pseudo.name.with_path(self.symbol_table_visitor.environment_path_of_var(pseudo, True)))
        result = MathVariable(var.name.with_path(self.symbol_table_visitor.environment_path_of_var(var)))
        return result

    def check_variable_is_import(self, var: PythonVariable):
        import_ref = self.symbol_table_visitor.imports.get(var.name.name)
        if var.frame.is_module() or var.frame.is_builtin():
            if import_ref and import_ref[0].parent == var.frame:
                # The variable represents a module, which has an import
                return import_ref[0], None
            elif imports_alias := self.symbol_table_visitor.imports_alias.get(var.frame):
                # The variable is an alias, which refers to a frame which is an import
                return var.frame, imports_alias['name']
        return None, None

    def visit_python_attribute(self, attr: PythonAttribute):
        if isinstance(attr.obj, PythonVariable):
            import_frame, alias = self.check_variable_is_import(attr.obj)
            if import_frame:
                # we reach here if the variable was a *module*
                # we check if the *module* contains the attribute as a symbol
                # e.g itertools.chain.from_iterable([]), where the attribute is `chain`
                #    AST: GETATTR(GETATTR(REF(itertools), chain)
                pseudo = PythonVariable(attr.attr)
                pseudo.frame = import_frame
                if alias and pseudo.frame.contains_variable(alias):
                    # The alias is for the module imported `doit` -> `chain`
                    # e.g    from itertools import chain as doit
                    pseudo = PythonVariable(alias)
                    pseudo.frame = import_frame
                    container = MathVariable(
                        pseudo.name.with_path(self.symbol_table_visitor.environment_path_of_var(pseudo, True)))
                    return Attribute(Atom(MFunctionType([], M_ANY, arity='?'), [attr.attr]), container)
                elif alias:
                    # The alias is for the import library `doit` -> `chain`
                    # e.g  import itertools as doit
                    if pseudo.frame.contains_variable(attr.attr):
                        return MathVariable(
                            pseudo.name.with_path(self.symbol_table_visitor.environment_path_of_var(pseudo, True)))
                else:
                    import_frame, alias = self.check_variable_is_import(pseudo)
                    if import_frame:
                        # check to see if the attribute is also an import frame
                        #  e.g  import optimistic_symbol.symbol_explore
                        return None
                    elif pseudo.frame.contains_variable(attr.attr):
                        return MathVariable(
                            pseudo.name.with_path(self.symbol_table_visitor.environment_path_of_var(pseudo)))
                    else:
                        # We should never reach here
                        raise Exception('Internal error in python_to_expr.visit_python_attribute')
            else:
                # We reach here if:
                # the attr.obj is a Variable, which is not a *module*, and is a symbol inside the frame
                # it can be a regular variable which is a symbol in the frame
                # or class definiton, or function definition that are also symbol in the frame, but also have child frames
                # e.g.
                result = self.visit_python_variable(attr.obj)
                return Attribute(Atom(MFunctionType([], M_ANY, arity='?'), [attr.attr]), result)

        if isinstance(attr.obj, PythonAttribute):
            result = self.visit_python_attribute(attr.obj)
            if result:
                return Attribute(Atom(MFunctionType([], M_ANY, arity='?'), [attr.attr]), result)
            else:
                # We reach here when the attribute both `obj` container and `attr` are an import
                import_frame = self.symbol_table_visitor.imports.get(attr.obj.attr)
                if import_frame and import_frame[0].contains_variable(attr.attr):
                    pseudo = PythonVariable(attr.attr)
                    pseudo.frame = import_frame[0]
                    return MathVariable(QualifiedName(attr.attr,
                                                      lexical_path=self.symbol_table_visitor.environment_path_of_var(
                                                          pseudo, True)))
        # if isinstance(attr.obj, PythonCall):
        return Attribute(Atom(MFunctionType([], M_ANY, arity='?'), [attr.attr]), self.visit(attr.obj))

    def visit_python_call(self, call: PythonCall):
        func = self.visit(call.func)
        if isinstance(func, MathVariable):
            name = func.name
            if is_python_operator(name):
                name = translate_python_operator(name.name)
            if is_python_builtin(name):
                trans = translate_python_builtin(name.name)
                if isinstance(trans, PythonBuiltinTransformer):
                    return trans.transform(call, self)
                name = trans
            if aggregative_op := PYTHON_AGGREGATIVE_FUNCTIONS.get(name):
                assert len(args := call.arglist) == 1
                stream = self.visit(args[0])
                assert isinstance(stream, Stream)
                return Aggregate(aggregative_op, stream.term, stream.container)
            return FunctionApplication(name, [self.visit(arg) for arg in call.arglist])
        elif isinstance(func, Attribute):
            attr_name = func.attribute.words[0]
            result = FunctionApplication(
                QualifiedName(attr_name, type=func.attribute.type, lexical_path=(METHOD_CALL_INDICATOR,)),
                [self.visit(arg) for arg in call.arglist], method_target=func.container)
            return result
        else:
            # TODO: do we need to support function expressions (change PythonCall accordingly)?
            raise Exception('Expressions as functions not yet supported!')

    def visit_python_statements(self, stmts: PythonStatements):
        exprs = tuple(e for e in map(self.visit, stmts.statements) if e is not IGNORE_ELEMENT)
        if not exprs:
            return IGNORE_ELEMENT
        if isinstance(e1 := exprs[0], Quantity) and e1.unit == '*String*':
            doc_string = e1.value
            exprs = exprs[1:]
        else:
            doc_string = None
        defs = []
        while exprs and isinstance(e1 := exprs[0], (FunctionDefinitionExpr, ClassDefinitionExpr, MathTypeDeclaration,
                                                    FunctionApplication, InitializedVariable)):
            if isinstance(e1, FunctionApplication):
                if e1.function.name == 'print':
                    # ignore print statements
                    exprs = exprs[1:]
                    continue
                # other function calls are not supported
                break
            defs.append(e1)
            exprs = exprs[1:]
        if len(exprs) == 1 and isinstance(exprs[0], PythonReturnExpr):
            value = exprs[0].retval
        elif not exprs:
            value = None
        else:
            raise Exception(f'{exprs[0].__class__.__name__}({exprs[0]}) not supported in function/class body')
        if doc_string or defs:
            return BodyExpr(element_doc_string=doc_string, defs=defs, value=value)
        else:
            return value

    def visit_python_expressions(self, pexprs: PythonExpressions):
        exprs = tuple(map(self.visit, pexprs.expressions))
        if len(exprs) == 1:
            return exprs[0]
        # FIXME: complete
        raise Exception('Implement return of several values as tuple')

    def visit_python_return(self, ret: PythonReturn):
        return PythonReturnExpr(self.visit(ret.retval))

    def visit_python_op(self, appl: PythonOp):
        if (op := PYTHON_OPERATORS.get(appl.op)) is not None:
            return (LogicalOperator if appl.op in PYTHON_LOGICAL_OPERATORS else FunctionApplication)(
                translate_python_operator(op.name), [self.visit(arg) for arg in appl.args])
        raise Exception(f'Unknown operator: {appl.op}')

    def visit_python_comparison(self, appl: PythonComparison):
        cur_arg = self.visit(appl.args[0])
        rest_args = map(self.visit, appl.args[1:])
        result = None
        # FIXME: this could cause multiple evaluations of the same expression for multiple ops
        # (but Python code assumed to be functional)
        for op, arg in zip(appl.ops, rest_args):
            cur_comp = Comparison(cur_arg, PYTHON_COMP_OPS_REV[op], arg)
            result = cur_comp if result is None else LogicalOperator(AND_SYMBOL, [result, cur_comp])
            cur_arg = arg
        return result

    def visit_python_subscripted(self, sub: PythonSubscripted):
        obj = self.visit(sub.obj)
        subscripts = [self.visit(s) for s in sub.subscripts]
        return Subscripted(obj, subscripts)

    def visit_python_set_cons(self, setc: PythonSetCons):
        return GeneralSet([self.visit(c) for c in setc.components])

    def visit_python_list_cons(self, listc: PythonListCons):
        # FIXME: We don't want mutable objects, need to think about it
        return GeneralSet([self.visit(c) for c in listc.components])

    def visit_python_for_comprehension(self, compr: PythonForComprehension):
        self.enclosing_context.append('for')
        result = ComprehensionContainer([var.name for var in compr.vars], self.visit(compr.container),
                                        self.visit(compr.rest) if compr.rest else None)
        self.enclosing_context.pop()
        return result

    def visit_python_if_comprehension(self, compr: PythonIfComprehension):
        return ComprehensionCondition(self.visit(compr.condition),
                                      self.visit(compr.rest) if compr.rest else None)

    def visit_python_set_compr(self, setcompr: PythonSetCompr):
        compr = setcompr.control
        if not isinstance(compr, PythonForComprehension):
            raise Exception('Control of set comprehension must have type PythonForComprehension')
        self.enclosing_context.append('set')
        result = Aggregate('SET', self.visit(setcompr.expr), self.visit(setcompr.control))
        self.enclosing_context.pop()
        return result

    def visit_python_gen_expr(self, gen: PythonGenExpr):
        self.enclosing_context.append('gen')
        result = Stream(self.visit(gen.expr), self.visit(gen.control))
        self.enclosing_context.pop()
        return result

    def visit_python_func_def(self, func: PythonFuncDef):
        self.enclosing_context.append('func')
        # TODO: support internal definitions (ignore IGNORE_ELEMENT)
        # FIXME: track all name components in visitor instead of using relative frame
        frame = func.frame
        enclosing = frame.parent
        is_method = enclosing.is_class()
        enclosing_lexical_path = environment_path_from_frame(enclosing)
        name = QualifiedName(func.name, lexical_path=enclosing_lexical_path)
        pars = [p.as_parameter_descriptor() for p in func.pars.args]
        decorators = tuple(isinstance(dec, PythonVariable)
                           and dec.name in (STATICMETHOD_QN, CLASSMETHOD_QN)
                           for dec in func.decorators)
        is_static_method = is_method and any(dec == STATICMETHOD_QN for dec in decorators)
        is_class_method = is_method and any(dec == STATICMETHOD_QN for dec in decorators)
        # add 'not is_classmethod' to prevent these from having a method_target
        if is_method and not is_static_method:
            target = ParameterDescriptor(pars[0].name,
                                         # MClassType(QualifiedName(enclosing.name[len(CLASS_FRAME_PREFIX):],
                                         MClassType(QualifiedName(enclosing.name,
                                                                  lexical_path=enclosing_lexical_path[1:])),
                                         kind=TARGET_PARM)
            pars = pars[1:]
        else:
            target = None
        result = FunctionDefinitionExpr(name, pars, python_type_to_abstract(func.res_type), None, self.visit(func.body),
                                        lexical_path=environment_path_from_frame(frame), method_target=target,
                                        is_static_method=is_static_method, is_class_method=is_class_method)
        self.enclosing_context.pop()
        return result

    def visit_python_class(self, cls: PythonClass):
        self.enclosing_context.append('class')
        supers = [self.visit(s) for s in cls.superclasses]
        # members = [self.visit(m) for m in cls.members.statements]
        members = self.visit(cls.members)
        if members is IGNORE_ELEMENT:
            members = []
        frame = cls.frame
        enclosing = frame.parent
        name = QualifiedName(cls.name, lexical_path=environment_path_from_frame(enclosing))
        result = ClassDefinitionExpr(name, supers, members)
        self.enclosing_context.pop()
        return result

    def visit_python_typed_expr(self, te: PythonTypedExpr):
        assert isinstance(te.expr, PythonVariable)
        return MathTypeDeclaration(te.expr.name.name, python_type_to_abstract(te.type_decl))

    def visit_python_assignment(self, assignment: PythonAssignment):
        if assignment.operator != '=':
            raise Exception('Mutating assignments to variables not supported')
        assignee = self.visit(assignment.lhs)
        if not isinstance(assignee, (MathVariable, MathTypeDeclaration)):
            raise Exception('Mutating assignments to data structures not supported')
        context = self.enclosing_context[-1]
        value = self.visit(assignment.rhs)
        if context == 'class' and isinstance(assignee, MathTypeDeclaration):
            result = InitializedVariable(assignee, value)
        elif (context == 'file' and isinstance(assignee, MathVariable) and isinstance(value, FunctionApplication) and
              value.function == NEW_TYPE_QN):
            assert len(value.args) == 2
            q = value.args[0]
            assert isinstance(q, Quantity) and q.unit == '*String*'
            assert assignee.name.name == q.value
            given_type = value.args[1]
            assert isinstance(given_type, MathVariable)
            a_type = next(t for t in MAtomicType.members() if t.for_python() == given_type.name.name)
            # result = ClassDefinitionExpr(assignee.var.name, [], is_newtype=True,
            #                              fields=(MathTypeDeclaration('*', a_type),))
            result = TypeAlias(assignee.name.name, a_type)
        else:
            result = PythonAssignmentExpr(assignee, value, context)
        # TODO: get actual text
        result.text = ''
        return result

    @staticmethod
    def convert_field(field: Union[MathTypeDeclaration, InitializedVariable]
                      ) -> Union[MathTypeDeclaration, InitializedVariable]:
        if isinstance(field, MathTypeDeclaration):
            return field
        if not (isinstance(init := field.init, FunctionApplication)
                and init.function in (METADATA_QN, SOLUTION_VARIABLE_QN)):
            return field
        primary_key = False
        is_domain = False
        is_solution_var = False

        if init.function == METADATA_QN:
            # FIXME: Deprecated, using solution_variable() and TotalMapping() instead, remove it once transition is complete
            for arg in init.args:
                # FIXME: support direct use of field: field(metadata=dict(primary_key=...)), as well as abbreviations
                if not isinstance(arg, NamedArgument) or arg.name not in ('primary_key', 'domain', 'solution'):
                    raise Exception(f'Metadata {arg.name} not recognized for dataclass field {field.function}')
                if arg.expr == TRUE_AS_QUANTITY:
                    if arg.name == 'primary_key':
                        primary_key = True
                    elif arg.name == 'domain':
                        is_domain = True
                    elif arg.name == 'solution':
                        is_solution_var = True
        if init.function == SOLUTION_VARIABLE_QN:
            is_solution_var = True
        result = field.var.with_options(primary_key=primary_key, is_domain=is_domain, is_solution_var=is_solution_var)
        result.text = field.text
        return result

    def visit_python_decorated(self, dec: PythonDecorated):
        decorated = self.visit(dec.decorated)
        decorated.decorators = [self.visit(d) for d in dec.decorators]
        if (isinstance(decorated, ClassDefinitionExpr) and
                any(isinstance(d, PythonCall) and isinstance(func := d.func, PythonVariable) and
                    func.name in DATA_RECORD_QN_GROUP
                    or isinstance(d, PythonVariable) and d.name in DATA_RECORD_QN_GROUP
                    for d in dec.decorators)):
            defs = decorated.get_defs()
            decorated = decorated.as_dataclass(
                [self.convert_field(d) for d in defs if isinstance(d, (MathTypeDeclaration, InitializedVariable))],
                removed_defs=[d for d in defs if isinstance(d, (MathTypeDeclaration, InitializedVariable))])
        return decorated

    def visit_python_keyword_arg(self, kwarg: PythonKeywordArg):
        return NamedArgument(kwarg.name, self.visit(kwarg.value))

    def visit_python_ifte(self, ifte: PythonIFTE):
        return IFTE(self.visit(ifte.cond), self.visit(ifte.pos), self.visit(ifte.neg))


def primary_key_from_python(init: Term):
    # TODO: support direct use of field: field(metadata=dict(primary_key=...)), as well as abbreviations
    return (isinstance(init, FunctionApplication) and
            init.function == METADATA_QN and (args := init.args) and
            any(isinstance(arg, NamedArgument) and arg.name == 'primary_key' and arg.expr == TRUE_AS_QUANTITY
                for arg in args))
