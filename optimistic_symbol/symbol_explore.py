indentation = "    "


def query_children(table, indent=0):
    space = indentation * indent
    print(
        f'{space} (type, name, id, line): {table.get_type()}, {table.get_name()}, {table.get_id()}, {table.get_lineno()}')
    query_symbols(table, indent)
    query_identifiers(table, indent)
    if "class" == table.get_type():
        query_class(table, indent)
    if "function" == table.get_type():
        query_function(table, indent)
    for ch in table.get_children():
        name = ch.get_name()
        print(f'{space} table {table.get_name()}, child: {name}')
        query_children(ch, indent + 1)


def query_function(func, indent=0):
    space = indentation * indent
    print(f'{space} Function Parameters {func.get_parameters()}')
    print(f'{space} Function Locals {func.get_locals()}')
    print(f'{space} Function Globals {func.get_globals()}')
    print(f'{space} Function nonlocals {func.get_nonlocals()}')
    print(f'{space} Function Frees {func.get_frees()}')


def query_class(aclass, indent=0):
    space = indentation * indent
    print(f'{space} Class Methods {aclass.get_methods()}')


def query_identifiers(table, indent=0):
    space = indentation * indent
    print(f'{space} Identifiers Frees {table.get_identifiers()}')


def query_symbols(table, indent=0):
    space = indentation * indent
    symbols = table.get_symbols()
    for symbol in symbols:
        if len(symbol.get_namespaces()) > 0:
            print(f'{space} Namespaces: ns={symbol.get_namespaces()}')
        print(f'{space} Symbol: name={symbol.get_name()},'
              f' imported={symbol.is_imported()},'
              f' referenced={symbol.is_referenced()},'
              f' imported={symbol.is_imported()},'
              f' param={symbol.is_parameter()},'
              f' global={symbol.is_global()},'
              f' nonlocal={symbol.is_nonlocal()},'
              f' declared_global={symbol.is_declared_global()},'
              f' local={symbol.is_local()},'
              f' free={symbol.is_free()},'
              f' assigned={symbol.is_assigned()},'
              f' namespace={symbol.is_namespace()},')
