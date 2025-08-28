from doctest import testmod

from rewriting.domain_analysis_rules import ConjunctionExtractor, RaiseConjunction, RaiseConjunctionOverUniversal
from rewriting.rules import RuleSet, OrderedRuleSets, exhaustively_apply_rules, get_all_rule_results
# from test.test_python_to_expr import python_string_to_expr
from validator2solver.optimistic_factory import python_string_to_expr
from tests.test_rules import extract_contents

FACT_EXTRACTION_RULES = OrderedRuleSets(RuleSet(ConjunctionExtractor()))

LOGICAL_SIMPLIFICATION_RULES = OrderedRuleSets(RuleSet(RaiseConjunction(), RaiseConjunctionOverUniversal()))


def test_conjunction_extractor1():
    r"""
    >>> for r in get_all_rule_results(ConjunctionExtractor(), extract_contents(python_string_to_expr('p and q\n'))):
    ...     print(r)
    $p
    $q
    """


def test_conjunction_raiser():
    r"""
    >>> print(exhaustively_apply_rules(LOGICAL_SIMPLIFICATION_RULES,
    ...                                python_string_to_expr('p and (q and (r and s)) and t\n')))
    Math-Module($p ∧ $q ∧ $r ∧ $s ∧ $t)
    """


def test_conjunction_over_universal():
    r"""
    >>> print(exhaustively_apply_rules(OrderedRuleSets(RuleSet(RaiseConjunctionOverUniversal())),
    ...                                python_string_to_expr('all(a is not None and all(b is not None and b != a for b in s2) for a in s1)\n')))
    Math-Module(∀a ∈ $s1. $a ≠ None*Nil* ∧ ∀a ∈ $s1. ∀b ∈ $s2. $b ≠ None*Nil* ∧ ∀a ∈ $s1. ∀b ∈ $s2. $b ≠ $a)
    """


# def test_conjunction_extractor():
#     r"""
#     >>> print(exhaustively_apply_rules(LOGICAL_SIMPLIFICATION_RULES, python_string_to_expr('p and q\n')))
#     0
#     """


if __name__ == '__main__':
    testmod()
    # expr = python_string_to_expr('all(a is not None and all(b is not None and b != a for b in s2) for a in s1)\n')
    # print('Expr: ', expr)
    # print('Trans:', exhaustively_apply_rules(OrderedRuleSets(RuleSet(RaiseConjunctionOverUniversal())), expr))
