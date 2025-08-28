from dataclasses import dataclass

import pandas
import sys
from abc import ABC, abstractmethod
from pandas import DataFrame
from typing import Tuple, Sequence, Mapping, Collection


class OptimizationException(Exception):
    pass


class OptimizationMissingObjectiveException(OptimizationException):
    pass


@dataclass
class OptimizationInput:
    """
    An optimization input, identified by a name; the data is given in a DataFrame.

    Use `OptimizationModel.expected_inputs()` to see the form of the inputs required by the model.

    Be sure to call `sort_index()` on the DataFrame to ensure efficiency of processing.
    """
    name: str
    table: DataFrame

    def describe(self, file=sys.stdout, print_all=False):
        print(f'OptimizationInput {self.name}', file=file)
        if print_all:
            with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
                print(self.table, file=file)
        else:
            print(self.table, file=file)


@dataclass
class OptimizationOutput:
    name: str
    table: DataFrame


class ViolatedConstraints:
    """
    TBD
    """
    pass


class OptimizationObjective:
    pass


@dataclass
class SingleObjective(OptimizationObjective):
    value: float

    def __repr__(self):
        return f'Single Objective is {self.value}'


@dataclass
class MultipleObjectives(OptimizationObjective):
    value: float
    objective_values: Mapping[str, float]

@dataclass
class InfeasibleObjectives(OptimizationObjective):
    value: str = "Infeasible"

    def __repr__(self):
        return f'Infeasible Objective'


class OptimizationModelSolver(ABC):
    def __init__(self, model: 'OptimizationModel'):
        self.optimization_model = model

    @abstractmethod
    def set_input(self, *inputs: OptimizationInput):
        raise NotImplementedError

    @abstractmethod
    def solve(self):
        """
        Call the solver to try to find an optimal solution.

        Should only be called after setting all inputs, using `set_input()`, unless the problem doesn't take any
        inputs.
        """
        raise NotImplementedError

    @abstractmethod
    def solution_available(self) -> bool:
        """
        Return True iff last call to `solve()` resulted in a feasible solution

        If result is True, `get_objective_value()` and `get_solution()` will report on the solution found.

        If result is False, `get_minimum_violated_constraints()` will report on the reasons no solution could be found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_objective_value(self) -> OptimizationObjective:
        raise NotImplementedError

    @abstractmethod
    def get_solution(self) -> Collection[OptimizationOutput]:
        raise NotImplementedError

    @abstractmethod
    def get_minimum_violated_constraints(self):
        raise NotImplementedError

    @abstractmethod
    def check_solution(self, solution: Collection[OptimizationOutput]) -> Tuple[
        OptimizationObjective, ViolatedConstraints]:
        raise NotImplementedError


class OptimizationModel(ABC):
    @abstractmethod
    def build(self) -> OptimizationModelSolver:
        raise NotImplementedError

    @abstractmethod
    def transform_input(self, input: OptimizationInput) -> str:
        raise NotImplementedError

    @abstractmethod
    def transform_solution(self, solution) -> Sequence[OptimizationOutput]:
        raise NotImplementedError

    @abstractmethod
    def transform_violated_constraints(self, solution) -> ViolatedConstraints:
        raise NotImplementedError
