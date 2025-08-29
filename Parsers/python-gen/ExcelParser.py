# Generated from D:/Yishai/ws/eco/Profile-Parser/Grammars/Excel.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,37,141,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,1,0,1,0,1,0,1,0,3,
        0,29,8,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,3,2,49,8,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,5,2,68,8,2,10,2,12,2,71,9,2,1,3,1,
        3,1,4,1,4,1,4,1,4,1,4,1,5,3,5,81,8,5,1,5,1,5,3,5,85,8,5,5,5,87,8,
        5,10,5,12,5,90,9,5,1,6,1,6,1,6,1,7,1,7,1,7,3,7,98,8,7,1,8,1,8,1,
        8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,109,8,8,1,8,1,8,1,8,5,8,114,8,8,10,
        8,12,8,117,9,8,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,3,9,129,8,
        9,1,10,3,10,132,8,10,1,10,1,10,1,10,3,10,137,8,10,1,11,1,11,1,11,
        0,2,4,16,12,0,2,4,6,8,10,12,14,16,18,20,22,0,4,1,0,4,5,1,0,8,9,2,
        0,1,1,11,15,3,0,21,22,26,26,35,36,156,0,28,1,0,0,0,2,32,1,0,0,0,
        4,48,1,0,0,0,6,72,1,0,0,0,8,74,1,0,0,0,10,80,1,0,0,0,12,91,1,0,0,
        0,14,97,1,0,0,0,16,108,1,0,0,0,18,128,1,0,0,0,20,136,1,0,0,0,22,
        138,1,0,0,0,24,29,3,6,3,0,25,26,5,1,0,0,26,29,3,4,2,0,27,29,3,2,
        1,0,28,24,1,0,0,0,28,25,1,0,0,0,28,27,1,0,0,0,29,30,1,0,0,0,30,31,
        5,0,0,1,31,1,1,0,0,0,32,33,5,2,0,0,33,34,5,1,0,0,34,35,3,4,2,0,35,
        36,5,3,0,0,36,3,1,0,0,0,37,38,6,2,-1,0,38,49,3,6,3,0,39,49,3,16,
        8,0,40,49,3,8,4,0,41,42,7,0,0,0,42,49,3,4,2,9,43,44,5,16,0,0,44,
        45,3,4,2,0,45,46,5,17,0,0,46,49,1,0,0,0,47,49,5,32,0,0,48,37,1,0,
        0,0,48,39,1,0,0,0,48,40,1,0,0,0,48,41,1,0,0,0,48,43,1,0,0,0,48,47,
        1,0,0,0,49,69,1,0,0,0,50,51,10,7,0,0,51,52,5,7,0,0,52,68,3,4,2,8,
        53,54,10,6,0,0,54,55,7,1,0,0,55,68,3,4,2,7,56,57,10,5,0,0,57,58,
        7,0,0,0,58,68,3,4,2,6,59,60,10,4,0,0,60,61,5,10,0,0,61,68,3,4,2,
        5,62,63,10,3,0,0,63,64,7,2,0,0,64,68,3,4,2,4,65,66,10,8,0,0,66,68,
        5,6,0,0,67,50,1,0,0,0,67,53,1,0,0,0,67,56,1,0,0,0,67,59,1,0,0,0,
        67,62,1,0,0,0,67,65,1,0,0,0,68,71,1,0,0,0,69,67,1,0,0,0,69,70,1,
        0,0,0,70,5,1,0,0,0,71,69,1,0,0,0,72,73,7,3,0,0,73,7,1,0,0,0,74,75,
        3,14,7,0,75,76,5,16,0,0,76,77,3,10,5,0,77,78,5,17,0,0,78,9,1,0,0,
        0,79,81,3,4,2,0,80,79,1,0,0,0,80,81,1,0,0,0,81,88,1,0,0,0,82,84,
        5,18,0,0,83,85,3,4,2,0,84,83,1,0,0,0,84,85,1,0,0,0,85,87,1,0,0,0,
        86,82,1,0,0,0,87,90,1,0,0,0,88,86,1,0,0,0,88,89,1,0,0,0,89,11,1,
        0,0,0,90,88,1,0,0,0,91,92,5,30,0,0,92,93,3,14,7,0,93,13,1,0,0,0,
        94,98,5,28,0,0,95,98,5,31,0,0,96,98,3,12,6,0,97,94,1,0,0,0,97,95,
        1,0,0,0,97,96,1,0,0,0,98,15,1,0,0,0,99,100,6,8,-1,0,100,109,3,18,
        9,0,101,102,5,16,0,0,102,103,3,16,8,0,103,104,5,17,0,0,104,109,1,
        0,0,0,105,106,3,20,10,0,106,107,3,18,9,0,107,109,1,0,0,0,108,99,
        1,0,0,0,108,101,1,0,0,0,108,105,1,0,0,0,109,115,1,0,0,0,110,111,
        10,3,0,0,111,112,5,19,0,0,112,114,3,16,8,4,113,110,1,0,0,0,114,117,
        1,0,0,0,115,113,1,0,0,0,115,116,1,0,0,0,116,17,1,0,0,0,117,115,1,
        0,0,0,118,129,5,23,0,0,119,129,3,22,11,0,120,121,5,29,0,0,121,122,
        5,16,0,0,122,123,3,10,5,0,123,124,5,17,0,0,124,129,1,0,0,0,125,129,
        5,25,0,0,126,129,5,24,0,0,127,129,5,27,0,0,128,118,1,0,0,0,128,119,
        1,0,0,0,128,120,1,0,0,0,128,125,1,0,0,0,128,126,1,0,0,0,128,127,
        1,0,0,0,129,19,1,0,0,0,130,132,5,33,0,0,131,130,1,0,0,0,131,132,
        1,0,0,0,132,133,1,0,0,0,133,137,5,34,0,0,134,135,5,33,0,0,135,137,
        5,20,0,0,136,131,1,0,0,0,136,134,1,0,0,0,137,21,1,0,0,0,138,139,
        5,31,0,0,139,23,1,0,0,0,13,28,48,67,69,80,84,88,97,108,115,128,131,
        136
    ]

class ExcelParser ( Parser ):

    grammarFileName = "Excel.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'='", "'{'", "'}'", "'+'", "'-'", "'%'", 
                     "'^'", "'*'", "'/'", "'&'", "'<'", "'>'", "'<='", "'>='", 
                     "'<>'", "'('", "')'", "','", "':'", "'!'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'#REF!'", "'SUM'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "INT", "BOOL", "CELL", "HORIZONTAL_RANGE", 
                      "VERTICAL_RANGE", "ERROR", "ERROR_REF", "FUNCTION", 
                      "REFERENCE_FUNCTION", "FUNCTION_PREFIX", "ID", "RESERVED_NAME", 
                      "FILE", "SHEET", "DECIMAL", "STRING", "WS" ]

    RULE_start = 0
    RULE_array_formula = 1
    RULE_formula = 2
    RULE_constant = 3
    RULE_function_call = 4
    RULE_arguments = 5
    RULE_prefixed_function = 6
    RULE_function = 7
    RULE_reference = 8
    RULE_reference_item = 9
    RULE_prefix = 10
    RULE_named_range = 11

    ruleNames =  [ "start", "array_formula", "formula", "constant", "function_call", 
                   "arguments", "prefixed_function", "function", "reference", 
                   "reference_item", "prefix", "named_range" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    INT=21
    BOOL=22
    CELL=23
    HORIZONTAL_RANGE=24
    VERTICAL_RANGE=25
    ERROR=26
    ERROR_REF=27
    FUNCTION=28
    REFERENCE_FUNCTION=29
    FUNCTION_PREFIX=30
    ID=31
    RESERVED_NAME=32
    FILE=33
    SHEET=34
    DECIMAL=35
    STRING=36
    WS=37

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(ExcelParser.EOF, 0)

        def constant(self):
            return self.getTypedRuleContext(ExcelParser.ConstantContext,0)


        def formula(self):
            return self.getTypedRuleContext(ExcelParser.FormulaContext,0)


        def array_formula(self):
            return self.getTypedRuleContext(ExcelParser.Array_formulaContext,0)


        def getRuleIndex(self):
            return ExcelParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart" ):
                return visitor.visitStart(self)
            else:
                return visitor.visitChildren(self)




    def start(self):

        localctx = ExcelParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [21, 22, 26, 35, 36]:
                self.state = 24
                self.constant()
                pass
            elif token in [1]:
                self.state = 25
                self.match(ExcelParser.T__0)
                self.state = 26
                self.formula(0)
                pass
            elif token in [2]:
                self.state = 27
                self.array_formula()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 30
            self.match(ExcelParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Array_formulaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def formula(self):
            return self.getTypedRuleContext(ExcelParser.FormulaContext,0)


        def getRuleIndex(self):
            return ExcelParser.RULE_array_formula

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArray_formula" ):
                listener.enterArray_formula(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArray_formula" ):
                listener.exitArray_formula(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArray_formula" ):
                return visitor.visitArray_formula(self)
            else:
                return visitor.visitChildren(self)




    def array_formula(self):

        localctx = ExcelParser.Array_formulaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_array_formula)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.match(ExcelParser.T__1)
            self.state = 33
            self.match(ExcelParser.T__0)
            self.state = 34
            self.formula(0)
            self.state = 35
            self.match(ExcelParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormulaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ExcelParser.RULE_formula

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ReservedNameContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def RESERVED_NAME(self):
            return self.getToken(ExcelParser.RESERVED_NAME, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReservedName" ):
                listener.enterReservedName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReservedName" ):
                listener.exitReservedName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReservedName" ):
                return visitor.visitReservedName(self)
            else:
                return visitor.visitChildren(self)


    class ConcatContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def formula(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExcelParser.FormulaContext)
            else:
                return self.getTypedRuleContext(ExcelParser.FormulaContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConcat" ):
                listener.enterConcat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConcat" ):
                listener.exitConcat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConcat" ):
                return visitor.visitConcat(self)
            else:
                return visitor.visitChildren(self)


    class UnaryOpContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def formula(self):
            return self.getTypedRuleContext(ExcelParser.FormulaContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryOp" ):
                listener.enterUnaryOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryOp" ):
                listener.exitUnaryOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryOp" ):
                return visitor.visitUnaryOp(self)
            else:
                return visitor.visitChildren(self)


    class ParenFormulaContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def formula(self):
            return self.getTypedRuleContext(ExcelParser.FormulaContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenFormula" ):
                listener.enterParenFormula(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenFormula" ):
                listener.exitParenFormula(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenFormula" ):
                return visitor.visitParenFormula(self)
            else:
                return visitor.visitChildren(self)


    class ComparisonContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def formula(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExcelParser.FormulaContext)
            else:
                return self.getTypedRuleContext(ExcelParser.FormulaContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparison" ):
                listener.enterComparison(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparison" ):
                listener.exitComparison(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)


    class PercentContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def formula(self):
            return self.getTypedRuleContext(ExcelParser.FormulaContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPercent" ):
                listener.enterPercent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPercent" ):
                listener.exitPercent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPercent" ):
                return visitor.visitPercent(self)
            else:
                return visitor.visitChildren(self)


    class MultiplicativeOpContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def formula(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExcelParser.FormulaContext)
            else:
                return self.getTypedRuleContext(ExcelParser.FormulaContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeOp" ):
                listener.enterMultiplicativeOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeOp" ):
                listener.exitMultiplicativeOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeOp" ):
                return visitor.visitMultiplicativeOp(self)
            else:
                return visitor.visitChildren(self)


    class ExponContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def formula(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExcelParser.FormulaContext)
            else:
                return self.getTypedRuleContext(ExcelParser.FormulaContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpon" ):
                listener.enterExpon(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpon" ):
                listener.exitExpon(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpon" ):
                return visitor.visitExpon(self)
            else:
                return visitor.visitChildren(self)


    class AdditiveOpContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def formula(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExcelParser.FormulaContext)
            else:
                return self.getTypedRuleContext(ExcelParser.FormulaContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveOp" ):
                listener.enterAdditiveOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveOp" ):
                listener.exitAdditiveOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveOp" ):
                return visitor.visitAdditiveOp(self)
            else:
                return visitor.visitChildren(self)


    class FunctionCallContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def function_call(self):
            return self.getTypedRuleContext(ExcelParser.Function_callContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)


    class ConstantFormulaContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def constant(self):
            return self.getTypedRuleContext(ExcelParser.ConstantContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstantFormula" ):
                listener.enterConstantFormula(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstantFormula" ):
                listener.exitConstantFormula(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstantFormula" ):
                return visitor.visitConstantFormula(self)
            else:
                return visitor.visitChildren(self)


    class ReferenceFormulaContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def reference(self):
            return self.getTypedRuleContext(ExcelParser.ReferenceContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReferenceFormula" ):
                listener.enterReferenceFormula(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReferenceFormula" ):
                listener.exitReferenceFormula(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReferenceFormula" ):
                return visitor.visitReferenceFormula(self)
            else:
                return visitor.visitChildren(self)



    def formula(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ExcelParser.FormulaContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_formula, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = ExcelParser.ConstantFormulaContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 38
                self.constant()
                pass

            elif la_ == 2:
                localctx = ExcelParser.ReferenceFormulaContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 39
                self.reference(0)
                pass

            elif la_ == 3:
                localctx = ExcelParser.FunctionCallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 40
                self.function_call()
                pass

            elif la_ == 4:
                localctx = ExcelParser.UnaryOpContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 41
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==4 or _la==5):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 42
                self.formula(9)
                pass

            elif la_ == 5:
                localctx = ExcelParser.ParenFormulaContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 43
                self.match(ExcelParser.T__15)
                self.state = 44
                self.formula(0)
                self.state = 45
                self.match(ExcelParser.T__16)
                pass

            elif la_ == 6:
                localctx = ExcelParser.ReservedNameContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 47
                self.match(ExcelParser.RESERVED_NAME)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 69
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 67
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                    if la_ == 1:
                        localctx = ExcelParser.ExponContext(self, ExcelParser.FormulaContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 50
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 51
                        localctx.op = self.match(ExcelParser.T__6)
                        self.state = 52
                        self.formula(8)
                        pass

                    elif la_ == 2:
                        localctx = ExcelParser.MultiplicativeOpContext(self, ExcelParser.FormulaContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 53
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 54
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==8 or _la==9):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 55
                        self.formula(7)
                        pass

                    elif la_ == 3:
                        localctx = ExcelParser.AdditiveOpContext(self, ExcelParser.FormulaContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 56
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 57
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==4 or _la==5):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 58
                        self.formula(6)
                        pass

                    elif la_ == 4:
                        localctx = ExcelParser.ConcatContext(self, ExcelParser.FormulaContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 59
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 60
                        localctx.op = self.match(ExcelParser.T__9)
                        self.state = 61
                        self.formula(5)
                        pass

                    elif la_ == 5:
                        localctx = ExcelParser.ComparisonContext(self, ExcelParser.FormulaContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 62
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 63
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 63490) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 64
                        self.formula(4)
                        pass

                    elif la_ == 6:
                        localctx = ExcelParser.PercentContext(self, ExcelParser.FormulaContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 65
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 66
                        self.match(ExcelParser.T__5)
                        pass

             
                self.state = 71
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(ExcelParser.INT, 0)

        def DECIMAL(self):
            return self.getToken(ExcelParser.DECIMAL, 0)

        def STRING(self):
            return self.getToken(ExcelParser.STRING, 0)

        def BOOL(self):
            return self.getToken(ExcelParser.BOOL, 0)

        def ERROR(self):
            return self.getToken(ExcelParser.ERROR, 0)

        def getRuleIndex(self):
            return ExcelParser.RULE_constant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstant" ):
                listener.enterConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstant" ):
                listener.exitConstant(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstant" ):
                return visitor.visitConstant(self)
            else:
                return visitor.visitChildren(self)




    def constant(self):

        localctx = ExcelParser.ConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_constant)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 103152615424) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Function_callContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def function(self):
            return self.getTypedRuleContext(ExcelParser.FunctionContext,0)


        def arguments(self):
            return self.getTypedRuleContext(ExcelParser.ArgumentsContext,0)


        def getRuleIndex(self):
            return ExcelParser.RULE_function_call

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_call" ):
                listener.enterFunction_call(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_call" ):
                listener.exitFunction_call(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction_call" ):
                return visitor.visitFunction_call(self)
            else:
                return visitor.visitChildren(self)




    def function_call(self):

        localctx = ExcelParser.Function_callContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_function_call)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.function()
            self.state = 75
            self.match(ExcelParser.T__15)
            self.state = 76
            self.arguments()
            self.state = 77
            self.match(ExcelParser.T__16)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def formula(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExcelParser.FormulaContext)
            else:
                return self.getTypedRuleContext(ExcelParser.FormulaContext,i)


        def getRuleIndex(self):
            return ExcelParser.RULE_arguments

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArguments" ):
                listener.enterArguments(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArguments" ):
                listener.exitArguments(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArguments" ):
                return visitor.visitArguments(self)
            else:
                return visitor.visitChildren(self)




    def arguments(self):

        localctx = ExcelParser.ArgumentsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_arguments)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 137436921904) != 0):
                self.state = 79
                self.formula(0)


            self.state = 88
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==18:
                self.state = 82
                self.match(ExcelParser.T__17)
                self.state = 84
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 137436921904) != 0):
                    self.state = 83
                    self.formula(0)


                self.state = 90
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Prefixed_functionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNCTION_PREFIX(self):
            return self.getToken(ExcelParser.FUNCTION_PREFIX, 0)

        def function(self):
            return self.getTypedRuleContext(ExcelParser.FunctionContext,0)


        def getRuleIndex(self):
            return ExcelParser.RULE_prefixed_function

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrefixed_function" ):
                listener.enterPrefixed_function(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrefixed_function" ):
                listener.exitPrefixed_function(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrefixed_function" ):
                return visitor.visitPrefixed_function(self)
            else:
                return visitor.visitChildren(self)




    def prefixed_function(self):

        localctx = ExcelParser.Prefixed_functionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_prefixed_function)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self.match(ExcelParser.FUNCTION_PREFIX)
            self.state = 92
            self.function()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNCTION(self):
            return self.getToken(ExcelParser.FUNCTION, 0)

        def ID(self):
            return self.getToken(ExcelParser.ID, 0)

        def prefixed_function(self):
            return self.getTypedRuleContext(ExcelParser.Prefixed_functionContext,0)


        def getRuleIndex(self):
            return ExcelParser.RULE_function

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction" ):
                listener.enterFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction" ):
                listener.exitFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction" ):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)




    def function(self):

        localctx = ExcelParser.FunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_function)
        try:
            self.state = 97
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [28]:
                self.enterOuterAlt(localctx, 1)
                self.state = 94
                self.match(ExcelParser.FUNCTION)
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 2)
                self.state = 95
                self.match(ExcelParser.ID)
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 3)
                self.state = 96
                self.prefixed_function()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReferenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ExcelParser.RULE_reference

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class SimpleRefContext(ReferenceContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.ReferenceContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def reference_item(self):
            return self.getTypedRuleContext(ExcelParser.Reference_itemContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleRef" ):
                listener.enterSimpleRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleRef" ):
                listener.exitSimpleRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleRef" ):
                return visitor.visitSimpleRef(self)
            else:
                return visitor.visitChildren(self)


    class PrefixedRefContext(ReferenceContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.ReferenceContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def prefix(self):
            return self.getTypedRuleContext(ExcelParser.PrefixContext,0)

        def reference_item(self):
            return self.getTypedRuleContext(ExcelParser.Reference_itemContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrefixedRef" ):
                listener.enterPrefixedRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrefixedRef" ):
                listener.exitPrefixedRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrefixedRef" ):
                return visitor.visitPrefixedRef(self)
            else:
                return visitor.visitChildren(self)


    class ParenRefContext(ReferenceContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.ReferenceContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def reference(self):
            return self.getTypedRuleContext(ExcelParser.ReferenceContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenRef" ):
                listener.enterParenRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenRef" ):
                listener.exitParenRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenRef" ):
                return visitor.visitParenRef(self)
            else:
                return visitor.visitChildren(self)


    class RangeContext(ReferenceContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.ReferenceContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def reference(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExcelParser.ReferenceContext)
            else:
                return self.getTypedRuleContext(ExcelParser.ReferenceContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRange" ):
                listener.enterRange(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRange" ):
                listener.exitRange(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRange" ):
                return visitor.visitRange(self)
            else:
                return visitor.visitChildren(self)



    def reference(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ExcelParser.ReferenceContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 16
        self.enterRecursionRule(localctx, 16, self.RULE_reference, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23, 24, 25, 27, 29, 31]:
                localctx = ExcelParser.SimpleRefContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 100
                self.reference_item()
                pass
            elif token in [16]:
                localctx = ExcelParser.ParenRefContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 101
                self.match(ExcelParser.T__15)
                self.state = 102
                self.reference(0)
                self.state = 103
                self.match(ExcelParser.T__16)
                pass
            elif token in [33, 34]:
                localctx = ExcelParser.PrefixedRefContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 105
                self.prefix()
                self.state = 106
                self.reference_item()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 115
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = ExcelParser.RangeContext(self, ExcelParser.ReferenceContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_reference)
                    self.state = 110
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 111
                    self.match(ExcelParser.T__18)
                    self.state = 112
                    self.reference(4) 
                self.state = 117
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Reference_itemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ExcelParser.RULE_reference_item

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class VertRangeContext(Reference_itemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.Reference_itemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VERTICAL_RANGE(self):
            return self.getToken(ExcelParser.VERTICAL_RANGE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVertRange" ):
                listener.enterVertRange(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVertRange" ):
                listener.exitVertRange(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVertRange" ):
                return visitor.visitVertRange(self)
            else:
                return visitor.visitChildren(self)


    class RefFunctionContext(Reference_itemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.Reference_itemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def REFERENCE_FUNCTION(self):
            return self.getToken(ExcelParser.REFERENCE_FUNCTION, 0)
        def arguments(self):
            return self.getTypedRuleContext(ExcelParser.ArgumentsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRefFunction" ):
                listener.enterRefFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRefFunction" ):
                listener.exitRefFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRefFunction" ):
                return visitor.visitRefFunction(self)
            else:
                return visitor.visitChildren(self)


    class HorizRangeContext(Reference_itemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.Reference_itemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def HORIZONTAL_RANGE(self):
            return self.getToken(ExcelParser.HORIZONTAL_RANGE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHorizRange" ):
                listener.enterHorizRange(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHorizRange" ):
                listener.exitHorizRange(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHorizRange" ):
                return visitor.visitHorizRange(self)
            else:
                return visitor.visitChildren(self)


    class ErrorRefContext(Reference_itemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.Reference_itemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ERROR_REF(self):
            return self.getToken(ExcelParser.ERROR_REF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterErrorRef" ):
                listener.enterErrorRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitErrorRef" ):
                listener.exitErrorRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitErrorRef" ):
                return visitor.visitErrorRef(self)
            else:
                return visitor.visitChildren(self)


    class NamedRangeContext(Reference_itemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.Reference_itemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def named_range(self):
            return self.getTypedRuleContext(ExcelParser.Named_rangeContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamedRange" ):
                listener.enterNamedRange(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamedRange" ):
                listener.exitNamedRange(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamedRange" ):
                return visitor.visitNamedRange(self)
            else:
                return visitor.visitChildren(self)


    class CellRefContext(Reference_itemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExcelParser.Reference_itemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def CELL(self):
            return self.getToken(ExcelParser.CELL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCellRef" ):
                listener.enterCellRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCellRef" ):
                listener.exitCellRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCellRef" ):
                return visitor.visitCellRef(self)
            else:
                return visitor.visitChildren(self)



    def reference_item(self):

        localctx = ExcelParser.Reference_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_reference_item)
        try:
            self.state = 128
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                localctx = ExcelParser.CellRefContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 118
                self.match(ExcelParser.CELL)
                pass
            elif token in [31]:
                localctx = ExcelParser.NamedRangeContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 119
                self.named_range()
                pass
            elif token in [29]:
                localctx = ExcelParser.RefFunctionContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 120
                self.match(ExcelParser.REFERENCE_FUNCTION)
                self.state = 121
                self.match(ExcelParser.T__15)
                self.state = 122
                self.arguments()
                self.state = 123
                self.match(ExcelParser.T__16)
                pass
            elif token in [25]:
                localctx = ExcelParser.VertRangeContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 125
                self.match(ExcelParser.VERTICAL_RANGE)
                pass
            elif token in [24]:
                localctx = ExcelParser.HorizRangeContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 126
                self.match(ExcelParser.HORIZONTAL_RANGE)
                pass
            elif token in [27]:
                localctx = ExcelParser.ErrorRefContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 127
                self.match(ExcelParser.ERROR_REF)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrefixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SHEET(self):
            return self.getToken(ExcelParser.SHEET, 0)

        def FILE(self):
            return self.getToken(ExcelParser.FILE, 0)

        def getRuleIndex(self):
            return ExcelParser.RULE_prefix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrefix" ):
                listener.enterPrefix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrefix" ):
                listener.exitPrefix(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrefix" ):
                return visitor.visitPrefix(self)
            else:
                return visitor.visitChildren(self)




    def prefix(self):

        localctx = ExcelParser.PrefixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_prefix)
        self._la = 0 # Token type
        try:
            self.state = 136
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 131
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==33:
                    self.state = 130
                    self.match(ExcelParser.FILE)


                self.state = 133
                self.match(ExcelParser.SHEET)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 134
                self.match(ExcelParser.FILE)
                self.state = 135
                self.match(ExcelParser.T__19)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Named_rangeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ExcelParser.ID, 0)

        def getRuleIndex(self):
            return ExcelParser.RULE_named_range

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamed_range" ):
                listener.enterNamed_range(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamed_range" ):
                listener.exitNamed_range(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamed_range" ):
                return visitor.visitNamed_range(self)
            else:
                return visitor.visitChildren(self)




    def named_range(self):

        localctx = ExcelParser.Named_rangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_named_range)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.match(ExcelParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[2] = self.formula_sempred
        self._predicates[8] = self.reference_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def formula_sempred(self, localctx:FormulaContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 8)
         

    def reference_sempred(self, localctx:ReferenceContext, predIndex:int):
            if predIndex == 6:
                return self.precpred(self._ctx, 3)
         




