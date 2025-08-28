import math
from typing import NewType, Tuple

from optimistic_client.meta.utils import count, constraint, minimize, record, solution_variable
from optimistic_client.optimization import OptimizationProblem, TotalMapping

"""
This is an attempt to replace many data classes by Mapping/TotalMapping.

Lessons learned:

* Use dataclass or Tuple for domain if necessary
* Use dataclass for range (allows addressing by field name rather than number)
* Need to support set(), keys(), values(), items() [also understand use of mapping as referring to keys]

Enhancements:

* Should support map, lambda, itemgetter, attrgetter

Open questions:

* How to infer domains?
 
"""

Area = NewType('Area', int)
Floor = NewType('Floor', str)
EmployeeType = NewType('EmployeeType', str)
OfficeType = NewType('OfficeType', str)
EmployeeId = NewType('EmployeeId', str)


@record
class OfficeTypeInfo:
    max_occupancy: int
    cost: float


@record
class EmployeeData:
    type: EmployeeType
    team_lead: EmployeeId
    is_team_lead: bool
    is_independent: bool
    area: Area


class RoomAllocationProblem9(OptimizationProblem):
    """
    Optimization problem of allocating employees to offices.

    This version uses the minimal number of type annotations necessary to generate the optimization specification.
    """
    employees: TotalMapping[EmployeeId, EmployeeData]
    building: TotalMapping[Tuple[Floor, OfficeType], int]
    office_type_by_employee_type: TotalMapping[EmployeeType, OfficeType]
    office_info: TotalMapping[OfficeType, OfficeTypeInfo]
    solution: TotalMapping[EmployeeId, Floor] = solution_variable()

    def all_floors(self):
        return {a[0] for a in self.building.keys()}

    def all_areas(self):
        return {e.area for e in self.employees.values()}

    def all_office_types(self):
        return set(self.office_type_by_employee_type.values())

    @constraint
    def same_floor(self):
        """
        Each employee must be assigned to the same floor as his/her team lead unless the team lead is independent
        """
        return all(self.solution[emp_id] == self.solution[emp_data.team_lead]
                   for emp_id, emp_data in self.employees.items()
                   if not self.employees[emp_data.team_lead].is_independent)

    def occupancy(self, f1: Floor, o1):
        """
        How many employees who need to be in offices of type o1 are placed on floor f1
        """
        return count(emp_id for emp_id, emp_data in self.employees.items()
                     if self.office_type_by_employee_type[emp_data.type] == o1
                     and self.solution[emp_id] == f1)

    @constraint
    def availability_constraint(self):
        return all(self.occupancy(f1, o1)
                   <= self.office_info[o1].max_occupancy * self.building[f1, o1]
                   for o1 in self.all_office_types()
                   for f1 in self.all_floors())

    def assigned_offices(self, o1: OfficeType, f1: Floor) -> int:
        return math.ceil(self.occupancy(f1, o1) / self.office_info[o1].max_occupancy)

    @minimize
    def cost_objective(self):
        return sum(self.assigned_offices(o1, f1) * self.office_info[o1].cost
                   for o1 in self.all_office_types()
                   for f1 in self.all_floors())

    def area_utilization(self, area, f1: Floor):
        return count(emp_id for emp_id, emp_data in self.employees.items()
                     if emp_data.area == area and self.solution[emp_id] == f1)

    def area_penalty(self, area: Area, f1: Floor):
        return 0 if self.area_utilization(area, f1) == 0 else 1

    @minimize(weight=20000)
    def area_objective(self):
        """
        Minimize penalties of spreading areas over multiple floors
        """
        return sum(self.area_penalty(a1, f1) for a1 in self.all_areas() for f1 in self.all_floors())
