from validator2solver.optimistic_factory import generate_ast_from_file


if __name__ == '__main__':
    file_path = r'../../optimistic_examples/room_allocation/room_allocation_bom_6_all_in_one.py'
    generate_ast_from_file(file_path, print_translations=True)

