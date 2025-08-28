from pathlib import Path

from scenoptic.excel_to_math import Scenario


def test_sheet(xl_file, sheet_name):
    s = Scenario(str(Path(__file__).joinpath(xl_file)), sheet_name)
    s.find_translation_arguments()
    print(f'{s.parameters=}')
    print(f'{s.objectives=}')
    for name, type in s.types.items():
        print(f'{name}: {type}')


if __name__ == '__main__':
    op_xl_file = r'../../../scenoptic_examples/user_stories/Supply-chain-for-OptaPlanner.xlsx'
    test_sheet(op_xl_file, 'S>s bool self-contained V2')
    print('----------')
    test_sheet(op_xl_file, 'Non-neg self-contained V2')
