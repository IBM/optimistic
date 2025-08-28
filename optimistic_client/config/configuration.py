import copy
import os
from typing import Text

import yaml


class ConfigIsInitializedException(Exception):
    pass


class ConfigIsNotInitializedException(Exception):
    pass


def config():
    return CONFIG


class _Configuration:
    def __init__(self):
        self._config = None

    def load(self, yaml_as_string):
        """Populates the config object with variables defined in yaml_as_string.
            Args:
                yaml_as_string: yaml text to load.
            Raises:
              ConfigIsInitializedException: if global config is already initialized.
                  Call `reset` before being able to `load` again.
              yaml.scanner.ScannerError: if the yaml text is incorrect.
        """
        if self._config is not None:
            raise ConfigIsInitializedException()

        # self._items = yaml.safe_load(yaml_as_string) or {}
        self._config = yaml.load(yaml_as_string, Loader=yaml.FullLoader) or {}

    def get(self, keys: Text = '', default=None):
        """Gets the value for given configuration key sequence.
        The sequence is searched as nested hierarchy of keys.
        For example:
          Given a YAML string with content:
          Parent:
            child: value
          `get('Parent.child')` would return `value`.
          `get('Parent')` returns {'child': 'value'}
          `get()` returns {'Parent', {'child': 'value'}}
        Args:
          keys: keys separated by dots, and treated as tuple
          default: returns default value if key does not exists
        Returns:
          the key value, if does not exists returns the default
        Raises:
          KeyError: if key does not exists, and `default` is not set
          ConfigIsNotInitializedException: if the global config hasn't been
              initialized yet.
        """
        if self._config is None:
            raise ConfigIsNotInitializedException()

        value_tree = self._config
        theKeys = keys.strip().split('.')
        for key in theKeys:
            if not isinstance(value_tree, dict) or key not in value_tree:
                if default is not None:
                    return default
                elif key == '':
                    break
                else:
                    raise KeyError(f'[{key}] - key is missing.')

            value_tree = value_tree.get(key)

        return copy.deepcopy(value_tree)

    def reset(self):
        """Resets the configuration
        Allows to load new configuration into the same object
        """
        self._config = None


def init_from_file(file_name):
    """Populates global config with contents of file_name
        Make sure the CONFIG instance is `reset` before loading new file.
    Args:
        file_name: The YAML config file
    Raises:
        OSError: if file_name does not exist or is a directory.
        ConfigIsInitializedException: if global config is already initialized.
        Call `reset` before being able to `init` again.
        yaml.scanner.ScannerError: if the yaml file is formatted incorrectly.
    """
    if not os.path.isfile(file_name):
        # raise IOError('File not found: %s' % file_name)
        print(f'Configuration File not found: {file_name}')
        return

    with open(file_name, 'r') as f:
        contents = ''.join(f.readlines())

    init(contents)


# Use the following if you get a YAML string, e.g. from database record
def init(yaml_as_string):
    CONFIG.load(yaml_as_string)


# Singleton - Global Config instance
default_filepath = '../optimistic_default.yaml'
CONFIG = _Configuration()
init_from_file(default_filepath)


def main():
    CONFIG.reset()
    print(os.getcwd())
    print("Loading default YAML file:")

    init_from_file(default_filepath)

    # Since the `optimistic_default.yaml` may be changed by developer,
    # We can expect the following to produce different resutls
    test_main()
    CONFIG.reset()

    print("\nLoading STRING YAML:")
    # Since we use local string, immutable, the results here are always repeatable
    yaml_as_string = (
        "directory: \n"
        "  samples: '../test-data/optimistic/samples' \n"
        "  actual: '../test-output/optimistic/actual'\n"
        "  expected: '../test-output/optimistic/expected'\n"
        "  regression: '../test-output/optimistic/regression'\n"
        "files:\n"
        "raise_exception: False\n"
        "create_opl: True\n"
        "create_python: True\n"
        "regression_diff: True\n"
        "print_results: False\n"
        "print_one_line: False\n")
    print(f'YAML AS STRING\n{yaml_as_string}')
    init(yaml_as_string)
    test_main()


def test_main():
    print(f'create_opl = {CONFIG.get("create_opl")}')
    print(f'samples = {CONFIG.get("directory.samples")}')
    try:
        print(f'missing = {CONFIG.get("missing")}')
    except KeyError as e:
        print(f'missing = Exception {e}')
    print(f'missing(with default) = {CONFIG.get("missing", True)}')

    # Validate that a `False` boolean value is treated as such
    print_results = CONFIG.get('print_results')
    if print_results:
        print(f'print_results = Exception Actual Value [{print_results}], Expecting it to behave as boolean [False]')
    else:
        print(f'print_results = {print_results}')

    # Validate that a `True` boolean value is treated as such
    regression_diff = CONFIG.get('regression_diff')
    if regression_diff:
        print(f'regression_diff = {regression_diff}')
    else:
        print(f'regression_diff = Exception Actual Value [{regression_diff}], Expecting it to behave as boolean [True]')

    print(f'Entire YAML = {CONFIG.get()}')


if __name__ == '__main__':
    main()
