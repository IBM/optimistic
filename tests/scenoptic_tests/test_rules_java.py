from scenoptic.scenoptic_rules import JAVA_RULES
from rewriting.rules import exhaustively_apply_rules, OrderedRuleSets
from tests.test_rules import get_expr


def print_rule_application(rulesets: OrderedRuleSets, python_input: str):
    print()
    print(python_input)
    expr = get_expr(python_input + '\n')
    print(expr)
    exhaustively_apply_rules(rulesets, expr, print_intermediate=True)


def test_java_set1():
    r"""
    >>> print_rule_application(JAVA_RULES, 'foo(bar, c1 + c2, True) not in {c1, c2}')
    <BLANKLINE>
    foo(bar, c1 + c2, True) not in {c1, c2}
    foo($bar, $c1 + $c2, True*Boolean*) ∉ {$c1, $c2}
    foo($bar, $c1 + $c2, True*Boolean*) ∉ $Set.of($c1, $c2)
    ¬(foo($bar, $c1 + $c2, True*Boolean*) ∈ $Set.of($c1, $c2))
    ¬$Set.of($c1, $c2).contains(foo($bar, $c1 + $c2, True*Boolean*))
    """
