from argparse import ArgumentParser
from pathlib import Path

from scenoptic.excel_to_opl import run_excel_test


def parse_generate_opl(args=None):
    parser = ArgumentParser(description='Generate Java classes from spreadsheet')
    parser.add_argument('-i', '--input-file', type=Path, help='name of spreadsheet file containing problem description')
    parser.add_argument('-o', '--output-mod-file', type=Path, help='path to output OPL model file')
    parser.add_argument('-s', '--sheet', type=str, help='name of sheet to analyze')
    parser.add_argument('-c', '--self-contained', default=False, action='store_true',
                        help='all information is in the spreadsheet')
    parsed = parser.parse_args(args)
    # print(f'Parsed args: {parsed}')
    return parsed


if __name__ == '__main__':
    default_excel_file = (
        str(Path(__file__).joinpath(
            r'../../../scenoptic_examples/user_stories/Supply-chain-for-OptPlanner-OPL.xlsx')))
    default_mod_file = Path(__file__).parent / '../../../test-output/scenoptic/actual/gen-supply-opl.mod'
    default_sheet = 'Business Model Optimization s,S'

    args = parse_generate_opl()
    excel_file = str(Path(__file__).joinpath(args.input_file or default_excel_file).resolve())
    if not Path(excel_file).exists():
        raise Exception(f'Excel file {excel_file} does not exist')
    sheet = args.sheet or default_sheet
    mod_file = str(Path(__file__).parent.joinpath(args.output_mod_file or default_mod_file).resolve())
    print(f'Opl Scenario excel file = {excel_file}')
    print(f'Opl Scenario excel sheet = {sheet}')
    print(f'Opl Scenario generated mod file = {mod_file}')
    run_excel_test(excel_file, mod_file, sheet)
