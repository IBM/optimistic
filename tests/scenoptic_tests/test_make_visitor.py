from codegen.utils import visitor_for
from parsing.python.python_rep import PythonElement
from validator2solver.optimistic_factory import generate_ast_from_file


@visitor_for(PythonElement)
class AbstractVisitor:
    pass


class Visitor(AbstractVisitor):
    def visit_python_file(self, obj):
        print('Entering File')
        super().visit_python_file(obj)
        line = obj.starts_on_line
        print(f'Exiting File, line {line}')

    def visit_python_class(self, obj):
        print(f'Entering class {obj.name}')
        super().visit_python_class(obj)
        line = obj.starts_on_line
        print(f'Exiting file {obj.name}, line {line}')

    def visit_python_func_def(self, obj):
        print(f'Entering Function {obj.name}')
        super().visit_python_func_def(obj)
        line = obj.starts_on_line
        print(f'Exiting function {obj.name}, line {line}')

    def visit_python_list_compr(self, obj):
        print(f'Entering List Comprehension {obj.expr}')
        super().visit_python_list_compr(obj)
        line = obj.starts_on_line
        print(f'Exiting List Comprehension {obj.expr}, line {line}')

    def visit_python_set_compr(self, obj):
        print(f'Entering Set Comprehension {obj.expr}')
        super().visit_python_set_compr(obj)
        line = obj.starts_on_line
        print(f'Exiting Set Comprehension {obj.expr}, line {line}')

    def visit_python_gen_expr(self, obj):
        print(f'Entering Gen Comprehension {obj.expr}')
        super().visit_python_gen_expr(obj)
        line = obj.starts_on_line
        print(f'Exiting Gen Comprehension {obj.expr}, line {line}')

    def visit_python_variable(self, obj):
        line = f', line: {obj.starts_on_line}'
        print(f'{obj}{line}')


if __name__ == '__main__':
    # print(collect_subclasses(PythonElement))
    # print([m[1].__name__ for m in getmembers(Visitor, isfunction)])
    # print(getmembers(AbstractVisitor, isfunction))
    # print(PythonComparison.__init__.__ignored_vars)
    val = generate_ast_from_file(r'../../optimistic_examples/room_allocation/resource_allocation_bom.py')
    Visitor().visit(val)
