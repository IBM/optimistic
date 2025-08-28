import math
from dataclasses import dataclass
from typing import Collection, Set

from optimistic_examples.room_allocation.resource_allocation_bom import Resource, Assignment, UniqueAssignment

from optimistic_client.optimization import OptimizationProblem
from optimistic_client.meta.utils import count, memoize_method, metadata, constraint, minimize
from optimistic_examples.room_allocation.room_allocation_bom_2 import EmployeeType, OFFICE_TYPE_BY_EMPLOYEE_TYPE, \
    OfficeType


@dataclass(unsafe_hash=True, frozen=True)
class Area:
    name: str


# TODO: Use NewType
@dataclass(unsafe_hash=True, frozen=True)
class Floor:
    desginator: str


@dataclass(unsafe_hash=True, frozen=True)
class OfficeAvailability:
    floor: Floor = metadata(primary_key=True)
    office_type: OfficeType = metadata(primary_key=True)
    rooms: int


@dataclass(unsafe_hash=True, frozen=True)
class Employee(Resource):
    type: EmployeeType
    number: int = metadata(primary_key=True)
    team_lead: int
    is_team_lead: bool
    is_independent: bool
    area: Area


@dataclass(unsafe_hash=True, frozen=True)
class FloorAssignment(Assignment):
    resource: Employee
    activity: Floor


@dataclass(unsafe_hash=True, frozen=True)
class RoomAllocationProblem3(OptimizationProblem, UniqueAssignment):
    """
    Optimization problem of allocating employees to offices
    """
    solution: Set[FloorAssignment]
    employees: Collection[Employee]
    building: Collection[OfficeAvailability]
    areas: Collection[Area]

    @constraint
    def legal_assignment(self):
        return all(a.resource in self.employees and a.activity in self.floors for a in self.solution)

    @constraint
    def constraint2(self) -> bool:
        """
        Each employee must be assigned to the same floor as his/her team lead unless the team lead is independent
        """
        return all(self.unique_assignment(e1) == self.unique_assignment(self.get_employee(e1.team_lead))
                   for e1 in self.employees if not self.get_employee(e1.team_lead).is_independent)

    # definition 1
    @staticmethod
    def office_type_by_employee_type(t_emp: EmployeeType) -> OfficeType:
        return OFFICE_TYPE_BY_EMPLOYEE_TYPE[t_emp]

    # TODO: should be auto-generated based on key
    @memoize_method
    def get_employee(self, number):
        return next(m for m in self.employees if m.number == number)

    # aux definition
    def occupancy(self, f1, o1):
        return count(e1 for e1 in self.employees
                     if self.office_type_by_employee_type(e1.type) == o1
                     and self.unique_assignment(e1) == f1)

    # TODO: should be auto-generated based on key
    def get_office_availability(self, f1, o1):
        return next(a.rooms for a in self.building if a.floor == f1 and a.office_type == o1)

    @constraint
    def constraint3(self) -> bool:
        return all(self.occupancy(f1, o1) <= o1.max_occupancy * self.get_office_availability(f1, o1)
                   for o1 in OfficeType.members()
                   for f1 in self.floors)

    # definition 2
    def area_utilization(self, area: Area, f1: Floor) -> int:
        return count(e1 for e1 in self.employees
                     if e1.is_team_lead and e1.area == area.name and self.unique_assignment(e1) == f1)

    # definition 3
    def cost_penalty(self, area: Area, f1: Floor) -> float:
        return 0. if self.area_utilization(area, f1) == 0 else 1.

    # definition 4
    def assigned_offices(self, o1: OfficeType, f1: Floor) -> int:
        return math.ceil(self.occupancy(f1, o1) / o1.max_occupancy)

    # definition 5
    def total_cost(self) -> float:
        return sum(self.assigned_offices(o1, f1) * o1.cost
                   for o1 in OfficeType.members()
                   for f1 in self.floors)

    @minimize(weight=20000)
    def objective1(self):
        return sum(self.cost_penalty(a1, f1) for a1 in self.areas for f1 in self.floors)

    @minimize
    def objective2(self):
        return self.total_cost()
