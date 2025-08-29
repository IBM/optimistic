# Generated from D:/Yishai/ws/eco/Profile-Parser/Grammars/Excel.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ExcelParser import ExcelParser
else:
    from ExcelParser import ExcelParser

# This class defines a complete generic visitor for a parse tree produced by ExcelParser.

class ExcelVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExcelParser#start.
    def visitStart(self, ctx:ExcelParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#array_formula.
    def visitArray_formula(self, ctx:ExcelParser.Array_formulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#ReservedName.
    def visitReservedName(self, ctx:ExcelParser.ReservedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#Concat.
    def visitConcat(self, ctx:ExcelParser.ConcatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#UnaryOp.
    def visitUnaryOp(self, ctx:ExcelParser.UnaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#ParenFormula.
    def visitParenFormula(self, ctx:ExcelParser.ParenFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#Comparison.
    def visitComparison(self, ctx:ExcelParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#Percent.
    def visitPercent(self, ctx:ExcelParser.PercentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#MultiplicativeOp.
    def visitMultiplicativeOp(self, ctx:ExcelParser.MultiplicativeOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#Expon.
    def visitExpon(self, ctx:ExcelParser.ExponContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#AdditiveOp.
    def visitAdditiveOp(self, ctx:ExcelParser.AdditiveOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#FunctionCall.
    def visitFunctionCall(self, ctx:ExcelParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#ConstantFormula.
    def visitConstantFormula(self, ctx:ExcelParser.ConstantFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#ReferenceFormula.
    def visitReferenceFormula(self, ctx:ExcelParser.ReferenceFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#constant.
    def visitConstant(self, ctx:ExcelParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#function_call.
    def visitFunction_call(self, ctx:ExcelParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#arguments.
    def visitArguments(self, ctx:ExcelParser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#prefixed_function.
    def visitPrefixed_function(self, ctx:ExcelParser.Prefixed_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#function.
    def visitFunction(self, ctx:ExcelParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#SimpleRef.
    def visitSimpleRef(self, ctx:ExcelParser.SimpleRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#PrefixedRef.
    def visitPrefixedRef(self, ctx:ExcelParser.PrefixedRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#ParenRef.
    def visitParenRef(self, ctx:ExcelParser.ParenRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#Range.
    def visitRange(self, ctx:ExcelParser.RangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#CellRef.
    def visitCellRef(self, ctx:ExcelParser.CellRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#NamedRange.
    def visitNamedRange(self, ctx:ExcelParser.NamedRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#RefFunction.
    def visitRefFunction(self, ctx:ExcelParser.RefFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#VertRange.
    def visitVertRange(self, ctx:ExcelParser.VertRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#HorizRange.
    def visitHorizRange(self, ctx:ExcelParser.HorizRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#ErrorRef.
    def visitErrorRef(self, ctx:ExcelParser.ErrorRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#prefix.
    def visitPrefix(self, ctx:ExcelParser.PrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExcelParser#named_range.
    def visitNamed_range(self, ctx:ExcelParser.Named_rangeContext):
        return self.visitChildren(ctx)



del ExcelParser