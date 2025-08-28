from enum import Enum
from pathlib import Path
from inflection import underscore, dasherize, parameterize

from typing import Tuple, Collection, Sequence, Dict, Any, Optional, Union


class ProcessConfigType(Enum):
    ALL = 'ALL'
    GRAPH = 'Graph'
    REGRESSION = 'Regression'
    REGISTRY = 'Registry'
    SOLVER = 'Solver'
    SIMULATE = 'Simulate'


class OptimizationConfigFS:
    def __init__(self,
                 config: Dict[str, Any] = None,
                 working_dir: Optional[str] = None,
                 kind: 'ProcessConfigType' = ProcessConfigType.ALL):
        self.config = config or {}
        self.name = dasherize(parameterize(underscore(self.config.get('name', 'Optimization'))))
        self.debug = self.config.get('debug', False)

        # if kind in (ProcessConfigType.GRAPH,) and not self.config['graph_model']:
        #     raise AttributeError('missing graph model configuration')
        #
        # if kind in (ProcessConfigType.ALL, ProcessConfigType.SOLVER) and not config['target_opl']:
        #     raise AttributeError('missing OPL model configuration')
        # if kind in (ProcessConfigType.ALL, ProcessConfigType.SOLVER) and not config['target_opl']['generated_dir']:
        #     raise AttributeError('missing Model Generation directory')
        self.working_dir = working_dir
        self.generated_path = None
        self.output_any_path = None
        self.file_system_created = False

    #
    # File System Access
    #
    def _create_file_system(self):
        if not self.file_system_created:
            if not self.generated_models_path().exists():
                self.generated_path.mkdir(parents=True, exist_ok=True)
            if not self.output_path().exists():
                self.output_path().mkdir(parents=True)
            self.file_system_created = True

    def _get_root_path(self):
        return self.working_dir or self.config.get('working_dir') or str(Path.cwd())

    def generated_models_path(self) -> Path:
        if not self.generated_path:
            self.generated_path = \
                Path(self._get_root_path()).resolve().joinpath('generated_models', self.name)
        return self.generated_path

    def output_path(self) -> Path:
        if not self.output_any_path:
            self.output_any_path = Path(self._get_root_path()).resolve().joinpath('output', self.name)
        return self.output_any_path

    #
    # Configuration Access
    #
    def value(self, key, default=None):
        return self.config.get(key, default)

    def knowledge_module_config(self, key, default=None) -> Any:
        return self.config.get('target_module', {}).get(key, default)

    def graph_config(self, key, default=None) -> Any:
        return self.config.get('graph_model', {}).get(key, default)

    def opl_config(self, key, default=None):
        return self.config.get('target_opl', {}).get(key, default)

    #
    # Optimization File System Files
    #
    def opl_solution_file(self) -> Path:
        return self.generated_models_path() / f'{self.name}.csv'

    def opl_model_file(self) -> Path:
        return self.generated_models_path() / f'{self.name}.mod'

    def opl_input_file(self):
        return Path.joinpath(self.generated_models_path(), self.name).with_suffix('.dat')

    def opl_template_file(self) -> Path:
        return Path(self.opl_config('template', 'opl_template.txt'))

