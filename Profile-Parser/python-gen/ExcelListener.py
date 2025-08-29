# Generated from D:/Yishai/ws/eco/Profile-Parser/Grammars/Excel.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ExcelParser import ExcelParser
else:
    from ExcelParser import ExcelParser

# This class defines a complete listener for a parse tree produced by ExcelParser.
class ExcelListener(ParseTreeListener):

    # Enter a parse tree produced by ExcelParser#start.
    def enterStart(self, ctx:ExcelParser.StartContext):
        pass

    # Exit a parse tree produced by ExcelParser#start.
    def exitStart(self, ctx:ExcelParser.StartContext):
        pass


    # Enter a parse tree produced by ExcelParser#array_formula.
    def enterArray_formula(self, ctx:ExcelParser.Array_formulaContext):
        pass

    # Exit a parse tree produced by ExcelParser#array_formula.
    def exitArray_formula(self, ctx:ExcelParser.Array_formulaContext):
        pass


    # Enter a parse tree produced by ExcelParser#ReservedName.
    def enterReservedName(self, ctx:ExcelParser.ReservedNameContext):
        pass

    # Exit a parse tree produced by ExcelParser#ReservedName.
    def exitReservedName(self, ctx:ExcelParser.ReservedNameContext):
        pass


    # Enter a parse tree produced by ExcelParser#Concat.
    def enterConcat(self, ctx:ExcelParser.ConcatContext):
        pass

    # Exit a parse tree produced by ExcelParser#Concat.
    def exitConcat(self, ctx:ExcelParser.ConcatContext):
        pass


    # Enter a parse tree produced by ExcelParser#UnaryOp.
    def enterUnaryOp(self, ctx:ExcelParser.UnaryOpContext):
        pass

    # Exit a parse tree produced by ExcelParser#UnaryOp.
    def exitUnaryOp(self, ctx:ExcelParser.UnaryOpContext):
        pass


    # Enter a parse tree produced by ExcelParser#ParenFormula.
    def enterParenFormula(self, ctx:ExcelParser.ParenFormulaContext):
        pass

    # Exit a parse tree produced by ExcelParser#ParenFormula.
    def exitParenFormula(self, ctx:ExcelParser.ParenFormulaContext):
        pass


    # Enter a parse tree produced by ExcelParser#Comparison.
    def enterComparison(self, ctx:ExcelParser.ComparisonContext):
        pass

    # Exit a parse tree produced by ExcelParser#Comparison.
    def exitComparison(self, ctx:ExcelParser.ComparisonContext):
        pass


    # Enter a parse tree produced by ExcelParser#Percent.
    def enterPercent(self, ctx:ExcelParser.PercentContext):
        pass

    # Exit a parse tree produced by ExcelParser#Percent.
    def exitPercent(self, ctx:ExcelParser.PercentContext):
        pass


    # Enter a parse tree produced by ExcelParser#MultiplicativeOp.
    def enterMultiplicativeOp(self, ctx:ExcelParser.MultiplicativeOpContext):
        pass

    # Exit a parse tree produced by ExcelParser#MultiplicativeOp.
    def exitMultiplicativeOp(self, ctx:ExcelParser.MultiplicativeOpContext):
        pass


    # Enter a parse tree produced by ExcelParser#Expon.
    def enterExpon(self, ctx:ExcelParser.ExponContext):
        pass

    # Exit a parse tree produced by ExcelParser#Expon.
    def exitExpon(self, ctx:ExcelParser.ExponContext):
        pass


    # Enter a parse tree produced by ExcelParser#AdditiveOp.
    def enterAdditiveOp(self, ctx:ExcelParser.AdditiveOpContext):
        pass

    # Exit a parse tree produced by ExcelParser#AdditiveOp.
    def exitAdditiveOp(self, ctx:ExcelParser.AdditiveOpContext):
        pass


    # Enter a parse tree produced by ExcelParser#FunctionCall.
    def enterFunctionCall(self, ctx:ExcelParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by ExcelParser#FunctionCall.
    def exitFunctionCall(self, ctx:ExcelParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by ExcelParser#ConstantFormula.
    def enterConstantFormula(self, ctx:ExcelParser.ConstantFormulaContext):
        pass

    # Exit a parse tree produced by ExcelParser#ConstantFormula.
    def exitConstantFormula(self, ctx:ExcelParser.ConstantFormulaContext):
        pass


    # Enter a parse tree produced by ExcelParser#ReferenceFormula.
    def enterReferenceFormula(self, ctx:ExcelParser.ReferenceFormulaContext):
        pass

    # Exit a parse tree produced by ExcelParser#ReferenceFormula.
    def exitReferenceFormula(self, ctx:ExcelParser.ReferenceFormulaContext):
        pass


    # Enter a parse tree produced by ExcelParser#constant.
    def enterConstant(self, ctx:ExcelParser.ConstantContext):
        pass

    # Exit a parse tree produced by ExcelParser#constant.
    def exitConstant(self, ctx:ExcelParser.ConstantContext):
        pass


    # Enter a parse tree produced by ExcelParser#function_call.
    def enterFunction_call(self, ctx:ExcelParser.Function_callContext):
        pass

    # Exit a parse tree produced by ExcelParser#function_call.
    def exitFunction_call(self, ctx:ExcelParser.Function_callContext):
        pass


    # Enter a parse tree produced by ExcelParser#arguments.
    def enterArguments(self, ctx:ExcelParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by ExcelParser#arguments.
    def exitArguments(self, ctx:ExcelParser.ArgumentsContext):
        pass


    # Enter a parse tree produced by ExcelParser#prefixed_function.
    def enterPrefixed_function(self, ctx:ExcelParser.Prefixed_functionContext):
        pass

    # Exit a parse tree produced by ExcelParser#prefixed_function.
    def exitPrefixed_function(self, ctx:ExcelParser.Prefixed_functionContext):
        pass


    # Enter a parse tree produced by ExcelParser#function.
    def enterFunction(self, ctx:ExcelParser.FunctionContext):
        pass

    # Exit a parse tree produced by ExcelParser#function.
    def exitFunction(self, ctx:ExcelParser.FunctionContext):
        pass


    # Enter a parse tree produced by ExcelParser#SimpleRef.
    def enterSimpleRef(self, ctx:ExcelParser.SimpleRefContext):
        pass

    # Exit a parse tree produced by ExcelParser#SimpleRef.
    def exitSimpleRef(self, ctx:ExcelParser.SimpleRefContext):
        pass


    # Enter a parse tree produced by ExcelParser#PrefixedRef.
    def enterPrefixedRef(self, ctx:ExcelParser.PrefixedRefContext):
        pass

    # Exit a parse tree produced by ExcelParser#PrefixedRef.
    def exitPrefixedRef(self, ctx:ExcelParser.PrefixedRefContext):
        pass


    # Enter a parse tree produced by ExcelParser#ParenRef.
    def enterParenRef(self, ctx:ExcelParser.ParenRefContext):
        pass

    # Exit a parse tree produced by ExcelParser#ParenRef.
    def exitParenRef(self, ctx:ExcelParser.ParenRefContext):
        pass


    # Enter a parse tree produced by ExcelParser#Range.
    def enterRange(self, ctx:ExcelParser.RangeContext):
        pass

    # Exit a parse tree produced by ExcelParser#Range.
    def exitRange(self, ctx:ExcelParser.RangeContext):
        pass


    # Enter a parse tree produced by ExcelParser#CellRef.
    def enterCellRef(self, ctx:ExcelParser.CellRefContext):
        pass

    # Exit a parse tree produced by ExcelParser#CellRef.
    def exitCellRef(self, ctx:ExcelParser.CellRefContext):
        pass


    # Enter a parse tree produced by ExcelParser#NamedRange.
    def enterNamedRange(self, ctx:ExcelParser.NamedRangeContext):
        pass

    # Exit a parse tree produced by ExcelParser#NamedRange.
    def exitNamedRange(self, ctx:ExcelParser.NamedRangeContext):
        pass


    # Enter a parse tree produced by ExcelParser#RefFunction.
    def enterRefFunction(self, ctx:ExcelParser.RefFunctionContext):
        pass

    # Exit a parse tree produced by ExcelParser#RefFunction.
    def exitRefFunction(self, ctx:ExcelParser.RefFunctionContext):
        pass


    # Enter a parse tree produced by ExcelParser#VertRange.
    def enterVertRange(self, ctx:ExcelParser.VertRangeContext):
        pass

    # Exit a parse tree produced by ExcelParser#VertRange.
    def exitVertRange(self, ctx:ExcelParser.VertRangeContext):
        pass


    # Enter a parse tree produced by ExcelParser#HorizRange.
    def enterHorizRange(self, ctx:ExcelParser.HorizRangeContext):
        pass

    # Exit a parse tree produced by ExcelParser#HorizRange.
    def exitHorizRange(self, ctx:ExcelParser.HorizRangeContext):
        pass


    # Enter a parse tree produced by ExcelParser#ErrorRef.
    def enterErrorRef(self, ctx:ExcelParser.ErrorRefContext):
        pass

    # Exit a parse tree produced by ExcelParser#ErrorRef.
    def exitErrorRef(self, ctx:ExcelParser.ErrorRefContext):
        pass


    # Enter a parse tree produced by ExcelParser#prefix.
    def enterPrefix(self, ctx:ExcelParser.PrefixContext):
        pass

    # Exit a parse tree produced by ExcelParser#prefix.
    def exitPrefix(self, ctx:ExcelParser.PrefixContext):
        pass


    # Enter a parse tree produced by ExcelParser#named_range.
    def enterNamed_range(self, ctx:ExcelParser.Named_rangeContext):
        pass

    # Exit a parse tree produced by ExcelParser#named_range.
    def exitNamed_range(self, ctx:ExcelParser.Named_rangeContext):
        pass



del ExcelParser