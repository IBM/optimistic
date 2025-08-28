from validator2solver.optimistic_factory import create_system_symbol_table_from_file
from optimistic_symbol.symbol_explore import query_children


if __name__ == '__main__':
    symbol_table = create_system_symbol_table_from_file(
        r'../../optimistic_examples/room_allocation/resource_allocation_bom.py')
    query_children(symbol_table)
