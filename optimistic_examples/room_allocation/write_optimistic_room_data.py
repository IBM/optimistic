import os
import sys
from collections import Counter

import pandas as pd

# Based on code by zalex

OFFICE_TYPE_BY_EMPLOYEE_TYPE = dict(KeyPerson='Manager', REG='Researcher', Student='Shelter', Supplier='Shelter')


class InputGenerator:
    def __init__(self, folder,
                 building_file_name='HRLoffices5.csv',  # 'HRL_buildingTririga.csv',
                 employee_file_name='Haifa_Site_Emp7.csv',
                 output_file_name='optimistic_input.dat'):
        self.MngRoomUtilization = 1
        self.RsmRoomUtilization = 2
        self.StudentRoomUtilization = 5
        self.SupplierRoomUtilization = 5
        self.AdminRoomUtilization = 2
        self.AreasIntegrity = 1  # Higher number => higher integrity
        self.ConfRooms = "161 259 260 560 660 695 722 445 759 760 L100 L59 L60 703 565 305 116 115 460".split()
        self.RoomUsageRSM = 'CUBE'
        self.RoomUsageManager = 'CUBEMGR'
        self.RoomUsageStudent = 'BOMB'
        self.CostSqM = 114.707141
        self.AvgCubeArea = 14
        self.AvgCubeMngArea = 11.5
        self.AvgCubeStudentArea = 30
        self.NumFloors = 7
        self.Optional = 'NO'
        self.folder = folder
        self.employee_file_name = employee_file_name
        self.tririga_file_name = building_file_name
        self.dat_file = output_file_name

    def write_opl(self):
        output_file = open(os.path.join(self.folder, self.dat_file), 'w')
        ee_file_new = os.path.join(self.folder, self.employee_file_name)
        file_ee = pd.read_csv(ee_file_new)
        df_ee = pd.DataFrame(file_ee)
        # emp_number	e_team	e_team_First 	emp_managerlevelcode	Department 	Single_Room	Independent	emp_type	KeyPerson
        SL = df_ee['e_team'].unique()
        areas = {int(r) for r in SL}
        # counter = 0
        # print(f'number_of_employees = {len(df_ee)};', file=opt_in)
        print("employees = {", file=output_file)
        for index, row in df_ee.iterrows():
            # if row['Single_Room'] == 'YES':
            #     counter = counter + 1
            if str(row['emp_number'].lstrip("0")) == str(row['KeyPerson']):
                row['emp_type'] = 'KeyPerson'
            # if (row['Single_Room'] == 'Optional'):
            #     row['Single_Room'] = self.Optional
            print("  <", '"{}"'.format(row['emp_number'].lstrip("0")), '"{}"'.format(row['emp_type']),
                  '"{}"'.format(row['KeyPerson']),  # = is_team_lead
                  1 if row['emp_type'] == 'KeyPerson' else 0,
                  1 if row['Independent'].upper() == 'YES' else 0,
                  row['e_team_First '][:2],  # = area
                  ">", file=output_file)
        print("};", file=output_file)

        # print(f'number_of_areas = {len(areas)};', file=opt_in)
        print(f'areas = {areas};', file=output_file)

        # print(f'number_of_office_types = {3};', file=opt_in)
        print('office_types = {', file=output_file)
        print(f'  <"Manager", 1, {11.5 * self.CostSqM}>', file=output_file)
        print(f'  <"Researcher", 2, {14 * self.CostSqM}>', file=output_file)
        print(f'  <"Shelter", 6, {30 * self.CostSqM}>', file=output_file)
        print('};', file=output_file)

        print('office_type_by_employee_type = #[', file=output_file)
        for emp, ofc in OFFICE_TYPE_BY_EMPLOYEE_TYPE.items():
            print(f'  "{emp}": "{ofc}"', file=output_file)
        print(']#;', file=output_file)

        # print(f'number_of_floors = {self.NumFloors};', file=opt_in)
        # floor_names = [f'"F{i}"' for i in range(1, self.NumFloors + 1)]

        rooms_mgr, rooms_researcher, rooms_student, floor_names = self.collect_rooms()
        quoted_floor_names = [f'"{fn}"' for fn in floor_names]
        quoted_floor_names.sort()
        print(f'floors = {{{", ".join(quoted_floor_names)}}};', file=output_file)

        # As set of sets -- doesn't work!
        # print('rooms = {', file=opt_in)
        # for floor in range(1, self.NumFloors + 1):
        #     print(f'  {{{rooms_mgr[floor]}, {rooms_mgr[floor]}, {rooms_mgr[floor]}}}', file=opt_in)
        # print('};', file=opt_in)

        # As array of arrays
        print('rooms = #[', file=output_file)
        for floor in sorted(floor_names):
            print(f'  "{floor}": #["Manager": {rooms_mgr[floor]}, '
                  f'"Researcher": {rooms_researcher[floor]}, '
                  f'"Shelter": {rooms_student[floor]}]#',
                  file=output_file)
        print(']#;', file=output_file)
        output_file.close()
        # print(counter)

    def collect_rooms(self):
        # This method supports both the Tririga and HRLoffices formats
        file = pd.read_csv(os.path.join(self.folder, self.tririga_file_name))
        df = pd.DataFrame(file)
        folder = self.folder
        floor_names = set()
        rooms = set()
        rooms_mgr = Counter()
        rooms_researcher = Counter()
        rooms_student = Counter()
        for index, row in df.iterrows():
            if 'Building ID' not in df:
                continue
            if row['Building ID'] not in ('972-31905:HLB', 'Haifa'):
                continue
            row['Floor ID'] = str(row['Floor ID'])
            if row['Floor ID'].startswith('0'):
                row['Floor ID'] = row['Floor ID'][1:]
            if row['Floor ID'] == 'E':
                continue
            if row['Room ID'] in self.ConfRooms:  # Filter conference rooms
                continue
            if row['Room ID'] in rooms:
                continue
            floor_names.add(str(row['Floor ID']))
            if row['Room Usage'].strip() == self.RoomUsageManager and row['architect plan '] == self.RoomUsageRSM:
                row['Room Usage'] = self.RoomUsageRSM
            floor_number = str(row['Floor ID'])
            if row['Room Usage'].strip() == self.RoomUsageStudent:
                rooms_student[floor_number] += 1
                rooms.add(row['Room ID'])
            elif row['Room Usage'].strip() == self.RoomUsageManager:
                rooms_mgr[floor_number] += 1
                rooms.add(row['Room ID'])
            elif row['Room Usage'].strip() == self.RoomUsageRSM:
                rooms_researcher[floor_number] += 1
                rooms.add(row['Room ID'])
        return rooms_mgr, rooms_researcher, rooms_student, floor_names


if __name__ == '__main__':
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = r'D:\Yishai\ws\CPLEX\OfficeSpaceOptimization\OSOpt'
    gen = InputGenerator(folder)
    gen.write_opl()
