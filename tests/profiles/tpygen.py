import os
from pathlib import Path

from codegen.abstract_rep import AttributeAccess, VariableAccess, ComparisonExpr, SetExpr, NumberExpr, \
    StringExpr, SetMembershipExpr
from validator2solver.python.python_generator import PythonVisitor
from eco_profiles.profiles_expr import PythonVisitorForProfiles
from math_rep.constants import LE_SYMBOL
from eco_profiles.parse_profiles import parse_profile_string, ProfileExtractor


def abstest():
    pv = PythonVisitor('abstext')
    attr1 = AttributeAccess('baz', AttributeAccess(['foo', 'bar'], VariableAccess(['var', 'iable'])))
    attr2 = AttributeAccess(['flight', 'number'], VariableAccess('leg1', 'Leg'))
    comp1 = ComparisonExpr(attr1, LE_SYMBOL, attr2)
    print(comp1.accept(pv))
    comp2 = SetExpr([VariableAccess('foo'), NumberExpr(3), StringExpr('LY001')])
    comp3 = SetMembershipExpr(VariableAccess('bar'), comp2)
    print(comp3.accept(pv))
    # for imp in comp2.imports:
    #     print(str(imp))


def e2etest(profile, line=None, code_dir=None, silent=False):
    if line:
        line_str = f' {line}'
    else:
        line_str = ''
    if not silent:
        print(f'***Text{line_str}: {profile}')
    tree, parser = parse_profile_string(profile)
    flat = tree.toStringTree(recog=parser).strip()
    if not silent:
        print(f'>>>Parsed{line_str}: {flat}')
    extractor = ProfileExtractor()
    abst = extractor.visit(tree)
    actual_paraphrase = abst.describe()
    if not silent:
        print(f'===Paraphrase{line_str}: {actual_paraphrase}')
    abst_code = abst.to_code_rep()
    pv = PythonVisitorForProfiles(f'profile{line}')
    code = pv.full_code(abst_code, actual_paraphrase)
    if code_dir:
        with open(os.path.join(code_dir, f'profile{line}.py'), 'w', encoding='utf8') as code_file:
            print(code, file=code_file)
    else:
        print(code)
    # code = abst_code.accept(pv)
    # print(f'<<<Code{line_str}:\n{code.fragment}')
    # imports = pv.pretty_imports()
    # if imports:
    #     print(f'+++Imports{line_str}: {imports}')
    # funcs = pv.pretty_helpers()
    # if funcs:
    #     print(f'@@@Functions{line_str}:\n{funcs}')


def test_profile(base_dir, profile_file, only_line=None, subdir='pygen/actual', silent=False) -> Path:
    line = 0
    with open(profile_file, 'r', encoding='utf8') as test_file:
        while True:
            try:
                profile = next(test_file).strip()
                ref = next(test_file).strip()
                paraphrase = next(test_file).strip()
            except Exception:
                break
            line += 1
            if only_line and line < only_line:
                continue
            elif only_line and line > only_line:
                break
            tree, parser = parse_profile_string(profile)
            flat = tree.toStringTree(recog=parser).strip()
            extractor = ProfileExtractor()
            actual_paraphrase = extractor.visit(tree).describe()
            output_dir = base_dir / subdir
            e2etest(profile, line=line, code_dir=output_dir, silent=silent)
    return output_dir


def run_text_tests():
    abstest()
    e2etest('the flight number of d1 is no greater than the flight-number of d2')
    e2etest('the flight number of d1 is different from 203')
    e2etest('the flight number of d1 is different from "203"')
    e2etest('the flight number of d1 is not "203"')
    e2etest('d1 is in {"LY001", "LY002"}')
    e2etest('for all Leg l2 in d1, the type of l2 is not "Travel"')
    e2etest('the sum of the duration of l1 for all Legs l1 in d1 '
            'such that the type of l1 is in {"Flight", "Travel", "Other-carrier", "Simulator"}'
            'is 1')
    e2etest('the sum of the duration of l1 for all Legs l1 in d1 '
            'such that the type of l1 is in {"Flight", "Travel", "Other-carrier", "Simulator"} '
            'is between 12.01 and 14')
    e2etest('the intersection of l1 and l2 is 1')
    e2etest('the length of (the intersection of the period of l1 and 08:00-20:00) is at least 20% of 12')


def test_all_profiles(silent=False):
    base_dir = (Path(__file__).parent.parent.parent / r'test-output').absolute()
    input_file = (base_dir / r'pygen/input-profiles.txt').absolute()
    return test_profile(base_dir, input_file, silent=silent)  # , only_line=18)


if __name__ == '__main__':
    # run_text_tests()
    test_all_profiles()
