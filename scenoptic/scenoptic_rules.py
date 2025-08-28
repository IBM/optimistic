from typing import Tuple, Any

from codegen.java.java_symbols import static_method_to_class_transform, JAVA_LIST_OF_QN, JAVA_LIST_CONTAINS_QN, \
    OBJECT_EQUALS_QN, COMPARABLE_COMPARE_TO_QN, JAVA_INTERNAL_FRAME_PATH
from math_rep.constants import NOT_ELEMENT_OF_SYMBOL, ELEMENT_OF_SYMBOL
from math_rep.expr import Negation, Comparison, FunctionApplication, GeneralSet, GeneralSequence, MathVariable, \
    Aggregate, \
    ComprehensionContainer, Subscripted, ComprehensionCondition, LambdaExpression, Quantity, ZERO_AS_QUANTITY, Cast
from math_rep.expression_types import QualifiedName, MType, M_NONE, M_INT, M_NUMBER, M_BOOLEAN, is_subtype
from math_rep.math_symbols import EQ_QN, NEQ_QN, GT_QN, LT_QN, LE_QN, GE_QN
from rewriting.patterns import Bindings, let, MATCH_ANY, one_of
from rewriting.rules import RewriteRule, OrderedRuleSets, RuleSet

# JAVA_COMPARISON_AS_MATH = {'=', NOT_EQUALS_SYMBOL, '<', '>', LE_SYMBOL, GE_SYMBOL}
# JAVA_OBJECT_COMPARISON_TO_MATH = {to_math(s) for s in JAVA_COMPARISON_AS_MATH}
JAVA_OBJECT_COMPARISON_TO_MATH = {EQ_QN, NEQ_QN, LT_QN, GT_QN, LE_QN, GE_QN}
JAVA_REVERSED_COMPARISON = {LT_QN: GT_QN,
                            GT_QN: LT_QN,
                            LE_QN: GE_QN,
                            GE_QN: LE_QN}


def is_object(mtype: MType):
    return not is_subtype(mtype, M_NUMBER) and mtype not in (M_NONE,)


def comparison_function_to_internal_name(func: QualifiedName) -> QualifiedName:
    return QualifiedName(func.name, func.type, lexical_path=JAVA_INTERNAL_FRAME_PATH)


class ConvertJavaObjectComparisons(RewriteRule):
    pattern = Comparison[let(cond=one_of(*JAVA_OBJECT_COMPARISON_TO_MATH)), 'lhs', 'rhs']

    def condition(self, obj: Comparison, bindings: Bindings) -> bool:
        lhs = bindings['lhs']
        rhs = bindings['rhs']
        return is_object(lhs.type) or is_object(rhs.type)

    def transform_single(self, obj, bindings: Bindings):
        def determine_args() -> Tuple[Any, Any, bool]:
            if is_object(lhs.type):
                return lhs, rhs, True
            return rhs, lhs, False

        cond = bindings['cond']
        lhs = bindings['lhs']
        rhs = bindings['rhs']
        compare_to, target, is_rhs_target = determine_args()
        if cond in (EQ_QN, NEQ_QN):
            result = FunctionApplication(function=OBJECT_EQUALS_QN, args=[compare_to], method_target=target)
            if cond == NEQ_QN:
                result = Negation(result)
            return result
        else:
            result = Comparison(FunctionApplication(function=COMPARABLE_COMPARE_TO_QN,
                                                    args=[compare_to],
                                                    method_target=target),
                                JAVA_REVERSED_COMPARISON.get(cond) if is_rhs_target else cond,
                                ZERO_AS_QUANTITY)
            return result


class NotInToNegation(RewriteRule):
    pattern = Comparison[NOT_ELEMENT_OF_SYMBOL, 'lhs', 'rhs']

    def transform_single(self, obj, bindings: Bindings):
        lhs = bindings['lhs']
        rhs = bindings['rhs']
        return Negation(Comparison(lhs, ELEMENT_OF_SYMBOL, rhs))


class SetMembershipToFunctionContain(RewriteRule):
    pattern = Comparison[ELEMENT_OF_SYMBOL, 'lhs', 'rhs']

    def transform_single(self, obj, bindings: Bindings):
        lhs = bindings['lhs']
        rhs = bindings['rhs']
        return FunctionApplication(function=JAVA_LIST_CONTAINS_QN, args=[lhs], method_target=rhs)


class GeneralSetToFunctionApplication(RewriteRule):
    pattern = GeneralSet[let(elements=...)]

    def transform_single(self, obj, bindings: Bindings):
        return FunctionApplication(function=JAVA_LIST_OF_QN,
                                   args=[e for e in bindings['elements']],
                                   method_target=MathVariable(static_method_to_class_transform(JAVA_LIST_OF_QN)))


class GeneralSequenceToFunctionApplication(RewriteRule):
    pattern = GeneralSequence[let(elements=...)]

    def transform_single(self, obj, bindings: Bindings):
        return FunctionApplication(function=JAVA_LIST_OF_QN,
                                   args=[e for e in bindings['elements']],
                                   method_target=MathVariable(static_method_to_class_transform(JAVA_LIST_OF_QN)))


class SubscriptedToGetMethodCall(RewriteRule):
    pattern = Subscripted[let(elements=...)]

    def transform_single(self, obj, bindings: Bindings):
        target = bindings['elements'][0]
        method = _determine_artifact_get(target)
        return FunctionApplication(function=method,
                                   args=bindings['elements'][1:],
                                   method_target=target)


def _determine_artifact_get(artifact):
    # TODO: Add dynamic type analysis information
    return QualifiedName('get', lexical_path=('*java-mockup*',))


class ComprehensionConditionToFunctionApplication(RewriteRule):
    pattern = ComprehensionCondition[let(condition=MATCH_ANY), let(rest=...)]

    def condition(self, obj, bindings: Bindings) -> bool:
        return not isinstance(bindings['condition'], LambdaExpression)

    def transform_single(self, obj, bindings: Bindings):
        return obj.with_argument(0, LambdaExpression([QualifiedName('x', lexical_path=('*java-mockup*',)),
                                                      QualifiedName('y', lexical_path=('*java-mockup*',))],
                                                     bindings['condition']))


class SimpleComprehensionToFunctionApplication(RewriteRule):
    pattern = Aggregate['SET',
                        let(term=...),
                        let(container=ComprehensionContainer[let(cond=MATCH_ANY),
                                                             let(rest=...)]),
    ]

    def transform_single(self, obj, bindings: Bindings):
        for key, value in bindings.bindings.items():
            print(f'{key}={value}')
        return obj


def helper_comp_to_func(term, container, rest):
    if rest.rest is None:
        pass


class SubscriptedToCast(RewriteRule):
    pattern = Subscripted[let(elements=...)]

    def transform_single(self, obj, bindings: Bindings):
        target = next(iter(bindings['elements']))
        artifact_method = QualifiedName('get', lexical_path=('*java-mockup*',))
        function = FunctionApplication(function=artifact_method,
                                       args=[e for i, e in enumerate(bindings['elements']) if i > 0],
                                       method_target=target)
        return Cast(M_INT, function)


JAVA_RULES = OrderedRuleSets(
    RuleSet(GeneralSetToFunctionApplication(),
            GeneralSequenceToFunctionApplication(),
            SubscriptedToCast(),
            NotInToNegation(),
            SetMembershipToFunctionContain(),
            ))

JAVA_RULES0 = OrderedRuleSets(
    RuleSet(SimpleComprehensionToFunctionApplication()
            ))

JAVA_RULES1 = OrderedRuleSets(
    RuleSet(SubscriptedToCast(),
            SubscriptedToGetMethodCall(),
            ))

JAVA_RULES3 = OrderedRuleSets(
    RuleSet(GeneralSetToFunctionApplication(),
            GeneralSequenceToFunctionApplication(),
            SubscriptedToCast(),
            ComprehensionConditionToFunctionApplication(),
            SimpleComprehensionToFunctionApplication()))

JAVA_RULES2 = OrderedRuleSets(
    RuleSet(NotInToNegation(),
            SetMembershipToFunctionContain(),
            GeneralSetToFunctionApplication(),
            GeneralSequenceToFunctionApplication(),
            SubscriptedToGetMethodCall(), ))
