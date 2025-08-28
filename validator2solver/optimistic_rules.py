from codegen.abstract_rep import IMPLIES_OPERATOR
from validator2solver.optimization_analyzer import OptimizationProblemAnalyzer
from codegen.utils import uniqueize_name
from math_rep.constants import AND_SYMBOL, IMPLIES_SYMBOL, LE_SYMBOL, NOT_EQUALS_SYMBOL, GE_SYMBOL, \
    NOT_ELEMENT_OF_SYMBOL, ELEMENT_OF_SYMBOL, FOR_ALL_SYMBOL
from validator2solver.domain_analysis import term_is_dvar, term_type
from math_rep.expr import IFTE, Negation, Comparison, FunctionApplication, LogicalOperatorAsExpression, Epsilon, \
    LogicalOperator, Attribute, MathVariable, Aggregate, Quantity, Stream, ComprehensionContainer, Quantifier, \
    ComprehensionCondition, IndexedMathVariable
from math_rep.expression_types import QualifiedName, MClassType, is_subtype, M_INT
from math_rep.math_symbols import AND_QN, OR_QN, LT_QN, GT_QN, NEQ_QN, PLUS_QN, EQ_QN, \
    CEIL_QN, TIMES_QN
from math_rep.math_frame import MATH_FRAME_PATH
from opl_repr.opl_frame_constants import INVENTED_VARS_FRAME_NAME
from validator2solver.python.symbol_default_modules import COUNT_QN, UNIQUE_ASSIGNMENT_METHOD_QN
from rewriting.patterns import Bindings, let, MATCH_ANY, ClassPattern
from rewriting.rules import RewriteRule, get_pre_and_post, prevent_type_propagation


class IfToImplications(RewriteRule):
    def __init__(self, force=False):
        self.force = force

    pattern = IFTE['cond', 'then', 'else']

    def condition(self, obj, bindings: Bindings) -> bool:
        return self.force or any(term_is_dvar(v) for v in bindings.bindings.values())

    def transform_single(self, obj, bindings: Bindings):
        cond = bindings['cond']
        pos = bindings['then']
        neg = bindings['else']
        return LogicalOperatorAsExpression(AND_SYMBOL, (LogicalOperatorAsExpression(IMPLIES_OPERATOR, (cond, pos)),
                                                        LogicalOperatorAsExpression(IMPLIES_OPERATOR,
                                                                                    (Negation(cond), neg))))


class LiftRightImplicationOverComparison(RewriteRule):
    pattern = Comparison[
        let(op=MATCH_ANY), 'comparand', LogicalOperatorAsExpression[IMPLIES_SYMBOL, 'cond', 'consequent']]

    def transform_single(self, obj, bindings: Bindings):
        return LogicalOperatorAsExpression(IMPLIES_SYMBOL,
                                           [bindings['cond'],
                                            Comparison(bindings['comparand'],
                                                       bindings['op'],
                                                       bindings['consequent'])])


class LiftLeftImplicationOverComparison(RewriteRule):
    pattern = Comparison[let(op=MATCH_ANY),
                         LogicalOperatorAsExpression[IMPLIES_SYMBOL, 'cond', 'consequent'], 'comparand']

    def transform_single(self, obj, bindings: Bindings):
        return LogicalOperatorAsExpression(IMPLIES_SYMBOL,
                                           [bindings['cond'],
                                            Comparison(bindings['consequent'],
                                                       bindings['op'],
                                                       bindings['comparand'])])


class LiftRightLogicalOperatorOverComparison(RewriteRule):
    pattern = Comparison[let(op=0), 'comparand', LogicalOperatorAsExpression[let(kind=0), let(args=...)]]

    def condition(self, obj, bindings: Bindings) -> bool:
        return bindings['kind'] in (AND_QN, OR_QN)

    def transform_single(self, obj, bindings: Bindings):
        kind = bindings['kind']
        comparand = bindings['comparand']
        op = bindings['op']
        return LogicalOperatorAsExpression(kind, [Comparison(comparand, op, arg) for arg in (bindings['args'])])


class LiftLeftLogicalOperatorOverComparison(RewriteRule):
    pattern = Comparison[let(op=0), LogicalOperatorAsExpression[let(kind=0), let(args=...)], 'comparand']

    def condition(self, obj, bindings: Bindings) -> bool:
        return bindings['kind'] in (AND_QN, OR_QN)

    def transform_single(self, obj, bindings: Bindings):
        kind = bindings['kind']
        comparand = bindings['comparand']
        op = bindings['op']
        return LogicalOperatorAsExpression(kind, [Comparison(arg, op, comparand) for arg in bindings['args']])


def pack_function_args(obj, func, new_args):
    if obj.method_target is not None:
        new_appl = FunctionApplication(func, new_args[1:], method_target=new_args[0])
    else:
        new_appl = FunctionApplication(func, new_args)
    return new_appl


class LiftImplicationOverFunctionApplication(RewriteRule):
    pattern = FunctionApplication[let(func=MATCH_ANY),
                                  let(pre=...),
                                  LogicalOperatorAsExpression[IMPLIES_SYMBOL, 'cond', 'consequent'],
                                  let(post=...)]

    def transform_single(self, obj: FunctionApplication, bindings: Bindings):
        pre, post = get_pre_and_post(bindings)
        new_args = [*pre, bindings['consequent'], *post]
        new_appl = pack_function_args(obj, bindings['func'], new_args)
        return LogicalOperatorAsExpression(IMPLIES_SYMBOL, [bindings['cond'], new_appl])


# FIXME: replace by lifting IFTE, expanding nested IFTEs
class LiftLogicalOperatorOverFunctionApplication(RewriteRule):
    pattern = FunctionApplication[let(func=0),
                                  let(pre=...),
                                  LogicalOperatorAsExpression[let(kind=0), let(largs=...)],
                                  let(post=...)]

    def condition(self, obj, bindings: Bindings) -> bool:
        return bindings['kind'] in (AND_QN, OR_QN)

    def transform_single(self, obj, bindings: Bindings):
        kind = bindings['kind']
        func = bindings['func']
        pre, post = get_pre_and_post(bindings)
        applications = [pack_function_args(obj, func, [*pre, larg, *post]) for larg in bindings['largs']]
        return LogicalOperatorAsExpression(kind, applications)


class EliminateLogicalOperatorAsExpression(RewriteRule):
    """
    Replace LogicalOperatorAsExpression by LogicalOperator.

    This rule must be in a RuleSet that runs after all lifting rules!
    """
    pattern = ClassPattern(LogicalOperatorAsExpression)

    def transform_single(self, obj, bindings: Bindings):
        return LogicalOperator(obj.kind, obj.elements)


class ReplaceStrictInequality(RewriteRule):
    pattern = Comparison[let(op=0), 'lhs', 'rhs']

    def transform_single(self, obj, bindings: Bindings):
        op = bindings['op']
        lhs = bindings['lhs']
        rhs = bindings['rhs']
        epsilon = (Quantity(1) if is_subtype(term_type(lhs), M_INT) and is_subtype(term_type(rhs), M_INT)
                   else Epsilon())
        if op == LT_QN:
            return lhs <= rhs - epsilon
        if op == GT_QN:
            return lhs >= rhs + epsilon
        if op == NEQ_QN:
            # TODO: this duplicates lhs and rhs, use LetExpr?
            return (lhs >= rhs + epsilon) | (lhs <= rhs - epsilon)
        return obj


def symmetrize_dict(d):
    return {**{val: key for key, val in d.items()}, **d}


NEGATED_COMPARISONS = symmetrize_dict({'<': GE_SYMBOL, '>': LE_SYMBOL, '=': NOT_EQUALS_SYMBOL,
                                       ELEMENT_OF_SYMBOL: NOT_ELEMENT_OF_SYMBOL})


class EliminateNegationOfComparison(RewriteRule):
    """
    Flip comparison operators to eliminate negations

    N.B. This transformation must precede ReplaceStrictInequality!
    """

    pattern = Negation[Comparison[let(op=0), 'lhs', 'rhs']]

    def transform_single(self, obj, bindings: Bindings):
        op = bindings['op']
        if op.lexical_path != MATH_FRAME_PATH:
            return obj
        if (rev_op := NEGATED_COMPARISONS.get(op.name)) is not None:
            return Comparison(bindings['lhs'], rev_op, bindings['rhs'])
        return obj


class EliminateSelfVariable(RewriteRule):
    """
    Remove the self variable corresponding to the optimization-problem class from a method target or attribute
    """

    def __init__(self, optimization_class: QualifiedName):
        self.optimization_class = optimization_class

    pattern = ClassPattern(FunctionApplication, Attribute)

    def condition(self, obj, bindings: Bindings) -> bool:
        container = obj.method_target if isinstance(obj, FunctionApplication) else obj.container
        if container is None:
            return False
        return (isinstance(container, MathVariable) and isinstance(ctype := term_type(container), MClassType) and
                ctype.class_name == self.optimization_class)

    def transform_single(self, obj, bindings: Bindings):
        if isinstance(obj, FunctionApplication):
            return obj.without_target()
        obj: Attribute
        result = MathVariable(QualifiedName(obj.attribute.to_c_identifier(), lexical_path=()))
        return result


class CountToSum(RewriteRule):
    """
    Replace Python count function by sum(...) 1
    """

    pattern = FunctionApplication[COUNT_QN]

    def transform_single(self, obj: FunctionApplication, bindings: Bindings):
        if isinstance(obj.args[0], (Stream, Aggregate)):
            return prevent_type_propagation(Aggregate('+', Quantity(1), obj.args[0].container))
        else:
            return prevent_type_propagation(Aggregate('+', Quantity(1),
                                                      ComprehensionContainer([QualifiedName('dummy', lexical_path=())],
                                                                             obj.args[0])))


class NotToEqZero(RewriteRule):
    """
    Replace logical negation of variable or attribute by comparison with 0 for non-dvars
    """

    pattern = Negation[let(arg=MATCH_ANY)]

    def condition(self, obj, bindings: Bindings) -> bool:
        return isinstance(arg := bindings['arg'], (MathVariable, Attribute)) and not term_is_dvar(arg)

    def transform_single(self, obj, bindings: Bindings):
        return prevent_type_propagation(Comparison(bindings['arg'], '=', Quantity(0)))


class BooleanToIntEquationInLogicalExpression(RewriteRule):
    """
    Replace variable or attribute that is not a dvar in a logical operator by a comparison with 0
    """

    # FIXME!!! replace logical op by sum if any arg is a dvar, o/w replace args by ...=1

    pattern = ClassPattern(LogicalOperator)

    def transform_single(self, obj, bindings: Bindings):
        elements = obj.elements
        new_elements = [e if not isinstance(e, (MathVariable, Attribute)) or term_is_dvar(e)
                        else Comparison(e, '=', Quantity(1))
                        for e in elements]
        if all(e is ne for e, ne in zip(elements, new_elements)):
            return obj
        return prevent_type_propagation(LogicalOperator(obj.kind, new_elements))


class QuantifiedBooleanToIntEquation(RewriteRule):
    """
    Replace top-level variable or attribute in quantifier by a comparison with 0
    """

    pattern = ClassPattern(Quantifier)

    def condition(self, obj, bindings: Bindings) -> bool:
        return isinstance(formula := obj.formula, (MathVariable, Attribute)) and not term_is_dvar(formula)

    def transform_single(self, obj, bindings: Bindings):
        return prevent_type_propagation(obj.with_formula(Comparison(obj.formula, '=', Quantity(1)), force=True))


# FIXME!!! Also treat ceil as argument of FunctionApplication, other Comparisons, and return values
# TODO: special case for eq: int
class EquatedCeil(RewriteRule):
    """
    Replace an equality to a ceil function with two inequalities
    """

    pattern = Comparison[EQ_QN, let(pre=...), let(ceil_appl=FunctionApplication[CEIL_QN]), let(post=...)]

    def condition(self, obj, bindings: Bindings) -> bool:
        pre, post = get_pre_and_post(bindings)
        eq = (pre or post)[0]
        return term_is_dvar(bindings['ceil_appl']) and is_subtype(eq.appl_info.type, M_INT)

    def transform_single(self, obj, bindings: Bindings):
        # TODO: use LetExpr
        ceil_arg = bindings['ceil_appl'].args[0]
        pre, post = get_pre_and_post(bindings)
        eq = (pre or post)[0]
        # TODO: consider reversing roles: eq>=ca && eq-1<ca
        return LogicalOperator(AND_SYMBOL, [Comparison(eq, GE_SYMBOL, ceil_arg),
                                            Comparison(eq, '<', FunctionApplication(PLUS_QN, [ceil_arg, Quantity(1)]))])


# FIXME!!! Also treat unique_assignment as argument of FunctionApplication, other Comparisons, and return values
# TODO: add implementation for array representation
class TwoEquatedUniqueAssignments(RewriteRule):
    """
    Replace an equality between two unique_assignment calls with a quantification over the solution variable
    """

    # FIXME!!!! domain is not legal_solution_var_name but var for all activities
    def __init__(self, solution_var: QualifiedName, all_activities: QualifiedName):
        self.solution_var = solution_var
        self.all_activities_var_name = all_activities

    pattern = Comparison[EQ_QN,
                         let(ua1=FunctionApplication[UNIQUE_ASSIGNMENT_METHOD_QN]),
                         let(ua2=FunctionApplication[UNIQUE_ASSIGNMENT_METHOD_QN])]

    def transform_single(self, obj, bindings: Bindings):
        ua1_arg = bindings['ua1'].args[0]
        ua2_arg = bindings['ua2'].args[0]
        # relying on the fact that Assignment accepts the resource as first parameter and activity as second
        var = MathVariable(QualifiedName(uniqueize_name('x', [v.name for v in obj.free_vars]),
                                         lexical_path=(INVENTED_VARS_FRAME_NAME,)))
        # FIXME! replace with IFF_SYMBOL
        return Quantifier(FOR_ALL_SYMBOL,
                          Comparison(FunctionApplication(self.solution_var, [ua1_arg, var]),
                                     '=',
                                     FunctionApplication(self.solution_var, [ua2_arg, var])),
                          ComprehensionContainer([var.name], MathVariable(self.all_activities_var_name)))


class EquatedUniqueAssignment(RewriteRule):
    """
    Replace an equality to a unique_assignment call with the corresponding solution variable

    N.B. This must be in a ruleset that follows TwoEquatedUniqueAssignments
    """

    def __init__(self, solution_var: QualifiedName):
        self.solution_var = solution_var

    pattern = Comparison[EQ_QN,
                         let(pre=...),
                         let(ua_appl=FunctionApplication[UNIQUE_ASSIGNMENT_METHOD_QN]),
                         let(post=...)]

    def condition(self, obj, bindings: Bindings) -> bool:
        pre, post = get_pre_and_post(bindings)
        eq = (pre or post)[0]
        # FIXME! this rule is run before dvar propagated, makes change too early!
        # return not term_is_dvar(eq)
        return not isinstance(eq, FunctionApplication) or eq.function != UNIQUE_ASSIGNMENT_METHOD_QN

    def transform_single(self, obj, bindings: Bindings):
        # TODO: use LetExpr
        ua_arg = bindings['ua_appl'].args[0]
        pre, post = get_pre_and_post(bindings)
        eq = (pre or post)[0]
        # relying on the fact that Assignment accepts the resource as first parameter and activity as second
        return FunctionApplication(self.solution_var, [ua_arg, eq])


class GlobalizeCeil(RewriteRule):
    """
    Replace a call to ceil that isn't equated to a variable by a global variable

    UNFINISHED, not used
    """

    def __init__(self, analyzer: OptimizationProblemAnalyzer):
        self.analyzer = analyzer

    pattern = FunctionApplication[CEIL_QN]

    def condition(self, obj, bindings: Bindings) -> bool:
        print('>>>>', obj)
        for fv in obj.free_vars:
            print('----', fv)
            print(' - -', self.analyzer._domain_table.get_info(fv).type)
        print('....', obj.bound_vars)
        return False


class MoveSumConditionToTerm(RewriteRule):
    """
    Replace a condition that depends on a dvar inside an aggregation operation (e.g., sum) to a multiple of the term
    """

    pattern = Aggregate['+',
                        let(term=MATCH_ANY),
                        let(container=ComprehensionContainer[let(cond=MATCH_ANY),
                                                             let(rest=ComprehensionCondition)])]

    def condition(self, obj, bindings: Bindings) -> bool:
        return term_is_dvar(bindings['rest'])

    def transform_single(self, obj, bindings: Bindings):
        rest = bindings['rest']
        # TODO: support recursive conditions
        assert rest.rest is None, 'Recursive condition not yet supported'
        cond = rest.condition
        if isinstance(cond, LogicalOperator):
            dec = [c for c in cond.elements if term_is_dvar(c)]
            non_dec = [c for c in cond.elements if not term_is_dvar(c)]
        else:
            dec = [cond]
            non_dec = []
        container = bindings['container']
        new_rest = (None if not non_dec else
                    ComprehensionCondition(LogicalOperator(AND_SYMBOL, non_dec)) if len(non_dec) > 1 else
                    ComprehensionCondition(non_dec[0]))
        return Aggregate(obj.op,
                         FunctionApplication(TIMES_QN, [bindings['term'], *dec]),
                         ComprehensionContainer(container.vars, container.container, new_rest))


# FIXME!! This rule is circular, may apply a constraint to itself, resulting in a tautology.  Need justifications!
class ReduceDomainTautologies(RewriteRule):
    """
    Replace an 'in' relationship with True when the same domain has been deduced for it
    """

    pattern = Comparison[ELEMENT_OF_SYMBOL]

    def condition(self, obj: Comparison, bindings: Bindings) -> bool:
        try:
            return obj.lhs.appl_info.domain.appl_info.value == obj.rhs.appl_info.value
        except AttributeError:
            return False

    def transform_single(self, obj, bindings: Bindings):
        return Quantity(True)


class CoerceBoolToEq(RewriteRule):
    """
    Replace a boolean variable b by an equation b == 1 in logical operators
    """

    pattern = LogicalOperator[let(op=MATCH_ANY), let(operands=...)]

    def condition(self, obj, bindings: Bindings) -> bool:
        return any(isinstance(oper, (MathVariable, IndexedMathVariable)) for oper in bindings['operands'])

    def transform_single(self, obj, bindings: Bindings):
        return LogicalOperator(bindings['op'],
                               [oper == 1 if isinstance(oper, (MathVariable, IndexedMathVariable)) else oper
                                for oper in bindings['operands']])


class CoerceNegatedBoolToEq(RewriteRule):
    """
    Replace the negation boolean variable b by an equation b == 0 in logical operators
    """

    pattern = Negation[let(operand=MATCH_ANY)]

    def condition(self, obj, bindings: Bindings) -> bool:
        return isinstance(bindings['operand'], (MathVariable, IndexedMathVariable))

    def transform_single(self, obj, bindings: Bindings):
        return bindings['operand'] == 0
