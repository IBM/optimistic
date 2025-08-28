from __future__ import annotations

import sys
from builtins import super
from collections import defaultdict, OrderedDict
from itertools import product
from typing import Optional, Union, MutableMapping, Tuple

from codegen.utils import visitor_for
from math_rep.constants import FOR_ALL_SYMBOL, ELEMENT_OF_SYMBOL, EXISTS_SYMBOL
from math_rep.dataflow import DataFlow, AbstractDFlowTable, AbstractDFlowBuilder
from math_rep.expr import MathVariable, Term, Attribute, Atom, Subscripted, \
    FunctionDefinitionExpr, ComprehensionContainer, FormalContent, Quantifier, \
    LogicalOperator, Comparison, DummyTerm, BodyExpr, FunctionApplication, MathModule, Aggregate, ClassDefinitionExpr, \
    Stream, TypeAlias, MathVariableArray, IndexedMathVariable, RangeExpr, Quantity, DomainDim, DefinedBy, \
    ApplicationSpecificInfo
from math_rep.expression_types import MType, M_ANY, WithMembers, MClassType, MFunctionType, type_intersection, \
    MStreamType, M_INT, M_BOOLEAN, MSetType, M_NUMBER, QualifiedName, to_c_identifier, M_NONE, M_BOTTOM, MArray
from math_rep.math_frame import MATH_FRAME_PATH
from math_rep.math_symbols import AND_QN, EQ_QN, ZIP_QN
from validator2solver.python.python_to_expr import METHOD_CALL_INDICATOR
from validator2solver.python.symbol_default_modules import BUILTIN_QN, UNIQUE_ASSIGNMENT_METHOD_QN, NEXT_QN
from validator2solver.python.symbol_table import PYTHON_BUILTIN_FRAME_NAME
from rewriting.rules import DEFAULT_EQUALITY_RULES, DEFAULT_SUBSTITUTION_RULES

SOLUTION_VAR_NAME = 'solution'

OPTIMISTIC_UTILS_PATH = ('utils', 'meta', 'optimistic_client', PYTHON_BUILTIN_FRAME_NAME)
PYTHON_MATH_PATH = ('math', PYTHON_BUILTIN_FRAME_NAME)

ELEMENT_OF_QN = QualifiedName(ELEMENT_OF_SYMBOL, lexical_path=MATH_FRAME_PATH)

DEBUG_STRING = '--debug-domain='
DEBUG_DOMAIN_OPTIONS = set(next((a for a in sys.argv if a.startswith(DEBUG_STRING)), DEBUG_STRING)[len(DEBUG_STRING):]
                           .split(','))


class DomainValue:
    pass


class InputValue(DomainValue):
    """
    A value that comes from the input of the optimization problem.  It can be:
        - The optimization-problem class itself (top level, no translation)
        - An input field of the optimization-problem class (a direct input of the optimization problem)
        - A (recursive) subfield of an input (can be translated to a container based on the input)

    Path is a sequence of strings, the first of which is the class name, and the rest are the attribute names.
    """

    def __init__(self, path: Tuple[str, ...]):
        self.path = path

    def with_attribute(self, attribute: str):
        return InputValue(self.path + (attribute,))

    def get_path(self):
        return self.path

    def __eq__(self, other):
        return type(self) == type(other) and self.path == other.path

    def __str__(self):
        return f'InputValue{self.path}'

    def __repr__(self):
        return f'InputValue{self.path}'


class RangeValue(DomainValue):
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop

    def get_value(self):
        return range(self.start, self.stop)

    def __eq__(self, other):
        return type(self) == type(other) and self.start == other.start and self.stop == other.stop

    def __str__(self):
        return f'RangeValue({self.start}, {self.stop})'


class DomainToTypeDataFlow(DataFlow):
    """
    Data-flow propagator that sets the type of a term `t` that has a domain `d` based on the type of `d`.

    N.B. The target of this object is a DomainInfo object, NOT a Term
    """

    def propagate(self, domain_table: 'DomainTable'):
        domain_type = self.source.appl_info.type
        if isinstance(domain_type, WithMembers):
            self.target.update_type(domain_type.element_type, domain_table)


class DomainInfo(ApplicationSpecificInfo):
    """
    Type and domain info for a MathVariable, including subexpressions (attributes and items).

    N.B. This class is NOT to be instantiated directly, use DomainTable.add_info() instead!
    """

    def __init__(self):
        self.type = M_ANY
        self.domain = None
        self.subexprs: MutableMapping[str, DomainInfo] = {}
        self.propagators = OrderedDict()
        self.propagator_additions = OrderedDict()
        self.deactivated = set()

    def get_info(self, path: Union[tuple, list]):
        info = self
        for element in path:
            info = self.subexprs.get(element)
            if info is None:
                return None
        return info

    def set_info(self, path: Union[tuple, list], new_info: 'DomainInfo'):
        info = self
        for element in path[:-1]:
            info = self.subexprs[element]
        info.subexprs[path[-1]] = new_info

    def get_type(self) -> MType:
        return self.type

    def update_type(self, new_type: MType, domain_table: 'DomainTable'):
        assert new_type is not None
        if self.type == new_type or new_type == M_ANY:
            return
        self.type = type_intersection(self.type, new_type)
        domain_table.add_to_agenda(self)

    def update_domain(self, new_domain: Term, domain_table: 'DomainTable'):
        if self.domain == new_domain or new_domain is None:
            return
        # TODO: implement intersection of domains (perhaps keep set of Terms, which need to be hashable)
        # meanwhile preventing replacement
        if self.domain is not None and self.domain != M_NONE:
            return
        self.domain = new_domain
        # domain_table.add_info(new_domain)
        DomainToTypeDataFlow(new_domain, self, domain_table)
        # domain_table.add_to_agenda(self)  # Done by data-flow above

    def update_value(self, new_value: DomainValue, domain_table: 'DomainTable'):
        if new_value is None:
            return
        try:
            current = self.value
            if current != new_value:
                # TODO: annotate values with their sources, either allow multiple or require a domain declaration
                print(f'WARNING: Attempt to change value from {current} to {new_value}')
                # raise Exception(f'Attempt to change value from {current} to {new_value}')
        except AttributeError:
            self.value = new_value
            self.propagate_value(domain_table)
            domain_table.add_to_agenda(self)

    def is_dvar(self):
        return hasattr(self, '_is_dvar')

    def set_dvar(self, domain_table: 'DomainTable'):
        if self.is_dvar():
            return
        self._is_dvar = True
        domain_table.add_to_agenda(self)
        if 'dvar' in DEBUG_DOMAIN_OPTIONS:
            print(f'DEBUG-DOMAIN: DVAR set on {self.last_term}')

    def propagate_value(self, domain_table):
        try:
            self.value
        except AttributeError:
            return
        for attr, info in self.subexprs.items():
            # TODO: add support for items if need to allow mappings or arrays in input dataclasses
            if not attr.startswith('['):
                info.update_value(self.value.with_attribute(attr), domain_table)

    def describe(self, link: str, indent=''):
        new_indent = indent + '  '
        domain = self.domain
        if isinstance(domain, DummyTerm):
            try:
                value = domain.appl_info.value
            except AttributeError:
                pass
            else:
                domain = f'DUMMY#{domain.serial}, value={value}'
        top = (f'{indent}DomainInfo for {link:}\n'
               f'{new_indent}* Type:   {self.type}\n'
               f'{new_indent}* Domain: {domain}')
        try:
            value = self.value
            top += f'\n{new_indent}* Value:  {value}'
        except AttributeError:
            pass
        if self.is_dvar():
            top += '\n' + f'{new_indent}* Decision variable'
        if subexprs := self.subexprs:
            subs = '\n'.join(s.describe(p, indent=new_indent) for p, s in subexprs.items())
            top += '\n' + subs
        return top


def term_is_dvar(term: Term):
    try:
        return term.appl_info.is_dvar()
    except AttributeError:
        return False


def term_type(term: Term):
    try:
        return term.appl_info.type
    except AttributeError:
        return M_ANY


@visitor_for(FormalContent, add_call_to='add_domain_info', collect_results=False)
class AddDomainInfoSuper:
    """
    Add domain_info objects to all subterms
    """

    def __init__(self, domain_table):
        self.domain_table = domain_table

    def add_domain_info(self, obj):
        self.domain_table.add_info(obj)


class AddDomainInfo(AddDomainInfoSuper):
    def visit_math_variable_array(self, arr: MathVariableArray):
        # redundant, since MVA has no term components; instead just add for this
        # super().visit_math_variable_array(arr)
        self.domain_table.add_info(arr)
        for dim in arr.dims:
            if isinstance(dim, Term):
                self.add_domain_info(dim)


@visitor_for(FormalContent, add_call_to='add_dvar_propagator', collect_results=False)
class ExtendedExprAbstractVisitor:
    def __init__(self, domain_table):
        self.domain_table = domain_table

    def add_dvar_propagator(self, obj: Term):
        if isinstance(obj, SKIP_DVAR):
            return
        for arg in obj.arguments():
            if not isinstance(arg, SKIP_DVAR):
                DecisionDataFlow(arg, obj, self.domain_table)


class DomainBuilder(ExtendedExprAbstractVisitor, AbstractDFlowBuilder):
    def __init__(self, domain_table: DomainTable, exists_is_dvar=False):
        super().__init__(domain_table)
        self.module = None
        self.containing_function: Optional[FunctionDefinitionExpr] = None
        self.in_optimization_problem_class = False
        self.exists_is_dvar = exists_is_dvar

    def visit_math_module(self, module: MathModule):
        if already_built(module):
            return
        if self.module is None:
            self.module = module
        super().visit_math_module(module)
        for call in module.method_calls:
            call: FunctionApplication
            MethodCallDataFlow(call.method_target, call, self.domain_table, self.module)

    def visit_math_variable(self, var: MathVariable):
        if already_built(var):
            return
        super().visit_math_variable(var)
        var.appl_info.update_type(var.name.type, self.domain_table)

    def visit_indexed_math_variable(self, ivar: IndexedMathVariable):
        if already_built(ivar):
            return
        super().visit_indexed_math_variable(ivar)
        if ivar.is_output():
            ivar.appl_info.set_dvar(self.domain_table)
        # Don't bother propagating dvar for a constant index
        if len(ivar.indexes) == 1 and not isinstance(ivar.indexes[0], Quantity):
            IndexedVarDomainDataFlow(ivar, ivar, self.domain_table)
            for i, index in enumerate(ivar.indexes):
                IndexedVarDomainDataFlow(index, ivar, self.domain_table)
                # otype = ivar.owner.domain_info.type
                # if not isinstance(otype, MArray) or isinstance(otype.dims[i], DomainDim):
                #     ArrayTypeDataFlow(index, ivar, i, self.domain_table)
            if isinstance(ivar.owner.dims[0], RangeExpr):
                for i in range(ivar.owner.dims[0].start, ivar.owner.dims[0].stop):
                    InverseIndexedVarDomainDataFlow(
                        self.domain_table.ensure_info(IndexedMathVariable(ivar.owner, Quantity(i))), ivar,
                        self.domain_table)
        ivar.appl_info.update_type(ivar.type, self.domain_table)

    def visit_math_variable_array(self, arr: MathVariableArray):
        if already_built(arr):
            return
        super().visit_math_variable_array(arr)
        for dim in arr.dims:
            if isinstance(dim, Term):
                self.visit(dim)
        if arr.is_output():
            arr.appl_info.set_dvar(self.domain_table)
        for i, dim in enumerate(arr.dims):
            if isinstance(dim, DomainDim):
                DomainDimToArrayDataFlow(dim, arr, i, self.domain_table)

    def visit_attribute(self, attr: Attribute):
        if already_built(attr):
            return
        super().visit_attribute(attr)
        if not isinstance(attr.attribute, Atom):
            return
        if attr.attribute.lexical_path:
            return
        self.domain_table.add_info(attr, type=attr.type, parent=attr.container,
                                   link=to_c_identifier(attr.attribute.words), do_register=True)
        AttributeDataFlow(attr.container, attr, self.domain_table)
        if (containing_function := self.containing_function) and attr.attribute.words == ['solution']:
            SolutionVarDataFlow(attr.container, attr, self.domain_table.optimization_problem.name.name,
                                self.domain_table)

    def visit_subscripted(self, sub: Subscripted):
        if already_built(sub):
            return
        super().visit_subscripted(sub)
        # FIXME! deal separately with index and value
        self.domain_table.add_info(sub, type=sub.type, parent=sub.obj, link='[]', do_register=True)

    def visit_class_definition_expr(self, classdef: ClassDefinitionExpr):
        if already_built(classdef):
            return
        if classdef == self.domain_table.optimization_problem:
            self.in_optimization_problem_class = True
        super().visit_class_definition_expr(classdef)
        self.in_optimization_problem_class = False

    def visit_function_definition_expr(self, funcdef: FunctionDefinitionExpr):
        if already_built(funcdef):
            return
        containing_function = self.containing_function
        if self.in_optimization_problem_class:
            self.containing_function = funcdef
        super().visit_function_definition_expr(funcdef)
        self.containing_function = containing_function
        params = funcdef.typed_parameters
        if target := funcdef.method_target:
            params = [funcdef.method_target] + params
        funcname_mvar = self.domain_table.new_math_variable(funcdef.name)
        self.domain_table.add_info(funcname_mvar, type=MFunctionType([p.type for p in params], funcdef.return_type))
        for param in params:
            param_mvar = self.domain_table.new_math_variable(
                QualifiedName(param.name, lexical_path=funcdef.lexical_path, type=param.type))
            self.domain_table.add_info(param_mvar, type=param.type)
        # set value for optimization problem class self variables
        if (self.domain_table.optimization_problem and target and isinstance(ttype := target.type, MClassType) and
                (class_name := ttype.class_name) == self.domain_table.optimization_problem.name):
            target_mvar = self.domain_table.new_math_variable(
                QualifiedName(target.name, lexical_path=funcdef.lexical_path, type=target.type))
            target_mvar.appl_info.update_value(InputValue((class_name.name,)), self.domain_table)
        retval = get_function_returned_value(funcdef)
        ReturnedValueDataFlow(retval, funcname_mvar, self.domain_table)
        # N.B. this is not really the value of the function, it is the return value!
        dummy = self.domain_table.create_dummy(('function-result', funcdef.name.name))
        ValueCopierDataFlow(retval, dummy, self.domain_table)
        retval.appl_info.update_domain(dummy, self.domain_table)
        DecisionDataFlow(funcdef, self.domain_table.new_math_variable(funcdef.name), self.domain_table)

    def visit_function_application(self, appl: FunctionApplication):
        if already_built(appl):
            return
        super().visit_function_application(appl)
        DecisionDataFlow(self.domain_table.new_math_variable(appl.function), appl, self.domain_table)
        func_var = self.domain_table.new_math_variable(appl.function)
        FunctionDefToApplicationDataFlow(func_var, appl, self.domain_table)
        dummy = self.domain_table.create_dummy(('function-domain', appl.function.name))
        ValueCopierDataFlow(appl, dummy, self.domain_table)
        func_var.appl_info.update_domain(dummy, self.domain_table)
        function_def = self.module.all_functions.get(appl.function) if self.module else None
        if function_def is None:
            pass
            # if appl.function.lexical_path not in (MATH_FRAME_PATH, (METHOD_CALL_INDICATOR,)):
            #     # FIXME! should be error?
            #     print(f'Function definition not found: {appl.function.describe(full_path=True)}')
        else:
            ValueCopierDataFlow(get_function_returned_value(function_def), appl, self.domain_table)
        if (containing_function := self.containing_function) and all(dec is not appl
                                                                     for dec in containing_function.decorators):
            if appl.function.lexical_path == (METHOD_CALL_INDICATOR,):
                self.domain_table.method_calls[appl.function].extend(
                    [appl, self.domain_table.new_math_variable(containing_function.name)])
            elif appl.function in (NEXT_QN,):
                AggregateResultDataFlow(appl.args[0], appl, self.domain_table)
        for arg in appl.args:
            DvarFlow(arg, appl, self.domain_table)

    def visit_comprehension_container(self, compr: ComprehensionContainer):
        if already_built(compr):
            return
        super().visit_comprehension_container(compr)
        vars = compr.vars
        container = compr.container
        if isinstance(container, FunctionApplication) and container.function == ZIP_QN:
            # FIXME! use MTupleType for zip, propagate from components to zip, support destructuring
            # special case for v1, .., vn in zip(c1, ..., cn)
            if len(vars) != len(container.args):
                raise Exception(f'Wrong number {len(vars)} of variables for zip: {container}')
            for var, arg in zip(vars, container.args):
                ComprehensionContainerDataFlow(arg, self.domain_table.new_math_variable(var), self.domain_table)
            return
        if len(vars) != 1:
            # FIXME! need to support destructuring, at least for dict.items()
            return
        var = vars[0]
        math_var = self.domain_table.new_math_variable(var)
        ComprehensionContainerDataFlow(container, math_var, self.domain_table)

    def visit_stream(self, stream: Stream):
        if already_built(stream):
            return
        super().visit_stream(stream)
        AggregateTypeDataFlow(stream.term, stream, self.domain_table)

    def visit_aggregate(self, aggr: Aggregate):
        if already_built(aggr):
            return
        super().visit_aggregate(aggr)
        ComprehensionDataFlow(aggr.term, aggr, self.domain_table)
        # TODO: add AggregateResultDataFlow for appropriate operators (e.g., sum)

    def visit_quantifier(self, quant: Quantifier):
        if already_built(quant):
            return
        super().visit_quantifier(quant)
        if self.exists_is_dvar and quant.kind == EXISTS_SYMBOL:
            for var in quant.container.vars:
                self.domain_table.new_math_variable(var).appl_info.set_dvar(self.domain_table)
        # TODO: add content

    def visit_comparison(self, comp: Comparison):
        if already_built(comp):
            return
        super().visit_comparison(comp)
        if comp.op != EQ_QN:
            return
        EqualityDomainAndValueDataFlow(comp.lhs, comp.rhs, self.domain_table)
        EqualityDomainAndValueDataFlow(comp.rhs, comp.lhs, self.domain_table)
        if hasattr(comp, 'is_definition'):
            DvarFlow(comp.rhs, comp.lhs, self.domain_table)

    def visit_range_expr(self, r: RangeExpr):
        if already_built(r):
            return
        super().visit_range_expr(r)
        r.appl_info.update_value(RangeValue(r.start, r.stop), self.domain_table)

    def visit_domain_dim(self, dd: DomainDim):
        if already_built(dd):
            return
        super().visit_domain_dim(dd)
        DomainDimDataFlow(dd.domain_of, dd, self.domain_table)

    def visit_defined_by(self, db: DefinedBy):
        if already_built(db):
            return
        for inp, outp in product(db.inputs, db.outputs):
            DvarFlow(inp, outp, self.domain_table)


class DomainTable(AbstractDFlowTable):
    def __init__(self, structs=None, optimization_problem: ClassDefinitionExpr = None, exists_is_dvar=False,
                 domain_builder_class=DomainBuilder, domain_adder_class=AddDomainInfo):
        # Remove old objects from interned classes
        super().__init__(domain_builder_class(self, exists_is_dvar=exists_is_dvar))
        self.var_table: MutableMapping[QualifiedName, DomainInfo] = {}  # WeakValueDictionary()
        self.structs = {} if structs is None else structs
        self.optimization_problem = optimization_problem
        self.domain_adder = domain_adder_class(self)
        self.method_calls = defaultdict(list)
        add_builtin_domains(self)
        self.dummies = {}
        # DEBUG
        self.dummy_counter_debug = 0

    def build(self, term: FormalContent):
        if term.appl_info is None:
            self.domain_adder.visit(term)
        super().build(term)
        return term

    def add_solution_dependences(self):
        for func in SOLUTION_DEPENDENT_FUNCTIONS:
            self.new_math_variable(func).appl_info.set_dvar(self)

    def add_info(self, term: Term, type: MType = M_ANY, domain: Optional[Term] = None,
                 parent: Optional[Term] = None, link: Optional[str] = None, do_register=False) -> DomainInfo:
        info = term.appl_info
        if info is None:
            if isinstance(term, IndexedMathVariable) and len(term.indexes) == 1 and isinstance(term.indexes[0],
                                                                                               Quantity):
                parent = term.owner
                link = f'[{term.indexes[0].value}'
                do_register = True
            if parent is not None:
                parent_info = parent.appl_info
                info = parent_info.get_info([link])
            else:
                info = None
            if not info:
                if isinstance(term, (MathVariable, MathVariableArray)):
                    term_var = term.name
                    info = self.var_table.get(term_var)
                    if info is None:
                        info = DomainInfo()
                        self.var_table[term_var] = info
                else:
                    info = DomainInfo()
            if hasattr(term, 'type') and (ttype := term.type) is not None and ttype != M_ANY:
                info.update_type(ttype, self)
        if DEBUG_DOMAIN_OPTIONS:
            info.last_term = term
        if type != M_ANY:
            info.update_type(type, self)
        if domain is not None:
            info.update_domain(domain, self)
        term.appl_info = info
        if do_register:
            self.register_info(info, parent=parent, link=link)
        return info

    def register_info(self, info: DomainInfo, parent: Optional[Term] = None, link: Optional[str] = None) -> DomainInfo:
        if parent is not None:
            parent_info = parent.appl_info
            parent_info.subexprs[link] = info
            parent_info.propagate_value(self)

    def ensure_info(self, term: Term, parent: Optional[Term] = None, link: Optional[str] = None):
        self.build(term)
        info = self.add_info(term, parent=parent, link=link, do_register=True)
        return term

    def get_info(self, var: QualifiedName, path: Union[tuple, list] = ()):
        return self.var_table[var].get_info(path)

    def add_to_agenda(self, info: DomainInfo):
        """
        Add a DomainInfo object into the agenda, for future propagation of information.
        """
        self.agenda[id(info)] = info

    def new_math_variable(self, name: QualifiedName) -> MathVariable:
        result = MathVariable(name)
        self.add_info(result)
        return result

    def propagate(self):
        while True:
            try:
                _, info = self.agenda.popitem(last=False)
            except KeyError:
                return
            info.propagators.update(info.propagator_additions)
            info.propagator_additions.clear()
            # remove deactivated propagators
            for p in info.deactivated:
                del info.propagators[p]
            info.deactivated = set()
            props = info.propagators.values()
            for df in props:
                df.propagate(self)

    def empty_agenda(self):
        return not self.agenda

    def create_dummy(self, role: Tuple[str, ...]):
        dummy = self.dummies.get(role)
        if dummy is not None:
            return dummy
        self.dummy_counter_debug += 1
        dummy = DummyTerm(role, self.dummy_counter_debug)
        self.dummies[role] = dummy
        self.add_info(dummy)
        return dummy

    def describe(self):
        var_table = self.var_table
        # DEBUG
        debug = '\n===========\n'.join(f'{dummy.appl_info.describe(dummy.describe())}'
                                       for dummy in self.dummies.values())
        if debug:
            debug = '\n' + debug
        return '\n===========\n'.join(var_table[var].describe(str(var))
                                      for var in sorted(var_table.keys())) + debug


# FIXME: deal with functions such as next, which propagate the type of their argument into the result type
# FIXME! Move this information to the Variable definition (in the frame), copy to MathVariable
# FIXME! add more refined types (int+, etc.)
BUILTIN_DOMAINS = [(QualifiedName('count', lexical_path=OPTIMISTIC_UTILS_PATH),
                    MFunctionType((MStreamType(M_ANY),), M_INT)),
                   (BUILTIN_QN.get('all'), MFunctionType((MStreamType(M_ANY),), M_BOOLEAN)),
                   (QualifiedName('ceil', lexical_path=PYTHON_MATH_PATH), MFunctionType((M_NUMBER,), M_INT))]

# FIXME! Move to Variable then to MathVariable
# FIXME!! this is called through self of the inheriting class, need to replace by QN of actual definition
SOLUTION_DEPENDENT_FUNCTIONS = {UNIQUE_ASSIGNMENT_METHOD_QN}


def add_builtin_domains(domain_table: DomainTable):
    for term, ttype in BUILTIN_DOMAINS:
        domain_table.add_info(MathVariable(term), type=ttype)


def get_element_struct(term: Term, domain_table: DomainTable):
    ttype = term.appl_info.type
    if not isinstance(ttype, MClassType):
        return None
    return domain_table.structs.get(ttype.class_name.name)


class AttributeDataFlow(DataFlow):
    """
    Data-flow propagator that sets the type of an Attribute (`c.a`) based on the type of its container (`c`)
    """

    def __init__(self, source: Term, target: Attribute, domain_table: DomainTable):
        assert source == target.container
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: DomainTable):
        container = self.source
        struct = get_element_struct(container, domain_table)
        if struct is None:
            return
        attr = self.target
        attr_name = attr.attribute
        assert isinstance(attr_name, Atom)
        assert attr_name.lexical_path == ()
        link_name = to_c_identifier(attr_name.words)
        field = struct.fields.get(link_name)
        if field is None:
            return
        attr_info = attr.appl_info
        attr_info.update_type(field.type, domain_table)
        if attr_info.domain is not None:
            return
        # TODO: use id(container) instead?
        dummy = domain_table.create_dummy(('link-domain', link_name, container.describe()))
        SetupAttributeValueDataFlow(container, dummy, domain_table, link_name)
        attr_info.update_domain(dummy, domain_table)


class SetupAttributeValueDataFlow(DataFlow):
    """
    Data-flow propagator that installs an AttributeValueDataFlow from the source (a container of an attribute) to the
    target (a dummy term to carry the domain of the attribute)
    """

    def __init__(self, source: Term, target: DummyTerm, domain_table: DomainTable, attr_name):
        super().__init__(source, target, domain_table)
        self.attr_name = attr_name

    def propagate(self, domain_table: 'DomainTable'):
        if (source_domain := self.source.appl_info.domain) is not None:
            AttributeValueDataFlow(source_domain, self.target, domain_table, self.attr_name)


class AttributeValueDataFlow(DataFlow):
    """
    Dafa-flow propagator to be used by `AttributeDataFlow` in order to set the value of the dummy node according to
    the value of the container.
    """

    def __init__(self, source: Term, target: Term, domain_table: DomainTable, attr_name):
        super().__init__(source, target, domain_table)
        self.attr_name = attr_name

    def propagate(self, domain_table: DomainTable):
        source_info = self.source.appl_info
        try:
            source_value = source_info.value
        except AttributeError:
            return
        self.target.appl_info.update_value(InputValue(source_value.get_path() + (self.attr_name,)), domain_table)


class ComprehensionContainerDataFlow(DataFlow):
    """
    Data-flow propagator that sets the type and domain of a comprehension variable based on the type of the container;
    for example, propagates from `c` to `x` in `... for x in c`
    """

    def __init__(self, source: Term, target: MathVariable, domain_table: DomainTable):
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: DomainTable):
        container = self.source
        container_info = container.appl_info
        var: MathVariable = self.target
        var_info = domain_table.get_info(var.name)
        var_info.update_domain(container, domain_table)
        container_type = container_info.type
        if isinstance(container_type, WithMembers):
            var_info.update_type(container_type.element_type, domain_table)


def same_type_as(t):
    return t


def set_type_of(t):
    return MSetType(t)


TRANSFER_AGGREGATE_TYPE = {'+': same_type_as, 'SET': set_type_of}


class ComprehensionDataFlow(DataFlow):
    """
    Data-flow propagator that sets the type of a comprehension expression based on the type of the term;
    for example, propagates from `t` to the whole expression in `{t for x in c}`.  The value of the expression
    is set based on the domain of `t`.
    """

    def __init__(self, source: Term, target: Term, domain_table: DomainTable):
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: DomainTable):
        term = self.source
        term_info = term.appl_info
        target = self.target
        target_info = target.appl_info
        target_info.update_domain(term, domain_table)
        term_type = term_info.type
        # TODO: currently only have set types, may need others in future
        target_info.update_type(TRANSFER_AGGREGATE_TYPE[target.op](term_type), domain_table)
        # FIXME: only set value if there aren't any conditions
        try:
            term_value = term_info.domain.appl_info.value
        except AttributeError:
            pass
        else:
            target_info.update_value(term_value, domain_table)


class EqualityDomainAndValueDataFlow(DataFlow):
    """
    Data-flow propagator that sets the domain info of one argument of an equality from the other.

    This is a heuristic, not a logically-certain inference!
    """

    def __init__(self, source: Term, target: Term, domain_table: DomainTable, force=False,
                 prevent_type_propagation=False):
        super().__init__(source, target, domain_table)
        self.force = force
        self.prevent_type_propagation = prevent_type_propagation

    def propagate(self, domain_table: DomainTable):
        source_info = self.source.appl_info
        target_info = self.target.appl_info
        # Don't apply this heuristic if target already has a domain or value
        if not self.force and (target_info.type != M_ANY or target_info.domain is not None):
            # return
            pass
        if source_info.type == M_BOTTOM:
            # Don't apply this for dummy nodes
            return
        if not self.prevent_type_propagation:
            target_info.update_type(source_info.type, domain_table)
        target_info.update_domain(source_info.domain, domain_table)
        try:
            value = source_info.value
        except AttributeError:
            return
        target_info.update_value(value, domain_table)


def get_function_returned_value(funcdef):
    body = funcdef.body
    if isinstance(body, BodyExpr):
        body = body.value
    return body


class MethodCallDataFlow(DataFlow):
    """
    Data-flow propagator that sets the qualified name of a function call to the correct method body based on the type
    of the method target
    """

    def __init__(self, source: Term, target: FunctionApplication, domain_table: DomainTable, module: MathModule):
        super().__init__(source, target, domain_table)
        self.module = module

    def propagate(self, domain_table: DomainTable):
        mt_type = self.source.appl_info.type
        # FIXME: treat class methods specially
        # For class methods, the source could be a class rather than an object, use that as the type in that case
        if not isinstance(mt_type, MClassType):
            return
        mt_class = self.module.classes.get(mt_type.class_name)
        if mt_class is None:
            return
        method: FunctionApplication = self.target
        method_name = method.function.name
        if (method_qn := self.module.member_of_class(mt_type.class_name, method_name)) is None:
            return
        target_function = method.function
        full_name_mv = domain_table.new_math_variable(method_qn)
        functions = domain_table.method_calls.get(target_function)
        if functions:
            for function in functions:
                DecisionDataFlow(full_name_mv, function, domain_table)
            del domain_table.method_calls[target_function]
        method_call_mv = domain_table.new_math_variable(method.function)
        EqualityDomainAndValueDataFlow(method_call_mv, full_name_mv, domain_table)
        EqualityDomainAndValueDataFlow(full_name_mv, method_call_mv, domain_table)
        # replace method-call QN with correct QN
        method.function = method_qn
        if method_qn in (NEXT_QN,):
            AggregateResultDataFlow(method.args[0], full_name_mv, domain_table)


SKIP_DVAR = (BodyExpr, TypeAlias, MathModule)


def already_built(fc: FormalContent):
    """
    Return True if term has already been built.  Mark as built now.
    """
    result = hasattr(fc, '_built')
    fc._built = True
    return result


# noinspection PyAbstractClass


@visitor_for(FormalContent, no_recursion=True, collect_results=False)
class ExprVisitorNoRecursion:
    pass


class ConstraintTypeExtractor(ExprVisitorNoRecursion):
    """
    Extract type and domain information from constraints of an optimization-problem class
    """

    def __init__(self, domain_table: DomainTable):
        self.domain_table = domain_table

    def visit_function_definition_expr(self, funcdef: FunctionDefinitionExpr):
        # print(f'Visiting function {funcdef}')
        self.visit(funcdef.body)

    def visit_quantifier(self, quant: Quantifier):
        if quant.kind == FOR_ALL_SYMBOL:
            self.visit(quant.formula)

    def visit_logical_operator(self, lop: LogicalOperator):
        if lop.kind == AND_QN:
            for e in lop.elements:
                self.visit(e)

    def visit_comparison(self, comp: Comparison):
        # print(f'Visiting comparison {comp}')
        if comp.op == ELEMENT_OF_QN:
            # No need to use a data-flow object here since this doesn't depend on the type or domain of the target
            # self.domain_table.add_info(comp.lhs)
            comp.lhs.appl_info.update_domain(comp.rhs, self.domain_table)


class ReturnedValueDataFlow(DataFlow):
    """
    Data-flow propagator that sets the return type of a function from the value returned by the function
    """

    def __init__(self, source: Term, target: MathVariable, domain_table: DomainTable):
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: DomainTable):
        source_info = self.source.appl_info
        target_info = self.target.appl_info
        target_type = target_info.type
        if isinstance(target_type, MFunctionType):
            target_info.update_type(target_type.with_result_type(source_info.type), domain_table)
            target_info.update_domain(source_info.domain, domain_table)
            try:
                target_info.update_value(source_info.value, domain_table)
            except AttributeError:
                pass


class ValueCopierDataFlow(DataFlow):
    """
    Data-flow propagator that sets the value of a term from the value of an equal term
    """

    def __init__(self, source: Term, target: Term, domain_table: DomainTable):
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: DomainTable):
        source_info = self.source.appl_info
        try:
            source_value = source_info.value
        except AttributeError:
            return
        self.target.appl_info.update_value(source_value, domain_table)


class FunctionDefToApplicationDataFlow(DataFlow):
    """
    Data-flow propagator that sets the type of a function application based on the type of the function
    """

    def __init__(self, source: Term, target: FunctionApplication, domain_table: DomainTable):
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: DomainTable):
        source_info = self.source.appl_info
        target_info = self.target.appl_info
        source_type = source_info.type
        if isinstance(source_type, MFunctionType):
            target_info.update_type(source_type.result_type, domain_table)


class SolutionVarDataFlow(DataFlow):
    """
    Data-flow propagator that sets an attribute whose attribute-name is 'solution' to be a decision variable if
    the type of the container is the optimization class
    """

    def __init__(self, source: Term, target: Attribute, optimization_class, domain_table: DomainTable):
        super().__init__(source, target, domain_table)
        self.optimization_class = optimization_class

    def propagate(self, domain_table: DomainTable):
        container_type = self.source.appl_info.type
        if isinstance(container_type, MClassType) and container_type.class_name.name == self.optimization_class:
            self.target.appl_info.set_dvar(domain_table)


# TODO: unify with DvarFlow
class DecisionDataFlow(DataFlow):
    """
    Data-flow propagator that sets the is_dvar property of a term based on another term it uses
    """

    def __init__(self, source: Term, target: Union[Term, DomainInfo], domain_table: DomainTable):
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: DomainTable):
        if self.source.appl_info.is_dvar():
            self.target.appl_info.set_dvar(domain_table)
            self.deactivate()  # no point in doing more than once


class DvarFlow(DataFlow):
    """
    Data-flow propagator that sets the target term to be a decision var if the source term is one.

    Used to propagate dvar status from args to function calls, and from the rhs to the lhs of a defining expression.
    """

    def __init__(self, source: Term, target: MathVariable, domain_table: 'DomainTable'):
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: 'DomainTable'):
        if self.source.appl_info.is_dvar():
            self.target.appl_info.set_dvar(domain_table)
            self.deactivate()


# TODO: add reverse inference if necessary
class AggregateResultDataFlow(DataFlow):
    """
    Data-flow propagator that sets the type of an aggregate expression (such as sum, next) that returns an element
    of the same type as the term, from the type of the term
    """

    def __init__(self, source: Term, target: Term, domain_table: DomainTable):
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: DomainTable):
        if isinstance(source_type := self.source.appl_info.type, WithMembers):
            self.target.appl_info.update_type(source_type.element_type, domain_table)


class AggregateTypeDataFlow(DataFlow):
    """
    Data-flow propagator that sets the type of an aggregate collection operation from the type of the elements
    """

    def __init__(self, source: Term, target: Term, domain_table: DomainTable, container_type=MStreamType):
        self.container_type = container_type
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: DomainTable):
        if (source_type := self.source.appl_info.type) != M_ANY:
            self.target.appl_info.update_type(self.container_type(source_type), domain_table)


class IndexedVarDomainDataFlow(DataFlow):
    """
    Data-flow propagator that sets all instances of a generic IMV that is a dvar to dvars
    """

    def __init__(self, source_term: Term, target_var: IndexedMathVariable, domain_table: DomainTable):
        # NOTE: in this case, the targets will be determined dynamically based on the target_var's domain
        super().__init__(source_term, target_var, domain_table)

    def propagate(self, domain_table: 'DomainTable'):
        ivar = self.target
        if not ivar.appl_info.is_dvar():
            return
        index_domain = ivar.indexes[0].appl_info.domain
        if isinstance(index_domain, RangeExpr):
            for i in range(index_domain.start, index_domain.stop):
                instance = IndexedMathVariable(ivar.owner, Quantity(i))
                domain_table.build(instance)
                instance.appl_info.set_dvar(domain_table)
            self.deactivate()


class InverseIndexedVarDomainDataFlow(DataFlow):
    """
    Data-flow propagator that sets a generic IMV to a dvar if all concrete instances are dvars
    """

    def __init__(self, source_var: IndexedMathVariable, target_var: IndexedMathVariable, domain_table: DomainTable):
        super().__init__(source_var, target_var, domain_table)

    def propagate(self, domain_table: 'DomainTable'):
        ivar = self.target
        index_domain = ivar.indexes[0].appl_info.domain
        if isinstance(index_domain, RangeExpr) and all(
                domain_table.ensure_info(ivar.owner[i]).appl_info.is_dvar()
                for i in range(index_domain.start, index_domain.stop)):
            ivar.appl_info.set_dvar(domain_table)
            self.deactivate()


class IndexedVarTypeDataFlow(DataFlow):
    """
    Data-flow propagator that sets the type of an IndexedMathVariable based on the type of its owner

    **Not used, doesn't seem necessary**
    """

    def __init__(self, source: MathVariableArray, target: IndexedMathVariable, domain_table: DomainTable):
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: DomainTable):
        source_type = self.source.appl_info.type
        if isinstance(source_type, MArray):
            self.target.appl_info.update_type(source_type.element_type)


class DomainDimDataFlow(DataFlow):
    """
    Data flow propagator that sets the value of a DomainDim based on the value of the domain of its domain_of
    field.
    """

    def __init__(self, source: Term, target: DomainDim, domain_table: 'DomainTable'):
        super().__init__(source, target, domain_table)

    def propagate(self, domain_table: 'DomainTable'):
        # TODO: this assumes that the value is part of the initialization of the domain; if this is not the case,
        # TODO: add another propagator for the value
        source_domain = self.source.appl_info.domain
        if not source_domain:
            return
        try:
            value = source_domain.appl_info.value
        except AttributeError:
            return
        self.target.appl_info.update_value(value, domain_table)


class DomainDimToArrayDataFlow(DataFlow):
    """
    Data-flow propagator that sets the type of a MathVariableArray from the type of the value of its dimension if
    that is a range
    """

    def __init__(self, source: DomainDim, target: MathVariableArray, i: int, domain_table: DomainTable):
        super().__init__(source, target, domain_table)
        self.i = i

    def propagate(self, domain_table: DomainTable):
        try:
            value = self.source.appl_info.value
        except AttributeError:
            return
        vtype = self.target.appl_info.type
        if not isinstance(vtype, MArray):
            return
        if isinstance(value, RangeValue):
            self.target.appl_info.update_type(vtype.with_dim(self.i, value.get_value()), domain_table)


# N.B. these are NOT heuristic
DEFAULT_EQUALITY_RULES.append(EqualityDomainAndValueDataFlow)
DEFAULT_SUBSTITUTION_RULES.extend((EqualityDomainAndValueDataFlow, DecisionDataFlow))

# class ArrayTypeDataFlow(DataFlow):
#     """
#     Data flow propagator that sets the dimensions of the type of an IndexedMathVariable according to the domains of the
#     indexes.
#     """
#
#     def __init__(self, source: Term, target: IndexedMathVariable, i: int, domain_table: DomainTable):
#         super().__init__(source, target, domain_table)
#         self.i = i
#
#     def propagate(self, domain_table: DomainTable):
#         index_domain = self.source.domain_info.domain
#         if not index_domain:
#             return
#         try:
#             value = index_domain.domain_info.value
#         except AttributeError:
#             return
#         vtype = self.target.owner.domain_info.type
#         if not isinstance(vtype, MArray):
#             return
#         self.target.owner.update_type(vtype.with_dim(self.i, value), domain_table)
