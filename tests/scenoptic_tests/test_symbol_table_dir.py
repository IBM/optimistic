import os
from pathlib import Path

from parsing.python.symbol_default_imports import add_import_frame
from test_utils import Tee
from validator2solver.optimistic_factory import analyze_symbol_table_from_file, get_target_module_json, \
    generate_symbol_table_package, describe, plan_symbol_table_order

test_output_dir = '../../test-output/symbol_table_dir/actual/'
actual_dir = Path(test_output_dir)
test_root_dir = Path.resolve(Path.joinpath(Path(__file__), '../../..'))


def do_test(filePath, builtin_frame):
    filename = os.path.basename(filePath)

    if filename.endswith(".py"):
        module_name = filename[:-3]
    outputFile = actual_dir.joinpath(str(module_name) + "_symbol_table.log")
    test_tee = Tee(outputFile)

    config = {
        'symbol_table_config': {
            'enable_code_testing': False,
            'disable_imports_mockup': True,
            'enable_attribute_analysis': False,
            'debug': False,
        },
        'target_module': get_target_module_json(test_root_dir, filePath)['target_module']
    }

    registry, existing, priority = analyze_symbol_table_from_file(config=config, print_translations=True)

    planned_registry, planned_priority = plan_symbol_table_order(registry, priority)

    symbol_registry, symbol_visitor = generate_symbol_table_package(planned_registry, config=config,
                                                                    builtin_frame=builtin_frame,
                                                                    print_translations=True)
    with test_tee:
        print(f'File: {filename} {config["target_module"]["module_name"]}\n')
        print(f'Existing {sorted(existing)}')
        print(f'Priority {priority}')
        print(f'Registry {registry}')
        print(f'Topological Sort {planned_priority}')
        print(f'Planned Registry -{planned_registry}')
        print(f'Symbol Registry -{symbol_registry}')
        print(f'Symbol Table builtin frame')
        describe(describe(symbol_visitor.builtin_frame))
        print('Frame Imports:')
        for akey, avalue in symbol_visitor.imports.items():
            print(f'   {akey} -> {avalue}')


tests = {'samples/symbol_table/pkg/test_pkg_01.py': {'run': False, 'builtin': add_import_frame(do_examples=False)},
         'samples/symbol_table/pkg/test_pkg_02.py': {'run': False, 'builtin': add_import_frame(do_examples=False)},
         'samples/symbol_table/pkg/test_pkg_03.py': {'run': True, 'builtin': add_import_frame(do_examples=False)}
         }

if __name__ == '__main__':
    for key, value in tests.items():
        if value['run']:
            do_test(key, value['builtin'])
