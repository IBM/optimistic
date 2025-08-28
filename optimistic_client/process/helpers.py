from dataclasses import fields

from optimistic_client.load.analyze_total_mapping import AnalyzeTotalMapping
from optimistic_client.load.loader import create_problem_instance
from optimistic_client.load.verify_model_field_types import VerifyModelFieldTypes
from optimistic_client.load.verify_column_mapping import VerifyColumnMapping


def run_solution(name,
                 cls,
                 input_files_dict,
                 column_mapping=None,
                 verbose=False):
    verify_field_types = VerifyModelFieldTypes(cls)
    verify_field_types.verify()
    verify_field_types.report()

    verify_col_names = VerifyColumnMapping(cls, input_files_dict, column_mapping)
    is_col_ok = verify_col_names.verify()
    verify_col_names.report()

    if not is_col_ok:
        print(f'Aborting, issues with column mapping, please fix...')
        return None

    #
    # Load CSV data into Total Mapping dictionary objects
    #
    _problem = create_problem_instance(cls,
                                       input_files_dict,
                                       column_mapping)

    analyze = AnalyzeTotalMapping(cls,
                                  input_files_dict,
                                  column_mapping,
                                  verbose=True)
    analyze.analyze(_problem)
    analyze.report()

    if verbose:
        for field in fields(cls):
            print(f'{field.name}:\n {getattr(_problem, field.name)}')
    return _problem
