import json
from optimistic_examples.room_allocation.room_allocation_bom_sc import RoomAllocationProblem
import pandas as pd


def read_json(file_name):
    with open(file_name) as input_file:
        data = json.load(input_file)
        # print(data)
        return data


def populate_employees(json_data):
    empl = pd.DataFrame.from_dict(json_data)
    empl.loc[empl.type == 'REG', 'type'] = 'Researcher'
    empl.loc[empl.type == 'KeyPerson', 'type'] = 'Manager'
    return empl


def populate_floors(json_data):
    floors = pd.json_normalize(json_data).set_index('floor')
    floors.columns = floors.columns.str.replace('^rooms.', '')
    return floors


def populate_areas(json_data):
    areas = pd.DataFrame(json_data, columns=['areas'])
    return areas


def populate_solution(json_data, employees, floors):
    solution = pd.DataFrame.from_dict(json_data)
    return solution


def populate_office_type_by_employee_type(json_data):
    items = json_data.items()
    office_type_by_employee_type = pd.DataFrame(
        {'employee_type': [i[0] for i in items], 'office_type': [i[1] for i in items]})
    office_type_by_employee_type.loc[
        office_type_by_employee_type.employee_type == 'REG', 'employee_type'] = 'Researcher'
    office_type_by_employee_type.loc[
        office_type_by_employee_type.employee_type == 'KeyPerson', 'employee_type'] = 'Manager'
    return office_type_by_employee_type


def populate_office_types(json_data):
    office_types = pd.DataFrame.from_dict(json_data)
    return office_types


def display_problem_results(title, prob):
    doPrintTransformations = True
    print(f'>>>>    Simulation for Test {title}')
    print('-----------------------------------------------------------------')
    print(f'Objective is {prob.objective()}')
    print(f'Objective 1 on maximize area utilization is [{prob.area_objective()}]')
    print(f'Objective 2 on minimize total cost is [{prob.cost_objective()}]')
    print()
    print(f'Constraints are [{prob._constraints()}]')
    print(f'Constraint Legal Assignment is [{prob.legal_assignment()}]')
    print(f'Constraint on has unique assignment is [{prob.constraint1()}]')
    print(f'Constraint on Employee same floor as team lead is [{prob.same_floor()}]')
    print(f'Constraint on floor occupancy less than floor capacity is [{prob.availability_constraint()}]')
    print()
    # print(f'Area Utilization [{prob.area_utilization()}]')
    # print(f'Cost Penalty [area=86, floor=3] = [{prob.cost_penalty(86,3)}]')
    # print(f'Cost Penalty [area=86, floor=7] = [{prob.cost_penalty(86,7)}]')
    # print(f'assigned_offices\n  [{prob.assigned_offices()}]')
    # print(f'Total Cost\n  [{prob.total_cost()}]')
    # print(f'office_type_by_employee_type   [{prob.office_type_by_employee_type("Supplier")}]')
    print()
    if not doPrintTransformations:
        prob.transformation()


if __name__ == '__main__':
    doPrintInput = True
    doPrintSolution = False

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 400)
    input_json_file = '../../room_allocation/data/room-allocation-input.json'
    input_data = read_json(input_json_file)
    employees = populate_employees(input_data['employees'])
    floors = populate_floors(input_data['rooms'])
    areas = populate_areas(input_data['areas'])
    office_type_by_employee = populate_office_type_by_employee_type(input_data['officeTypeByEmployee'])
    office_types = populate_office_types(input_data['office_types'])

    if doPrintInput:
        print(f'Input - Employees\n {employees}\n')
        print(f'Input - Floors\n {floors}\n')
        print(f'Input - Areas\n {areas}\n')
        print(f'Input - Office Type by Employee Type\n {office_type_by_employee}\n')
        print(f'Input - Office Types\n {office_types}\n')

    if True:
        input_solution_file_bad = '../../room_allocation/data/room-allocation-b1-output-bad1.json'
        solution_data = read_json(input_solution_file_bad)
        solutions = populate_solution(solution_data, employees, floors)
        if doPrintSolution:
            print(f'Input - Solution\n {solutions}')
        prob1 = RoomAllocationProblem(solutions, employees, floors, areas, office_type_by_employee, office_types)
        display_problem_results("BAD OPL", prob1)

    if True:
        input_solution_file = '../../room_allocation/data/room-allocation-b1-output.json'
        solution_data = read_json(input_solution_file)
        solutions = populate_solution(solution_data, employees, floors)
        if doPrintSolution:
            print(f'Input - Solution\n {solutions}')
        prob1 = RoomAllocationProblem(solutions, employees, floors, areas, office_type_by_employee, office_types)
        display_problem_results("Boolean OPL", prob1)

    if True:
        input_solution_file2 = '../../room_allocation/data/room-allocation-m1-output.json'
        solution_data2 = read_json(input_solution_file2)
        solutions2 = populate_solution(solution_data2, employees, floors)
        if doPrintSolution:
            print(f'Input - Solution\n {solutions2}')
        prob2 = RoomAllocationProblem(solutions2, employees, floors, areas, office_type_by_employee, office_types)
        display_problem_results("Array Mapping OPL", prob2)
