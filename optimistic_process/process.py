from abc import ABC, abstractmethod


class OptimizationProcess(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    def get_solver(self):
        pass

    def get_model(self):
        pass
