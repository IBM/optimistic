from collections import deque
from pathlib import Path

from codegen.utils import visitor_for
from generated.Python3Parser import Python3Parser
from generated.Python3Visitor import Python3Visitor
from validator2solver.python.python_rep import PythonElement, PythonFile, PythonStatements, PythonVariable, PythonAttribute, \
    PythonImport, PythonImportFrom, PythonImportAll, PythonImportAs

OPTIMISTIC_CLIENT_PACKAGE = 'optimistic_client'


@visitor_for(PythonElement, collect_results=False)
class AbstractVisitor:
    pass


class SymbolTablePackageVisitor(AbstractVisitor):
    def __init__(self, root_path):
        self.root_path = root_path
        self.modules = []

    def visit_python_file(self, obj):
        super().visit_python_file(obj)

    def visit_python_class(self, obj):
        pass

    def visit_python_func_def(self, obj):
        pass

    def visit_python_import(self, obj):
        # print(f'Import -> {obj}[{obj.names}] ')
        import_ref = deque()
        for e in obj.names:
            if isinstance(e, PythonVariable):
                import_ref.append((e.name.name, None))
            if isinstance(e, PythonAttribute):
                import_ref = self.resolve_attribute_chain(import_ref, e)
            if isinstance(e, PythonImportAs):
                import_ref.append((e.name, e.new_name))
        # print(f'Import -> {import_ref}')
        root_location = Path(self.root_path)
        for item in import_ref:
            parts = item[0].split('.')
            location = root_location
            module = ''
            file = ''
            for path in parts:
                if location.joinpath(path).exists() and location.joinpath(path).is_dir():
                    module += path if module == '' else '.' + path
                    location = location.joinpath(path)
                elif location.joinpath(path + '.py').is_file():
                    module += path if module == '' else '.' + path
                    file = path + '.py'
            if location.joinpath(file).exists() and location.joinpath(file).is_file():
                self.modules.append({module: {'location': location, 'file': file}})
            # print(f'Item {item[0]}-{parts}  Module - {module} - {location}/{file}\n{self.modules}\n')

    def visit_python_import_from(self, obj):
        # print(f'Import from-> {obj}[{obj.names} -- {obj.package}] ')
        import_ref = deque()
        if isinstance(obj.package, PythonVariable):
            import_ref.append((obj.package.name.name, None))
        if isinstance(obj.package, PythonAttribute):
            import_ref = self.resolve_attribute_chain(import_ref, obj.package)
        # print(f'Import from-> {import_ref}')
        root_location = Path(self.root_path)
        location = root_location
        module = ''
        file = ''
        for item in import_ref:
            parts = item[0].split('.')
            if parts[0] == OPTIMISTIC_CLIENT_PACKAGE:
                # This is part of the framework, not the individual optimization problem
                continue
            for path in parts:
                if location.joinpath(path).exists() and location.joinpath(path).is_dir():
                    module += path if module == '' else '.' + path
                    location = location.joinpath(path)
                elif location.joinpath(path + '.py').is_file():
                    module += path if module == '' else '.' + path
                    file = path + '.py'
            if location.joinpath(file).exists() and location.joinpath(file).is_file():
                self.modules.append({module: {'location': location, 'file': file}})
            # print(f'Item {item[0]}-{parts}  Module - {module} - {location}/{file}\n{self.modules}\n')

        for aname in obj.names:
            name = ''
            if isinstance(aname, PythonImportAs):
                name = aname.name
            elif isinstance(aname, PythonVariable):
                name = aname.name.name
            result = self.resolve_import_from_names(name, module, location, file)
            if result:
                self.modules.append(result)
                # print(f'ItemNames {result}\n')
        # print(f'{self.modules}\n')

    def resolve_attribute_chain(self, stack, obj):
        if isinstance(obj, PythonVariable):
            stack.append((obj.name.name, None))
        if isinstance(obj, PythonAttribute):
            stack = self.resolve_attribute_chain(stack, obj.obj)
            stack.append((str(obj.attr), None))
        return stack

    def resolve_import_from_names(self, module_name, module, location, file):
        changed = False
        name = module_name
        if location.joinpath(name).exists() and location.joinpath(name).is_dir():
            module += name if module == '' else '.' + name
            location = location.joinpath(name)
            changed = True
        elif location.joinpath(name + '.py').is_file():
            module += name if module == '' else '.' + name
            file = name + '.py'
            changed = True
        if changed and location.joinpath(file).exists() and location.joinpath(file).is_file():
            return {module: {'location': location, 'file': file}}


class PythonImportExtractor(Python3Visitor):
    def visitFile_input(self, ctx: Python3Parser.File_inputContext):
        content = []
        for stmt in ctx.stmt():
            res = self.visit(stmt)
            if isinstance(res, PythonImport) or \
                    isinstance(res, PythonImportAs) or \
                    isinstance(res, PythonImportFrom):
                content.append(res)

        return PythonFile(content)

    def visitStmt(self, ctx: Python3Parser.StmtContext):
        return self.visit(ctx.simple_stmt() or ctx.compound_stmt())

    def visitSimple_stmt(self, ctx: Python3Parser.Simple_stmtContext):
        if len(contents := ctx.small_stmt()) != 1:
            return PythonStatements([self.visit(smstmt) for smstmt in contents])
        else:
            return self.visit(contents[0])

    def visitSmall_stmt(self, ctx: Python3Parser.Small_stmtContext):
        return self.visit(ctx.expr_stmt() or ctx.del_stmt() or ctx.pass_stmt() or ctx.flow_stmt() or ctx.import_stmt()
                          or ctx.global_stmt() or ctx.nonlocal_stmt() or ctx.assert_stmt())

    def visitImport_stmt(self, ctx: Python3Parser.Import_stmtContext):
        return self.visit(ctx.import_name() or ctx.import_from())

    def visitImport_name(self, ctx: Python3Parser.Import_nameContext):
        return PythonImport(self.visit(ctx.dotted_as_names()))

    def visitDotted_as_names(self, ctx: Python3Parser.Dotted_as_namesContext):
        return [self.visit(name) for name in ctx.dotted_as_name()]

    def visitDotted_as_name(self, ctx: Python3Parser.Dotted_as_nameContext):
        if ctx.NAME() and ctx.NAME().getText() is not None:
            return PythonImportAs(ctx.dotted_name().getText(), ctx.NAME().getText())
        return PythonVariable(ctx.dotted_name().getText())

    def visitImport_from(self, ctx: Python3Parser.Import_fromContext):
        if ctx.relative:
            raise OptimisticPythonParserException('Relative imports not supported!')
        from_pkg = self.visit(ctx.dotted_name())
        if ctx.import_all:
            return PythonImportFrom(from_pkg, [PythonImportAll()])
        return PythonImportFrom(from_pkg, self.visit(ctx.import_as_names()))

    def visitImport_as_names(self, ctx: Python3Parser.Import_as_namesContext):
        return [self.visit(name) for name in ctx.import_as_name()]

    def visitImport_as_name(self, ctx: Python3Parser.Import_as_nameContext):
        if (new_name := ctx.new_name) is not None:
            text_name = new_name.text
            return PythonImportAs(ctx.NAME(0).getText(), text_name)
        return PythonVariable(ctx.NAME(0).getText())

    def visitDotted_name(self, ctx: Python3Parser.Dotted_nameContext):
        names = ctx.NAME()
        result = PythonVariable(names[0].getText())
        for attr in names[1:]:
            result = PythonAttribute(result, attr.getText())
        return result
