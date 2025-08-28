import re
import time
import subprocess
from abc import ABC, abstractmethod
from typing import Tuple, Collection, Dict, Any, Sequence, Optional

from optimistic_process.models import OptimizationModel, OptimizationModelSolver, OptimizationInput, OptimizationOutput, \
    OptimizationObjective, OptimizationMissingObjectiveException, SingleObjective, ViolatedConstraints, \
    InfeasibleObjectives
from optimistic_process.report import Report, ReportLogger, timeit
from optimistic_process.artifacts import ArtifactsOPL, OptimizationModelOPLArtifactsFileSystem


class OPLOptimizationModelSolver(OptimizationModelSolver, ABC):
    def __init__(self, model: 'OptimizationModel',
                 artifacts: Optional[ArtifactsOPL] = None):
        super().__init__(model)
        self.artifacts = artifacts if artifacts else OptimizationModelOPLArtifactsFileSystem()
        self.report = ReportLogger()
        self.debug = False

        self.mod_as_str = None

        self.inputs = []
        self.prepared_input = []
        self.objective = None
        self.solution = None
        self.is_solution_available = False

    @abstractmethod
    def prepare_input(self) -> Sequence[str]:
        raise NotImplementedError()

    @abstractmethod
    def template_properties(self, user_properties: Optional[Dict[str, Any]] = None):
        raise NotImplementedError()

    def set_artifacts(self, artifacts: ArtifactsOPL):
        self.artifacts = artifacts

    def _prepare_opl_mod(self):
        if self.mod_as_str:
            return self.mod_as_str

        template = self.artifacts.load_opl_template()
        template_properties = self.template_properties()
        self.mod_as_str = template.render(**template_properties)

        self.artifacts.store_opl_mod(self.mod_as_str.split('\n'))
        return self.mod_as_str

    def _prepare_to_solve(self):
        self._prepare_opl_mod()
        input_results = self.prepare_input()
        self.artifacts.store_opl_dat(input_results)

    def set_input(self, *inputs: OptimizationInput):
        for data in inputs:
            self.report.add(Report.LOG, f'Solver - Input: adding input {data.name}')
            self.inputs.append(data)
        self.is_solution_available = False
        self.solution = None
        self.artifacts.reset_optimization_solution()
        self.artifacts.reset_opl_dat()

    def solve(self):
        """
        Call the solver to try to find an optimal solution.

        Should only be called after setting all inputs, using `set_input()`, unless the problem doesn't take any
        inputs.
        """
        start_time = phase_start = time.time()
        if self.debug:
            print(f'Solver: Starting Solve of Graph Model [{self.optimization_model.name}]')
        self.is_solution_available = False
        # Store temporal input
        self._prepare_to_solve()
        self.report.add(Report.SUCCESS, f'Solver: Input transform Success, {timeit(phase_start)} ...')

        # Solve the model with the temporal input
        phase_start = time.time()
        try:
            mod = str(self.artifacts.id_opl_mod())
            dat = str(self.artifacts.id_opl_dat())

            self.report.add(Report.SUCCESS, f'Solver: Running opl with model [{mod}] and data [{dat}]')
            completed = subprocess.run(['oplrun', mod, dat],
                                       check=False,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as err:
            self.report.add((Report.FAILURE, Report.STATS), f'Solve ERROR: {err}, {timeit(phase_start)}')
            self.inputs = []
        else:
            results = completed.stdout.decode("utf-8")
            # if self.debug:
            #     self.report.add(Report.LOG, f'Solver: Completed with opl engine results [{results}]]')
            if completed.returncode:
                self.report.add(Report.FAILURE, f'Solver: ERROR return code: {completed.returncode}')
                self.report.add(Report.FAILURE,
                                f'solver: ERROR Have {len(completed.stdout)} bytes in stdout:\n{results}')
                self.report.add((Report.FAILURE, Report.STATS),
                                f'solver: ERROR Have {len(completed.stderr)} bytes in stderr:\n{results},\n '
                                f'{timeit(phase_start)}')
            OBJECTIVE_PATTERN = re.compile(r'OBJECTIVE.?\s+([-+]?\d*\.?\d*)')
            objective = OBJECTIVE_PATTERN.search(results)
            self.report.add(Report.LOG,
                            f'Solver: Completed with opl engine objective match [{objective}]],'
                            f' {timeit(phase_start)}')
            if objective:
                self.objective = SingleObjective(float(objective.group(1)))
                self.is_solution_available = True
            else:
                INFEASIBLE_PATTERN = re.compile(r'^(.*)infeasible(.*)$')
                objective = INFEASIBLE_PATTERN.match(results)
                # if objective:
                self.objective = InfeasibleObjectives()
                self.is_solution_available = False
            if self.debug:
                self.report.add(Report.LOG, f'Solver: returncode: {completed.returncode}')
                self.report.add(Report.LOG, f'Solver: Have {len(completed.stdout)} bytes in stdout:\n{results}')
                self.report.add(Report.LOG,
                                f'Solver: Have {len(completed.stderr)} bytes in stderr:\n{completed.stderr.decode("utf-8")}')
            self.report.add(Report.SUMMARY,
                            f'Solver: Objective Exists[{self.solution_available()}]\n\t {self.objective}')
            self.report.add((Report.SUMMARY, Report.STATS), f'Solver: Complete, {timeit(start_time)} ....')
        finally:
            self.inputs = []

    def solution_available(self) -> bool:
        return self.is_solution_available

    def get_objective_value(self) -> OptimizationObjective:
        if not self.objective:
            raise OptimizationMissingObjectiveException()
        return self.objective

    def get_solution(self) -> Collection[OptimizationOutput]:
        if not self.solution_available():
            return []
        if not self.solution:
            lines = self.artifacts.load_optimization_solution()
            self.solution = self.optimization_model.transform_solution(lines)
        return self.solution

    def get_minimum_violated_constraints(self):
        return NotImplementedError

    def check_solution(self, solution: Collection[OptimizationOutput]
                       ) -> Tuple[OptimizationObjective, ViolatedConstraints]:
        print('Warning: check_solution() called, not yet implemented!')
        return SingleObjective(9876), ViolatedConstraints()
