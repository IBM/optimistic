from argparse import ArgumentParser
from pathlib import Path

from scenoptic.excel_to_optaplanner import ScenarioForOptaPlanner

TESTS = dict(bool=dict(sheet='S>s bool self-contained V2'),
             nonneg=dict(sheet='Non-neg self-contained V2'),
             sumif=dict(sheet='Non-neg SUMIF V2'),
             sumifs=dict(sheet='Non-neg SUMIFS V2'),
             countifs=dict(sheet='Non-neg COUNTIFS V2'),
             complex=dict(book='aggregate-tests.xlsx', sheet='Complex-expressions'),
             simplified=dict(book='aggregate-tests.xlsx', sheet='Simplified'),
             aggregate=dict(book='aggregate-tests.xlsx', sheet='Sheet1'),
             scalars=dict(book='aggregate-tests.xlsx', sheet='Scalars'))


def parse_generate_optaplanner(args=None):
    parser = ArgumentParser(description='Generate Java classes from spreadsheet')
    parser.add_argument('-o', '--output-path', type=Path, help='path to output java files')
    parsed = parser.parse_args(args)
    return parsed


if __name__ == '__main__':
    default_excel_file = (
        (Path(__file__).joinpath(
            r'../../../scenoptic_examples/user_stories/Supply-chain-for-OptaPlanner.xlsx')))
    default_java_dir = r'../../../../OptaPlanner/OP-experiments/Generated/src'
    default_java_path = Path(__file__).parent / default_java_dir

    args = parse_generate_optaplanner()
    java_base_path = args.output_path or default_java_path

    for name, args in TESTS.items():
        print(f'Generating code for {name}...', end=' ')
        excel_file = (Path(__file__) / '../../../scenoptic_examples/user_stories' / args['book'] if 'book' in args
                      else default_excel_file)
        s = ScenarioForOptaPlanner(None, None, excel_file, sheet=args['sheet'])
        s.build()
        s.to_java(java_base_path)
        print('Done.')
