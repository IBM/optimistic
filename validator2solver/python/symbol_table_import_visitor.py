from collections import deque
from typing import MutableMapping, Mapping

from codegen.utils import visitor_for
from math_rep.expression_types import QualifiedName
from validator2solver.python.python_rep import PythonElement, PythonVariable, PythonAttribute, PythonImportAll, PythonImportAs, \
    PythonSetCompr, PythonForComprehension
from validator2solver.python.python_builtins import PYTHON_BUILTIN_FRAME
from validator2solver.python.symbol_table import Frame, Variable, TOP_LEVEL_FRAME_NAME, FrameKind, \
    PYTHON_BUILTIN_FRAME_NAME, lexical_path_as_string, environment_path_from_frame


@visitor_for(PythonElement, collect_results=False)
class AbstractVisitor:
    pass


class FrameStack:
    def __init__(self, root=PYTHON_BUILTIN_FRAME):
        self.stack = []
        self.builtin_frame = root
        if root:
            self.stack.append(root)

    def add(self, frame, add_parent=True):
        if not self.empty() and add_parent:
            parent = self.stack[len(self.stack) - 1]
            if parent:
                parent.children.append(frame)
                frame.parent = parent
        self.stack.append(frame)

    def empty(self):
        return len(self.stack) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty stack")
        else:
            frame = self.stack[-1]
            self.stack = self.stack[:-1]
            return frame

    def current(self):
        return self.stack[len(self.stack) - 1]

    def head(self):
        return self.builtin_frame


def is_ast_and_symbol_table_same(obj, table, frame_name):
    if obj.starts_on_line == table.get_lineno():
        # print(
        #     f'Both AST [{frame_name}] and Symbol Table [{table.get_type()} {table.get_name()}] at same level [{obj.starts_on_line}]')
        return True
    return False


def lookup_symbol_table_children(stack, obj, table, frame_name, lookup_variables=None):
    for ch in table.get_children():
        name = ch.get_name()
        lookup_variables_match = True
        if lookup_variables:
            # FIXME: here we check that the given table has all the variables of the lookup_varaibles
            # but, this may not be correct, if the lookup_variable is just partial
            # e.g for the code:
            #      {{row[i] for row in {(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12)}} for i in {0, 1, 2, 3}}
            #  the lookup variable has:  ['row'], it should have collected alsot the 'i', but due to the fact
            #       that `i` is part of the `term` it is not analyzed in the create_frame
            #  while the table has: ['.0' , 'i', 'row']
            #
            if len(list(x for x in lookup_variables if x in (s.get_name() for s in ch.get_symbols()))) == 0:
                lookup_variables_match = False
            # for symbol in ch.get_symbols():
            #     symbol_name = symbol.get_name()
            #     if '.0' != symbol_name not in lookup_variables:
            #         lookup_variables_match = False
        if not lookup_variables_match:
            continue
        if is_ast_and_symbol_table_same(obj, ch, frame_name):
            return ch
    # We reach here, and if lookup_variables is not empty,
    # we might be in the case of nested SET Comprehensions, or Generator Expressions,
    # So we must look into past table stack... for the same
    if stack and lookup_variables:
        for older_table in stack.stack[::-1]:
            ch = lookup_symbol_table_children(None, obj, older_table.table, frame_name, lookup_variables)
            if ch:
                return ch


def choose_variables_for_frame(table):
    variables = []
    symbols = table.get_symbols()
    for symbol in symbols:
        if symbol.is_local() and not symbol.is_imported():
            variables.append(Variable(symbol.get_name()))
    return set(variables)


def add_frame(parent: Frame, child: Frame):
    target_child = child
    if ch := parent.contains_child(child):
        target_child = ch
        ch.add_variables(child.variables)
    else:
        if not parent.contains_variable(target_child.name):
            parent.variables = {*parent.variables, Variable(child.name)}
        parent.children.append(target_child)
        target_child.parent = parent
    return target_child


class SymbolTableImportVisitor(AbstractVisitor):
    def __init__(self, module_name, symbol_table, builtin_frame=PYTHON_BUILTIN_FRAME, debug=False,
                 enable_code_testing=True, disable_imports_mockup=True, enable_attribute_analysis=False):
        self.symbol_table = symbol_table
        self.module_name = module_name or TOP_LEVEL_FRAME_NAME
        self.imports = {}
        self.imports_alias = {}
        self.builtin_frame = builtin_frame
        self.stack = FrameStack(builtin_frame)
        self.root = None
        self.indentation = "    "
        self.enable_code_testing = enable_code_testing
        self.disable_imports_mockup = disable_imports_mockup
        self.enable_attribute_analysis = enable_attribute_analysis
        self.TESTING_FRAME = None
        self.debug = debug
        self.exceptions = []

    def visit_python_file(self, obj):
        # variables = choose_variables_for_frame(self.symbol_table)
        # obj.frame = self.root = frame = Frame(name=self.module_name, kind=FrameKind.MODULE, table=self.symbol_table,
        #                                       variables=variables)
        variables = choose_variables_for_frame(self.symbol_table)
        parent = self.builtin_frame
        target_names = self.module_name.split('.')
        if len(target_names) == 1:
            frame = Frame(name=self.module_name, kind=FrameKind.MODULE, table=self.symbol_table,
                          variables=variables)
            frame = add_frame(parent, frame)
            obj.frame = self.root = frame
            self.stack.add(frame, False)
        else:
            for index in range(len(target_names) - 1):
                frame = Frame(name=target_names[index], kind=FrameKind.MODULE, table=self.symbol_table,
                              variables={Variable(target_names[index + 1])})
                parent = add_frame(parent, frame)
                if index == 0:
                    self.root = parent
                self.stack.add(parent, False)
            frame = Frame(name=target_names[len(target_names) - 1], kind=FrameKind.MODULE, table=self.symbol_table,
                          variables=variables)
            frame = add_frame(parent, frame)
            self.stack.add(frame, False)

        super().visit_python_file(obj)
        self.stack.remove()

    def visit_python_class(self, obj):
        frame = self.create_frame(obj, f'{obj.name}', kind=FrameKind.CLASS)
        obj.frame = frame
        self.stack.add(frame)
        super().visit_python_class(obj)
        self.stack.remove()
        if self.debug:
            line = obj.starts_on_line
            print(f'CLASS -> {obj}, line {line}, {frame}')

    def visit_python_func_def(self, obj):
        frame = self.create_frame(obj, f'{obj.name}', kind=FrameKind.FUNCTION)
        obj.frame = frame
        self.stack.add(frame)
        super().visit_python_func_def(obj)
        self.stack.remove()

    def visit_python_list_compr(self, obj):
        # frame = self.create_frame(obj, f'{obj.expr}', FrameKind.COMPREHENSION_LIST)
        frame = self.create_frame(obj, f'', FrameKind.COMPREHENSION_LIST)
        obj.frame = frame
        self.stack.add(frame)
        super().visit_python_list_compr(obj)
        self.stack.remove()

    def visit_python_set_compr(self, obj):
        # frame = self.create_frame(obj, f'{obj.expr}', FrameKind.COMPREHENSION_SET)
        frame = self.create_frame(obj, f'', FrameKind.COMPREHENSION_SET)
        obj.frame = frame
        self.stack.add(frame)
        super().visit_python_set_compr(obj)
        self.stack.remove()

    def visit_python_gen_expr(self, obj):
        # frame = self.create_frame(obj, f'{obj.expr}', FrameKind.COMPREHENSION_GEN)
        frame = self.create_frame(obj, f'', FrameKind.COMPREHENSION_GEN)
        obj.frame = frame
        self.stack.add(frame)
        super().visit_python_gen_expr(obj)
        self.stack.remove()

    def visit_python_variable(self, obj):
        frame = self.stack.current()
        defining_frame, is_import = self.find_variable_frame(obj.name, frame, self.builtin_frame)
        obj.frame = defining_frame
        current_path = obj.name.lexical_path
        new_path = self.environment_path_of_var(obj)
        if alias := self.imports_alias.get(obj.frame):
            new_path = tuple(path for path in new_path if path != alias['name'] and alias['alias'] == obj.name.name)
        if current_path != new_path:
            if self.debug:
                print(f'Changing lexical path for [{obj.name.name}] from {current_path} to {new_path}')
            obj.name = obj.name.with_path(new_path, override=current_path == (PYTHON_BUILTIN_FRAME_NAME,))
        if self.debug:
            line = obj.starts_on_line
            print(f'{obj}, line {line}, {obj.frame}')
        return defining_frame

    def visit_python_import(self, obj):
        """

        """
        frame = self.stack.current()
        if self.debug:
            print(f'Import -> {obj}[{obj.names}] , {frame}')
        import_ref = deque()
        for e in obj.names:
            if isinstance(e, PythonVariable):
                import_ref.append((e.name.name, None))
            if isinstance(e, PythonAttribute):
                import_ref = self.resolve_attribute_chain(import_ref, e)
            if isinstance(e, PythonImportAs):
                import_ref.append((e.name, e.new_name))
        if self.debug:
            print(f'Import -> {import_ref}')
        try:
            self.assert_import_frame_exist(import_ref, self.stack.head())
        except:
            if self.disable_imports_mockup:
                raise
            else:
                self.add_import_to_head(import_ref)

    def visit_python_import_from(self, obj):
        frame = self.stack.current()
        if self.debug:
            print(f'Import from-> {obj}[{obj.names} -- {obj.package}] , {frame}')
        import_ref = deque()
        if isinstance(obj.package, PythonVariable):
            import_ref.append((obj.package.name.name, None))
        if isinstance(obj.package, PythonAttribute):
            import_ref = self.resolve_attribute_chain(import_ref, obj.package)
        if self.debug:
            print(f'Import from-> {import_ref}')
        try:
            self.assert_import_frame_exist(import_ref, self.stack.head(), obj.names)
        except:
            if self.disable_imports_mockup:
                raise
            else:
                self.add_import_to_head(import_ref, obj.names)

    def visit_python_attribute(self, obj):
        """
        For simple cases the current algorithm can
        1. Find the attribute frame in the local or import module
        2. add it also with `alias`to the lookup of imports
        However,
            It is possible that we don't know what object we get as an attribute:
            e.g.  outer().inner()
            it is not straight forward what `outer()` returns, can be internal attribute in the `outer` frame
            or entirely another object instance

        in any case it is necessary to run the attribute algorithm for cases like:
            import itertools as doit
            doit.chain.from_iterable([])

        Where the AST:
            CALL(GETATTR(GETATTR(REF(*python-builtins*.itertools.doit), chain), from_iterable); LIST()))
        and we need to attach to
            REF(*python-builtins*.itertools.doit)
            the itertools frame
        """
        frame = self.stack.current()
        if self.debug:
            line = obj.starts_on_line
            print(f'ATTR -> {obj}, line {line}, {frame}')
        ref_queue = self.resolve_attribute_chain(deque(), obj)
        if self.debug:
            print(f'ATTR -> {obj}, REF -> {ref_queue}, {[var for var in ref_queue]}---{ref_queue.pop()}')
        if self.enable_attribute_analysis:
            variable = obj.attr
            try:
                parent_frame = super().visit_python_attribute(obj)
            except:
                variable = ".".join(var[0] for var in ref_queue) + '.' + variable
                parent_frame = [self.builtin_frame]
            defining_frame, is_import = self.find_variable_frame(variable, frame, parent_frame[0])
            if is_import:
                self.register_import_symbol(variable, defining_frame)
                for e in variable.split("."):
                    self.register_import_symbol(e, defining_frame)
                if defining_frame.is_mockup():
                    if isinstance(obj.obj, PythonVariable):
                        obj.obj.frame = defining_frame
            return defining_frame
        else:
            super().visit_python_attribute(obj)

    def visit_python_parm(self, obj):
        obj.frame = self.stack.current()
        super().visit_python_parm(obj)  # replace qualified name of type (if any) according to its frame
        if self.debug:
            line = obj.starts_on_line
            print(f'PARAM -> {obj}, line {line}, {obj.frame}')

    # def visit_python_list_cons(self, obj):
    #     pass

    def find_import_frame(self, var, frame, target_parent, builtin_frame=PYTHON_BUILTIN_FRAME):
        defining_ast_frame = self.find_variable_in_import_frame(var, target_parent)
        if defining_ast_frame:
            return defining_ast_frame, True
        if builtin_frame.mockup and not self.disable_imports_mockup:
            mockup_frame = Frame(name=f'{var.name}', kind=FrameKind.UNKNOWN, mockup=True)
            builtin_frame.children.append(mockup_frame)
            mockup_frame.parent = builtin_frame
            builtin_frame.variables_by_role = {Variable(var.name), *builtin_frame.variables_by_role}
            # return mockup_frame, True
            return builtin_frame, True
        elif frame == builtin_frame:
            return frame, False
        elif self.enable_code_testing:
            if not self.TESTING_FRAME:
                self.TESTING_FRAME = Frame(name=f'*testing*', kind=FrameKind.MODULE, mockup=True)
                builtin_frame.children.append(self.TESTING_FRAME)
                self.TESTING_FRAME.parent = builtin_frame
            if not self.TESTING_FRAME.contains_variable(var.name):
                symbol_name = var.name
                if isinstance(var.name, QualifiedName):
                    symbol_name = var.name.name
                self.TESTING_FRAME.variables = {Variable(symbol_name), *self.TESTING_FRAME.variables}
            return self.TESTING_FRAME, False
        else:
            defining_ast_frame, is_import = self.find_import_frame(var, frame, self.builtin_frame, builtin_frame)
            if not defining_ast_frame:
                raise Exception(f'Missing Import Frame for {var}')
            return defining_ast_frame, is_import

    def find_variable_frame(self, var_name, frame, builtin_frame=PYTHON_BUILTIN_FRAME):
        var = Variable(var_name) if isinstance(var_name, str) else var_name
        defining_ast_frame = self.find_ast_variable_in_frame(var, frame)
        if defining_ast_frame is None:
            return self.find_import_frame(var, frame, builtin_frame, builtin_frame)
        return defining_ast_frame, False

    def find_ast_variable_in_frame(self, obj, frame):
        if not frame:
            return None
        if frame.contains_variable(obj.name):
            return frame
        else:
            return self.find_ast_variable_in_frame(obj, frame.parent)

    def find_variable_in_import_frame(self, obj, frame):
        if not frame:
            return None

        if PYTHON_BUILTIN_FRAME_NAME == frame.name:
            # The obj is member of the builtin frame
            # it must be a module, so we return the module frame
            for ch in frame.children:
                if ch.qualified_name() == obj.name:
                    return ch if ch.is_file() else frame
        if frame.contains_variable(obj.name):
            return frame

        for ch in frame.children:
            if rs_frame := self.find_variable_in_import_frame(obj, ch):
                return rs_frame

        # if we reach here we must check if the object is actually an alias
        # to existing frame
        if alias_frame := self.imports.get(obj.name):
            # TODO: Check if alias in imports
            if alias_frame[0] == frame:
                return frame

        return None

    def resolve_attribute_chain(self, stack, obj):
        if isinstance(obj, PythonVariable):
            stack.append((obj.name.name, None))
        if isinstance(obj, PythonAttribute):
            stack = self.resolve_attribute_chain(stack, obj.obj)
            stack.append((str(obj.attr), None))
        return stack

    def register_import_symbol(self, name, frame, alias=None):
        frame_path = lexical_path_as_string(frame)
        if frame.contains_variable(name):
            frame_path += '.' + name

        if alias:
            if not self.imports_alias.get(frame):
                self.imports_alias[frame] = {'name': name, 'alias': alias}
            if not self.imports.get(alias):
                self.imports[alias] = []
            if frame not in self.imports[alias]:
                self.imports[alias] = [frame, *self.imports[alias]]

        alias_path = None
        parent = frame
        while parent:
            if alias_elem := self.imports_alias.get(parent):
                alias_path = frame_path.replace(alias_elem['name'], alias_elem['alias'])
                alias_path = alias_path[alias_path.find(alias_elem['alias']):]
            parent = parent.parent

        if alias_path:
            self.imports[alias_path] = [frame]

        if not alias and not alias_path:
            target_names = [name, *name.split('.')] if name.find('.') > 0 else [name]

            for a_name in target_names:
                if not self.imports.get(a_name):
                    self.imports[a_name] = []

                if frame not in self.imports[a_name]:
                    self.imports[a_name] = [frame, *self.imports[a_name]]

            if not self.imports.get(frame_path):
                self.imports[frame_path] = [frame]

    def assert_import_frame_exist(self, import_name_stack, parent_frame, symbols=[]):
        frame = self.stack.head()

        for module_name, alias in import_name_stack:
            target_names = module_name.split('.')
            for i, name in enumerate(target_names):
                found = False
                for ch in frame.children:
                    if ch.qualified_name() == name:
                        target_alias = alias if i == len(target_names) - 1 else None
                        frame = ch
                        self.register_import_symbol(name, frame, target_alias)
                        found = True
                        break
            if not found:
                self.exceptions.append({'name': module_name, 'is_symbol': False})
                raise Exception(f'Missing Import Frame {module_name}')

        # In case of `from...import` we can expect symbol variables that
        # are variables in current frame and have their own frame set as child to current frame
        for s in symbols:
            if isinstance(s, PythonImportAll):
                raise Exception(
                    f'Detected Any [{"*"}] Import from [{".".join(import_name_stack)}] change to a specific module attribute')
            alias = None
            symbol_name = None
            if isinstance(s, PythonImportAs):
                symbol_name = s.name
                alias = s.new_name
            if isinstance(s, PythonVariable):
                symbol_name = s.name.name
            if frame.contains_variable(symbol_name):
                self.register_import_symbol(symbol_name, frame, alias)
            else:
                self.exceptions.append({'name': s, 'is_symbol': True, 'frame': frame})
                raise Exception(f'Missing Symbol Variable {s} in Frame {frame.name}')
        return frame

    def add_import_to_head(self, import_name_stack, symbols=[]):
        parent = self.stack.head()
        frame = None
        for module_name, alias in import_name_stack:
            frame = Frame(name=f'{module_name}', kind=FrameKind.MODULE, mockup=True)
            parent.children.append(frame)
            frame.parent = parent
            self.register_import_symbol(module_name, frame, alias)
            if not parent.is_builtin():
                variables = [Variable(frame.name)]
                parent.variables = {*variables, *parent.variables}
            parent = frame
        variables = []
        for symbol in symbols:
            if isinstance(symbol, PythonImportAll):
                raise Exception(
                    f'Detected Any [{"*"}] Import from [{".".join(import_name_stack)}] change to a specific module attribute')
            alias = None
            if isinstance(symbol, PythonImportAs):
                symbol_name = symbol.new_name
                alias = symbol.name
            else:
                symbol_name = symbol.name.name
            variables.append(Variable(symbol_name))
            self.register_import_symbol(symbol_name, frame, alias)
        frame.variables = {*frame.variables, *variables}

    def create_frame(self, obj, frame_name, kind):
        table = self.stack.current().table
        lookup_variables = []
        if kind in (FrameKind.COMPREHENSION_GEN, FrameKind.COMPREHENSION_SET, FrameKind.COMPREHENSION_LIST):
            if isinstance(obj, PythonSetCompr) and isinstance(obj.control, PythonForComprehension):
                rest = obj.control
                while rest:
                    if isinstance(rest, PythonForComprehension):
                        for var in rest.vars:
                            if isinstance(var, PythonVariable):
                                lookup_variables.append(var.name.name)
                    rest = rest.rest
        next_table = lookup_symbol_table_children(self.stack, obj, table, frame_name, lookup_variables)
        variables = choose_variables_for_frame(next_table)
        return Frame(name=frame_name, kind=kind, table=next_table, variables=variables)

    def environment_path_of_var(self, var, alias_already_accounted=False):
        new_path = environment_path_from_frame(var.frame)
        var_name = var.name.name
        alias_name = var_name
        if alias := self.imports_alias.get(var.frame):
            # For a module alias we also must not include the original frame name in the path
            # i.e  `import itertools as doit`
            # AST:  We expect REF(doit)  instead of REF(itertools.doit)
            if not alias_already_accounted:
                new_path = tuple(path for path in new_path if path != alias['name'] and alias['alias'] == alias_name)
                var_name = alias['name']
        if var.frame.parent == self.builtin_frame and not var.frame.contains_variable(var_name):
            # Usually, we set the frame of the root module variable to itself, instead of it's parent `*builtin_frame*`
            # i.e import itertools:
            # AST: we expect REF(itertools) instead of REF(itertools.itertools)

            name = var.frame.name if not var.frame.is_file() else var.frame.qualified_name()
            # new_path = tuple(path for path in new_path if path != var.frame.qualified_name())
            new_path = tuple(path for path in new_path if path != name)
        return new_path

    def describe(self, root=None, indent=0):
        space = self.indentation * indent
        if root is None:
            root = self.root
        if root is not None:
            print(f'{space}{root.describe()}')
            for frame in root.children:
                self.describe(frame, indent + 1)

    def create_class_members(self) -> MutableMapping[QualifiedName, Mapping[str, QualifiedName]]:
        """
        Return a dict mapping qualified names of classes to a mapping from member names to their qualified names for all
        members of the class (fields and methods)
        """

        def collect_class_members(frame: Frame, result: MutableMapping[QualifiedName, Mapping[str, QualifiedName]]):
            if frame.is_class():
                # assert frame.name.startswith(CLASS_FRAME_PREFIX)
                assert frame.kind == FrameKind.CLASS
                frame_path = environment_path_from_frame(frame)
                # class_qn = QualifiedName(frame.name[len(CLASS_FRAME_PREFIX):], lexical_path=frame_path[1:])
                class_qn = QualifiedName(frame.name, lexical_path=frame_path[1:])
                result[class_qn] = {var.name: QualifiedName(var.name, lexical_path=frame_path)
                                    for var in frame.variables}
            for subframe in frame.children:
                collect_class_members(subframe, result)

        result = {}
        collect_class_members(self.builtin_frame, result)
        return result
