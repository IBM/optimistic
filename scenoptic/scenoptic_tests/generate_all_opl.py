from argparse import ArgumentParser
from pathlib import Path

from scenoptic.excel_to_opl import run_excel_test

TESTS = dict(bool=dict(sheet='S>s bool self-contained V2'),
             nonneg=dict(sheet='Non-neg self-contained V2'),
             sumif=dict(sheet='Non-neg SUMIF V2'),
             sumifs=dict(sheet='Non-neg SUMIFS V2'),
             countifs=dict(sheet='Non-neg COUNTIFS V2'),
             complex=dict(book='aggregate-tests.xlsx', sheet='Complex-expressions'),
             simplified=dict(book='aggregate-tests.xlsx', sheet='Simplified'),
             # aggregate=dict(book='aggregate-tests.xlsx', sheet='Sheet1'),
             # scalars=dict(book='aggregate-tests.xlsx', sheet='Scalars')
             )


def parse_generate_opl(args=None):
    parser = ArgumentParser(description='Generate OPL code from spreadsheet')
    parser.add_argument('-o', '--output-path', type=Path, help='path to output java files')
    parser.add_argument('-t', '--test', type=str, action='append', help='test name(s) to perform')
    parsed = parser.parse_args(args)
    return parsed


if __name__ == '__main__':
    default_excel_file = (
        (Path(__file__).joinpath(
            r'../../../scenoptic_examples/user_stories/Supply-chain-for-OptaPlanner.xlsx')))
    default_opl_dir = r'../../test-output/scenoptic'
    default_opl_path = Path(__file__).parent / default_opl_dir / 'actual'

    command_args = parse_generate_opl()
    opl_base_path = command_args.output_path or default_opl_path

    for name, args in TESTS.items():
        if command_args.test and name not in command_args.test:
            continue
        print(f'Generating code for {name}...')
        excel_file = (Path(__file__) / '../../../scenoptic_examples/user_stories' / args['book'] if 'book' in args
                      else default_excel_file).resolve()
        sheet = args['sheet']
        mod_file = (opl_base_path / f'gen-{name}-opl.mod').resolve()
        print(f'Opl Scenario excel file = {excel_file}')
        print(f'Opl Scenario excel sheet = {sheet}')
        print(f'Opl Scenario generated mod file = {mod_file}')
        run_excel_test(excel_file, mod_file, sheet)
    print('Done.')
