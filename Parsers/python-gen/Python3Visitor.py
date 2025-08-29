# Generated from D:/Yishai/ws/pycharm/Parsers/python3-py/Python3.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .Python3Parser import Python3Parser
else:
    from Python3Parser import Python3Parser

# This class defines a complete generic visitor for a parse tree produced by Python3Parser.

class Python3Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by Python3Parser#single_input.
    def visitSingle_input(self, ctx:Python3Parser.Single_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#file_input.
    def visitFile_input(self, ctx:Python3Parser.File_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#eval_input.
    def visitEval_input(self, ctx:Python3Parser.Eval_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorator.
    def visitDecorator(self, ctx:Python3Parser.DecoratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorators.
    def visitDecorators(self, ctx:Python3Parser.DecoratorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorated.
    def visitDecorated(self, ctx:Python3Parser.DecoratedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorated_subject.
    def visitDecorated_subject(self, ctx:Python3Parser.Decorated_subjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#async_funcdef.
    def visitAsync_funcdef(self, ctx:Python3Parser.Async_funcdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#funcdef.
    def visitFuncdef(self, ctx:Python3Parser.FuncdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#parameters.
    def visitParameters(self, ctx:Python3Parser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#parmlist_nonempty.
    def visitParmlist_nonempty(self, ctx:Python3Parser.Parmlist_nonemptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#parmlist_rest.
    def visitParmlist_rest(self, ctx:Python3Parser.Parmlist_restContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#parmlist_kw.
    def visitParmlist_kw(self, ctx:Python3Parser.Parmlist_kwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#posargslist.
    def visitPosargslist(self, ctx:Python3Parser.PosargslistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#kwargslist.
    def visitKwargslist(self, ctx:Python3Parser.KwargslistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#tfpdef.
    def visitTfpdef(self, ctx:Python3Parser.TfpdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#varargslist.
    def visitVarargslist(self, ctx:Python3Parser.VarargslistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#vfpdef.
    def visitVfpdef(self, ctx:Python3Parser.VfpdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#stmt.
    def visitStmt(self, ctx:Python3Parser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#simple_stmt.
    def visitSimple_stmt(self, ctx:Python3Parser.Simple_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#small_stmt.
    def visitSmall_stmt(self, ctx:Python3Parser.Small_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#special_assign.
    def visitSpecial_assign(self, ctx:Python3Parser.Special_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#reg_assign.
    def visitReg_assign(self, ctx:Python3Parser.Reg_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#annassign.
    def visitAnnassign(self, ctx:Python3Parser.AnnassignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlist_star_expr.
    def visitTestlist_star_expr(self, ctx:Python3Parser.Testlist_star_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#test_star_expr.
    def visitTest_star_expr(self, ctx:Python3Parser.Test_star_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#augassign.
    def visitAugassign(self, ctx:Python3Parser.AugassignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#del_stmt.
    def visitDel_stmt(self, ctx:Python3Parser.Del_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#pass_stmt.
    def visitPass_stmt(self, ctx:Python3Parser.Pass_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#flow_stmt.
    def visitFlow_stmt(self, ctx:Python3Parser.Flow_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#break_stmt.
    def visitBreak_stmt(self, ctx:Python3Parser.Break_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#continue_stmt.
    def visitContinue_stmt(self, ctx:Python3Parser.Continue_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#return_stmt.
    def visitReturn_stmt(self, ctx:Python3Parser.Return_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yield_stmt.
    def visitYield_stmt(self, ctx:Python3Parser.Yield_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#raise_stmt.
    def visitRaise_stmt(self, ctx:Python3Parser.Raise_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_stmt.
    def visitImport_stmt(self, ctx:Python3Parser.Import_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_name.
    def visitImport_name(self, ctx:Python3Parser.Import_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_from.
    def visitImport_from(self, ctx:Python3Parser.Import_fromContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_as_name.
    def visitImport_as_name(self, ctx:Python3Parser.Import_as_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dotted_as_name.
    def visitDotted_as_name(self, ctx:Python3Parser.Dotted_as_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#import_as_names.
    def visitImport_as_names(self, ctx:Python3Parser.Import_as_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dotted_as_names.
    def visitDotted_as_names(self, ctx:Python3Parser.Dotted_as_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dotted_name.
    def visitDotted_name(self, ctx:Python3Parser.Dotted_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#global_stmt.
    def visitGlobal_stmt(self, ctx:Python3Parser.Global_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#nonlocal_stmt.
    def visitNonlocal_stmt(self, ctx:Python3Parser.Nonlocal_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#assert_stmt.
    def visitAssert_stmt(self, ctx:Python3Parser.Assert_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#compound_stmt.
    def visitCompound_stmt(self, ctx:Python3Parser.Compound_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#async_stmt.
    def visitAsync_stmt(self, ctx:Python3Parser.Async_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#if_stmt.
    def visitIf_stmt(self, ctx:Python3Parser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#while_stmt.
    def visitWhile_stmt(self, ctx:Python3Parser.While_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#for_stmt.
    def visitFor_stmt(self, ctx:Python3Parser.For_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#try_stmt.
    def visitTry_stmt(self, ctx:Python3Parser.Try_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#with_stmt.
    def visitWith_stmt(self, ctx:Python3Parser.With_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#with_item.
    def visitWith_item(self, ctx:Python3Parser.With_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#except_clause.
    def visitExcept_clause(self, ctx:Python3Parser.Except_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#suite.
    def visitSuite(self, ctx:Python3Parser.SuiteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#test.
    def visitTest(self, ctx:Python3Parser.TestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#test_nocond.
    def visitTest_nocond(self, ctx:Python3Parser.Test_nocondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#lambdef.
    def visitLambdef(self, ctx:Python3Parser.LambdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#lambdef_nocond.
    def visitLambdef_nocond(self, ctx:Python3Parser.Lambdef_nocondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#or_test.
    def visitOr_test(self, ctx:Python3Parser.Or_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#and_test.
    def visitAnd_test(self, ctx:Python3Parser.And_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#not_test.
    def visitNot_test(self, ctx:Python3Parser.Not_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comparison.
    def visitComparison(self, ctx:Python3Parser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comp_op.
    def visitComp_op(self, ctx:Python3Parser.Comp_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#star_expr.
    def visitStar_expr(self, ctx:Python3Parser.Star_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#expr.
    def visitExpr(self, ctx:Python3Parser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#xor_expr.
    def visitXor_expr(self, ctx:Python3Parser.Xor_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#and_expr.
    def visitAnd_expr(self, ctx:Python3Parser.And_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#shift_expr.
    def visitShift_expr(self, ctx:Python3Parser.Shift_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arith_expr.
    def visitArith_expr(self, ctx:Python3Parser.Arith_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#term.
    def visitTerm(self, ctx:Python3Parser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#factor.
    def visitFactor(self, ctx:Python3Parser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#power.
    def visitPower(self, ctx:Python3Parser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_expr.
    def visitAtom_expr(self, ctx:Python3Parser.Atom_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_tuple.
    def visitAtom_tuple(self, ctx:Python3Parser.Atom_tupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_list.
    def visitAtom_list(self, ctx:Python3Parser.Atom_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_dict_or_set.
    def visitAtom_dict_or_set(self, ctx:Python3Parser.Atom_dict_or_setContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_name.
    def visitAtom_name(self, ctx:Python3Parser.Atom_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_number.
    def visitAtom_number(self, ctx:Python3Parser.Atom_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_strings.
    def visitAtom_strings(self, ctx:Python3Parser.Atom_stringsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_ellipsis.
    def visitAtom_ellipsis(self, ctx:Python3Parser.Atom_ellipsisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_none.
    def visitAtom_none(self, ctx:Python3Parser.Atom_noneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_true.
    def visitAtom_true(self, ctx:Python3Parser.Atom_trueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atom_false.
    def visitAtom_false(self, ctx:Python3Parser.Atom_falseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlist_comp.
    def visitTestlist_comp(self, ctx:Python3Parser.Testlist_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlist_comp1.
    def visitTestlist_comp1(self, ctx:Python3Parser.Testlist_comp1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlist_comp2.
    def visitTestlist_comp2(self, ctx:Python3Parser.Testlist_comp2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#trailer_args.
    def visitTrailer_args(self, ctx:Python3Parser.Trailer_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#trailer_subscripts.
    def visitTrailer_subscripts(self, ctx:Python3Parser.Trailer_subscriptsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#trailer_attribute.
    def visitTrailer_attribute(self, ctx:Python3Parser.Trailer_attributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subscriptlist.
    def visitSubscriptlist(self, ctx:Python3Parser.SubscriptlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subscript.
    def visitSubscript(self, ctx:Python3Parser.SubscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#exprlist.
    def visitExprlist(self, ctx:Python3Parser.ExprlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#expr_or_star.
    def visitExpr_or_star(self, ctx:Python3Parser.Expr_or_starContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlist.
    def visitTestlist(self, ctx:Python3Parser.TestlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dict_compr.
    def visitDict_compr(self, ctx:Python3Parser.Dict_comprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#set_compr.
    def visitSet_compr(self, ctx:Python3Parser.Set_comprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dict_compr_component.
    def visitDict_compr_component(self, ctx:Python3Parser.Dict_compr_componentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#classdef.
    def visitClassdef(self, ctx:Python3Parser.ClassdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arglist.
    def visitArglist(self, ctx:Python3Parser.ArglistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arg_or_gen.
    def visitArg_or_gen(self, ctx:Python3Parser.Arg_or_genContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arg_assign.
    def visitArg_assign(self, ctx:Python3Parser.Arg_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arg_kw.
    def visitArg_kw(self, ctx:Python3Parser.Arg_kwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arg_rest.
    def visitArg_rest(self, ctx:Python3Parser.Arg_restContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comp_iter.
    def visitComp_iter(self, ctx:Python3Parser.Comp_iterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comp_for.
    def visitComp_for(self, ctx:Python3Parser.Comp_forContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comp_if.
    def visitComp_if(self, ctx:Python3Parser.Comp_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#encoding_decl.
    def visitEncoding_decl(self, ctx:Python3Parser.Encoding_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yield_expr.
    def visitYield_expr(self, ctx:Python3Parser.Yield_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yield_arg.
    def visitYield_arg(self, ctx:Python3Parser.Yield_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#number.
    def visitNumber(self, ctx:Python3Parser.NumberContext):
        return self.visitChildren(ctx)



del Python3Parser