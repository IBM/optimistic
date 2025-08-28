import os
import symtable
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

import antlr4
from antlr4 import BailErrorStrategy
from toposort import toposort_flatten

from validator2solver.codegen.opl.opl_generator import OplVisitor
from generated.Python3Lexer import Python3Lexer
from generated.Python3Parser import Python3Parser
from optimistic_client.config import configuration
from validator2solver.python.parse_python_spec import PythonSpecExtractor
from validator2solver.python.python_generator import PythonVisitor
from validator2solver.python.python_rep import PythonElement
from validator2solver.python.python_to_expr import PythonToExpr
from validator2solver.python.python_builtins import PYTHON_BUILTIN_FRAME
from validator2solver.python.symbol_table import Frame
from validator2solver.python.symbol_table_import_visitor import SymbolTableImportVisitor, add_frame as visitor_add_frame
from validator2solver.python.symbol_table_package_visitor import SymbolTablePackageVisitor, PythonImportExtractor


#####
##
# utils
##
######

def get_config(file_path=None):
    aconfig = configuration.config()
    if file_path:
        aconfig.reset()
        target = Path(file_path).resolve()
        print(f'Loading configuration: {target}')
        configuration.init_from_file(target)
    return aconfig


def get_target_module_json(target_root_dir, file_path, module_name=None):
    return {'target_module': {
        'root_path': target_root_dir,
        'module_name': module_name or get_module_name(file_path, target_root_dir),
        'module': file_path
    }}


def get_module_name(filePath, root_path):
    file = Path(filePath)
    if not file.is_absolute():
        file = root_path / file
    if file.is_file():
        relative = file.resolve().relative_to(root_path)
        module_name = '.'.join(Path(str(relative)[:-len(relative.name)]).parts) + '.' + relative.stem
        return module_name
    raise Exception(f"Invalid file {file.resolve().absolute()}")


def get_code(file_path):
    with open(file_path, 'r') as test_file:
        spec = test_file.read()
        return spec


def add_frame(parent: Frame, child: Frame):
    return visitor_add_frame(parent, child)


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def suggest_module_name(file_path):
    filename = os.path.basename(file_path)
    if filename.endswith(".py"):
        module_name = filename[:-3]
    else:
        module_name = filename
    return module_name


#####
##
# Factories for end to end creation
##
######
def create_registry(config=None, builtin_frame=PYTHON_BUILTIN_FRAME, print_translations=False):
    registry, existing, priority = analyze_symbol_table_from_file(config=config, print_translations=print_translations)

    planned_registry, planned_priority = plan_symbol_table_order(registry, priority)

    symbol_registry, symbol_visitor = generate_symbol_table_package(planned_registry, config=config,
                                                                    builtin_frame=builtin_frame,
                                                                    print_translations=print_translations)

    root_registry = symbol_registry[0]
    for module_name in root_registry:
        root_model = root_registry[module_name]['model']
        for module in symbol_registry[1:]:
            for m_name in module:
                model = module[m_name]['model']
                root_model.add_module(model)

    if print_translations:
        print(
            f'File: {os.path.basename(config["target_module"]["module"])} {config["target_module"]["module_name"]}\n')
        print(f'Existing {sorted(existing)}')
        print(f'Priority {priority}')
        print(f'Registry {registry}')
        print(f'Topological Sort {planned_priority}')
        print(f'Planned Registry -{planned_registry}')
        print(f'Symbol Registry -{symbol_registry}')
        print(f'Symbol Table builtin frame')
        describe(describe(symbol_visitor.builtin_frame))
        print('Frame Imports:')
        for akey, avalue in symbol_visitor.imports.items():
            print(f'   {akey} -> {avalue}')

    return symbol_registry


#####
##
# Factories for creating the Python AST
##
######


def create_ast_from_string(spec):
    input_stream = antlr4.InputStream(spec)
    lexer = Python3Lexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    parser._errHandler = BailErrorStrategy()
    tree = parser.file_input()
    return tree, parser


def generate_ast_from_file(file_path, print_translations=False, print_result=False):
    spec = get_code(file_path)
    return generate_ast_from_string(spec, print_translations, print_result)


def generate_ast_from_string(spec, print_translations=False, print_result=False):
    tree, parser = create_ast_from_string(spec)
    if print_result:
        print(f'Result: {tree.toStringTree(recog=parser).strip()}')
    extractor = PythonSpecExtractor()
    result = extractor.visit(tree)
    # print(result)
    if print_translations:
        for text, trans in extractor.mapping:
            print('=====')
            print(text)
            print('-----')
            print(trans.describe() if isinstance(trans, PythonElement) else trans)
    return result


#####
##
# Factories for analyzing package structure for creating the Symbol Table from the Python AST
##
######
def generate_symbol_table_package(planned_registry, config=None, builtin_frame=PYTHON_BUILTIN_FRAME,
                                  print_translations=False):
    root = builtin_frame
    symbol_registry = []
    ast_module = symbol_visitor = None
    root_registry = None
    root_symbol_visitor = None
    for module in planned_registry:
        for module_name in module:
            file_path = str(Path(module[module_name]['location']).joinpath(module[module_name]['file']))

            ast_module, symbol_visitor = generate_symbol_table_from_file(file_path, module_name=module_name,
                                                                         config=config,
                                                                         print_translations=False,
                                                                         builtin_frame=root)
            expr = generate_expr(ast_module, symbol_visitor)
            # module[module_name]['model'] = expr
            copy = {module_name: {
                'location': module[module_name]['location'],
                'file': module[module_name]['file'],
                'ast': ast_module,
                'model': expr
            }}
            if module_name == config['target_module']['module_name']:
                root_registry = copy
                root_symbol_visitor = symbol_visitor
            else:
                symbol_registry.append(copy)
            if print_translations:
                print(f'File: {file_path}')
                print(f'AST: {ast_module}')
                print(f'EXPR: {expr}\n')

    symbol_registry.insert(0, root_registry)
    return symbol_registry, root_symbol_visitor


def plan_symbol_table_order(module_registry, module_priority, print_translations=False):
    if len(module_priority) == 0:
        planned_registry = []
        for module in module_registry:
            planned_registry.append(module_registry[module])
        return planned_registry, []

    d = defaultdict(list)
    for k, v in module_priority:
        d[k].append(v)

    for k in d.keys():
        d[k] = set(d[k])

    planned_priority = toposort_flatten(d)

    planned_registry = []
    for target in planned_priority:
        if target in module_registry:
            planned_registry.append(module_registry[target])

    return planned_registry, planned_priority


def analyze_symbol_table_from_file(config=None,
                                   print_translations=False):
    root_path = config['target_module']['root_path']
    module_name = config['target_module']['module_name']
    file_path = config['target_module']['module']
    file = (Path(root_path) / file_path).resolve()
    candidate = {module_name: {'location': file.parent, 'file': file.name}}

    registry, existing, priority = _analyze_symbol_table_from_string(candidate=candidate, root_path=root_path,
                                                                     print_translations=print_translations)

    return registry, existing, priority


def _analyze_symbol_table_from_string(candidate, root_path,
                                      module_registry={}, existing_modules=set(), module_priority=[],
                                      print_translations=False):
    registry = module_registry if module_registry else {}
    existing = existing_modules if existing_modules else set()
    priority = module_priority if module_priority else []

    module_name = next(iter(candidate))
    file_path = candidate[module_name]['location'].joinpath(candidate[module_name]['file'])
    code = get_code(str(file_path))

    # ast_module = generate_ast_from_string(code)

    # Replacing the above line with simple Python parser
    # we drop everything in the generated AST , besides the Import statements
    tree, parser = create_ast_from_string(code)
    extractor = PythonImportExtractor()
    ast_module = extractor.visit(tree)

    visitor = SymbolTablePackageVisitor(root_path)
    visitor.visit(ast_module)

    keep_candidate = deepcopy(candidate)
    keep_candidate[module_name]['ast'] = ast_module
    registry[module_name] = keep_candidate

    new_registry = []
    for candidate in visitor.modules:
        for key in candidate:
            priority.append((module_name, key))
            if key not in existing:
                existing.add(key)
                new_registry.append(candidate)

    for e in new_registry:
        registry, existing, priority = _analyze_symbol_table_from_string(e, root_path, registry, existing, priority,
                                                                         print_translations)

    return registry, existing, priority


#####
##
# Factories for creating the Symbol Table from the Python AST
##
######


def describe(root, indent=0, indentation="    "):
    space = indentation * indent
    if root:
        print(f'{space}{root.describe()}')
        for frame in root.children:
            describe(frame, indent + 1)


def create_system_symbol_table_from_file(file_path, print_translations=False):
    filename = os.path.basename(file_path)
    if filename.endswith(".py"):
        module_name = filename[:-3]
    else:
        module_name = filename

    if print_translations:
        print(file_path)
        print(filename)
        print(module_name)

    code = get_code(file_path)
    return create_system_symbol_table_from_string(code, file_path, print_translations)


def create_system_symbol_table_from_string(code, filename, print_translations=False):
    symbol_table = symtable.symtable(code, filename, 'exec')
    return symbol_table


DEFAULT_SYMBOL_VISITOR_CONFIG = {
    'symbol_table_config': {
        'enable_code_testing': False,
        'disable_imports_mockup': True,
        'enable_attribute_analysis': False,
        'debug': False
    }
}


def generate_symbol_table_from_file(file_path, module_name=None, ast_module=None, config=None,
                                    print_translations=False, builtin_frame=PYTHON_BUILTIN_FRAME) -> (
        Any, SymbolTableImportVisitor):
    aconfig = config if config else DEFAULT_SYMBOL_VISITOR_CONFIG
    code = get_code(file_path)
    module_name = module_name if module_name else suggest_module_name(file_path)
    return generate_symbol_table_from_string(code, module_name, ast_module, aconfig, print_translations, builtin_frame)


def generate_symbol_table_from_string(code, module_name=None, ast_module=None, config=None, print_translations=False,
                                      builtin_frame=PYTHON_BUILTIN_FRAME) -> (Any, SymbolTableImportVisitor):
    aconfig = (config.get('symbol_table_config') if config and config.get('symbol_table_config') else
               DEFAULT_SYMBOL_VISITOR_CONFIG['symbol_table_config'])
    symbol_table = create_system_symbol_table_from_string(code, 'any')
    if ast_module is None:
        ast_module = generate_ast_from_string(code)

    visitor = SymbolTableImportVisitor(module_name, symbol_table, builtin_frame=builtin_frame,
                                       debug=aconfig.get('debug', False),
                                       enable_code_testing=aconfig.get('enable_code_testing', False),
                                       disable_imports_mockup=aconfig.get('disable_imports_mockup', True),
                                       enable_attribute_analysis=aconfig.get('enable_attribute_analysis', False))
    visitor.visit(ast_module)
    if print_translations:
        print(f'Symbol Table Factory')
        describe(visitor.root)
        print(f'Symbol Table builtin frame')
        describe(describe(visitor.builtin_frame))
        print('Frame Imports:')
        for key, value in visitor.imports.items():
            print(f'   {key} -> {value}')
    return ast_module, visitor


#####
##
# Factories for creating the Optimistic model (math expression) from AST, and Symbol Tables
##
######

def generate_expr_from_file(file_path, module_name=None, config=None, print_translations=False,
                            builtin_frame=PYTHON_BUILTIN_FRAME,
                            print_all=False):
    spec = get_code(file_path)
    module_name = module_name if module_name else suggest_module_name(file_path)
    return generate_expr_from_string(spec, module_name, config, print_translations, builtin_frame, print_all)


def generate_expr_from_string(spec, module_name=None, config=None, print_translations=False,
                              builtin_frame=PYTHON_BUILTIN_FRAME,
                              print_all=False):
    ast_tree = generate_ast_from_string(spec, print_result=False)
    ast, symbol_visitor = generate_symbol_table_from_string(spec, module_name, ast_module=ast_tree,
                                                            config=config,
                                                            print_translations=print_translations,
                                                            builtin_frame=builtin_frame)
    expr = generate_expr(ast, symbol_visitor)
    if print_all:
        generate_expr_end_to_end(expr)
    return expr


def generate_expr(ast, symbol_visitor):
    expr_extractor = PythonToExpr(symbol_visitor)
    expr = expr_extractor.visit(ast)
    return expr


def python_string_to_expr(spec, is_test=True, config=None, print_translations=False,
                          builtin_frame=PYTHON_BUILTIN_FRAME):
    """
    Use this to test pure expressions, without full import schemas
    like when testing patterns/rules
    """
    aconfig = config
    if is_test and not config:
        aconfig = {
            'symbol_table_config': {
                'enable_code_testing': True,
                'disable_imports_mockup': True,
                'enable_attribute_analysis': False,
                'debug': False,
            }}
    return generate_expr_from_string(spec, config=aconfig,
                                     print_translations=print_translations,
                                     builtin_frame=builtin_frame)


def generate_expr_end_to_end(expr):
    print('Expression:', expr)
    python_extractor = PythonVisitor('optimistic')
    code_rep = expr.to_code_rep()
    code = python_extractor.full_code(code_rep, '')
    print(f'Code:\n{code}')
    opl_extractor = OplVisitor(allow_undefined_vars=True)  # FIXME!!! should be False
    opl = code_rep.accept(opl_extractor).value
    print('OPL:', opl)
