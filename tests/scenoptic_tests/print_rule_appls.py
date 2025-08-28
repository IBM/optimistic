from validator2solver.optimistic_rules import IfToImplications, EliminateNegationOfComparison, \
    LiftLeftImplicationOverComparison, LiftRightLogicalOperatorOverComparison, LiftImplicationOverFunctionApplication, \
    LiftRightImplicationOverComparison, LiftLeftLogicalOperatorOverComparison, \
    LiftLogicalOperatorOverFunctionApplication
from rewriting.rules import exhaustively_apply_rules, OrderedRuleSets, RuleSet
from validator2solver.codegen.opl.opl_generator import OplVisitor
from tests.test_rules import get_expr, ALL_RULES


def print_rule_application(rulesets: OrderedRuleSets, python_input: str):
    print()
    print(python_input)
    expr = get_expr(python_input + '\n')
    print(expr)
    result = exhaustively_apply_rules(rulesets, expr, print_intermediate=True)
    code_rep = result.to_code_rep()
    ## Following doesn't work for fragments (unknown functions); always creates function
    # python_code = PythonVisitor('optimistic').full_code(code_rep, '')
    # print('Python:')
    # print(python_code)
    opl_extractor = OplVisitor(cplex=False, allow_undefined_vars=True)
    opl_code = code_rep.accept(opl_extractor).value
    print('OPL:')
    print(opl_code)


RULES_WO_EPSILON = OrderedRuleSets(
    RuleSet(IfToImplications()),
    RuleSet(EliminateNegationOfComparison()),
    RuleSet(LiftLeftImplicationOverComparison(), LiftRightImplicationOverComparison(),
            LiftRightLogicalOperatorOverComparison(), LiftLeftLogicalOperatorOverComparison(),
            LiftImplicationOverFunctionApplication(), LiftLogicalOperatorOverFunctionApplication()))

if __name__ == '__main__':
    print_rule_application(ALL_RULES, '0 if a < b else 1')
    print_rule_application(RULES_WO_EPSILON, '0 if a < b else 1')
    print_rule_application(ALL_RULES, 'x == (0 if a < b else 1)')
    print_rule_application(ALL_RULES, 'x == f(0 if a < b else 1)')
    print_rule_application(ALL_RULES, 'x >= f(0 if a < b else 1) + 10')
