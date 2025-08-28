import os
from pathlib import Path

from parsing.python.symbol_default_imports import add_import_frame
from parsing.python.symbol_table import Frame, FrameKind, Variable
from validator2solver.optimistic_factory import generate_symbol_table_from_file, add_frame
from parsing.python.python_to_expr import PythonToExpr
from test_utils import Tee

test_output_dir = '../../test-output/symbol_table/actual/'
actual_dir = Path(test_output_dir)


def add_itertools_frame(buitlin_frame=None):
    buitlin_frame = add_import_frame(buitlin_frame, do_examples=True)

    add_frame(buitlin_frame, Frame(name=f'sys', kind=FrameKind.MODULE))

    module_first_frame = add_frame(buitlin_frame, Frame(name=f'optimistic', kind=FrameKind.MODULE,
                                                        variables={Variable('optimistic_factory')}))
    add_frame(module_first_frame, Frame(name=f'optimistic_factory', kind=FrameKind.MODULE,
                                        variables={Variable('generate_ast_from_file')}))

    module_first_frame = add_frame(buitlin_frame, Frame(name=f'optimistic_symbol', kind=FrameKind.MODULE,
                                                        variables={Variable('symbol_explore')}))
    module_frame = add_frame(module_first_frame, Frame(name=f'symbol_explore', kind=FrameKind.MODULE,
                                                       variables={Variable('parse_file')}))
    add_frame(module_frame, Frame(name='from_iterable', kind=FrameKind.FUNCTION))

    module_first_frame = add_frame(buitlin_frame, Frame(name=f'requirements', kind=FrameKind.MODULE,
                                                        variables={Variable('expr')}))
    module_frame = add_frame(module_first_frame, Frame(name=f'expr', kind=FrameKind.MODULE,
                                                       variables={Variable('IFTE'), Variable('Negation'),
                                                                  Variable('AGGREGATE_SYMBOL_MAP')}))
    func_frame = add_frame(module_frame, Frame(name='IFTE', kind=FrameKind.FUNCTION, variables={Variable('describe')}))
    add_frame(func_frame, Frame(name='describe', kind=FrameKind.FUNCTION))
    func_frame = add_frame(module_frame,
                           Frame(name='Negation', kind=FrameKind.FUNCTION, variables={Variable('to_code_rep')}))
    add_frame(func_frame, Frame(name='to_code_rep', kind=FrameKind.FUNCTION, variables={Variable('accept')}))

    return buitlin_frame


def do_test(filePath, builtin_frame):
    filename = os.path.basename(filePath)
    if filename.endswith(".py"):
        module_name = filename[:-3]
    outputFile = actual_dir.joinpath(str(module_name) + "_symbol_table.log")
    test_tee = Tee(outputFile)

    config = {
        'symbol_table_config': {
            'enable_code_testing': False,
            'disable_imports_mockup': True,
            'enable_attribute_analysis': False,
            'debug': True,
        }}

    ast, symbol_table_visitor = generate_symbol_table_from_file(filePath, config=config, print_translations=True,
                                                                builtin_frame=builtin_frame)

    expr_extractor = PythonToExpr(symbol_table_visitor)
    expr = expr_extractor.visit(ast)

    with test_tee:
        print(f'File: {filename}')
        print(f'AST: {ast}')
        print(f'Expression: {expr}')


tests = {'../test-data/symbol_table/test_symbol_table_input.py': {'run': False, 'builtin': add_itertools_frame()},
         '../test-data/symbol_table/test_short.py': {'run': False, 'builtin': add_itertools_frame()},
         '../test-data/symbol_table/test_short_02.py': {'run': False, 'builtin': add_itertools_frame()},
         '../test-data/symbol_table/test_short_03.py': {'run': False, 'builtin': add_itertools_frame()},
         '../test-data/symbol_table/test_short_04.py': {'run': False, 'builtin': add_itertools_frame()},
         '../test-data/symbol_table/test_short_05.py': {'run': False, 'builtin': add_itertools_frame()},
         '../test-data/symbol_table/test_long.py': {'run': True, 'builtin': add_itertools_frame()},
         '../test-data/symbol_table/test_long_02.py': {'run': True, 'builtin': add_itertools_frame()},
         '../test-data/symbol_table/test_long_03.py': {'run': True, 'builtin': add_itertools_frame()},
         '../test-data/symbol_table/test_long_04.py': {'run': True, 'builtin': add_itertools_frame()}
         }

# tests = {'../test-data/symbol_table/test_symbol_table_input.py': {'run': False, 'builtin': add_itertools_frame()},
#          '../test-data/symbol_table/test_short.py': {'run': True, 'builtin': add_itertools_frame()},
#          '../test-data/symbol_table/test_short_02.py': {'run': True, 'builtin': add_itertools_frame()},
#          '../test-data/symbol_table/test_short_03.py': {'run': True, 'builtin': add_itertools_frame()},
#          '../test-data/symbol_table/test_short_04.py': {'run': True, 'builtin': add_itertools_frame()},
#          '../test-data/symbol_table/test_short_05.py': {'run': True, 'builtin': add_itertools_frame()},
#          '../test-data/symbol_table/test_long.py': {'run': False, 'builtin': add_itertools_frame()},
#          '../test-data/symbol_table/test_long_02.py': {'run': False, 'builtin': add_itertools_frame()},
#          '../test-data/symbol_table/test_long_03.py': {'run': False, 'builtin': add_itertools_frame()},
#          '../test-data/symbol_table/test_long_04.py': {'run': False, 'builtin': add_itertools_frame()}
#          }

# tests = {'../test-data/symbol_table/test_symbol_table_input.py': {'run': True, 'builtin': add_itertools_frame()}
#          }

if __name__ == '__main__':
    for key, value in tests.items():
        if value['run']:
            do_test(key, value['builtin'])
