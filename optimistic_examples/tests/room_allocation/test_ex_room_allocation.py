import json
from optimistic_examples.room_allocation.room_allocation_bom_2 import RoomAllocationProblem, Employee, Floor, Area, \
    FloorAssignment, \
    EmployeeType, OfficeType
from optimistic_examples.room_allocation.room_allocation_bom_3 import RoomAllocationProblem3


def read_json(file_name):
    with open(file_name) as input_file:
        data = json.load(input_file)
        # print(data)
        return data


def populate_employees(json_data):
    employees = []
    for empl in json_data:
        # print(empl)
        target_type = 'Researcher' if empl['type'] == 'REG' else \
            'Manager' if empl['type'] == 'KeyPerson' else empl['type']

        empl_type = [m for m in EmployeeType.members() if m.type_name == target_type][0]
        newEmployee = Employee(empl_type, empl['number'], empl['team_lead'], empl['is_team_lead'],
                               empl['is_independent'], empl['area'])
        # print(newEmployee)
        employees.append(newEmployee)
    # return populate_team_lead(employees)
    return frozenset(employees)


def populate_team_lead(employees):
    emp_with_team_lead = []
    for empl in employees:
        team_lead = next((m for m in employees if m.number == empl.team_lead))
        # team_lead = [m for m in employees if m.number == empl.team_lead][0]
        print(empl, team_lead)
        newEmployee = Employee(empl.type, empl.number, team_lead, empl.is_team_lead, empl.is_independent, empl.area)
        emp_with_team_lead.append(newEmployee)
    return emp_with_team_lead


def populate_floors(json_data):
    floors = []
    for room in json_data:
        rooms = {}
        for key, number_of_rooms_type_in_floor in room['rooms'].items():
            # print(room['floor'], ': ', key, '->', number_of_rooms_type_in_floor)
            office_type = [m for m in OfficeType.members() if m.type_name == key][0]
            newMapping = {office_type: number_of_rooms_type_in_floor}
            rooms.update(newMapping)
            # print(newMapping)
        newFloor = Floor(room['floor'], rooms)
        floors.append(newFloor)
        # print(newFloor)
    # print(floors)
    return frozenset(floors)


def populate_areas(json_data):
    areas = []
    for area in json_data:
        newArea = Area(area)
        areas.append(newArea)
    return frozenset(areas)


def populate_solution(json_data, employees, floors):
    solution = set()
    for assignment in json_data:
        # TODO: replace searches by dicts
        employee = next(m for m in employees if m.number == assignment['resource'])
        floor = next(m for m in floors if m.designator == assignment['activity'])
        # print(solution, employee.number, floor.designator)
        new_assignment = FloorAssignment(employee, floor)
        solution.add(new_assignment)
    # print(solutions[0])
    return frozenset(solution)


def display_problem_results(title, prob):
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


if __name__ == '__main__':
    input_json_file = '../../room_allocation/data/room-allocation-input.json'
    input_data = read_json(input_json_file)
    employees = populate_employees(input_data['employees'])
    floors = populate_floors(input_data['rooms'])
    areas = populate_areas(input_data['areas'])
    if not True:
        input_solution_file_bad = '../../room_allocation/data/room-allocation-b1-output-bad1.json'
        solution_data = read_json(input_solution_file_bad)
        solutions = populate_solution(solution_data, employees, floors)
        prob1 = RoomAllocationProblem(solutions, employees, floors, areas)
        display_problem_results("Bad OPL", prob1)

    if True:
        input_solution_file = '../../room_allocation/data/room-allocation-b1-output.json'
        solution_data = read_json(input_solution_file)
        solutions = populate_solution(solution_data, employees, floors)
        prob1 = RoomAllocationProblem(solutions, employees, floors, areas)
        display_problem_results("Boolean OPL", prob1)

    if True:
        input_solution_file2 = '../../room_allocation/data/room-allocation-m1-output.json'
        solution_data2 = read_json(input_solution_file2)
        solutions2 = populate_solution(solution_data2, employees, floors)
        prob2 = RoomAllocationProblem(solutions2, employees, floors, areas)
        display_problem_results("Array Mapping OPL", prob2)

    if True:
        input_solution_file_bad = '../../room_allocation/data/room-allocation-b1-output-bad1.json'
        solution_data = read_json(input_solution_file_bad)
        solutions = populate_solution(solution_data, employees, floors)
        prob3 = RoomAllocationProblem3(solutions, employees, floors, areas)
        print('V3: Bad OPL:')
        print('  Failed constraints:', ', '.join(prob3.check_constraints()))
        print('  Objective: ', prob3.compute_objective())

    if True:
        input_solution_file3 = '../../room_allocation/data/room-allocation-b1-output.json'
        solution_data = read_json(input_solution_file3)
        solutions = populate_solution(solution_data, employees, floors)
        prob4 = RoomAllocationProblem3(solutions, employees, floors, areas)
        print('V3: Good OPL:')
        print('  Failed constraints:', ', '.join(prob4.check_constraints()))
        print('  Objective: ', prob4.compute_objective())
