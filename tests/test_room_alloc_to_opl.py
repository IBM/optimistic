from pathlib import Path
from typing import Mapping

import sys

from validator2solver.opt_to_opl import OptimizationModelOplImplementer
from validator2solver.optimistic_factory import get_target_module_json
from validator2solver.optimization_analyzer import OptimizationProblemAnalyzer
from validator2solver.python.symbol_default_imports import add_import_frame

test_output_dir = '../../optimistic/test-output/room-allocation/actual/'


def test_optimization_problem(optimization_file, file_suffix, test_output_dir: Path, test_root_dir: Path,
                              builtin=False, with_imports=False, only_heur=False,
                              opl_implementer_params: Mapping[str, object] = None, module_name=None):
    config = {
        'symbol_table_config': {
            'enable_code_testing': False,
            'disable_imports_mockup': True,
            'enable_attribute_analysis': False,
            'debug': False,
        },
        'target_module': get_target_module_json(test_root_dir, optimization_file, module_name)['target_module']
    }

    builtin_frame = (builtin if builtin else
                     add_import_frame(do_examples=False) if with_imports
                     else add_import_frame(do_examples=True))
    analyzer_h = OptimizationProblemAnalyzer()
    analyzer_h.from_python_file(config=config, builtin_frame=builtin_frame, with_imports=with_imports)
    opl_h = OptimizationModelOplImplementer(analyzer_h, use_type_heuristic=True, **(opl_implementer_params or {}))

    with open(test_output_dir / f'types-{file_suffix}.txt', 'w', encoding='utf-8') as f:
        print(analyzer_h._domain_table.describe(), file=f)
    with open(test_output_dir / f'opl-heur-{file_suffix}.txt', 'w', encoding='utf-8') as f:
        print(opl_h.full_implementation_to_opl(), file=f)

    if not only_heur:
        analyzer_no_h = OptimizationProblemAnalyzer()
        analyzer_no_h.from_python_file(config=config, builtin_frame=builtin_frame, with_imports=with_imports)
        opl_no_h = OptimizationModelOplImplementer(analyzer_no_h, use_type_heuristic=False)

        with open(test_output_dir / f'opl-no-heur-{file_suffix}.txt', 'w', encoding='utf-8') as f:
            print(opl_no_h.full_implementation_to_opl(), file=f)
    return opl_h


room_allocation_tests = {
    'optimistic_examples/room_allocation/room_allocation_bom_4.py': {
        'run': True, 'suffix': '4', 'with_imports': False},
    'optimistic_examples/room_allocation/room_allocation_bom_5_all_in_one.py': {
        'run': True, 'suffix': '5in1', 'with_imports': False},
    'optimistic_examples/room_allocation/room_allocation_bom_6_all_in_one.py': {
        'run': True, 'suffix': '6in1', 'with_imports': False},
    'optimistic_examples/room_allocation/room_allocation_bom_7.py': {
        'run': True, 'suffix': '7', 'with_imports': True},
    'optimistic_examples/room_allocation/room_allocation_bom_8.py': {
        'run': True, 'suffix': '8', 'with_imports': True},
    'optimistic_examples/room_allocation/room_allocation_bom_8_a.py': {
        'run': True, 'suffix': '8_a', 'with_imports': True},
    'optimistic_examples/room_allocation/room_allocation_bom_9.py': {
        'run': True, 'suffix': '9', 'with_imports': True}
}


def run_opl_tests(tests, test_output_dir, test_root_dir: Path, debug=False, only_heur=True,
                  opl_implementer_params: Mapping[str, object] = None, module_name=None):
    for key, value in tests.items():
        if value['run']:
            builtin_frame = value['builtin'] if value.get('builtin', False) else False
            test_optimization_problem(key, file_suffix=value.get('suffix', 'def'), test_output_dir=test_output_dir,
                                      test_root_dir=test_root_dir,
                                      builtin=builtin_frame, with_imports=value.get('with_imports', False),
                                      only_heur=only_heur, opl_implementer_params=opl_implementer_params,
                                      module_name=module_name)


def debug_5_no_heur(test_output_dir):
    file_suffix = '5in1'
    optimization_file = 'room_allocation_bom_5_all_in_one.py'
    analyzer = OptimizationProblemAnalyzer()
    analyzer.from_python_file('room_allocation/' + optimization_file)
    opl_no_h = OptimizationModelOplImplementer(analyzer, use_type_heuristic=False)
    with open(test_output_dir + f'opl-no-heur-{file_suffix}.txt', 'w', encoding='utf-8') as f:
        print(opl_no_h.full_implementation_to_opl(), file=f)


def main():
    if len(sys.argv) > 1:
        actual_tests = {k: v for k, v in room_allocation_tests.items() if v['suffix'] in sys.argv[1:]}
    else:
        actual_tests = room_allocation_tests
    test_root_dir = Path(__file__).parent.parent.parent / 'optimistic' / 'optimistic-examples'
    run_opl_tests(actual_tests, test_output_dir, test_root_dir=test_root_dir, debug=False)


if __name__ == '__main__':
    # debug_5_no_heur()
    main()
