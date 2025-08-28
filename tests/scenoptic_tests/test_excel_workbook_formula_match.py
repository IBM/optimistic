from argparse import ArgumentParser
from pathlib import Path

from scenoptic.excel_analyze_workbook import AnalyzeWorkbook
from scenoptic.excel_to_math import Scenario
from tests.scenoptic_tests.test_excel_formula_match import ScenarioTest

default_excel_file = (
    (Path(__file__).joinpath(
        r'../../scenoptic_examples/user_stories/formula-experiments.xlsx')))
default_sheet = "Spec"

default_scenario = ScenarioTest(default_excel_file, default_sheet)


def run_workbook_match(scenario: Scenario, verbose=False):
    scenario.find_translation_arguments()
    wb_analyze = AnalyzeWorkbook(scenario)
    wb_analyze.analyze(verbose=verbose)
    return wb_analyze


def test_run_workbook_match():
    """
    >>> run_workbook_match(default_scenario, verbose=False)
    WARNING: Unknown argument header: Name
    WARNING: Unknown argument header: Package
    Origin Cell "*worksheet*.Problem.Problem!J2":
      Compatible Cells: [*worksheet*.Problem.Problem!J3, *worksheet*.Problem.Problem!J4]
      Variability: Start -> (1 -> (0 -> (0 -> (0 -> (0 -> (0: (Problem!C2) -> ()))),2 -> (0 -> (0 -> (0: (Problem!D2) -> ())))),2 -> (0 -> (0 -> (0: (Problem!C2) -> ())))))
      Referenced Cells: [Problem!C2, Problem!D2]
    Origin Cell "*worksheet*.Problem.Problem!K2":
      Compatible Cells: [*worksheet*.Problem.Problem!K3, *worksheet*.Problem.Problem!K4, *worksheet*.Problem.Problem!K5, *worksheet*.Problem.Problem!K6]
      Variability: Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (Problem!C2) -> ()))),2 -> (0 -> (0 -> (0: (Problem!E2) -> ())))),2 -> (0 -> (0 -> (0 -> (0: (Problem!E2) -> ()))),2 -> (0 -> (0 -> (0: (Problem!C2) -> ()))))))))
      Referenced Cells: [Problem!C2, Problem!E2]
    Origin Cell "*worksheet*.Problem.Problem!L5":
      Compatible Cells: [*worksheet*.Problem.Problem!L6]
      Variability: Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (Problem!C5) -> ()))),2 -> (0 -> (0 -> (0: (Problem!E5) -> ())))),2 -> (0 -> (1 -> (0 -> (0 -> (0 -> (0: (Problem!E5) -> ()))),2 -> (0 -> (0 -> (0: (Problem!C5) -> ()))))))))))
      Referenced Cells: [Problem!C5, Problem!E5]
    Origin Cell "*worksheet*.inventory.inventory!C2":
      Compatible Cells: [*worksheet*.inventory.inventory!C3, *worksheet*.inventory.inventory!C4]
      Variability: Start -> (1 -> (0 -> (2 -> (2 -> (0 -> (1 -> (0: (inventory!A2) -> ())))))))
      Referenced Cells: [inventory!A2]
    Origin Cell "*worksheet*.inventory.inventory!K2":
      Compatible Cells: [*worksheet*.inventory.inventory!K3, *worksheet*.inventory.inventory!K4, *worksheet*.inventory.inventory!K5, *worksheet*.inventory.inventory!K6]
      Variability: Start -> (1 -> (0 -> (2 -> (0 -> (0 -> (0 -> (0 -> (0: (inventory!H2) -> ())),2 -> (0 -> (0: (inventory!I2) -> ()))))))))
      Referenced Cells: [inventory!H2, inventory!I2]
    <BLANKLINE>
    """


def parse_scenario_test_args(args=None):
    parser = ArgumentParser(description='Generate Java classes from spreadsheet')
    parser.add_argument('-i', '--input-file', type=Path, help='name of spreadsheet file containing problem description')
    parser.add_argument('-s', '--sheet', type=str, help='name of sheet to analyze')
    parsed = parser.parse_args(args)
    return parsed


if __name__ == '__main__':
    import doctest

    doctest.testmod()
