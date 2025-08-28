from typing import Sequence, Mapping, Any

import pandas as pd

from validator2solver.opt_to_opl import OptimizationModelOplImplementer
from validator2solver.optimization_analyzer import OptimizationProblemAnalyzer
from optimistic_process.artifacts import OptimizationModelOPLArtifactsFileSystem
from optimistic_process.knowledge_driven_optimization_solver import KnowledgeOptimizationModelSolver
from optimistic_process.models import OptimizationInput, OptimizationOutput, OptimizationModel, ViolatedConstraints
from optimistic_process.opl_model_solver import OPLOptimizationModelSolver
from parsing.python import add_import_frame
from parsing.python import Frame


class KnowledgeDrivenOptimizationModel(OptimizationModel):
    def __init__(self, name, config: Mapping[str, Any], builtins: Frame = None):
        super().__init__()
        self.name = name
        self._config = config
        self._debug = config.get('debug', False)
        self._builtins = builtins
        self._analyzer = None
        self._solver = None
        self._opl_model = None
        self._opl_model_str = None
        self._artifacts = None

    def _set_builtins(self):
        if not self._builtins:
            self._builtins = add_import_frame(do_examples=False)

    def build(self) -> KnowledgeOptimizationModelSolver:
        if self._solver:
            return self._solver

        # Initialize the BUILT INs Frames
        self._set_builtins()

        # Compute the AST, Optimization Model MathExpr
        self._analyzer = OptimizationProblemAnalyzer()

        self._analyzer.from_python_file(config=self._config,
                                        builtin_frame=self._builtins,
                                        with_imports=True)

        # Generate the OPL MODEL
        self._opl_model = OptimizationModelOplImplementer(self._analyzer,
                                                          use_type_heuristic=True,
                                                          print_intermediate=False)
        self._opl_model_str = self._opl_model.full_implementation_to_opl()

        # Create necessary solver file system structures
        # self._save_model()

        # Initialize a solver instance
        self._solver = KnowledgeOptimizationModelSolver(self, self._config)
        if isinstance(self._solver, OPLOptimizationModelSolver):
            self._artifacts = OptimizationModelOPLArtifactsFileSystem(config=self._config)
            self._solver.set_artifacts(self._artifacts)

        return self._solver

    def transform_input(self, input: OptimizationInput) -> str:
        data_types = self._opl_model.get_input_fields_types(input.name)
        if self._debug:
            print(f'Transform Input {input.name}:\n {data_types}')

        def _typeit(column_name, value):
            if data_types[column_name] in ('int', 'integer'):
                return f'{val}'

            if data_types[column_name] in ('str', 'string'):
                v = str(value).strip()
                if v.startswith('"') and v.endswith('"'):
                    return f'{v}'
                return f'"{v}"'

            return f'{val}'

        results = f'{input.name} = {{ \n'

        for index, row in input.table.iterrows():
            s = []
            for col, val in row.items():
                s.append(_typeit(col, val))
            results += f'\t<{" ".join(s)}>\n'

        results += f'}};\n'

        return results

    def transform_solution(self, solution) -> Sequence[OptimizationOutput]:
        df = pd.read_csv(self._artifacts.id_optimization_solution())
        return [OptimizationOutput(self._opl_model.legal_solution_var_name(), df)]

    def transform_violated_constraints(self, solution) -> ViolatedConstraints:
        raise NotImplementedError
