from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Sequence, Optional
from jinja2 import Environment, FileSystemLoader, Template, BaseLoader, PackageLoader

from optimistic_process.config import OptimizationConfigFS


class ArtifactsOPL(ABC):
    #
    # Optimization Artifacts
    #
    @abstractmethod
    def id_optimization_solution(self):
        pass

    @abstractmethod
    def reset_optimization_solution(self):
        pass

    @abstractmethod
    def store_optimization_solution(self, prepared: Sequence[str]):
        pass

    @abstractmethod
    def load_optimization_solution(self):
        pass

    @abstractmethod
    def id_opl_dat(self):
        pass

    @abstractmethod
    def reset_opl_dat(self):
        pass

    @abstractmethod
    def store_opl_dat(self, prepared: Sequence[str]):
        pass

    @abstractmethod
    def load_opl_dat(self):
        pass

    @abstractmethod
    def id_opl_mod(self):
        pass

    @abstractmethod
    def reset_opl_mod(self):
        pass

    @abstractmethod
    def store_opl_mod(self, prepared: Sequence[str]):
        pass

    @abstractmethod
    def load_opl_mod(self):
        pass

    @abstractmethod
    def load_opl_template(self) -> Template:
        pass


class OptimizationModelOPLArtifactsFileSystem(ArtifactsOPL):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = OptimizationConfigFS(config)
        self.file_system_created = False

    #
    # File System utilities
    #
    def _create_file_system(self):
        if not self.file_system_created:
            if not self.config.generated_models_path().exists():
                self.config.generated_path.mkdir(parents=True, exist_ok=True)
            if not self.config.output_path().exists():
                self.config.output_path().mkdir(parents=True)
            self.file_system_created = True

    def _store(self, path, prepared):
        self._create_file_system()
        with path.open(mode='w', encoding='utf-8') as f:
            for data in prepared:
                _ = f.write(f'{data}\n')

    def _load(self, path):
        self._create_file_system()
        lines = []
        if path.exists():
            lines = path.read_text().splitlines()
        return lines

    def _reset(self, path):
        self._create_file_system()
        if path.exists():
            path.unlink()

    #
    # Optimization Artifacts
    #
    def id_optimization_solution(self):
        return self.config.opl_solution_file()

    def reset_optimization_solution(self):
        self._reset(self.id_optimization_solution())

    def store_optimization_solution(self, prepared: Sequence[str]):
        self._store(self.id_optimization_solution(), prepared)

    def load_optimization_solution(self):
        return self._load(self.id_optimization_solution())

    def id_opl_dat(self):
        return self.config.opl_input_file()

    def reset_opl_dat(self):
        self._reset(self.id_opl_dat())

    def store_opl_dat(self, prepared: Sequence[str]):
        self._store(self.id_opl_dat(), prepared)

    def load_opl_dat(self):
        return self._load(self.id_opl_dat())

    def id_opl_mod(self):
        return self.config.opl_model_file()

    def reset_opl_mod(self):
        self._reset(self.id_opl_mod())

    def store_opl_mod(self, prepared: Sequence[str]):
        self._store(self.id_opl_mod(), prepared)

    def load_opl_mod(self):
        return self._load(self.id_opl_mod())

    def _load_string_template(self, template_str):
        env = Environment(loader=BaseLoader())
        env.trim_blocks = True
        env.rstrip_blocks = True
        env.lstrip_blocks = True

        return env.from_string(source=template_str)

    def _load_filesystem_template(self, params, template_name):
        file_loader = FileSystemLoader(**params)
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.rstrip_blocks = True
        env.lstrip_blocks = True

        template = env.get_template(template_name)
        return template

    def _load_package_template(self, params, template_name):
        pkg_loader = PackageLoader(**params)
        env = Environment(loader=pkg_loader)
        env.trim_blocks = True
        env.rstrip_blocks = True
        env.lstrip_blocks = True

        template = env.get_template(template_name)
        return template

    def load_opl_template(self,
                          user_params: Optional[Dict[str, Any]] = None,
                          user_template_name: Optional[str] = None) -> Template:
        kind = self.config.opl_config('template_kind', 'pkg')
        if kind == 'file':
            params = user_params or self.config.opl_config('template_file')
            if not params:
                params = {
                    "searchpath": Path().cwd(),
                    "encoding": "utf-8",
                    "followlinks": False
                }
            template = user_template_name or str(self.config.opl_template_file().name)
            if template in (None, 'None'):
                template = 'opl_template.txt'
            return self._load_filesystem_template(params, template)
        if kind == 'str':
            template_str = self.config.opl_config('template_str')
            return self._load_string_template(template_str)
        if kind == 'pkg':
            params = user_params or self.config.opl_config('template_pkg')
            if not params:
                params = {
                    "package_name": "optimistic_process",
                    "package_path": "templates",
                    "encoding": "utf-8"
                }
            template = user_template_name or str(self.config.opl_template_file().name)
            if template in (None, 'None'):
                template = 'opl_template.txt'
            return self._load_package_template(params, template)
