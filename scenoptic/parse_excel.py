from dataclasses import dataclass

import antlr4
from functools import wraps
from numbers import Number
from typing import Tuple, Dict, Sequence

from ExcelLexer import ExcelLexer
from ExcelParser import ExcelParser
from ExcelVisitor import ExcelVisitor
from codegen.utils import decorate_method
from math_rep.constants import LE_SYMBOL, GE_SYMBOL, NOT_EQUALS_SYMBOL
from math_rep.math_frame import MATH_FRAME_PATH
from math_rep.expr import Quantity, StringTerm, FunctionApplication, FormalContent, Comparison, MathVariable, \
    LambdaExpression
from scenoptic.scenoptic_expr import Cell, CellsRange, Cells
from math_rep.expression_types import MType, M_ANY, QualifiedName, as_math_name
from scenoptic.excel_analyze_variability import VariabilityTree, bind_cell_variability_by_tree
from scenoptic.excel_data import ExcelData, CellReference
from scenoptic.excel_symbols import as_excel_name, excel_var_path
from scenoptic.xl_utils import cell_to_coords, as_cell_qn, cell_as_str

COMPARISON_OPERATORS = {'<=': LE_SYMBOL, '>=': GE_SYMBOL, '<>': NOT_EQUALS_SYMBOL,
                        '=': '=', '<': '<', '>': '>'}


def ctx_text(ctx):
    return ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop)


def copy_text(method):
    @wraps(method)
    def copier(self, *args, **kw):
        result = method(self, *args, **kw)
        result.text = ctx_text(args[0])
        return result

    return copier


class ArgList(FormalContent):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def describe(self, parent_binding=None):
        return '(' + ', '.join(arg.describe() for arg in self.args) + ')'

    def to_code_rep(self):
        raise Exception('ArgList is an intermediate structure and cannot be translated to code')

    def with_argument(self, index, arg):
        raise Exception('Cannot change arguments of ArgList')


@dataclass
class ObjectWrapper:
    """
    Wrap an object so that copy_text can assign to its .text field
    """
    obj: object


class ExcelFormulaExtractor(ExcelVisitor, metaclass=decorate_method((copy_text, 'visit*'))):
    def __init__(self,
                 scenario: ExcelData,
                 current_sheet_name: str = None,
                 origin_cell_qn: QualifiedName = None,
                 node_to_cell: Dict[int, CellReference] = None):
        self.scenario = scenario
        self.sheet = current_sheet_name or scenario.specification_sheet_name()
        self.origin_cell_qn = origin_cell_qn
        self.node_to_cell = node_to_cell or dict()
        self.node_to_mv, self.unique_cell_reference = self._bind_cell_reference_to_math_variable()

    def _bind_cell_reference_to_math_variable(self) -> Tuple[Dict[int, MathVariable], Sequence[QualifiedName]]:
        node_to_mv = dict()
        unique_mv_qn = dict()
        if self.node_to_cell and self.origin_cell_qn:
            for key, cell_ref in self.node_to_cell.items():
                mtype = self.find_cell_type(cell_ref.row, cell_ref.col, cell_ref.sheet)
                mv_qn = QualifiedName(cell_as_str(cell_ref.row, cell_ref.col, cell_ref.sheet),
                                      type=mtype,
                                      lexical_path=excel_var_path(self.origin_cell_qn.name))
                mv = MathVariable(mv_qn)
                node_to_mv[key] = mv
                if unique_mv_qn.get(cell_ref, None) is None:
                    unique_mv_qn[cell_ref] = mv_qn

        return node_to_mv, sorted(unique_mv_qn.values())

    def get_type_of_cell_expr(self, cell, sheet: str = None) -> MType:
        row = cell.row
        col = cell.col
        return self.find_cell_type(row, col, sheet)

    def get_type_of_cell_lexer(self, cell, sheet: str = None) -> Tuple[MType, int, int]:
        cell_spec = cell.getText()
        row, col = cell_to_coords(cell_spec)
        return self.find_cell_type(row, col, sheet), row, col

    def find_cell_type(self, row: int, col: int, sheet: str = None) -> MType:
        cell_qn = as_cell_qn(row, col, sheet or self.sheet)
        ctype = self.scenario.get_type(cell_qn)
        mtype = ctype.mtype if ctype is not None else M_ANY
        return mtype

    def make_cell(self, cell, sheet=None):
        if isinstance(cell, Cell):
            return cell
        mtype, row, col = self.get_type_of_cell_lexer(cell, sheet)
        return Cell(row, col, sheet or self.sheet, mtype)

    def visitStart(self, ctx: ExcelParser.StartContext):
        ctx_formula = ctx.formula()
        if ctx_formula and self.unique_cell_reference:
            formula = self.visit(ctx_formula)
            new_var_names = [
                FormalContent.fresh_name(QualifiedName(f'v{i + 1}', lexical_path=MATH_FRAME_PATH, type=cell_qn.type),
                                         'lambda-var')
                for i, cell_qn in enumerate(self.unique_cell_reference)]
            new_vars = [MathVariable(v) for v in new_var_names]
            return LambdaExpression(new_var_names,
                                    formula.substitute(dict(zip(self.unique_cell_reference, new_vars))))
        else:
            return self.visit(ctx.constant() or ctx_formula or ctx.array_formula())

        # return self.visit(ctx.constant() or ctx.formula() or ctx.array_formula())

    def visitArray_formula(self, ctx: ExcelParser.Array_formulaContext):
        raise Exception('Array formulas not yet supported')

    def visitReservedexcel_name(self, ctx: ExcelParser.ReservedNameContext):
        raise Exception('Reserved names not yet supported')

    def visitConcat(self, ctx: ExcelParser.ConcatContext):
        return FunctionApplication(as_excel_name('*concatenate-string*'),
                                   [self.visit(ctx.formula(0)), self.visit(ctx.formula(1))])

    def visitUnaryOp(self, ctx: ExcelParser.UnaryOpContext):
        return FunctionApplication(as_excel_name(ctx.op.text), [self.visit(ctx.formula())])

    def visitComparison(self, ctx: ExcelParser.ComparisonContext):
        return Comparison(self.visit(ctx.formula(0)), COMPARISON_OPERATORS[ctx.op.text],
                          self.visit(ctx.formula(1)))

    def visitPercent(self, ctx: ExcelParser.PercentContext):
        return FunctionApplication(as_math_name('%'), [self.visit(ctx.formula())])

    def visitMultiplicativeOp(self, ctx: ExcelParser.MultiplicativeOpContext):
        return FunctionApplication(as_excel_name(ctx.op.text),
                                   [self.visit(ctx.formula(0)), self.visit(ctx.formula(1))])

    def visitExpon(self, ctx: ExcelParser.ExponContext):
        return FunctionApplication(as_math_name('^'), [self.visit(ctx.formula(0)), self.visit(ctx.formula(1))])

    def visitAdditiveOp(self, ctx: ExcelParser.AdditiveOpContext):
        return FunctionApplication(as_excel_name(ctx.op.text),
                                   [self.visit(ctx.formula(0)), self.visit(ctx.formula(1))])

    def visitFunctionCall(self, ctx: ExcelParser.FunctionCallContext):
        return self.visit(ctx.function_call())

    def visitConstantFormula(self, ctx: ExcelParser.ConstantFormulaContext):
        return self.visit(ctx.constant())

    def visitReferenceFormula(self, ctx: ExcelParser.ReferenceFormulaContext):
        return self.visit(ctx.reference())

    def visitConstant(self, ctx: ExcelParser.ConstantContext):
        if ctx.INT():
            return Quantity(int(ctx.INT().getText()))
        if ctx.DECIMAL():
            return Quantity(float(ctx.DECIMAL().getText()))
        if ctx.STRING():
            return StringTerm(ctx.STRING().getText()[1:-1].replace('""', '"'))
        if ctx.BOOL():
            return Quantity(ctx.BOOL().getText() == 'TRUE', '*Boolean*')
        raise Exception(f"Can't translate error value: {ctx.ERROR().getText()}")

    def visitFunction_call(self, ctx: ExcelParser.Function_callContext):
        args: ArgList = self.visit(ctx.arguments())
        func = self.visit(ctx.function())
        return FunctionApplication(as_excel_name(func.obj), args.args)

    def visitPrefixed_function(self, ctx: ExcelParser.Prefixed_functionContext):
        return self.visit(ctx.function())

    def visitFunction(self, ctx: ExcelParser.FunctionContext):
        if (id := ctx.ID()) is not None:
            return ObjectWrapper(id.getText())
        if (function := ctx.FUNCTION()) is not None:
            return ObjectWrapper(function.getText())
        return self.visit(ctx.prefixed_function())

    def visitArguments(self, ctx: ExcelParser.ArgumentsContext):
        return ArgList([self.visit(arg) for arg in ctx.formula()])

    def visitParenFormula(self, ctx: ExcelParser.ParenFormulaContext):
        return self.visit(ctx.formula())

    def visitSimpleRef(self, ctx: ExcelParser.SimpleRefContext):
        return self.visit(ctx.reference_item())

    def visitPrefixedRef(self, ctx: ExcelParser.PrefixedRefContext):
        referenced_item = self.visit(ctx.reference_item())
        # If Cell is not fixed, we get here MathVariable, which we return upward
        if isinstance(referenced_item, Cell):
            # Fixed Cells, we extract the sheet name and pass it on
            sheet_name = ctx.prefix().getText()
            if sheet_name.endswith('!'):
                sheet_name = sheet_name[:-1]
            sheet = normalize_excel_format_special_characters(sheet_name)
            if isinstance(referenced_item, Cell):
                mtype = self.get_type_of_cell_expr(referenced_item, sheet)
                referenced_item = referenced_item.with_sheet_and_type(sheet, ctype=mtype)
        return referenced_item

    def visitParenRef(self, ctx: ExcelParser.ParenRefContext):
        return self.visit(ctx.reference())

    def visitRange(self, ctx: ExcelParser.RangeContext):
        ref1 = self.visit(ctx.reference(0))
        ref2 = self.visit(ctx.reference(1))
        # ref1 = self.visit(ctx.reference())
        # ref2 = self.make_cell(ctx.CELL())
        if isinstance(ref1, Cell) and isinstance(ref2, Cell):
            # FIXME: sheets should be assigned correctly at the CellRefContext or PrefixedRef
            if ref1.sheet != ref2.sheet:
                ref2 = ref2.with_sheet(ref1.sheet)
            return Cells(ref1, ref2)

        else:
            return CellsRange(ref1, ref2)

    def visitCellRef(self, ctx: ExcelParser.CellRefContext):
        if (mv := self.node_to_mv.get(id(ctx), None)) is not None:
            # Non fixed cell, return as MathVariable
            return mv
        # Fixed Cell, return as Cell
        return self.make_cell(ctx.CELL())

    def visitNamedRange(self, ctx: ExcelParser.NamedRangeContext):
        return self.visit(ctx.named_range())

    def visitRefFunction(self, ctx: ExcelParser.RefFunctionContext):
        raise Exception('Reference functions not yet supported')

    def visitVertRange(self, ctx: ExcelParser.VertRangeContext):
        raise Exception('Vertical ranges not yet supported')

    def visitHorizRange(self, ctx: ExcelParser.HorizRangeContext):
        raise Exception('Horizontal ranges not yet supported')

    def visitErrorRef(self, ctx: ExcelParser.ErrorRefContext):
        raise Exception(f"Can't translate error value: {ctx.ERROR_REF().getText()}")

    def visitPrefix(self, ctx: ExcelParser.PrefixContext):
        raise Exception('Prefixes not yet supported')

    def visitNamed_range(self, ctx: ExcelParser.Named_rangeContext):

        named_range_candidate = ctx.ID().getText()
        if self.scenario.is_named_range(named_range_candidate):
            return self.scenario.named_range_value(named_range_candidate)
        raise Exception(f'Invalid named range <{named_range_candidate}>')


def parse_formula(formula, scenario: ExcelData, current_sheet_name: str):
    if isinstance(formula, str):
        formula = formula.strip()
        if formula.startswith('='):
            parser = get_excel_parser(formula)
            tree = parser.start()
            extractor = ExcelFormulaExtractor(scenario, current_sheet_name)
            # print(tree.toStringTree(recog=parser).strip())
            return extractor.visit(tree)
    if isinstance(formula, Number):
        return Quantity(formula)
    return StringTerm(formula)


def parse_formula_with_variability(formula: str,
                                   scenario: ExcelData,
                                   current_sheet_name: str,
                                   origin_cell_qn: QualifiedName,
                                   variability: VariabilityTree):
    if isinstance(formula, str):
        formula = formula.strip()
        if formula.startswith('='):
            parser = get_excel_parser(formula)
            tree = parser.start()
            if origin_cell_qn is not None and variability is not None:
                node_to_cell = bind_cell_variability_by_tree(tree, variability, verbose=False)
            extractor = ExcelFormulaExtractor(scenario, current_sheet_name, origin_cell_qn, node_to_cell)
            return extractor.visit(tree)
    if isinstance(formula, Number):
        return Quantity(formula)
    return StringTerm(formula)


def parse_excel_cell_or_range(cell_or_range_str, scenario: ExcelData):
    if isinstance(cell_or_range_str, str):
        parser = get_excel_parser(cell_or_range_str)
        tree = parser.reference()
        extractor = ExcelFormulaExtractor(scenario)
        return extractor.visit(tree)
    return StringTerm(cell_str)


def get_excel_parser(cell_or_range_content):
    if isinstance(cell_or_range_content, str):
        formula = cell_or_range_content.strip()
        input_stream = antlr4.InputStream(formula)
        lexer = ExcelLexer(input_stream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = ExcelParser(stream)
        return parser


def describe_formula(formula, scenario: ExcelData):
    result = parse_formula(formula, scenario)
    return result.describe()


def normalize_excel_format_special_characters(sheet_name: str):
    sheet = sheet_name.strip()
    if sheet.startswith("'") and sheet.endswith("'"):
        sheet = sheet[1:-1]
    return sheet.replace("''", "'")
