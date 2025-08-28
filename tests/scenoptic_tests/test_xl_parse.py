from typing import Optional

from scenoptic import OplVisitor

from scenoptic.excel_data import ExcelData, CellType
from scenoptic.parse_excel import parse_formula


class EmptyScenario(ExcelData):
    def get_type(self, cell: str) -> Optional[CellType]:
        return None

    def cell_value(self, row, col, req_type=None, sheet=None, cast_to=None, empty_values=()):
        return None


def formula_to_opl(formula):
    abs_rep = parse_formula(formula, EmptyScenario())
    print(abs_rep.describe())
    code = abs_rep.to_code_rep()
    visitor = OplVisitor()
    return code.accept(visitor).value


if __name__ == '__main__':
    if False:
        # print(describe_formula('ab'))
        print(describe_formula('0'))
        print(describe_formula('"foo"'))
        print(describe_formula('"foo""bar"'))
        print(describe_formula('TRUE'))
        print(describe_formula('FALSE'))
        # print(parse_formula('#VALUE!'))
        print(describe_formula('=-10'))
        print(describe_formula('=2-10*5+99'))
        print(describe_formula('=(2-10)*(5+99)'))
        print(describe_formula('="a" & " b "'))
        print(describe_formula('=1 < 2'))
        print(describe_formula('=1 <= 2'))
        print(describe_formula('=1 > 2'))
        print(describe_formula('=1 >= 2'))
        print(describe_formula('=1 <> 2'))
        print(describe_formula('=and(A1 <> 2^3, 1=2%)'))
        print(describe_formula('=A1 : B2 * C3: D4'))
        print(describe_formula('=a_range + C:AA + 31:32'))

    if True:
        # print(describe_formula('Foo'))
        print(formula_to_opl('="Foo"'))
        print(formula_to_opl('0'))
        print(formula_to_opl('=0'))
        print(formula_to_opl('=1+(2*5)'))
        print(formula_to_opl('=(1+2)*5'))
        print(formula_to_opl('=AND (TRUE, FALSE)'))
        print(formula_to_opl('=-1<>1'))
        print(formula_to_opl('=A4 <= 5'))
        print(formula_to_opl('=$A$4:C7'))
        print(formula_to_opl('=sum($A$4:C7)'))
        print(formula_to_opl('=max($A$4:C7)'))
        print(formula_to_opl('=sum($A$4:A7)'))
        print(formula_to_opl('=max($A$4:A7)'))
        print(formula_to_opl('=sum($A$4:C4)'))
        print(formula_to_opl('=max($A$4:C4)'))
        print(formula_to_opl('=if(1=2, A$3, b4-c5)'))
