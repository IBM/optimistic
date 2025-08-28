from ast import literal_eval
from functools import wraps
from typing import Sequence
from re import compile
import itertools


from codegen.utils import decorate_method
from generated.Python3Parser import Python3Parser
from generated.Python3Visitor import Python3Visitor
from validator2solver.python.python_rep import PythonElement, PythonFile, PythonStatements, PythonReturn, PythonExpressions, \
    PythonIFTE, PythonOp, PythonComparison, PythonCall, PythonSubscripted, PythonAttribute, \
    PythonTupleCons, PythonListCons, Comprehension, PythonDictCons, PythonVariable, PythonConstant, Components, \
    EmptyContents, PythonDictCompr, PythonSetCompr, PythonSetCons, PythonIncDict, PythonDictPair, PythonForComprehension, PythonIfComprehension, PythonNotImplemented, PythonPass, PythonSlice, PythonFuncDef, \
    PythonParmlist, PythonKeywordParm, PythonParm, PythonRestParm, PythonGenExpr, PythonUnpack, PythonClass, \
    PythonDecorated, PythonDestructure, PythonAssignment, PythonTypedExpr, PythonImport, PythonImportFrom, \
    PythonImportAll, PythonImportAs, PythonAssert, PythonKeywordArg, PythonIfStatement, PythonContainerCons
from codegen.parameters import ONLY_KW


class OptimisticPythonParserException(Exception):
    pass


def zip_right(s1: Sequence, s2: Sequence, padding=None) -> Sequence:
    """
    Zip the given sequences, padding the second sequence to the length of the first one.

    :param s1: longer sequence
    :param s2: shorter sequence to be padded
    :return: zipped sequences
    """
    pad2 = itertools.chain(itertools.repeat(padding, len(s1) - len(s2)), s2)
    return zip(s1, pad2)


NONEXISTENT = object()


def ctx_text(ctx):
    return ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop)


def copy_text(method):
    @wraps(method)
    def copier(self, *args, **kw):
        result = method(self, *args, **kw)
        text = ctx_text(args[0])
        next_item = (text, result)
        # also put on result.text
        if not self.mapping or self.mapping[-1] != next_item:
            self.mapping.append(next_item)
        # put starting line number
        if isinstance(result, PythonElement):
            result._starts_on_line = args[0].start.line
        return result

    return copier


def replace_not_implemented(method):
    @wraps(method)
    def fixer(self, *args, **kw):
        result = method(self, *args, **kw)
        if result is None:
            result = PythonNotImplemented
        return result

    return fixer


class PythonSpecExtractor(Python3Visitor,
                          metaclass=decorate_method((copy_text, 'visit*'), (replace_not_implemented, 'visit*'))):
    def __init__(self):
        self.mapping = []

    def visitFile_input(self, ctx: Python3Parser.File_inputContext):
        return PythonFile([self.visit(stmt) for stmt in ctx.stmt()])

    def visitStmt(self, ctx: Python3Parser.StmtContext):
        return self.visit(ctx.simple_stmt() or ctx.compound_stmt())

    def visitCompound_stmt(self, ctx: Python3Parser.Compound_stmtContext):
        return self.visit(ctx.if_stmt() or ctx.while_stmt() or ctx.for_stmt() or ctx.try_stmt() or ctx.with_stmt()
                          or ctx.funcdef() or ctx.classdef() or ctx.decorated() or ctx.async_stmt())

    def visitIf_stmt(self, ctx: Python3Parser.If_stmtContext):
        conditions = [self.visit(cond) for cond in ctx.test()]
        blocks = [self.visit(block) for block in ctx.blocks]
        else_block = self.visit(eb) if (eb := ctx.else_block) else None
        return PythonIfStatement(conditions, blocks, else_block)

    def visitFuncdef(self, ctx: Python3Parser.FuncdefContext):
        name = ctx.NAME().getText()
        pars = self.visit(ctx.parameters())
        res_type = self.visit(test) if (test := ctx.test()) is not None else None
        body = self.visit(ctx.suite())
        return PythonFuncDef(name, pars, res_type, body)

    def visitParameters(self, ctx: Python3Parser.ParametersContext):
        if (args := ctx.typedargslist()) is not None:
            return self.visit(args)
        return PythonParmlist([])

    def visitParmlist_kw(self, ctx: Python3Parser.Parmlist_kwContext):
        return PythonParmlist([PythonKeywordParm(self.visit(ctx.tfpdef()))])

    def visitParmlist_rest(self, ctx: Python3Parser.Parmlist_restContext):
        parms = []
        if (rest := ctx.rest) is not None:
            parms.append(PythonRestParm(self.visit(rest)))
        for name, default in itertools.zip_longest(ctx.kw_only_args, ctx.kw_only_defaults):
            pt = self.visit(name).with_kind(ONLY_KW)
            parms.append(pt.with_init(self.visit(default)) if default else pt)
        if (kw := ctx.kw) is not None:
            parms.append(PythonKeywordParm(self.visit(kw)))
        return PythonParmlist(parms)

    def visitParmlist_nonempty(self, ctx: Python3Parser.Parmlist_nonemptyContext):
        parms = self.visit(ctx.posargslist())
        if (kwlist := ctx.kwargslist()) is not None:
            if (rest := ctx.rest) is not None:
                parms.append(PythonRestParm(self.visit(rest)))
            parms.extend(self.visit(kwlist))
        if (kw := ctx.kw) is not None:
            parms.append(PythonKeywordParm(self.visit(kw)))
        return PythonParmlist(parms)

    def visitPosargslist(self, ctx: Python3Parser.PosargslistContext):
        parms = []
        for name, default in zip_right(ctx.args, ctx.defaults, padding=NONEXISTENT):
            if default is NONEXISTENT:
                parms.append(self.visit(name))
            else:
                parms.append(self.visit(name).with_init(self.visit(default)))
        return parms

    def visitKwargslist(self, ctx: Python3Parser.KwargslistContext):
        parms = []
        for name, default in zip_right(ctx.args, ctx.defaults, padding=NONEXISTENT):
            if default is NONEXISTENT:
                parms.append(self.visit(name).with_kind(ONLY_KW))
            else:
                parms.append(self.visit(name).with_kind(ONLY_KW).with_init(self.visit(default)))
        return parms

    def visitTfpdef(self, ctx: Python3Parser.TfpdefContext):
        name = ctx.NAME().getText()
        if (typedef := ctx.test()) is not None:
            return PythonParm(name, ptype=self.visit(typedef))
        return PythonParm(name)

    def visitSuite(self, ctx: Python3Parser.SuiteContext):
        if (stmt := ctx.simple_stmt()) is not None:
            return self.visit(stmt)
        else:
            return PythonStatements([self.visit(stmt) for stmt in ctx.stmt()])

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

    def visitAssert_stmt(self, ctx: Python3Parser.Assert_stmtContext):
        doc = self.visit(doc_expr) if (doc_expr := ctx.test(1)) is not None else None
        return PythonAssert(self.visit(ctx.test(0)), doc)

    def visitSpecial_assign(self, ctx: Python3Parser.Special_assignContext):
        if ctx.yield_expr() is not None:
            raise OptimisticPythonParserException('yield expressions not supported!')
        if ctx.augassign() is not None:
            raise OptimisticPythonParserException('Augmented assignment not supported!')
        lhs = self.visit(ctx.lhs)
        type_decl = self.visit(ctx.annassign().type_decl)
        if (rhs := ctx.annassign().value) is not None:
            rhs = self.visit(rhs)
            return PythonAssignment(PythonTypedExpr(lhs, type_decl), '=', rhs)
        return PythonTypedExpr(lhs, type_decl)

    def visitReg_assign(self, ctx: Python3Parser.Reg_assignContext):
        if ctx.yield_expr():
            raise OptimisticPythonParserException('yield expressions not supported!')
        # Note: this contains the lhs as well
        expr_lists = [self.visit(e) for e in ctx.testlist_star_expr()]
        result = expr_lists[-1]
        for left in reversed(expr_lists[:-1]):
            result = PythonAssignment(left, '=', result)
        return result

    def visitTestlist_star_expr(self, ctx: Python3Parser.Testlist_star_exprContext):
        if len(exprs := ctx.test_star_expr()) == 1:
            return self.visit(exprs[0])
        return PythonDestructure([self.visit(c) for c in exprs])

    def visitTest_star_expr(self, ctx: Python3Parser.Test_star_exprContext):
        return self.visit(ctx.test() or ctx.star_expr())

    def visitFlow_stmt(self, ctx: Python3Parser.Flow_stmtContext):
        return self.visit(ctx.break_stmt() or ctx.continue_stmt() or ctx.return_stmt() or ctx.raise_stmt()
                          or ctx.yield_stmt())

    def visitReturn_stmt(self, ctx: Python3Parser.Return_stmtContext):
        if (testlist := ctx.testlist()) is not None:
            result = self.visit(testlist)
        else:
            result = None
        return PythonReturn(result)

    def visitTestlist(self, ctx: Python3Parser.TestlistContext):
        return PythonExpressions([self.visit(test) for test in ctx.test()])

    def visitTest(self, ctx: Python3Parser.TestContext):
        if (val1 := ctx.or_test(0)) is not None:
            if (test := ctx.or_test(1)) is not None:
                val2 = ctx.test()
                return PythonIFTE(self.visit(test), self.visit(val1), self.visit(val2))
            else:
                return self.visit(val1)
        else:
            return self.visit(ctx.lambdef())

    def binary_helper(self, operator, operands):
        if len(operands) == 1:
            return self.visit(operands[0])
        return PythonOp(operator, [self.visit(op) for op in operands])

    def visitOr_test(self, ctx: Python3Parser.Or_testContext):
        return self.binary_helper('or', ctx.and_test())

    def visitAnd_test(self, ctx: Python3Parser.And_testContext):
        return self.binary_helper('and', ctx.not_test())

    def visitNot_test(self, ctx: Python3Parser.Not_testContext):
        if (test := ctx.not_test()) is not None:
            return PythonOp('not', [self.visit(test)])
        return self.visit(ctx.comparison())

    def var_op_helper(self, expr_type, operators, operands):
        if len(operands) == 1:
            return self.visit(operands[0])
        result = self.visit(operands[0])
        for val, op in zip(operands[1:], operators):
            result = PythonOp(op.text, [result, self.visit(val)])
        return result

    def visitComparison(self, ctx: Python3Parser.ComparisonContext):
        if ops := ctx.comp_op():
            return PythonComparison([op.getText() for op in ops], [self.visit(exp) for exp in ctx.expr()])
        else:
            return self.visit(ctx.expr(0))

    def visitExpr(self, ctx: Python3Parser.ExprContext):
        return self.binary_helper('|', ctx.xor_expr())

    def visitXor_expr(self, ctx: Python3Parser.Xor_exprContext):
        return self.binary_helper('^', ctx.and_expr())

    def visitAnd_expr(self, ctx: Python3Parser.And_exprContext):
        return self.binary_helper('&', ctx.shift_expr())

    def visitShift_expr(self, ctx: Python3Parser.Shift_exprContext):
        return self.var_op_helper('shift', ctx.op, ctx.arith_expr())

    def visitArith_expr(self, ctx: Python3Parser.Arith_exprContext):
        return self.var_op_helper('additive', ctx.op, ctx.term())

    def visitTerm(self, ctx: Python3Parser.TermContext):
        return self.var_op_helper('multiplicative', ctx.op, ctx.factor())

    def visitFactor(self, ctx: Python3Parser.FactorContext):
        if (power := ctx.power()) is not None:
            return self.visit(power)
        return PythonOp(ctx.op.text, [self.visit(ctx.factor())])

    def visitPower(self, ctx: Python3Parser.PowerContext):
        if (factor := ctx.factor()) is not None:
            return PythonOp('**', [self.visit(ctx.atom_expr()), self.visit(factor)])
        return self.visit(ctx.atom_expr())

    def visitAtom_expr(self, ctx: Python3Parser.Atom_exprContext):
        atom = self.visit(ctx.atom())
        if trailers := ctx.trailer():
            result = atom
            for trailer in trailers:
                result = self.visit(trailer)(result)
            return result
        return atom

    def visitTrailer_args(self, ctx: Python3Parser.Trailer_argsContext):
        if (args := ctx.arglist()) is not None:
            arglist = self.visit(args)
        else:
            arglist = []
        return lambda func: PythonCall(func, arglist)

    def visitArglist(self, ctx: Python3Parser.ArglistContext):
        return [self.visit(arg) for arg in ctx.argument()]

    def visitArg_assign(self, ctx: Python3Parser.Arg_assignContext):
        # N.B. The name is specified in the grammar as a 'test', but should be a simple name
        # Therefore we use only the text here, without a recursive visit
        return PythonKeywordArg(ctx_text(ctx.test(0)), self.visit(ctx.test(1)))

    def visitArg_or_gen(self, ctx: Python3Parser.Arg_or_genContext):
        if (comp := ctx.comp_for()) is not None:
            return PythonGenExpr(self.visit(ctx.test()), self.visit(ctx.comp_for()))
        return self.visit(ctx.test())

    def visitTrailer_subscripts(self, ctx: Python3Parser.Trailer_subscriptsContext):
        return lambda obj: PythonSubscripted(obj, self.visit(ctx.subscriptlist()))

    def visitSubscriptlist(self, ctx: Python3Parser.SubscriptlistContext):
        return [self.visit(sub) for sub in ctx.subscript()]

    def visitSubscript(self, ctx: Python3Parser.SubscriptContext):
        if (sub := ctx.sub_expr) is not None:
            return self.visit(sub)
        from_expr = self.visit(ctx.from_expr) if ctx.from_expr else None
        to_expr = self.visit(ctx.to_expr) if ctx.to_expr else None
        step_expr = self.visit(ctx.step_expr) if ctx.step_expr else None
        return PythonSlice(from_expr, to_expr, step_expr)

    def visitTrailer_attribute(self, ctx: Python3Parser.Trailer_attributeContext):
        return lambda obj: PythonAttribute(obj, ctx.NAME().getText())

    def visitAtom_tuple(self, ctx: Python3Parser.Atom_tupleContext):
        if (yld := ctx.yield_expr()) is not None:
            raise OptimisticPythonParserException('yield expressions not supported!')
        if ctx.testlist_comp() is None:
            return PythonTupleCons([])
        contents = self.visit(ctx.testlist_comp())
        if isinstance(contents, PythonElement):
            return contents
        return PythonTupleCons(contents.components)

    def visitAtom_list(self, ctx: Python3Parser.Atom_listContext):
        if ctx.testlist_comp() is None:
            return PythonListCons([])
        contents = self.visit(ctx.testlist_comp())
        if isinstance(contents, Comprehension):
            return contents.as_list()
        if not isinstance(contents, PythonContainerCons):
            return PythonListCons([contents])
        return PythonListCons(contents.components)

    def visitAtom_dict_or_set(self, ctx: Python3Parser.Atom_dict_or_setContext):
        if (contents := ctx.dictorsetmaker()) is not None:
            return self.visit(contents)
        else:
            return PythonDictCons([])

    def visitAtom_name(self, ctx: Python3Parser.Atom_nameContext):
        return PythonVariable(ctx.NAME().getText())

    def visitAtom_number(self, ctx: Python3Parser.Atom_numberContext):
        return PythonConstant(self.visit(ctx.number()))

    def visitNumber(self, ctx: Python3Parser.NumberContext):
        if (intval := ctx.INTEGER()) is not None:
            return int(intval.getText())
        if (floatval := ctx.FLOAT_NUMBER()) is not None:
            return float(floatval.getText())
        if (imagval := ctx.IMAG_NUMBER()) is not None:
            return complex(imagval.getText())
        raise Exception('Unknown number type')

    STR_START = compile(r'["\']')

    def visitAtom_strings(self, ctx: Python3Parser.Atom_stringsContext):
        def safe_eval(string):
            string_start = self.STR_START.search(string).start()
            if string[:string_start].lower().find('f') >= 0:
                return f'{string[:string_start]}"{literal_eval(string[string_start:])}"'
            else:
                return literal_eval(string)

        if len(strings := ctx.STRING()) == 1:
            return PythonConstant(safe_eval(strings[0].getText()))
        return PythonConstant(''.join(safe_eval(s.getText()) for s in strings))

    def visitAtom_ellipsis(self, ctx: Python3Parser.Atom_ellipsisContext):
        return PythonConstant(Ellipsis)

    def visitAtom_none(self, ctx: Python3Parser.Atom_noneContext):
        return PythonConstant(None)

    def visitAtom_true(self, ctx: Python3Parser.Atom_trueContext):
        return PythonConstant(True)

    def visitAtom_false(self, ctx: Python3Parser.Atom_falseContext):
        return PythonConstant(False)

    def visitTestlist_comp(self, ctx: Python3Parser.Testlist_compContext):
        return self.visit(ctx.testlist_comp1() or ctx.testlist_comp2())

    def visitTestlist_comp1(self, ctx: Python3Parser.Testlist_comp1Context):
        return PythonGenExpr(self.visit(ctx.test_star_expr()), self.visit(ctx.comp_for()))

    def visitTestlist_comp2(self, ctx: Python3Parser.Testlist_comp2Context):
        if len(ctx.test_star_expr()) > 1 or ctx.extra_comma is not None:
            return Components([self.visit(c) for c in ctx.test_star_expr()])
        elif len(ctx.test_star_expr()) == 1:
            return self.visit(ctx.test_star_expr(0))
        else:
            return EmptyContents()

    def visitDict_compr(self, ctx: Python3Parser.Dict_comprContext):
        if (comp := ctx.comp_for()) is not None:
            spec = self.visit(ctx.dict_compr_component(0))
            return PythonDictCompr(spec.key, spec.value, self.visit(comp))
        return PythonDictCons([self.visit(c) for c in ctx.dict_compr_component()])

    def visitSet_compr(self, ctx: Python3Parser.Set_comprContext):
        if (comp := ctx.comp_for()) is not None:
            return PythonSetCompr(self.visit(ctx.test_star_expr(0)), self.visit(comp))
        return PythonSetCons([self.visit(c) for c in ctx.test_star_expr()])

    def visitDict_compr_component(self, ctx: Python3Parser.Dict_compr_componentContext):
        if (dstar := ctx.expr()) is not None:
            return PythonIncDict(self.visit(dstar))
        return PythonDictPair(self.visit(ctx.test(0)), self.visit(ctx.test(1)))

    def visitComp_for(self, ctx: Python3Parser.Comp_forContext):
        return PythonForComprehension(self.visit(ctx.exprlist()), self.visit(ctx.or_test()),
                                      self.visit(more) if (more := ctx.comp_iter()) else None)

    def visitExprlist(self, ctx: Python3Parser.ExprlistContext):
        return [self.visit(e) for e in ctx.expr_or_star()]

    def visitExpr_or_star(self, ctx: Python3Parser.Expr_or_starContext):
        return self.visit(ctx.expr() or ctx.star_expr())

    def visitStar_expr(self, ctx: Python3Parser.Star_exprContext):
        return PythonUnpack(self.visit(ctx.expr()))

    def visitComp_iter(self, ctx: Python3Parser.Comp_iterContext):
        return self.visit(ctx.comp_if() or ctx.comp_for())

    def visitComp_if(self, ctx: Python3Parser.Comp_ifContext):
        return PythonIfComprehension(self.visit(ctx.test_nocond()),
                                     self.visit(more) if (more := ctx.comp_iter()) else None)

    def visitPass_stmt(self, ctx: Python3Parser.Pass_stmtContext):
        return PythonPass()

    def visitClassdef(self, ctx: Python3Parser.ClassdefContext):
        superclasses = self.visit(args) if (args := ctx.arglist()) else []
        return PythonClass(ctx.NAME().getText(), superclasses, self.visit(ctx.suite()))

    def visitDecorated(self, ctx: Python3Parser.DecoratedContext):
        return PythonDecorated(self.visit(ctx.decorators()), self.visit(ctx.decorated_subject()))

    def visitDecorators(self, ctx: Python3Parser.DecoratorsContext):
        return [self.visit(d) for d in ctx.decorator()]

    def visitDecorator(self, ctx: Python3Parser.DecoratorContext):
        base = self.visit(ctx.dotted_name())
        if (args := ctx.arglist()) is not None:
            return PythonCall(base, self.visit(args))
        else:
            return base

    def visitDotted_name(self, ctx: Python3Parser.Dotted_nameContext):
        names = ctx.NAME()
        result = PythonVariable(names[0].getText())
        for attr in names[1:]:
            result = PythonAttribute(result, attr.getText())
        return result

    def visitDecorated_subject(self, ctx: Python3Parser.Decorated_subjectContext):
        return self.visit(ctx.classdef() or ctx.funcdef() or ctx.async_funcdef())




