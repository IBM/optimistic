from test.test_room_alloc_to_opl import run_opl_tests

tests = {'variable-representation/var_rep_opt_example1.py': {'run': True, 'suffix': 'var-rep-1', 'with_imports': False}}
test_output_dir = '../../test-output/var-rep/'

if __name__ == '__main__':
    run_opl_tests(tests, test_output_dir, debug=False, opl_implementer_params=dict(use_legal_solution_var=False))
