# Generated from D:/Yishai/ws/eco/Profile-Parser/Grammars/Profiles.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ProfilesParser import ProfilesParser
else:
    from ProfilesParser import ProfilesParser

# This class defines a complete generic visitor for a parse tree produced by ProfilesParser.

class ProfilesVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ProfilesParser#profile.
    def visitProfile(self, ctx:ProfilesParser.ProfileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#Negation.
    def visitNegation(self, ctx:ProfilesParser.NegationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#In.
    def visitIn(self, ctx:ProfilesParser.InContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#UniversalCond.
    def visitUniversalCond(self, ctx:ProfilesParser.UniversalCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#Between.
    def visitBetween(self, ctx:ProfilesParser.BetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#BindingExistentialWithDiff.
    def visitBindingExistentialWithDiff(self, ctx:ProfilesParser.BindingExistentialWithDiffContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#BindingExistentialWithUnique.
    def visitBindingExistentialWithUnique(self, ctx:ProfilesParser.BindingExistentialWithUniqueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#ParenCond.
    def visitParenCond(self, ctx:ProfilesParser.ParenCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#UnaryPredAppl.
    def visitUnaryPredAppl(self, ctx:ProfilesParser.UnaryPredApplContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#TemporalOp.
    def visitTemporalOp(self, ctx:ProfilesParser.TemporalOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#Disjunction.
    def visitDisjunction(self, ctx:ProfilesParser.DisjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#ExistentialCond.
    def visitExistentialCond(self, ctx:ProfilesParser.ExistentialCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#Comparison.
    def visitComparison(self, ctx:ProfilesParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#Conjunction.
    def visitConjunction(self, ctx:ProfilesParser.ConjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#PredicateAppl.
    def visitPredicateAppl(self, ctx:ProfilesParser.PredicateApplContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#BindingExistentialUnique.
    def visitBindingExistentialUnique(self, ctx:ProfilesParser.BindingExistentialUniqueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#IsConstant.
    def visitIsConstant(self, ctx:ProfilesParser.IsConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#AtomicPred.
    def visitAtomicPred(self, ctx:ProfilesParser.AtomicPredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#ConjunctivePred.
    def visitConjunctivePred(self, ctx:ProfilesParser.ConjunctivePredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#DisjunctivePred.
    def visitDisjunctivePred(self, ctx:ProfilesParser.DisjunctivePredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#unary_predicate.
    def visitUnary_predicate(self, ctx:ProfilesParser.Unary_predicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#FunctionApp.
    def visitFunctionApp(self, ctx:ProfilesParser.FunctionAppContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#PercentOf.
    def visitPercentOf(self, ctx:ProfilesParser.PercentOfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#function_name.
    def visitFunction_name(self, ctx:ProfilesParser.Function_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#existential.
    def visitExistential(self, ctx:ProfilesParser.ExistentialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#binding_existential_with_diff.
    def visitBinding_existential_with_diff(self, ctx:ProfilesParser.Binding_existential_with_diffContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#binding_existential_with_unique.
    def visitBinding_existential_with_unique(self, ctx:ProfilesParser.Binding_existential_with_uniqueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#binding_existential_with_unique1.
    def visitBinding_existential_with_unique1(self, ctx:ProfilesParser.Binding_existential_with_unique1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#binding_existential_unique.
    def visitBinding_existential_unique(self, ctx:ProfilesParser.Binding_existential_uniqueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#ForAll.
    def visitForAll(self, ctx:ProfilesParser.ForAllContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#Every.
    def visitEvery(self, ctx:ProfilesParser.EveryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#aggregate.
    def visitAggregate(self, ctx:ProfilesParser.AggregateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#such_that.
    def visitSuch_that(self, ctx:ProfilesParser.Such_thatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#MultipleAttributes.
    def visitMultipleAttributes(self, ctx:ProfilesParser.MultipleAttributesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#SingleAttribute.
    def visitSingleAttribute(self, ctx:ProfilesParser.SingleAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#to_be.
    def visitTo_be(self, ctx:ProfilesParser.To_beContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#ComparisonOp1.
    def visitComparisonOp1(self, ctx:ProfilesParser.ComparisonOp1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#ComparisonOp2.
    def visitComparisonOp2(self, ctx:ProfilesParser.ComparisonOp2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#ComparisonOp3.
    def visitComparisonOp3(self, ctx:ProfilesParser.ComparisonOp3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#ComparisonOp4.
    def visitComparisonOp4(self, ctx:ProfilesParser.ComparisonOp4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#eq_not_eq.
    def visitEq_not_eq(self, ctx:ProfilesParser.Eq_not_eqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#TemporalOrder.
    def visitTemporalOrder(self, ctx:ProfilesParser.TemporalOrderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#TemporalOverlap.
    def visitTemporalOverlap(self, ctx:ProfilesParser.TemporalOverlapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#TemporalDisjoint.
    def visitTemporalDisjoint(self, ctx:ProfilesParser.TemporalDisjointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#greater.
    def visitGreater(self, ctx:ProfilesParser.GreaterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#smaller.
    def visitSmaller(self, ctx:ProfilesParser.SmallerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#quantity.
    def visitQuantity(self, ctx:ProfilesParser.QuantityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#general_set.
    def visitGeneral_set(self, ctx:ProfilesParser.General_setContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#conjunction_of_np.
    def visitConjunction_of_np(self, ctx:ProfilesParser.Conjunction_of_npContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#disjunction_of_np.
    def visitDisjunction_of_np(self, ctx:ProfilesParser.Disjunction_of_npContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#AtomicExpr.
    def visitAtomicExpr(self, ctx:ProfilesParser.AtomicExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#DisjunctionExpr.
    def visitDisjunctionExpr(self, ctx:ProfilesParser.DisjunctionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#FunctionExpr.
    def visitFunctionExpr(self, ctx:ProfilesParser.FunctionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#SetExpr.
    def visitSetExpr(self, ctx:ProfilesParser.SetExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#ConjunctionExpr.
    def visitConjunctionExpr(self, ctx:ProfilesParser.ConjunctionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#AttributeExpr.
    def visitAttributeExpr(self, ctx:ProfilesParser.AttributeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#AggregateExpr.
    def visitAggregateExpr(self, ctx:ProfilesParser.AggregateExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#ParenExpr.
    def visitParenExpr(self, ctx:ProfilesParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#PhraseExpr.
    def visitPhraseExpr(self, ctx:ProfilesParser.PhraseExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#QuantityExpr.
    def visitQuantityExpr(self, ctx:ProfilesParser.QuantityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#StringExpr.
    def visitStringExpr(self, ctx:ProfilesParser.StringExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#VariableExpr.
    def visitVariableExpr(self, ctx:ProfilesParser.VariableExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#TimeExpr.
    def visitTimeExpr(self, ctx:ProfilesParser.TimeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#PeriodExpr.
    def visitPeriodExpr(self, ctx:ProfilesParser.PeriodExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#period.
    def visitPeriod(self, ctx:ProfilesParser.PeriodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#phrase.
    def visitPhrase(self, ctx:ProfilesParser.PhraseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#noun_phrase.
    def visitNoun_phrase(self, ctx:ProfilesParser.Noun_phraseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#verb_phrase.
    def visitVerb_phrase(self, ctx:ProfilesParser.Verb_phraseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#type_name.
    def visitType_name(self, ctx:ProfilesParser.Type_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProfilesParser#article.
    def visitArticle(self, ctx:ProfilesParser.ArticleContext):
        return self.visitChildren(ctx)



del ProfilesParser