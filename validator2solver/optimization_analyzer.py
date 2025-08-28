# TODO: support multiple solver types (LP, MIP, QP, CP, ...) and choose the best one for the given problem
from dataclasses import dataclass
from itertools import chain
from typing import Mapping

from validator2solver.domain_analysis import DomainTable, ConstraintTypeExtractor, SOLUTION_VAR_NAME
from math_rep.expr import MathModule, ClassDefinitionExpr, MathVariable, FunctionApplication, MathTypeDeclaration, \
    NamedArgument, Quantity, FunctionDefinitionExpr, TypeAlias, InitializedVariable
from math_rep.expression_types import MType, QualifiedName, MAtomicType
from validator2solver.optimistic_factory import generate_expr_from_file, create_registry
from validator2solver.python.python_to_expr import PythonToExpr
from validator2solver.python.symbol_default_modules import CONSTRAINT_QN, MAXIMIZE_QN, MINIMIZE_QN, \
    UNIQUE_ASSIGNMENT_CLASS_QN, OPTIMIZATION_PROBLEM_QN, DATA_RECORD_QN_GROUP, RECORD_QN


def find_decorator(expr, *decorator: QualifiedName):
    return next((d for d in expr.decorators
                 if isinstance(d, MathVariable) and d.name in decorator or
                 isinstance(d, FunctionApplication) and d.function in decorator),
                None)


@dataclass
class Field:
    name: str
    type: MType
    is_primary_key: bool = False
    is_domain: bool = False
    is_solution_var: bool = False

    def __str__(self):
        primary_key = ' (PK)' if self.is_primary_key else ''
        return f'{self.name}: {self.type}{primary_key}'


@dataclass
class Struct:
    name: str
    fields: Mapping[str, Field]

    def __str__(self):
        fields_str = ', '.join(str(f) for f in self.fields.values())
        return f'{self.name}: [{fields_str}]'


def analyze_optimization_problem_classes(expr: MathModule) -> MathModule:
    contents = []
    for c in expr.contents:
        if isinstance(c, ClassDefinitionExpr):
            # Look at the class MRO, if inherits from an OptimizationProblem
            all_superclasses = expr.all_superclasses.get(c.name, [])
            if any(s == OPTIMIZATION_PROBLEM_QN for s in all_superclasses) and not c.is_dataclass:
                # Possibly due to code transition to new methodology, the problem class is not
                # decorated with @dataclass, so the handling in "python_to_expr.visit_python_decorated()"
                # is skipped, need here to do just the same, transform the class into a data-class
                defs = c.get_defs()
                c = c.as_dataclass(
                    [PythonToExpr.convert_field(d) for d in defs if
                     isinstance(d, (MathTypeDeclaration, InitializedVariable))],
                    removed_defs=[d for d in defs if isinstance(d, (MathTypeDeclaration, InitializedVariable))])
                # TODO: replace RECORD_QN decorator with another indication, to avoid replacement elsewhere
                c.decorators = [MathVariable(RECORD_QN)]
                expr.classes[c.name] = c
        contents.append(c)
    expr.contents = contents
    return expr


def analyze_classes(expr: MathModule):
    structs = {}
    aliases = {}
    optimization_problems = []
    for c in expr.contents:
        if isinstance(c, ClassDefinitionExpr):
            fields = {}
            if not find_decorator(c, *DATA_RECORD_QN_GROUP):
                raise Exception('Only supporting dataclasses')
            for field in c.fields:
                if isinstance(field, MathTypeDeclaration):
                    fields[field.var] = Field(field.var, field.type, field.primary_key, field.is_domain,
                                              field.is_solution_var)

            if not fields:
                raise Exception(f'Dataclass {c.name} has no fields')
            if any(s.name == OPTIMIZATION_PROBLEM_QN for s in c.superclasses):
                # FIXME!! look at inherited classes as well
                optimization_problems.append(c)
            # FIXME: use QualifiedName's as indexes for structs?  Currently must not have two structs with the same name
            # FIXME! support inheritance of dataclasses (collect fields, identify references)
            structs[c.name.name] = Struct(c.name, fields)
        elif isinstance(c, TypeAlias):
            actual_type = c.mtype
            # FIXME! is it always true that NewType's are bounded?
            if isinstance(actual_type, MAtomicType):
                actual_type = actual_type.as_bounded()
            aliases[c.alias] = actual_type
        elif isinstance(c, Quantity) and isinstance(c.value, str):
            # Comment string, ignore
            pass
        else:
            raise Exception('Optimization module can only contain class definitions and type aliases')
    if len(optimization_problems) != 1:
        if not optimization_problems:
            raise Exception('Optimization problem class (subclass of OptimizationProblem) not found')
        else:
            # FIXME!!!! allow multiple subclasses, add parameter to choose which one to use
            raise Exception(f'Optimization module must have exactly one optimization problem class, '
                            f'found {len(optimization_problems)}')
    return optimization_problems[0], structs, aliases


class OptimizationProblemAnalyzer:
    """
    This class represents an analyzer for optimization models, providing information and transformations for translation
    into a language such as OPL.
    """

    def __init__(self):
        self._top_level_expr = None
        self._optimization_problem = None
        self._objectives = []
        self._constraints = []
        self._defs = []
        self._input_vars = None
        self._decision_vars = None
        self._structs = None
        self._aliases = None
        self._properties = {}
        self._solution_vars = None
        # FIXME: remove following
        self._solution_class = None
        self._inputs = None
        self._domain_table = None
        self._constraint_type_extractor = None

    def struct_by_name(self, name: QualifiedName) -> Struct:
        # FIXME: remove .name access when name changed to QN
        return self._structs[name.name]

    def from_python_file(self, config, builtin_frame, with_imports):
        # tree = generate_ast_from_file(file_path)
        # add_symbols(file_path, tree)
        # visitor = PythonToExpr()
        # self.top_level_expr = expr = visitor.visit(tree)
        expr = None
        if with_imports:
            registry = create_registry(config=config,
                                       builtin_frame=builtin_frame,
                                       print_translations=False)
            root_registry = registry[0]
            for module_name in root_registry:
                expr = root_registry[module_name]['model']
        else:
            expr = generate_expr_from_file(config['target_module']['module'],
                                           config=config,
                                           builtin_frame=builtin_frame)
        # print('Expression:', expr)
        if not isinstance(expr, MathModule):
            raise Exception(f'Top-level expression from Python must be a MathModule, found {type(expr).__name__}')
        self._top_level_expr = expr = analyze_optimization_problem_classes(expr)
        optimization_problem, self._structs, self._aliases = analyze_classes(expr)
        self._optimization_problem = optimization_problem

        # print('Structs')
        # for struct in self.structs.values():
        #     print(struct)
        # print('Optimization problems')
        # print(optimization_problem)

        self.analyze_optimization_problem()

        self.analyze_types()

        self.prepare_variable_representation()

        # print(self.constraints)
        # print(self.objectives)
        # print(self.defs)
        # print('Properties:', self.properties)
        # print('Solution class:', self.solution_class)
        # print('Inputs:', self.inputs)

    # FIXME!!!! remove dependence on unique-assignment
    def analyze_optimization_problem(self):
        optimization_problem = self._optimization_problem
        if not optimization_problem.defs:
            raise Exception(f'Optimization-problem class {optimization_problem.name} has no content')
        # FIXME!! look in inheritance hierarchy
        for func in optimization_problem.get_defs():
            if isinstance(func, (MathTypeDeclaration, MathVariable)):
                continue
            if not isinstance(func, FunctionDefinitionExpr):
                raise Exception(f'Internal class definitions not supported in {optimization_problem.name}')
            found_decorators = []
            if find_decorator(func, CONSTRAINT_QN):
                self._constraints.append(func)
                found_decorators.append('constraint')
            # TODO: remove code duplication
            if d := find_decorator(func, MINIMIZE_QN):
                if isinstance(d, MathVariable):
                    self._objectives.append((func, 1))
                else:
                    w = next((arg.expr for arg in d.args if isinstance(arg, NamedArgument) and arg.name == 'weight'),
                             Quantity(1))
                    if isinstance(w, Quantity):
                        weight = w.value
                    else:
                        weight = 1
                    self._objectives.append((func, weight))
                found_decorators.append('minimize')
            if d := find_decorator(func, MAXIMIZE_QN):
                if isinstance(d, MathVariable):
                    self._objectives.append((func, -1))
                else:
                    w = next((arg.expr for arg in d.args if isinstance(arg, NamedArgument) and arg.name == 'weight'),
                             Quantity(1))
                    if isinstance(w, Quantity):
                        weight = w.value
                    else:
                        weight = 1
                    self._objectives.append((func, -weight))
                found_decorators.append('maximize')
            if len(found_decorators) > 1:
                raise Exception(f'Method {func.name} may only have one of the decorators {", ".join(found_decorators)}')
            if found_decorators:
                if func.typed_parameters:
                    raise Exception(f'Method decorated with {found_decorators} cannot have arguments '
                                    f'but has {func.typed_parameters}')
            else:
                self._defs.append(func)
        if any(s.name == UNIQUE_ASSIGNMENT_CLASS_QN for s in optimization_problem.superclasses):
            # FIXME!! look in inheritance hierarchy
            self._properties['unique-assignment'] = True
        # TODO? check for dynamic replacement of name
        # FIXME!! allow multiple solution vars and/or solution as tuple; use solution in metadata instead of fixed name
        # FIXME: remove solution_var once conversion complete
        opt_cls_fields = self._structs[optimization_problem.name.name].fields
        solution_var = opt_cls_fields.get(SOLUTION_VAR_NAME)
        solution_vars = tuple(chain([] if solution_var is None else [solution_var],
                                    (field for field_name, field in opt_cls_fields.items()
                                     if field.is_solution_var and field_name != SOLUTION_VAR_NAME)))
        if not solution_vars:
            raise Exception(f'No solution variable in problem class {optimization_problem.name}')
        self._solution_vars = solution_vars
        self._solution_class = solution_vars[0].type
        self._inputs = [f for f in opt_cls_fields.values()
                        if f.name not in [v.name for v in solution_vars]]

    def analyze_types(self):
        if self._domain_table is None:
            self._domain_table = DomainTable(self._structs, self._optimization_problem, exists_is_dvar=True)
        self._domain_table.build(self._top_level_expr)
        self._domain_table.add_solution_dependences()
        if self._constraint_type_extractor is None:
            self._constraint_type_extractor = ConstraintTypeExtractor(self._domain_table)
        for constraint in self._constraints:
            self._constraint_type_extractor.visit(constraint)
        self._domain_table.propagate()
        # print(self.domain_table.describe())

    def prepare_variable_representation(self):
        # FIXME!!! compute representation
        print(self._solution_vars)
