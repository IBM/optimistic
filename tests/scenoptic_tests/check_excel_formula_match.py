from pathlib import Path

from tests.scenoptic_tests.test_excel_formula_match import run_all_formula_expr, ScenarioTest, default_excel_file, \
    parse_scenario_test_args

if __name__ == '__main__':
    args = parse_scenario_test_args()
    excel_file = (Path(__file__).parent.joinpath(args.input_file).resolve() if args.input_file
                  else default_excel_file)
    if not Path(excel_file).exists():
        raise Exception(
            f'Excel file {Path(excel_file).resolve()} does not exist')
    sheet = args.sheet
    test_scenario = ScenarioTest(excel_file, sheet)
    # print(f'Testing Formula Matching')
    # run_all_formula_match(test_scenario)
    print('Testing Formula to Expression')
    run_all_formula_expr(test_scenario, verbose=True)  # , indexes=(5,))
