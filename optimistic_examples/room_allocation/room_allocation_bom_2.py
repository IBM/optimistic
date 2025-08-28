import math
from dataclasses import dataclass
from typing import Collection, Set, Mapping

from optimistic_examples.room_allocation import facilities_bom
from optimistic_examples.room_allocation.facilities_bom import RoomType
from optimistic_examples.room_allocation.resource_allocation_bom import Resource, ResourceAllocationProblem, Assignment

from optimistic_client.meta.utils import count, memoize_method, metadata
from optimistic_client.meta.infrastructure import KeepMembersMixin


@dataclass(unsafe_hash=True)
class OfficeType(RoomType, KeepMembersMixin):
    max_occupancy: int
    type_name: str
    cost: float

    # def __init__(self, type_name, max_occupancy, cost):
    #     self.type_name = type_name
    #     self.max_occupancy = max_occupancy
    #     self.cost = cost

    # def __eq__(self, o: object) -> bool:
    #     return (isinstance(o, OfficeType)
    #             and self.type_name == o.type_name and self.max_occupancy == o.max_occupancy and self.cost == o.cost)

    # def __hash__(self) -> int:
    #     return 3 * hash(self.type_name) + 5000 * self.max_occupancy + 7 * hash(self.cost)


COST_PER_SQM = 114.707141

MANAGER_OFFICE = OfficeType(1, 'Manager', 11.5 * COST_PER_SQM)
RESEARCHER_OFFICE = OfficeType(2, 'Researcher', 14 * COST_PER_SQM)
SHELTER = OfficeType(6, 'Shelter', 30 * COST_PER_SQM)


@dataclass
class Floor(facilities_bom.Floor, KeepMembersMixin):
    rooms: Mapping[RoomType, int]

    def __init__(self, designator, rooms):
        self.designator = designator
        self.rooms = rooms

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Floor) and self.rooms == o.rooms

    def __hash__(self) -> int:
        # return 11 * hash(self.designator) + 13 * hash(tuple(sorted(self.rooms.items())))
        return 11 * hash(self.designator)


FLOORS = [Floor(f'F{i}', {}) for i in range(1, 8)]


class EmployeeType(KeepMembersMixin):
    def __init__(self, type_name):
        self.type_name = type_name

    def __eq__(self, o: object) -> bool:
        return isinstance(o, EmployeeType) and self.type_name == o.type_name

    def __hash__(self) -> int:
        return hash(self.type_name) + 123


# TODO: replace manager by requires_single_room field in Employee
MANAGER = EmployeeType('Manager')
RESEARCHER = EmployeeType('Researcher')
STUDENT = EmployeeType('Student')
SUPPLIER = EmployeeType('Supplier')

OFFICE_TYPE_BY_EMPLOYEE_TYPE = {MANAGER: MANAGER_OFFICE, RESEARCHER: RESEARCHER_OFFICE,
                                STUDENT: SHELTER, SUPPLIER: SHELTER}


@dataclass(unsafe_hash=True, frozen=True)
class Area:
    name: str


# FIXME: define Areas
AREAS = []


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
class RoomAllocationProblem(ResourceAllocationProblem):
    """
    Optimization problem of allocating employees to offices
    """
    solution: Set[FloorAssignment]
    employees: Collection[Employee]
    floors: Collection[Floor]
    areas: Collection[Area]

    def constraints(self) -> bool:
        return self.legal_assignment() and self.constraint1() and self.constraint2() and self.constraint3()

    def legal_assignment(self):
        return all(a.resource in self.employees and a.activity in self.floors for a in self.solution)

    def constraint1(self) -> bool:
        return self.has_unique_assignment()

    def constraint2(self) -> bool:
        """
        Each employee must be assigned to the same floor as his/her team lead unless the team lead is independent
        """
        return all(self.unique_assignment(e1) == self.unique_assignment(self.get_employee_by_number(e1.team_lead))
                   for e1 in self.employees if not self.get_employee_by_number(e1.team_lead).is_independent)

    # definition 1
    @staticmethod
    def office_type_by_employee_type(t_emp: EmployeeType) -> OfficeType:
        return OFFICE_TYPE_BY_EMPLOYEE_TYPE[t_emp]

    @memoize_method
    def get_employee_by_number(self, number):
        return next(m for m in self.employees if m.number == number)

    # aux definition
    # @memoize_method
    def occupancy(self, f1, o1):
        return count(e1 for e1 in self.employees
                     if self.office_type_by_employee_type(e1.type) == o1
                     and self.unique_assignment(e1) == f1)

    def constraint3(self) -> bool:
        return all(self.occupancy(f1, o1) <= o1.max_occupancy * f1.rooms[o1]
                   for o1 in OfficeType.members()
                   for f1 in self.floors)

    # definition 2
    # @memoize_method
    def area_utilization(self, area: Area, f1: Floor) -> int:
        return count(e1 for e1 in self.employees
                     if e1.is_team_lead and e1.area == area.name and self.unique_assignment(e1) == f1)

    # definition 3
    # @memoize_method
    def cost_penalty(self, area: Area, f1: Floor) -> float:
        return 0. if self.area_utilization(area, f1) == 0 else 1.

    # definition 4
    # @memoize_method
    def assigned_offices(self, o1: OfficeType, f1: Floor) -> int:
        return math.ceil(self.occupancy(f1, o1) / o1.max_occupancy)

    # definition 5
    def total_cost(self) -> float:
        return sum(self.assigned_offices(o1, f1) * o1.cost
                   for o1 in OfficeType.members()
                   for f1 in self.floors)

    def objective(self) -> float:
        return 20000 * self.objective1() + 1 * self.objective2()

    def objective1(self):
        return sum(self.cost_penalty(a1, f1) for a1 in self.areas for f1 in self.floors)

    def objective2(self):
        return self.total_cost()


if __name__ == '__main__':
    print([m for m in OfficeType.members()])
    print([m.type_name for m in EmployeeType.members()])
    print(FLOORS)
    print([m.designator for m in Floor.members()])
    solution = set()
    prob = RoomAllocationProblem(EmployeeType.members(), Floor.members(), AREAS, solution)
