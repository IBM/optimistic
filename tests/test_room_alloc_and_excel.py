import filecmp
from pathlib import Path
from unittest import TestCase

from scenoptic import excel_to_opl
from tests.profiles.tpygen import test_all_profiles
from tests.test_room_alloc_to_opl import run_opl_tests, room_allocation_tests


class TestRoomAllocationAndExcel(TestCase):
    def test_room_alloc8(self, base_folder: Path = None):
        if base_folder is None:
            base_folder = Path(__file__).parent.parent.parent / 'optimistic'
        actual_path = base_folder / 'test-output/room-allocation/actual/'
        ref_path = base_folder / 'test-output/room-allocation/expected/'
        test_root_dir = base_folder
        run_opl_tests(
            {f'{k}': v
             for k, v in room_allocation_tests.items()
             if v['suffix'] in ('8',)},
            actual_path, test_root_dir=test_root_dir, debug=False)
        assert filecmp.cmp(actual_path / 'opl-heur-8.txt', ref_path / 'opl-heur-8.txt', shallow=False), \
            'Generated OPL file different for RoomAllocation8'

    def test_excel_to_opl(self):
        excel_to_opl.run_excel_test(excel_to_opl.default_excel_file, excel_to_opl.default_mod_file)
        assert filecmp.cmp(excel_to_opl.default_mod_file, excel_to_opl.default_ref_file, shallow=False), \
            'Generated OPL file different for RoomAllocation8'

    def test_eco_profiles(self):
        output_dir = test_all_profiles(silent=True).resolve().absolute()
        expected_dir = (output_dir / '../expected').resolve().absolute()
        expected_files = [f.name for f in expected_dir.glob('*.py')]
        _, mismatch, errors = filecmp.cmpfiles(expected_dir, output_dir, expected_files)
        if not mismatch and not errors:
            return
        report = []
        if mismatch:
            report.append(f'Mismatched files: {", ".join(mismatch)}.')
        if errors:
            report.append(f'Errors for files: {", ".join(errors)}.')
        raise Exception(' '.join(report))
