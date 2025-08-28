from pathlib import Path

from tests.scenoptic_tests.test_excel_formula_match import parse_scenario_test_args, default_excel_file, ScenarioTest
from tests.scenoptic_tests.test_excel_workbook_formula_match import run_workbook_match

args = parse_scenario_test_args()
excel_file = (Path(__file__).parent.joinpath(args.input_file).resolve() if args.input_file
              else default_excel_file)
if not Path(excel_file).exists():
    raise Exception(
        f'Excel file {Path(excel_file).resolve()} does not exist')
sheet = args.sheet
test_scenario = ScenarioTest(excel_file, sheet)
print(f'Testing Workbook Formula Matching')
print(run_workbook_match(test_scenario, verbose=True))
