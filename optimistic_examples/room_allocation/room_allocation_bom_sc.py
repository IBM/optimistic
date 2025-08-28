import pandas as pd
import numpy as np
from dataclasses import dataclass

@dataclass(unsafe_hash=True, frozen=True)
class RoomAllocationProblem:
    solution: pd.DataFrame
    employees: pd.DataFrame
    floors: pd.DataFrame
    areas: pd.DataFrame
    office_type_by_employee: pd.DataFrame
    office_types: pd.DataFrame

    def transformation(self):
        employee_solution_df = self.trans_employee_solution()
        print("Employee-Solution Join Table:\n", employee_solution_df)

        employee_teamlead_solution_df = self.trans_employee_solution_team_lead()
        print("Employee-Solution & Team-Lead-Solution Join Table:\n", employee_teamlead_solution_df)

        employee_occupancy_df = self.trans_num_of_employee_occupancy_by_floor_office_type()
        print("Number of Employees Occupancy by (floor - office Type) Join Table:\n", employee_occupancy_df)

        room_employee_occupancy_df = self.trans_num_of_rooms_and_employees_occupancy_by_floor_office_type()
        print("Number of Rooms & Employees Occupancy by (floor - office Type) Join Table:\n", room_employee_occupancy_df)

        cost_occupancy_df = self.trans_occupancy_and_cost()
        print("Cost and Occupancy by (floor - office Type) Join Table:\n", cost_occupancy_df)

    def trans_employee_solution(self):
        # First merge the solution with the employees, the new dataframe adds for each employee (i.e `resource`)
        # the corresponding `floor`(i.e `activity`) assigned by the solution
        #  inidcating `one_to_one` forces duplicate check during the merge, i.e no more than one solution assignment
        merge1 = pd.merge(self.solution, self.employees, left_on='resource', right_on='number',
                          how='outer')  # , validate='one_to_one'
        return merge1

    def trans_employee_solution_team_lead(self):
        merge1 = self.trans_employee_solution()
        # print(merge1)

        team_lead_suffix = '_manager'
        employee_suffix = '_employee'

        # Add for each employee what `floor`(i.e `activity`) was assigned for his team lead
        merge2 = merge1.merge(self.solution, left_on=['team_lead'], right_on=['resource'],
                              suffixes=[employee_suffix, team_lead_suffix])

        # Add for each employee indication if his team lead is independent
        merge3 = merge2.merge(self.employees[['number', 'is_independent']], left_on='team_lead', right_on='number',
                              suffixes=[employee_suffix, team_lead_suffix])
        return merge3

    def merged_employee_solution(self):
        return self.trans_employee_solution()
        # return self.employee_solution_df

    def merged_employee_team_lead_solution(self):
        return self.trans_employee_solution_team_lead()
        # return self.employee_teamlead_solution_df

    def trans_num_of_employee_occupancy_by_floor_office_type(self):
        # Aggregate occupancy based on `employee` `type` and `floor` assignment.
        occupancy = self.merged_employee_solution().groupby(['activity', 'type']).size().reset_index(name='num_employees')
        # print("occupancy:\n", occupancy)

        # Add to the aggregation the assigned `office_type` based on `employee_type`
        merged = pd.merge(occupancy, self.office_type_by_employee, left_on='type', right_on='employee_type', how='left')
        # print("merged:\n", merged)

        # Group  by `floor` (i.e.`activity) & `office_type`, and compute corresponding `num_of_employees` occupancy
        # Note:
        #   Join rows, where `Supplier` and `Student` on the same floor, since `Shelter` is used by both
        merge101 = merged.groupby(['office_type', 'activity']).agg({'num_employees': ['sum']})
        merge101.columns = merge101.columns.droplevel(1)
        merge102 = merge101.reset_index()
        # print('merged 102:\n', merge102)
        return merge102

    def trans_num_of_rooms_and_employees_occupancy_by_floor_office_type(self):
        employee_occupancy = self.trans_num_of_employee_occupancy_by_floor_office_type()
        # Pivot the floors table, using stack() so that we have index that we can use to merge
        # based on `floor` (i.e.`activity) & `office_type` tuple
        floor_pivot101 = self.floors.stack().to_frame('num_of_rooms')
        floor_pivot102 = pd.DataFrame(floor_pivot101, index=floor_pivot101.index.set_names(['activity', 'office_type']))
        # above replaces -->> floor_pivot101.index.set_names(['activity', 'office_type'], inplace=True)
        # print('floor_pivot 102:\n', floor_pivot102)  # .reset_index())

        # Merge, add the `num_of_rooms` and `office type` to each `employee type` and `floor` tuple
        merged201 = pd.merge(employee_occupancy, floor_pivot102, left_on=['activity', 'office_type'], right_index=True, how='left')
        # print('merged 201:\n', merged201)

        return merged201

    def trans_occupancy_and_cost(self):
        occupancy = self.trans_num_of_rooms_and_employees_occupancy_by_floor_office_type()
        # Add `cost` and `max_oocupancy` per `floor` and `office_type`
        merged301 = pd.merge(occupancy, self.office_types, left_on='office_type', right_on='type_name', how='left')
        merged302 = merged301.drop(columns=['type_name'])
        # print('merged 302:\n', merged302)

        return merged302

    def constraints(self) -> bool:
        return self.legal_assignment() and self.constraint1() and self.constraint2() and self.constraint3()

    def legal_assignment(self):
        are_resource_assignment_valid_employees = self.solution.resource.isin(self.employees.number)
        are_activity_assignment_valid_floors = self.solution['activity'].isin(self.floors.index)
        return are_activity_assignment_valid_floors.all() and are_resource_assignment_valid_employees.all()
        # return all(a.resource in self.employees and a.activity in self.floors for a in self.solution)

    def constraint1(self) -> bool:
        """
        Each employee is assigned to a unique floor
        """
        return not any(self.solution.duplicated(['resource']))
        # return self.has_unique_assignment()

    def constraint2(self) -> bool:
        """
        Each employee must be assigned to the same floor as his team lead unless the team lead is independent
        """
        # Choose employees whose team lead is not independent
        df_info = self.trans_employee_solution_team_lead()
        df_selected = df_info[df_info.is_independent_manager == 0]
        # Check the employees are the same floor as their manager

        return (df_selected.activity_employee == df_selected.activity_manager).all()
        # return all(self.unique_assignment(e1) == self.unique_assignment(self.get_employee_by_number(e1.team_lead))
        #            for e1 in self.employees if not self.get_employee_by_number(e1.team_lead).is_independent)

    # definition 1
    def office_type_by_employee_type(self, t_emp):
        return self.office_type_by_employee.loc[self.office_type_by_employee['employee_type'] == t_emp, 'office_type'].iloc[0]
        #return OFFICE_TYPE_BY_EMPLOYEE_TYPE[t_emp]


    # aux definition
    # @memoize_method
    def occupancy(self):
        # Aggregate occupancy based on `employee` `type` and `floor` assignment.
        occupancy = self.merged_employee_solution().groupby(['activity', 'type']).size().reset_index(
            name='num_employees')
        # print("occupancy:\n", occupancy)

        # Add to the aggregation the assigned `office_type` based on `employee_type`
        merged = pd.merge(occupancy, self.office_type_by_employee, left_on='type', right_on='employee_type', how='left')
        # print("merged:\n", merged)

        # Group  by `floor` (i.e.`activity) & `office_type`, and compute corresponding `num_of_employees` occupancy
        # Note:
        #   Join rows, where `Supplier` and `Student` on the same floor, since `Shelter` is used by both
        merge101 = merged.groupby(['office_type', 'activity']).agg({'num_employees': ['sum']})
        merge101.columns = merge101.columns.droplevel(1)
        merge102 = merge101.reset_index()
        # print('merged 102:\n', merge102)

        return merge102
        # return count(e1 for e1 in self.employees
        #              if self.office_type_by_employee_type(e1.type) == o1
        #              and self.unique_assignment(e1) == f1)

    def constraint3(self) -> bool:
        """
        The number of employees whose office-type is O in a given floor F must not exceed
        the sum of the max-occupancy of the offices of type O on floor F
        """
        employee_occupancy = self.trans_num_of_employee_occupancy_by_floor_office_type()
        room_occupancy = self.trans_occupancy_and_cost()

        return (employee_occupancy.num_employees <= room_occupancy.num_of_rooms * room_occupancy.max_occupancy).all()
        # return all(self.occupancy(f1, o1) <= o1.max_occupancy * f1.rooms[o1]
        #            for o1 in OfficeType.members()
        #            for f1 in self.floors)

    # definition 2
    # @memoize_method
    def area_utilization(self) -> int:
        """
        The area-utilization of an area and floor is the number of team-leads in that area on that floor.
        """
        merged = self.merged_employee_solution()
        selected = merged[merged.area.isin(self.areas.areas) & merged.is_team_lead]

        area_utilization = selected.groupby(['area', 'activity']).size().reset_index(name='count')
        # print("area_utilization\n", area_utilization)
        return area_utilization
        # return count(e1 for e1 in self.employees
        #              if e1.is_team_lead and e1.area == area.name and self.unique_assignment(e1) == f1)

    # definition 3
    # @memoize_method
    def cost_penalty(self, area, f1) -> float:
        area_utilization = self.area_utilization()
        selected = area_utilization.loc[(area_utilization['area'] == area) & (area_utilization.activity == str(f1))]
        return 0. if selected.empty else 1.0
        # return 0. if self.area_utilization(area, f1) == 0 else 1.

    # definition 4
    # @memoize_method
    def assigned_offices(self) -> int:
        assigned_offices = self.trans_occupancy_and_cost()
        assigned_offices['assigned_offices'] = (assigned_offices.num_employees / assigned_offices.max_occupancy).apply(np.ceil)
        return assigned_offices
        # return math.ceil(self.occupancy(f1, o1) / o1.max_occupancy)

    # definition 5
    def total_cost(self) -> float:
        occupancy = self.assigned_offices()
        return (occupancy.assigned_offices * occupancy.cost).sum()
        # return sum(self.assigned_offices(o1, f1) * o1.cost
        #            for o1 in OfficeType.members()
        #            for f1 in self.floors)

    def objective(self) -> float:
        return 20000 * self.objective1() + 1 * self.objective2()

    def objective1(self):
        return len(self.area_utilization())
        # return sum(self.cost_penalty(a1, f1) for a1 in self.areas for f1 in self.floors)

    def objective2(self):
        return self.total_cost()

