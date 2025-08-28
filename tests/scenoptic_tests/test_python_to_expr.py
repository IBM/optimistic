from pathlib import Path

from parsing.python.symbol_default_imports import add_import_frame
from test_utils import Tee
from validator2solver.optimistic_factory import get_target_module_json, create_registry

test_output_dir = '../../test-output/python_to_expr/actual/'
actual_dir = Path(test_output_dir)

# Module: ( File_system_path, requested_module_package, module_file_name, class_problem, config_suffix, do_examples)
_modules = {
    ('../test-data/optimistic/core_mapping', 'experiment', 'internal_problem', 'InternalProblem', '', False),
    # ('../test-data/optimistic/core_mapping', 'experiment', 'internal_problem_39', 'InternalProblem', '', False),
    # ('../optimistic_examples/room_allocation', 'experiment', 'room_allocation_bom_8', 'RoomAllocationProblem8', '', True),
    # ('../optimistic_examples/room_allocation', 'experiment', 'room_allocation_bom_8', 'RoomAllocationProblem8_a', '', True),
    # ('../optimistic_examples/room_allocation', 'experiment', 'room_allocation_bom_9', 'RoomAllocationProblem9', '', False),
}


def _config(test_path,
            optimization_file,
            module_name,
            name=None,
            working_dir=None):
    config = {
        'name': name or 'Python_To_Expr',
        'working_dir': working_dir or '',
        'target_module': get_target_module_json(str(test_path), str(optimization_file), module_name=module_name)[
            'target_module'],
        'target_opl': {
            # 'template_kind': 'pkg',
            # 'template': 'room_allocation_knowledge_opl_template.txt',
            # "template_pkg": {
            #     'package_name': 'optimistic_process',
            #     'package_path': 'templates',
            #     'encoding': 'utf-8'
            # }
        },
        'symbol_table_config': {
            'enable_code_testing': False,
            'disable_imports_mockup': True,
            'enable_attribute_analysis': False,
            'debug': False,
        },
    }
    return config


def _requested_module_package_name(experiment):
    return f'{experiment[1]}.{experiment[2]}'


def _requested_module_file_path(experiment):
    return f'{experiment[0]}/{experiment[2]}.py'


def _load_module(experiment):
    import sys
    from importlib.util import spec_from_loader, module_from_spec
    from importlib.machinery import SourceFileLoader

    spec = spec_from_loader(_requested_module_package_name(experiment),
                            SourceFileLoader(_requested_module_package_name(experiment),
                                             _requested_module_file_path(experiment)))
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        try:
            del sys.modules[spec.name]
        except KeyError:
            pass
    problem_model = getattr(module, experiment[3])
    # print(problem_model.__module__)
    # print(dir(module))
    # print(sys.modules)
    # employee_model = getattr(module, 'EmployeeData')
    # instance = problem_model({employee_model(33, 'A'), employee_model(55, 'A')}, 455)
    # print(instance.students_score)
    return problem_model


def run_all_modules():
    for experiment in _modules:
        # _load_module(experiment)
        file_path = Path(_requested_module_file_path(experiment)).resolve()
        config = _config(str(file_path.parent),
                         file_path,
                         _requested_module_package_name(experiment))
        print(config)
        test_math_module_expr_creation(experiment, config)


def test_math_module_expr_creation(experiment, config):
    registry = create_registry(config=config,
                               builtin_frame=add_import_frame(do_examples=experiment[5]),
                               print_translations=True)

    file_path = Path(_requested_module_file_path(experiment)).resolve()
    outputFile = actual_dir.joinpath(str(file_path.stem) + "_expr.log")
    test_tee = Tee(outputFile)

    with test_tee:
        for candidate in registry:
            for module in candidate:
                expr = candidate[module]['model']
                print(f'Module [{module}] - Expression: \n{expr}\n\n')


if __name__ == '__main__':
    run_all_modules()
