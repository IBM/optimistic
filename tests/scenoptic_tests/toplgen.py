from scenoptic import OplVisitor

from scenoptic.excel_to_opl import cell_to_constraint
from scenoptic.parse_excel import parse_formula
from tests.scenoptic_tests.test_xl_parse import EmptyScenario


def constraint_of(contents):
    abs_rep = parse_formula(contents, EmptyScenario())
    print(abs_rep.describe())
    code = abs_rep.to_code_rep()
    visitor = OplVisitor()
    return code.accept(visitor)


if __name__ == '__main__':
    print(constraint_of('=2*if(1=2, A$3, b4-c5)+if(x5, -1, -2)').value)
    print(constraint_of('=2*if(1=2, if(x5, -1, -2), b4-c5)').value)
    print(cell_to_constraint('abc89', '=if(1=2, A$3, b4-c5)')[0].code.value)
