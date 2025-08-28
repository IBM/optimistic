import importlib
from abc import ABC, abstractmethod
from collections import defaultdict
from itertools import chain, dropwhile
from operator import itemgetter
from typing import Sequence, Tuple, Optional, Generator, Mapping

import inflect
from inflection import pluralize, underscore, camelize, singularize

from codegen.abstract_rep import PLUS_OPERATOR, TIMES_OPERATOR
from opl_repr.opl_frame_constants import OPL_USER_FRAME_NAME, PARAMETER_FRAME_NAME
from validator2solver.codegen.opl.opl_generator import OplVisitor
from validator2solver.optimization_analyzer import OptimizationProblemAnalyzer
from codegen.parameters import ParameterDescriptor
from codegen.utils import uniqueize_name
from math_rep.constants import FOR_ALL_SYMBOL
from validator2solver.domain_analysis import DomainInfo
from math_rep.expr import FunctionDefinitionExpr, BodyExpr, Comparison, MathVariable, FunctionApplication, \
    Quantifier, ComprehensionContainer, Quantity, Term, Aggregate
from math_rep.expression_types import MSetType, MClassType, MType, M_BOOLEAN, WithMembers, QualifiedName, M_INT, \
    MFunctionType
from validator2solver.python.python_to_expr import METHOD_CALL_INDICATOR
from validator2solver.python.symbol_default_modules import UNIQUE_ASSIGNMENT_CLASS_QN
from validator2solver.python.symbol_table import FUNCTION_FRAME_PREFIX
from validator2solver.optimistic_rules import EliminateSelfVariable, CountToSum, NotToEqZero, \
    BooleanToIntEquationInLogicalExpression, QuantifiedBooleanToIntEquation, IfToImplications, \
    EliminateNegationOfComparison, LiftLeftImplicationOverComparison, LiftRightImplicationOverComparison, \
    LiftRightLogicalOperatorOverComparison, LiftLeftLogicalOperatorOverComparison, \
    LiftImplicationOverFunctionApplication, LiftLogicalOperatorOverFunctionApplication, ReplaceStrictInequality, \
    EquatedCeil, TwoEquatedUniqueAssignments, MoveSumConditionToTerm, EquatedUniqueAssignment
from rewriting.rules import OrderedRuleSets, RuleSet, exhaustively_apply_rules


def get_element_type(collection_type, no_exception=False):
    if not isinstance(collection_type, WithMembers):
        if no_exception:
            return True
        raise Exception(f'Solution of type {collection_type} not yet supported')
    return collection_type.element_type


class OplCoder(ABC):
    """
    A coder that generates an OPL reference to a variable
    """

    @abstractmethod
    def reference(self, var: 'OplVariable', *args: str):
        raise NotImplementedError()

    @abstractmethod
    def domain_reference(self, var: 'OplVariable'):
        raise NotImplementedError()


class DefaultOplCoder(OplCoder):
    def reference(self, var: 'OplVariable', *args: str):
        args_text = ''.join(f'[{arg}]' for arg in args)
        return f'{var.name}{args_text}'

    def domain_reference(self, var: 'OplVariable'):
        return var.name


DEFAULT_OPL_CODER = DefaultOplCoder()


class CodeOplVarWithStructParameter(OplCoder):
    def __init__(self, domain: Optional[str] = None):
        self.domain = domain

    def reference(self, var: 'OplVariable', *args: str):
        return f'{var.name}[<{", ".join(args)}>]'

    def domain_reference(self, var: 'OplVariable'):
        return self.domain or var.name


class OplVariable:
    def __init__(self, name: str, vtype: MType, subscripts: Sequence[str], is_dvar: bool,
                 role: tuple, opl_value: Optional[str] = None, parm_names: Optional[Sequence[str]] = None,
                 opl_coder: OplCoder = DEFAULT_OPL_CODER, fields_and_vars=None, doc_string=''):
        """
        :param name: OPL variable name
        :param vtype: type of variable
        :param subscripts: sequence of variables containing values for each subscript
        :param is_dvar: true iff this is a decision variable
        :param role: role of this variable, a tuple whose first element is the role name and following values
            are parameters
        :param opl_value: the initialization value for the variable (optional)
        :param parm_names: sequence of parameter names (required only if opl_value is provided)
        :param doc_string: documentation string for the variable (optional)

        Supported roles are: domain; input; struct; solution; legal-solution; method
        """
        self.name = name
        self.type = vtype
        self.subscripts = subscripts
        self.is_dvar = is_dvar
        self.representing = role
        self.opl_value = opl_value
        self.parm_names = parm_names
        self.fields_and_vars = fields_and_vars
        self.opl_coder = opl_coder
        self.doc_string = doc_string

    def to_opl(self, dir: Optional['OptimizationModelOplImplementer']) -> str:
        doc = f'// {doc_string}\n' if (doc_string := self.doc_string) else ''
        subs = (''.join(f'[{s}]' for s in self.subscripts) if not self.parm_names
                else ''.join(f'[{name} in {s}]' for name, s in zip(self.parm_names, self.subscripts)))
        value = f' = {v}' if (v := self.opl_value) else ''
        if dir is not None:
            type_str = vtype if (vtype := dir.actual_type(self.type).def_for_opl(self.name)
                                 ) is not None else f'*** E02: no type for {self.name} ***'
        else:
            type_str = self.type.def_for_opl(self.name)
        return f'{doc}{"dvar " if self.is_dvar else ""}{type_str}{subs}{value};'

    def opl_reference(self, *args: str):
        return self.opl_coder.reference(self, *args)

    def domain_reference(self):
        return self.opl_coder.domain_reference(self)


class VariableDirectory:
    """
    A directory of all OPL variables defined in a project, each with a corresponding source in the mathematical
    representation and a usage type
    """

    def __init__(self):
        self._variables_by_name = {}
        self._variables_by_role = {}

    def add_variable(self, var: OplVariable):
        """
        Add a variable to the directory.

        N.B. This method will destructively change the variable name to avoid conflicts!
        """
        unique_name = uniqueize_name(var.name, self._variables_by_name)
        var.name = unique_name
        self._variables_by_name[unique_name] = var
        self._variables_by_role[var.representing] = var

    def get_variable_by_name(self, name: str):
        return self._variables_by_name.get(name)

    def get_variable_by_role(self, role: tuple):
        return self._variables_by_role.get(role)

    def get_variable_names(self):
        return self._variables_by_name.keys()

    def get_variable_roles(self):
        return self._variables_by_role.keys()

    def all_roles_of_kind(self, kind: str):
        return (role for role in self._variables_by_role.keys() if role[0] == kind)

    def iter_with_role(self):
        return self._variables_by_role.items()


IMPLEMENTATION_ORDER = dict(struct=0, solution=1, input=2, method=3, other=1000)


def opl_user_var(name):
    return QualifiedName(name, lexical_path=(OPL_USER_FRAME_NAME,))


# FIXME!!!! remove dependence on 'activity' and 'resource', unique assignments
class OptimizationModelOplImplementer:
    full_line_comment = '//'

    # TODO: add variables for auxiliary functions, determine which are dvars
    # TODO: infer solution_to_inputs mapping from types when possible (nice to have)
    def __init__(self, analyzer: OptimizationProblemAnalyzer, use_type_heuristic=True, print_intermediate=False,
                 use_legal_solution_var=False, epsilon=1e-10):
        """
        :param analyzer: OptimizationModel from which to generate the OPL code
        :param use_type_heuristic: True iff assuming that a unique column of a certain type contains all elements
            of that type
        :param use_legal_solution_var: True to use a special variable for legal solutions; only needed when there are
            constraints that can be implemented without using decision variables, and this advanced features isn't
            supported yet
        """
        self.use_legal_solution_var = use_legal_solution_var
        self.print_intermediate = print_intermediate
        self.analyzer = analyzer
        self.epsilon = epsilon
        self.element_type = get_element_type(self.analyzer._solution_class)
        self.solution_struct = self.analyzer._structs[self.element_type.class_name.name]
        etypes = [etype for f in analyzer._inputs if (etype := get_element_type(f.type)) is not None]
        etypes.sort()
        dup_types = {e1 for e1, e2 in zip(etypes, etypes[1:]) if e1 == e2}
        self.variables = VariableDirectory()
        self.inflect_engine = inflect.engine()
        if use_type_heuristic:
            self.type_to_var = self.create_type_to_var_mapping()
        else:
            self.type_to_var = {etype: f.name for f in analyzer._inputs
                                if (etype := get_element_type(f.type)) is not None
                                and etype not in dup_types}
        self.inputs_defined = False
        self.variables_defined = False
        self.opl_generator = None
        # FIXME!! self.solution_var_name() may be changed by OplVariable; need to determine this earlier
        solution_var_name = QualifiedName(self.solution_var_name(), lexical_path=())
        self.analyzer._domain_table.new_math_variable(solution_var_name).appl_info.set_dvar(
            self.analyzer._domain_table)
        supers = self.analyzer._top_level_expr.all_superclasses[self.analyzer._optimization_problem.name]
        self.has_unique_assignment = UNIQUE_ASSIGNMENT_CLASS_QN in supers
        if self.has_unique_assignment:
            activity_type = self.solution_struct.fields['activity'].type
            all_activities = (self.type_to_var.get(activity_type)
                              or f'*** E04: no domain for type {activity_type.for_opl()} ***')
        self.preparatory_rules = OrderedRuleSets(
            RuleSet(CountToSum(),
                    # GlobalizeCeil(self.om),
                    EliminateSelfVariable(self.analyzer._optimization_problem.name),
                    NotToEqZero(),
                    BooleanToIntEquationInLogicalExpression(),
                    QuantifiedBooleanToIntEquation(),
                    EquatedCeil(),
                    (TwoEquatedUniqueAssignments(solution_var_name, QualifiedName(all_activities, lexical_path=()))
                     if self.has_unique_assignment else None),
                    MoveSumConditionToTerm(),
                    # ReduceDomainTautologies()  # circular!
                    ),
            RuleSet(EquatedUniqueAssignment(solution_var_name)) if self.has_unique_assignment else None,
            # RuleSet(GlobalizeCeil(self.om)),
            RuleSet(IfToImplications()),
            RuleSet(EliminateNegationOfComparison()),
            RuleSet(LiftLeftImplicationOverComparison(),
                    LiftRightImplicationOverComparison(),
                    LiftRightLogicalOperatorOverComparison(),
                    LiftLeftLogicalOperatorOverComparison(),
                    LiftImplicationOverFunctionApplication(),
                    LiftLogicalOperatorOverFunctionApplication(),
                    ReplaceStrictInequality()
                    ))

    def create_type_to_var_mapping(self):
        inputs = self.analyzer._inputs
        result = {fc: input.name for input in inputs
                  if isinstance(ft := input.type, WithMembers) and isinstance(fc := ft.element_type, MClassType)}
        fields_of_inputs = defaultdict(list)
        solution_class_name = self.analyzer._optimization_problem.name.name
        for field in inputs:
            if isinstance(ft := field.type, WithMembers) and isinstance(fc := ft.element_type, MClassType):
                struct = self.analyzer._structs.get(fc.class_name.name)
                if struct:
                    for subfield in struct.fields.values():
                        if isinstance(st := subfield.type, MClassType):
                            fields_of_inputs[st].append(
                                (st, (solution_class_name, field.name, subfield.name), subfield.is_domain))
        for class_name, paths in fields_of_inputs.items():
            if class_name in result.keys():
                continue
            if len(paths) == 1:
                # only one path, apply heuristic
                vtype, path, *_ = paths[0]
                opl_value = self.value_to_opl(path)
            else:
                # more than one column; check 'domain' annotations
                domains = [p for p in paths if p[2]]
                if not domains:
                    # heuristic failed
                    continue
                if len(domains) == 1:
                    vtype, path, *_ = domains[0]
                    opl_value = self.value_to_opl(path)
                else:
                    # more than one domain, create union
                    vtype = domains[0][0]
                    domain_paths = [d[1] for d in domains]
                    opl_value = ' union '.join(self.value_to_opl(path) for path in domain_paths)
                    path = (solution_class_name, '*all*', domain_paths[0][-1])
            var = OplVariable(self.domain_var_name(path), MSetType(vtype), [], False, ('domain',) + path,
                              opl_value=opl_value)
            self.variables.add_variable(var)
            result[vtype] = var.name
        return result

    def struct_name(self, struct: str) -> str:
        return camelize(struct)

    @staticmethod
    def var_name(name, plural=False) -> str:
        n1 = underscore(name)
        return pluralize(n1) if plural else n1

    def solution_var_name(self) -> str:
        return self.var_name(self.solution_struct.name.name, plural=True)

    def legal_solution_var_name(self) -> str:
        return f'legal_{self.solution_var_name()}'

    def domain_variable_for_parameter(self, name: str, domain_info: DomainInfo):
        parm_domain = domain_info.domain
        try:
            value = parm_domain.appl_info.value
        except AttributeError:
            result = self.type_to_var.get(domain_info.type)
            if result:
                return result
            return f'*** E01: no value for parameter {name} ***'
        return self.domain_variable_for_value(value)

    def domain_variable_for_value(self, value):
        path = value.path
        role = ('domain',) + path
        existing = self.variables.get_variable_by_role(role)
        if existing:
            return existing.name
        var_name = self.domain_var_name(path)
        struct_name = path[0]
        for field_name in path[1:-1]:
            struct = self.analyzer._structs[struct_name]
            field = struct.fields[field_name]
            struct_name = field.type.element_type.class_name
        struct = self.analyzer._structs[struct_name.name]
        field = struct.fields[path[-1]]
        vtype = field.type
        variable = OplVariable(var_name, MSetType(vtype), [], False, role, opl_value=self.value_to_opl(value.path))
        self.variables.add_variable(variable)
        return variable.name

    def domain_var_name(self, path):
        return 'set_of_' + '_'.join(underscore(p)
                                    for p in chain((singularize(n.replace('*', ''))
                                                    for n in path[1:-1]), [pluralize(path[-1])]))

    def define_inputs(self):
        if self.inputs_defined:
            return
        self.inputs_defined = True
        for input in self.analyzer._inputs:
            self.variables.add_variable(OplVariable(input.name, input.type, [], False, ('input', input.name)))

    def define_variables(self):
        if self.variables_defined:
            return
        self.variables_defined = True
        for struct in self.analyzer._structs.values():
            if struct.name != self.analyzer._optimization_problem.name:
                self.variables.add_variable(OplVariable(struct.name.name, MClassType(struct.name), [], False,
                                                        ('struct', struct.name.name)))
        solution_mapping = {}
        solution_struct = self.analyzer._structs[self.element_type.class_name.name]
        for field in solution_struct.fields.keys():
            if (ftype := self.solution_struct.fields[field].type) in self.type_to_var:
                solution_mapping[field] = self.type_to_var[ftype]
            else:
                solution_mapping[field] = f'*** E03: No source found for solution field {field} ***'
                # raise Exception(f'No source specified for solution field {field}')
        fields_and_vars = [(field, solution_mapping[field]) for field in solution_struct.fields.keys()]
        if self.use_legal_solution_var:
            cond = ", ".join(f"{fn} in {input}" for fn, input in fields_and_vars)
            self.variables.add_variable(
                OplVariable(self.legal_solution_var_name(), self.analyzer._solution_class, [], False,
                            ('legal-solution',),
                            opl_value=f'{{<{", ".join(map(itemgetter(0), fields_and_vars))}> | {cond}}}'))
        # FIXME!!!! Only sets can be implemented as boolean variables, collections (= multisets) need a number
        # FIXME! support multiple solution vars (role must have an additional component, numeric?)
        coder = (CodeOplVarWithStructParameter(self.legal_solution_var_name()) if self.use_legal_solution_var
                 else DEFAULT_OPL_CODER)
        subscripts = ([self.legal_solution_var_name()] if self.use_legal_solution_var
                      else list(map(itemgetter(1), fields_and_vars)))
        self.variables.add_variable(
            OplVariable(self.solution_var_name(), M_BOOLEAN, subscripts, True,
                        ('solution',), opl_coder=coder, fields_and_vars=fields_and_vars, doc_string='Solution'))
        # TODO: following line collects inherited methods, but not builtin ones
        #        for method in self.om.top_level_expr.all_class_methods(self.om.optimization_problem.name):
        for method in self.analyzer._optimization_problem.get_defs():
            if not isinstance(method, FunctionDefinitionExpr):
                continue
            # don't create variables for constraints, these are translated to code
            if any(method is c for c in self.analyzer._constraints):
                continue
            if any(method is c[0] for c in self.analyzer._objectives):
                continue
            # ignore temporary method-call indicators
            if method.name.lexical_path == (METHOD_CALL_INDICATOR,):
                continue
            name = method.name.name
            doc = body.element_doc_string if isinstance(body := method.body, BodyExpr) else method.func_doc_string or ''
            doc = f'\n{self.full_line_comment} '.join(doc.strip().split('\n'))
            # FIXME!! need specific return types, subscripts
            # TODO: handle more precise types for dvars
            # FIXME: types of constraints are bool, of objectives float
            method_type = self.analyzer._domain_table.get_info(method.name).type
            if isinstance(method_type, MFunctionType):
                return_type = method_type.result_type
            else:
                raise Exception(f'Type of {name} is not a function type: {method_type}')
            dvar = self.qn_is_dvar(method.name)
            if dvar:
                value = None
                parm_names = None
            else:
                self.ensure_opl_coder()
                value = self.new_expr(method.get_value())
                parm_names = [p.name for p in method.typed_parameters]
            method_path = method.name.lexical_path
            parm_path = (f'{FUNCTION_FRAME_PREFIX}{method.name.name}', *method_path)
            self.variables.add_variable(
                OplVariable(self.var_name(name), return_type,
                            [self.domain_variable_for_parameter(p.name, self.parameter_info(parm_path, p))
                             for p in method.typed_parameters],
                            dvar, ('method', name), opl_value=value, parm_names=parm_names,
                            doc_string=doc))

    def parameter_info(self, parm_path: Sequence[str], parm: ParameterDescriptor) -> DomainInfo:
        p_qn = QualifiedName(parm.name, lexical_path=parm_path)
        return self.analyzer._domain_table.get_info(p_qn)

    def value_to_opl(self, path: Tuple[str, ...]):
        path_len = len(path)
        if path_len <= 1:
            raise Exception(f'Cannot compile class {path[0]} to OPL')
        if path_len == 2:
            # TODO: this assumes names are used as-is, may need to change in future (see OptimizationModel)
            return path[1]
        # FIXME: make sure all variables are distinct
        # new_var = f'_{singularize(value.path[1])}'
        name = singularize(path[1])
        # N.B. Assuming that this is a standalone expression, no need to uniqueize new_var
        new_var = underscore(self.inflect_engine.a(name)).replace(' ', '_')
        rest_path = '.'.join(path[2:])
        return f'{{{new_var}.{rest_path} | {new_var} in {path[1]}}}'

    def ensure_opl_coder(self):
        """
        Ensure that self.opl_coder is initialized.

        **WARNING:** Do not call this method before all variables have been defined!
        """
        vars_by_role = self.variables._variables_by_role  # {role: var.name for role, var in self.variables.iter_with_role()}
        if self.opl_generator:
            self.opl_generator.update_variables(vars_by_role)
        else:
            solution_qn = QualifiedName('solution', lexical_path=())
            opl_solution_qn = QualifiedName(self.variables.get_variable_by_role(('solution',)).name,
                                            lexical_path=(OPL_USER_FRAME_NAME,))
            self.opl_generator = OplVisitor(allow_undefined_vars=True,  # FIXME!!! should be False
                                            variables_by_role=vars_by_role,
                                            variable_translations={solution_qn: opl_solution_qn})

    def full_implementation_to_opl(self) -> str:
        self.define_inputs()
        self.define_variables()
        constraints = self.implement_constraints()
        objectives = self.implement_objectives()
        variables = self.implement_variables(('solution', 'method'))
        domain_variables = self.implement_variables(('domain',))
        inputs = self.implement_inputs()
        epsilon_def = 'float epsilon = 1e-10;\n\n' if 'epsilon' in self.opl_generator.named_constants else ''
        return (epsilon_def +
                '// data structures:\n' +
                '\n\n'.join(self.implement_struct(struct) for struct in self.analyzer._structs.values()
                            if struct.name != self.analyzer._optimization_problem.name) +
                '\n\n// Inputs:\n' +
                inputs +
                '\n\n// Domains:\n' +
                domain_variables +
                ('\n\n// Legal solutions:\n' +
                 self.implement_solution_vars()
                 if self.use_legal_solution_var else '') +
                '\n\n// Variables:\n' +
                variables +
                '\n\n// Objective:\n' +
                objectives +
                '\n\n// Constraints\n' +
                constraints)

    def actual_type(self, possible_alias, for_dvar=True):
        if possible_alias is None:
            return None
        if not for_dvar and possible_alias == M_BOOLEAN:
            # TODO: use int+ when available
            return M_INT
        if isinstance(possible_alias, MClassType):
            # TODO: use qualified names
            class_name = possible_alias.class_name.name
            actual = self.analyzer._aliases.get(class_name)
            if actual is not None:
                return actual
        elif isinstance(possible_alias, WithMembers):
            return possible_alias.with_element_type(self.actual_type(possible_alias.element_type, for_dvar=for_dvar))
        return possible_alias

    def implement_struct(self, struct, indent='  ') -> str:
        tuple_fields = '\n'.join(f'{indent}{"key " if field.is_primary_key else ""}'
                                 f'{self.actual_type(field.type, for_dvar=False).for_opl()} '
                                 f'{field.name};' for field in struct.fields.values())
        struct_name = self.variables.get_variable_by_role(("struct", struct.name.name)).name
        tuple_def = f'tuple {struct_name} {{\n{tuple_fields}\n}}'
        for_dvar = ''
        return tuple_def + for_dvar

    # TODO: The relationship between solution variables (e.g., Employee, Floor) and the fields of the solution class
    # (e.g., RoomAllocationProblem) need to be specified somehow.  In the RoomAllocationProblem3 example, this is
    # done in the legal_assignment method, which needs to be analyzed to extract this information.  Perhaps a more
    # structured way should be created.
    def implement_solution_vars(self) -> str:
        return self.variables.get_variable_by_role(('legal-solution',)).to_opl(self)

    def struct_of_input(self, input):
        """
        Return the OPL type of the struct that is the type of the given input variable
        """
        element_type = input.type.element_type
        if isinstance(element_type, MClassType):
            struct_var = self.variables.get_variable_by_role(("struct", element_type.class_name))
            if struct_var:
                return struct_var.name
            # FIXME! This should raise an exception, since the struct is not recognized
            # Workaround until imports handled correctly
        return element_type.for_opl()

    def get_solution_fields_names(self) -> Tuple[Sequence[str]]:
        solution_struct = self.analyzer._structs[self.element_type.class_name.name]
        return (field for field in solution_struct.fields.keys())

    def get_input_fields_types(self, input_name: str) -> Mapping[str, str]:
        return {field_name: type_str for input_tuple_name, field_name, type_str in self.typeit_of_inputs()
                if input_tuple_name == input_name}

    def typeit_of_inputs(self) -> Generator[Tuple[str, str, str], None, None]:
        return ((input.name, field.name, self.actual_type(field.type, for_dvar=False).for_opl())
                for input, struct in ((input, struct)
                                      for input in (self.variables.get_variable_by_role(role)
                                                    for role in self.variables.all_roles_of_kind('input'))
                                      for struct in self.analyzer._structs.values() if
                                      input.type.element_type.class_name.name == struct.name.name)

                for field in struct.fields.values())

    def class_of_inputs(self):
        # TODO: Need to complete implementation to run the actual python file with input and solution Instances
        self.define_inputs()

        def _get_class(opl_variable):
            this = opl_variable.type.element_type.class_name
            m = list(dropwhile(lambda s: s.startswith('*'), reversed(this.lexical_path)))
            print(f'DEFINE  {this.name} {".".join(m)}')
            module = importlib.import_module('.'.join(m))
            class_ = getattr(module, this.name)
            return class_

        for role in self.variables.all_roles_of_kind('input'):
            candidate = self.variables.get_variable_by_role(role)
            c = _get_class(candidate)

    def implement_inputs(self) -> str:
        return '\n'.join(f'{{{self.struct_of_input(input)}}} {input.name} = ...;'
                         for input in (self.variables.get_variable_by_role(role)
                                       for role in self.variables.all_roles_of_kind('input')))

    def implement_variables(self, roles) -> str:
        return '\n'.join(self.variables.get_variable_by_role(v).to_opl(self) for v in
                         chain.from_iterable(
                             self.variables.all_roles_of_kind(r) for r in roles))

    def new_expr(self, expr: Term, doc_string=None):
        self.analyzer._domain_table.build(expr)
        self.analyzer._domain_table.propagate()
        transformed = exhaustively_apply_rules(self.preparatory_rules, expr, self.analyzer._domain_table,
                                               print_intermediate=self.print_intermediate)
        # if transformed in (Quantity(1), Quantity(True)):
        #     return ''
        result = self.opl_generator.visit(transformed.to_code_rep()).value
        if doc_string:
            result = f'{self.full_line_comment} {doc_string}\n{self.opl_generator.indentation}{result}'
        return result

    @staticmethod
    def first_doc_line(doc: str):
        return next((line for line in doc.split('\n') if line.strip()), '')

    def implement_objectives(self) -> str:
        comments = []
        for n, objective in enumerate(self.analyzer._objectives):
            doc = objective[0].func_doc_string
            if not doc and isinstance(body := objective[0].body, BodyExpr):
                doc = body.element_doc_string
            if doc:
                doc = self.first_doc_line(doc)
            else:
                doc = 'N/A'
            comments.append(f'{n + 1}. {doc.strip()}')
        comment_str = '\n'.join(f'{self.full_line_comment} {doc}' for doc in comments)
        self.ensure_opl_coder()
        expression = self.new_expr(FunctionApplication(PLUS_OPERATOR,
                                                       [FunctionApplication(TIMES_OPERATOR,
                                                                            [Quantity(objective[1]),
                                                                             objective[0].get_value()])
                                                        for objective in self.analyzer._objectives]))
        return f'{comment_str}\nminimize {expression};'

    def convert_constraint(self, constraint: FunctionDefinitionExpr):
        params = constraint.typed_parameters
        if not params:
            return self.new_expr(
                Comparison(MathVariable(constraint.name), '=', constraint.get_value()))
        result = Comparison(FunctionApplication(constraint.name, [MathVariable(QualifiedName(arg.name, lexical_path=()))
                                                                  for arg in params]),
                            '=', constraint.get_value())
        subscripts = self.variables.get_variable_by_role(('method', constraint.name.name)).subscripts
        for arg, subscript in zip(reversed(params), reversed(subscripts)):
            arg_name = QualifiedName(arg.name, lexical_path=(PARAMETER_FRAME_NAME,))
            result = Quantifier(FOR_ALL_SYMBOL, result,
                                ComprehensionContainer([arg_name],
                                                       MathVariable(QualifiedName(subscript, lexical_path=()))))
        return self.new_expr(result, doc_string=constraint.func_doc_string)

    def implement_constraints(self) -> str:
        self.ensure_opl_coder()
        constraints = [opl_constraint for c in self.analyzer._constraints
                       if (opl_constraint := self.new_expr(c.get_value())) not in ('1', 'true')]
        # FIXME!! modify or remove for other representations (e.g., array)
        # FIXME!!!! consider other variables in the representation
        if self.has_unique_assignment:
            solution_var: OplVariable = self.variables.get_variable_by_role(('solution',))
            resource_var = opl_user_var(solution_var.fields_and_vars[0][0])
            activity_var = opl_user_var(solution_var.fields_and_vars[1][0])
            resource_domain = opl_user_var(solution_var.fields_and_vars[0][1])
            activity_domain = opl_user_var(solution_var.fields_and_vars[1][1])
            unique_assignment_constraint = self.new_expr(
                Quantifier(FOR_ALL_SYMBOL,
                           Comparison(Aggregate('+',
                                                FunctionApplication(opl_user_var(solution_var.name),
                                                                    [MathVariable(resource_var),
                                                                     MathVariable(activity_var)]),
                                                ComprehensionContainer([activity_var], MathVariable(activity_domain))),
                                      '=', Quantity(1)),
                           ComprehensionContainer([resource_var], MathVariable(resource_domain))),
                doc_string='Unique-assignment constraint')
            constraints = [unique_assignment_constraint] + constraints
        # Add definitions, but only for decision variables
        constraints.extend([self.convert_constraint(func)
                            for func in self.analyzer._defs if self.qn_is_dvar(func.name)])
        return 'subject to {\n' + '\n\n'.join(f'{self.opl_generator.indentation}{c};' for c in constraints) + '\n}'

    def qn_is_dvar(self, qn: QualifiedName) -> bool:
        return self.analyzer._domain_table.get_info(qn).is_dvar()
