from typing import Dict, Any, Optional, Sequence

from optimistic_process.artifacts import ArtifactsOPL
from optimistic_process.models import OptimizationModel
from optimistic_process.opl_model_solver import OPLOptimizationModelSolver


class KnowledgeOptimizationModelSolver(OPLOptimizationModelSolver):
    def __init__(self, model: 'OptimizationModel',
                 artifacts: Optional[ArtifactsOPL] = None):
        super().__init__(model, artifacts)

    def prepare_input(self) -> Sequence[str]:
        prepared_input = []
        if not self.inputs:
            # FIXME: raise exceptions
            return

        for data in self.inputs:
            prepared_input.append(self.optimization_model.transform_input(data))

        return prepared_input

    def template_properties(self, user_properties: Optional[Dict[str, Any]] = None):
        solution_fields_str = '\"\\"\" +'
        is_first = True
        for field in self.optimization_model._opl_model.get_solution_fields_names():
            if is_first:
                is_first = False
            else:
                solution_fields_str += ' + \"\\",\\"\" +'
            solution_fields_str += f'assign.{field}'
        solution_fields_str += '+ \"\\"\"'

        template_properties = {
            'model': self.optimization_model._opl_model_str,
            'output_file_path': str(self.artifacts.id_optimization_solution()).replace("\\", "\\\\"),
            'column_names': ",".join(self.optimization_model._opl_model.get_solution_fields_names()),
            'solution_fields': solution_fields_str,
            'legal_solution_name': self.optimization_model._opl_model.legal_solution_var_name(),
            'solution_var_name': self.optimization_model._opl_model.solution_var_name()
        }
        if user_properties:
            template_properties.update(user_properties)

        return template_properties
