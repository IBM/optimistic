from math_rep.expr import MathModule, FormalContent
from rewriting.patterns import pattern_match
from validator2solver.optimistic_factory import python_string_to_expr
from rewriting.rules import apply_rule, exhaustively_apply_rules, RuleSet, OrderedRuleSets
from validator2solver.optimistic_rules import IfToImplications, LiftLeftImplicationOverComparison, \
    LiftRightImplicationOverComparison, LiftRightLogicalOperatorOverComparison, LiftLeftLogicalOperatorOverComparison, \
    LiftImplicationOverFunctionApplication, LiftLogicalOperatorOverFunctionApplication, ReplaceStrictInequality, \
    EliminateNegationOfComparison


def extract_contents(module: MathModule) -> FormalContent:
    bindings = next(pattern_match(MathModule['contents'], module), None)
    if bindings is not None:
        return bindings['contents']
    return module


def get_expr(python_text):
    return extract_contents(python_string_to_expr(python_text))


def test_rule(rule, python):
    expr = get_expr(python)
    print(expr)
    print(apply_rule(rule, expr))


def test_precedence1():
    r"""
    >>> print(python_string_to_expr('p and (q or r) and s\n'))
    Math-Module($p ∧ ($q ∨ $r) ∧ $s)
    >>> print(python_string_to_expr('p and q or r and s\n'))
    Math-Module($p ∧ $q ∨ $r ∧ $s)
    """


def test_ifte1():
    r"""
    >>> test_rule(IfToImplications(force=True),'0 if p else 1\n')
    $p ? 0 : 1
    ($p ⇒ 0) ∧ (¬$p ⇒ 1)
    >>> test_rule(IfToImplications(force=True),'0 if x<y else 1\n')
    $x < $y ? 0 : 1
    ($x < $y ⇒ 0) ∧ (¬($x < $y) ⇒ 1)
    """


def test_apply_rules1():
    r"""
    >>> print(exhaustively_apply_rules(OrderedRuleSets(RuleSet(IfToImplications(force=True))),
    ...       python_string_to_expr('0 if p else 1\n')))
    Math-Module(($p ⇒ 0) ∧ (¬$p ⇒ 1))
    >>> print(exhaustively_apply_rules(OrderedRuleSets(RuleSet(IfToImplications(force=True), LiftRightImplicationOverComparison(),
    ...                                LiftRightLogicalOperatorOverComparison(),
    ...                                LiftLeftLogicalOperatorOverComparison())),
    ...                               python_string_to_expr('x==(0 if p else 1)\n')))
    Math-Module(($p ⇒ $x = 0) ∧ (¬$p ⇒ $x = 1))
    >>> print(exhaustively_apply_rules(OrderedRuleSets(RuleSet(IfToImplications(force=True),
    ...                                                        LiftLeftImplicationOverComparison(),
    ...                                                        LiftRightLogicalOperatorOverComparison(),
    ...                                                        LiftLeftLogicalOperatorOverComparison())),
    ...                                python_string_to_expr('(0 if p else 1)==x\n')))
    Math-Module(($p ⇒ 0 = $x) ∧ (¬$p ⇒ 1 = $x))
    """


ALL_RULES = OrderedRuleSets(
    RuleSet(IfToImplications(force=True)),
    RuleSet(EliminateNegationOfComparison()),
    RuleSet(LiftLeftImplicationOverComparison(), LiftRightImplicationOverComparison(),
            LiftRightLogicalOperatorOverComparison(), LiftLeftLogicalOperatorOverComparison(),
            LiftImplicationOverFunctionApplication(), LiftLogicalOperatorOverFunctionApplication(),
            ReplaceStrictInequality()))


def test_apply_rules2():
    r"""
    >>> print(exhaustively_apply_rules(ALL_RULES,
    ...                                python_string_to_expr('(0 if p else 1)<(2 if q else 3)\n')))
    Math-Module(($q ⇒ ($p ⇒ 0 ≤ 2 - ε) ∧ (¬$p ⇒ 1 ≤ 2 - ε)) ∧ (¬$q ⇒ ($p ⇒ 0 ≤ 3 - ε) ∧ (¬$p ⇒ 1 ≤ 3 - ε)))
    >>> print(exhaustively_apply_rules(ALL_RULES, python_string_to_expr('x==(0 if p else 1)+10\n')))
    Math-Module(($p ⇒ $x = 10) ∧ (¬$p ⇒ $x = 11))
    >>> print(exhaustively_apply_rules(ALL_RULES, python_string_to_expr('x==f((0 if p else 1)+10)\n')))
    Math-Module(($p ⇒ $x = f(10)) ∧ (¬$p ⇒ $x = f(11)))
    >>> print(exhaustively_apply_rules(ALL_RULES, python_string_to_expr('x!=f((0 if p else 1)+10)\n')))
    Math-Module(($p ⇒ $x ≥ f(10) + ε ∨ $x ≤ f(10) - ε) ∧ (¬$p ⇒ $x ≥ f(11) + ε ∨ $x ≤ f(11) - ε))
    >>> print(exhaustively_apply_rules(ALL_RULES, python_string_to_expr('0 if x<y else 1\n')))
    Math-Module(($x ≤ $y - ε ⇒ 0) ∧ ($x ≥ $y ⇒ 1))
    """


def test_opl1():
    r"""
    >>> print(exhaustively_apply_rules(ALL_RULES,
    ...                                python_string_to_expr('cp(area,f1)==(2 if au(area,f1)==0 else 3)\n')))
    Math-Module((au($area, $f1) = 0 ⇒ cp($area, $f1) = 2) ∧ (au($area, $f1) ≥ ε ∨ au($area, $f1) ≤ -(ε) ⇒ cp($area, $f1) = 3))
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=False)

    # print(Comparison(MathVariable(QualifiedName('a')),
    #                  '=',
    #                  apply_rule(IfToImplications(), get_expr('0 if x<y else 1\n'))))
    # print(exhaustively_apply_rules([IfToImplications(), LiftLogicalOperatorOverRightComparison()],
    #                                python_string_to_expr('x==(0 if p else 1)\n')))
    # print(exhaustively_apply_rules([IfToImplications(), LiftLeftImplicationOverComparison(),
    #                                 LiftRightImplicationOverComparison()],
    #                                python_string_to_expr('(0 if p else 1)<(2 if q else 3)\n')))
    ## Math-Module(($p ⇒ $q ⇒ 0 < 2) ∧ ($p ⇒ ¬$q ⇒ 0 < 3) ∧ (¬$p ⇒ $q ⇒ 1 < 2) ∧ (¬$p ⇒ ¬$q ⇒ 1 < 3))
    # print(exhaustively_apply_rules(ALL_RULES, python_string_to_expr('(0 if p else 1)+10\n')))
    # print(exhaustively_apply_rules([IfToImplications(), LiftRightImplicationOverComparison()],
    #                                python_string_to_expr('x==(0 if p else 1)\n')))
    # print(exhaustively_apply_rules(ALL_RULES, python_string_to_expr('f(0 if p else 1, 10)\n')))
    # print(exhaustively_apply_rules(ALL_RULES, python_string_to_expr('x<y\n')))
    # print(exhaustively_apply_rules(ALL_RULES, python_string_to_expr('0 if x<y else 1\n')))
    # print(exhaustively_apply_rules(ALL_RULES,
    #                                python_string_to_expr('cp(area,f1)==(2 if au(area,f1)==0 else 3)\n')))
