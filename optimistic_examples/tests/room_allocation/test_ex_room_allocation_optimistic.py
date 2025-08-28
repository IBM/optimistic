from pathlib import Path
from test import Tee
from optimistic_examples.room_allocation.prep_data.phase_cur.main_optimistic_opl_input_model import get_config, \
    DataGenerator

from optimistic_examples.room_allocation.room_allocation_bom_8 import Employee, OfficeTypeInfo, \
    OfficeTypeByEmployeeType, OfficeAvailability, FloorAssignment, RoomAllocationProblem8

test_output_dir = '../../../test-output/room-allocation/actual/'
actual_dir = Path(test_output_dir)


def display_problem_results(title, prob):
    outputFile = actual_dir.joinpath("python-6.txt")
    test_tee = Tee(outputFile)

    with test_tee:
        print(f'>>>>    Simulation for Test {title}')
        print('-----------------------------------------------------------------')
        print(f'Objective 1 on minimize area utilization, is [{prob.area_objective()}]')
        print(f'Objective 2 on minimize total cost, is [{prob.cost_objective()}]')
        print()
        print(f'Constraint: Each Employee must be assigned to same floor as team lead, is [{prob.same_floor()}]')
        print(f'Constraint: Each floor occupancy less than floor capacity is [{prob.availability_constraint()}]')
        print()
        print(f'Failed constraints:', ', '.join(prob.check_constraints()) or 'None (all pass)')
        print('\n  Objective: ', prob.compute_objective())


if __name__ == '__main__':
    target = Path("test_input_dev.yaml").resolve()
    print(f'Test configuration: {target}')
    config = get_config(target)
    example = 'room_allocation'
    gen = DataGenerator(config, example)
    employees = gen.create(Employee)
    office_type_by_employee = gen.create(OfficeTypeByEmployeeType)
    office_availability = gen.create(OfficeAvailability)
    office_type_info = gen.create(OfficeTypeInfo)
    solution = gen.create(FloorAssignment)
    prob1 = RoomAllocationProblem8(solution, employees, office_availability, office_type_by_employee, office_type_info)
    display_problem_results("Optimistic generated", prob1)
