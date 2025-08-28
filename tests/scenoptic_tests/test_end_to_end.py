import sys

from test_process.execute import EndToEnd
from pathlib import Path
from optimistic_client.config import configuration


# config = configuration.config()

# DEFAULT_CONFIG = {
#         'directory': {
#             'samples': r'..\optimistic_samples',
#             'actual': r'..\optimistic_samples_actual',
#             'expected': r'..\optimistic_samples_expected',
#             'regression': r'..\optimistic_samples_regression'
#         },
#         'files': [],
#         'raise_exception': False,
#         'create_opl': True,
#         'create_python': True,
#         'regression_diff': True,
#         'print_results': False,
#         'print_one_line': False,
#          'symbol_table_config': {
#             'enable_code_testing': False,
#             'disable_imports_mockup': True,
#             'enable_attribute_analysis': False,
#             'debug': False
#         }
#     }


def get_config(filePath=None):
    aconfig = configuration.config()
    if filePath:
        aconfig.reset()
        target = Path(filePath).resolve()
        print(f'Loading configuration: {target}')
        configuration.init_from_file(target)
    return aconfig


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # config = get_config(r'..\\optimistic_dev.yaml')
        config = get_config(sys.argv[1])
    else:
        config = get_config()

    SAMPLES_DIR = config.get('test_e2e.directory.samples')
    ACTUAL_DIR = config.get('test_e2e.directory.actual')
    EXPECTED_DIR = config.get('test_e2e.directory.expected')
    REGRESSION_DIR = config.get('test_e2e.directory.regression')

    if not Path(SAMPLES_DIR).exists():
        raise Exception(f'Samples directory not found: {Path(SAMPLES_DIR).resolve()}')

    # Create directories if they does not exists
    if not Path(ACTUAL_DIR).exists():
        Path(ACTUAL_DIR).mkdir(parents=True, exist_ok=True)

    if not Path(EXPECTED_DIR).exists():
        Path(EXPECTED_DIR).mkdir(parents=True, exist_ok=True)

    if not Path(REGRESSION_DIR).exists():
        Path(REGRESSION_DIR).mkdir(parents=True, exist_ok=True)

    for path in sorted(Path(SAMPLES_DIR).glob('*.py')):
        # - All files if `config['files']` is empty
        # - Otherwise, only the selected files in the config['files']
        files = config.get('test_e2e.files')
        if not files or not files[0]:
            files = []
        if path.is_file() and path.name in files or not files:
            task = EndToEnd(config, path)
            task.execute()
