from argparse import ArgumentParser
from cProfile import Profile
from pathlib import Path

from scenoptic.excel_to_optaplanner import run_excel_test


def parse_generate_optaplanner(args=None):
    parser = ArgumentParser(description='Generate Java classes from spreadsheet')
    parser.add_argument('-i', '--input-file', type=Path, help='name of spreadsheet file containing problem description')
    parser.add_argument('-o', '--output-path', type=Path, help='path to output java files')
    parser.add_argument('-s', '--sheet', type=str, help='name of sheet to analyze')
    parser.add_argument('-n', '--name', type=str, default=None, help='base name for Java classes')
    parser.add_argument('-p', '--package', type=str, help='base package for Java classes')
    parser.add_argument('-P', '--profile', type=Path, help='path to file for profiler output')
    parser.add_argument('-c', '--self-contained', default=False, action='store_true',
                        help='all information is in the spreadsheet (now redundant)')
    parsed = parser.parse_args(args)
    # print(f'Parsed args: {parsed}')
    return parsed


if __name__ == '__main__':
    default_excel_file = (
        (Path(__file__).joinpath(
            r'../../../scenoptic_examples/user_stories/Supply-chain-for-OptaPlanner.xlsx')))
    default_java_dir = r'../../../../OptaPlanner/OP-experiments/Generated/src'
    default_java_path = Path(__file__).parent / default_java_dir
    default_sheet = None

    args = parse_generate_optaplanner()
    excel_file = (Path(__file__) / '../../../scenoptic_examples/user_stories' / args.input_file if args.input_file
                  else default_excel_file)
    if not Path(excel_file).exists():
        raise Exception(f'Excel file {Path(excel_file).resolve()} does not exist')
    sheet = args.sheet
    java_base_path = args.output_path or default_java_path
    base_package = args.package
    print(f'OptaPlanner Scenario excel file = {Path.resolve(excel_file).absolute()}')
    print(f'OptaPlanner Scenario excel sheet = {sheet}')
    print(f'OptaPlanner Scenario Java output Path = {Path.resolve(java_base_path).absolute()}')
    if args.profile:
        with Profile() as pr:
            run_excel_test(excel_file, java_base_path, sheet, args.name, base_package)
            pr.print_stats(sort='time')
            pr.dump_stats(args.profile)
    else:
        run_excel_test(excel_file, java_base_path, sheet, args.name, base_package)
