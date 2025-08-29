# Generated from D:/Yishai/ws/eco/Profile-Parser/Grammars/Profiles.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ProfilesParser import ProfilesParser
else:
    from ProfilesParser import ProfilesParser

# This class defines a complete listener for a parse tree produced by ProfilesParser.
class ProfilesListener(ParseTreeListener):

    # Enter a parse tree produced by ProfilesParser#profile.
    def enterProfile(self, ctx:ProfilesParser.ProfileContext):
        pass

    # Exit a parse tree produced by ProfilesParser#profile.
    def exitProfile(self, ctx:ProfilesParser.ProfileContext):
        pass


    # Enter a parse tree produced by ProfilesParser#Negation.
    def enterNegation(self, ctx:ProfilesParser.NegationContext):
        pass

    # Exit a parse tree produced by ProfilesParser#Negation.
    def exitNegation(self, ctx:ProfilesParser.NegationContext):
        pass


    # Enter a parse tree produced by ProfilesParser#In.
    def enterIn(self, ctx:ProfilesParser.InContext):
        pass

    # Exit a parse tree produced by ProfilesParser#In.
    def exitIn(self, ctx:ProfilesParser.InContext):
        pass


    # Enter a parse tree produced by ProfilesParser#UniversalCond.
    def enterUniversalCond(self, ctx:ProfilesParser.UniversalCondContext):
        pass

    # Exit a parse tree produced by ProfilesParser#UniversalCond.
    def exitUniversalCond(self, ctx:ProfilesParser.UniversalCondContext):
        pass


    # Enter a parse tree produced by ProfilesParser#Between.
    def enterBetween(self, ctx:ProfilesParser.BetweenContext):
        pass

    # Exit a parse tree produced by ProfilesParser#Between.
    def exitBetween(self, ctx:ProfilesParser.BetweenContext):
        pass


    # Enter a parse tree produced by ProfilesParser#BindingExistentialWithDiff.
    def enterBindingExistentialWithDiff(self, ctx:ProfilesParser.BindingExistentialWithDiffContext):
        pass

    # Exit a parse tree produced by ProfilesParser#BindingExistentialWithDiff.
    def exitBindingExistentialWithDiff(self, ctx:ProfilesParser.BindingExistentialWithDiffContext):
        pass


    # Enter a parse tree produced by ProfilesParser#BindingExistentialWithUnique.
    def enterBindingExistentialWithUnique(self, ctx:ProfilesParser.BindingExistentialWithUniqueContext):
        pass

    # Exit a parse tree produced by ProfilesParser#BindingExistentialWithUnique.
    def exitBindingExistentialWithUnique(self, ctx:ProfilesParser.BindingExistentialWithUniqueContext):
        pass


    # Enter a parse tree produced by ProfilesParser#ParenCond.
    def enterParenCond(self, ctx:ProfilesParser.ParenCondContext):
        pass

    # Exit a parse tree produced by ProfilesParser#ParenCond.
    def exitParenCond(self, ctx:ProfilesParser.ParenCondContext):
        pass


    # Enter a parse tree produced by ProfilesParser#UnaryPredAppl.
    def enterUnaryPredAppl(self, ctx:ProfilesParser.UnaryPredApplContext):
        pass

    # Exit a parse tree produced by ProfilesParser#UnaryPredAppl.
    def exitUnaryPredAppl(self, ctx:ProfilesParser.UnaryPredApplContext):
        pass


    # Enter a parse tree produced by ProfilesParser#TemporalOp.
    def enterTemporalOp(self, ctx:ProfilesParser.TemporalOpContext):
        pass

    # Exit a parse tree produced by ProfilesParser#TemporalOp.
    def exitTemporalOp(self, ctx:ProfilesParser.TemporalOpContext):
        pass


    # Enter a parse tree produced by ProfilesParser#Disjunction.
    def enterDisjunction(self, ctx:ProfilesParser.DisjunctionContext):
        pass

    # Exit a parse tree produced by ProfilesParser#Disjunction.
    def exitDisjunction(self, ctx:ProfilesParser.DisjunctionContext):
        pass


    # Enter a parse tree produced by ProfilesParser#ExistentialCond.
    def enterExistentialCond(self, ctx:ProfilesParser.ExistentialCondContext):
        pass

    # Exit a parse tree produced by ProfilesParser#ExistentialCond.
    def exitExistentialCond(self, ctx:ProfilesParser.ExistentialCondContext):
        pass


    # Enter a parse tree produced by ProfilesParser#Comparison.
    def enterComparison(self, ctx:ProfilesParser.ComparisonContext):
        pass

    # Exit a parse tree produced by ProfilesParser#Comparison.
    def exitComparison(self, ctx:ProfilesParser.ComparisonContext):
        pass


    # Enter a parse tree produced by ProfilesParser#Conjunction.
    def enterConjunction(self, ctx:ProfilesParser.ConjunctionContext):
        pass

    # Exit a parse tree produced by ProfilesParser#Conjunction.
    def exitConjunction(self, ctx:ProfilesParser.ConjunctionContext):
        pass


    # Enter a parse tree produced by ProfilesParser#PredicateAppl.
    def enterPredicateAppl(self, ctx:ProfilesParser.PredicateApplContext):
        pass

    # Exit a parse tree produced by ProfilesParser#PredicateAppl.
    def exitPredicateAppl(self, ctx:ProfilesParser.PredicateApplContext):
        pass


    # Enter a parse tree produced by ProfilesParser#BindingExistentialUnique.
    def enterBindingExistentialUnique(self, ctx:ProfilesParser.BindingExistentialUniqueContext):
        pass

    # Exit a parse tree produced by ProfilesParser#BindingExistentialUnique.
    def exitBindingExistentialUnique(self, ctx:ProfilesParser.BindingExistentialUniqueContext):
        pass


    # Enter a parse tree produced by ProfilesParser#IsConstant.
    def enterIsConstant(self, ctx:ProfilesParser.IsConstantContext):
        pass

    # Exit a parse tree produced by ProfilesParser#IsConstant.
    def exitIsConstant(self, ctx:ProfilesParser.IsConstantContext):
        pass


    # Enter a parse tree produced by ProfilesParser#AtomicPred.
    def enterAtomicPred(self, ctx:ProfilesParser.AtomicPredContext):
        pass

    # Exit a parse tree produced by ProfilesParser#AtomicPred.
    def exitAtomicPred(self, ctx:ProfilesParser.AtomicPredContext):
        pass


    # Enter a parse tree produced by ProfilesParser#ConjunctivePred.
    def enterConjunctivePred(self, ctx:ProfilesParser.ConjunctivePredContext):
        pass

    # Exit a parse tree produced by ProfilesParser#ConjunctivePred.
    def exitConjunctivePred(self, ctx:ProfilesParser.ConjunctivePredContext):
        pass


    # Enter a parse tree produced by ProfilesParser#DisjunctivePred.
    def enterDisjunctivePred(self, ctx:ProfilesParser.DisjunctivePredContext):
        pass

    # Exit a parse tree produced by ProfilesParser#DisjunctivePred.
    def exitDisjunctivePred(self, ctx:ProfilesParser.DisjunctivePredContext):
        pass


    # Enter a parse tree produced by ProfilesParser#unary_predicate.
    def enterUnary_predicate(self, ctx:ProfilesParser.Unary_predicateContext):
        pass

    # Exit a parse tree produced by ProfilesParser#unary_predicate.
    def exitUnary_predicate(self, ctx:ProfilesParser.Unary_predicateContext):
        pass


    # Enter a parse tree produced by ProfilesParser#FunctionApp.
    def enterFunctionApp(self, ctx:ProfilesParser.FunctionAppContext):
        pass

    # Exit a parse tree produced by ProfilesParser#FunctionApp.
    def exitFunctionApp(self, ctx:ProfilesParser.FunctionAppContext):
        pass


    # Enter a parse tree produced by ProfilesParser#PercentOf.
    def enterPercentOf(self, ctx:ProfilesParser.PercentOfContext):
        pass

    # Exit a parse tree produced by ProfilesParser#PercentOf.
    def exitPercentOf(self, ctx:ProfilesParser.PercentOfContext):
        pass


    # Enter a parse tree produced by ProfilesParser#function_name.
    def enterFunction_name(self, ctx:ProfilesParser.Function_nameContext):
        pass

    # Exit a parse tree produced by ProfilesParser#function_name.
    def exitFunction_name(self, ctx:ProfilesParser.Function_nameContext):
        pass


    # Enter a parse tree produced by ProfilesParser#existential.
    def enterExistential(self, ctx:ProfilesParser.ExistentialContext):
        pass

    # Exit a parse tree produced by ProfilesParser#existential.
    def exitExistential(self, ctx:ProfilesParser.ExistentialContext):
        pass


    # Enter a parse tree produced by ProfilesParser#binding_existential_with_diff.
    def enterBinding_existential_with_diff(self, ctx:ProfilesParser.Binding_existential_with_diffContext):
        pass

    # Exit a parse tree produced by ProfilesParser#binding_existential_with_diff.
    def exitBinding_existential_with_diff(self, ctx:ProfilesParser.Binding_existential_with_diffContext):
        pass


    # Enter a parse tree produced by ProfilesParser#binding_existential_with_unique.
    def enterBinding_existential_with_unique(self, ctx:ProfilesParser.Binding_existential_with_uniqueContext):
        pass

    # Exit a parse tree produced by ProfilesParser#binding_existential_with_unique.
    def exitBinding_existential_with_unique(self, ctx:ProfilesParser.Binding_existential_with_uniqueContext):
        pass


    # Enter a parse tree produced by ProfilesParser#binding_existential_with_unique1.
    def enterBinding_existential_with_unique1(self, ctx:ProfilesParser.Binding_existential_with_unique1Context):
        pass

    # Exit a parse tree produced by ProfilesParser#binding_existential_with_unique1.
    def exitBinding_existential_with_unique1(self, ctx:ProfilesParser.Binding_existential_with_unique1Context):
        pass


    # Enter a parse tree produced by ProfilesParser#binding_existential_unique.
    def enterBinding_existential_unique(self, ctx:ProfilesParser.Binding_existential_uniqueContext):
        pass

    # Exit a parse tree produced by ProfilesParser#binding_existential_unique.
    def exitBinding_existential_unique(self, ctx:ProfilesParser.Binding_existential_uniqueContext):
        pass


    # Enter a parse tree produced by ProfilesParser#ForAll.
    def enterForAll(self, ctx:ProfilesParser.ForAllContext):
        pass

    # Exit a parse tree produced by ProfilesParser#ForAll.
    def exitForAll(self, ctx:ProfilesParser.ForAllContext):
        pass


    # Enter a parse tree produced by ProfilesParser#Every.
    def enterEvery(self, ctx:ProfilesParser.EveryContext):
        pass

    # Exit a parse tree produced by ProfilesParser#Every.
    def exitEvery(self, ctx:ProfilesParser.EveryContext):
        pass


    # Enter a parse tree produced by ProfilesParser#aggregate.
    def enterAggregate(self, ctx:ProfilesParser.AggregateContext):
        pass

    # Exit a parse tree produced by ProfilesParser#aggregate.
    def exitAggregate(self, ctx:ProfilesParser.AggregateContext):
        pass


    # Enter a parse tree produced by ProfilesParser#such_that.
    def enterSuch_that(self, ctx:ProfilesParser.Such_thatContext):
        pass

    # Exit a parse tree produced by ProfilesParser#such_that.
    def exitSuch_that(self, ctx:ProfilesParser.Such_thatContext):
        pass


    # Enter a parse tree produced by ProfilesParser#MultipleAttributes.
    def enterMultipleAttributes(self, ctx:ProfilesParser.MultipleAttributesContext):
        pass

    # Exit a parse tree produced by ProfilesParser#MultipleAttributes.
    def exitMultipleAttributes(self, ctx:ProfilesParser.MultipleAttributesContext):
        pass


    # Enter a parse tree produced by ProfilesParser#SingleAttribute.
    def enterSingleAttribute(self, ctx:ProfilesParser.SingleAttributeContext):
        pass

    # Exit a parse tree produced by ProfilesParser#SingleAttribute.
    def exitSingleAttribute(self, ctx:ProfilesParser.SingleAttributeContext):
        pass


    # Enter a parse tree produced by ProfilesParser#to_be.
    def enterTo_be(self, ctx:ProfilesParser.To_beContext):
        pass

    # Exit a parse tree produced by ProfilesParser#to_be.
    def exitTo_be(self, ctx:ProfilesParser.To_beContext):
        pass


    # Enter a parse tree produced by ProfilesParser#ComparisonOp1.
    def enterComparisonOp1(self, ctx:ProfilesParser.ComparisonOp1Context):
        pass

    # Exit a parse tree produced by ProfilesParser#ComparisonOp1.
    def exitComparisonOp1(self, ctx:ProfilesParser.ComparisonOp1Context):
        pass


    # Enter a parse tree produced by ProfilesParser#ComparisonOp2.
    def enterComparisonOp2(self, ctx:ProfilesParser.ComparisonOp2Context):
        pass

    # Exit a parse tree produced by ProfilesParser#ComparisonOp2.
    def exitComparisonOp2(self, ctx:ProfilesParser.ComparisonOp2Context):
        pass


    # Enter a parse tree produced by ProfilesParser#ComparisonOp3.
    def enterComparisonOp3(self, ctx:ProfilesParser.ComparisonOp3Context):
        pass

    # Exit a parse tree produced by ProfilesParser#ComparisonOp3.
    def exitComparisonOp3(self, ctx:ProfilesParser.ComparisonOp3Context):
        pass


    # Enter a parse tree produced by ProfilesParser#ComparisonOp4.
    def enterComparisonOp4(self, ctx:ProfilesParser.ComparisonOp4Context):
        pass

    # Exit a parse tree produced by ProfilesParser#ComparisonOp4.
    def exitComparisonOp4(self, ctx:ProfilesParser.ComparisonOp4Context):
        pass


    # Enter a parse tree produced by ProfilesParser#eq_not_eq.
    def enterEq_not_eq(self, ctx:ProfilesParser.Eq_not_eqContext):
        pass

    # Exit a parse tree produced by ProfilesParser#eq_not_eq.
    def exitEq_not_eq(self, ctx:ProfilesParser.Eq_not_eqContext):
        pass


    # Enter a parse tree produced by ProfilesParser#TemporalOrder.
    def enterTemporalOrder(self, ctx:ProfilesParser.TemporalOrderContext):
        pass

    # Exit a parse tree produced by ProfilesParser#TemporalOrder.
    def exitTemporalOrder(self, ctx:ProfilesParser.TemporalOrderContext):
        pass


    # Enter a parse tree produced by ProfilesParser#TemporalOverlap.
    def enterTemporalOverlap(self, ctx:ProfilesParser.TemporalOverlapContext):
        pass

    # Exit a parse tree produced by ProfilesParser#TemporalOverlap.
    def exitTemporalOverlap(self, ctx:ProfilesParser.TemporalOverlapContext):
        pass


    # Enter a parse tree produced by ProfilesParser#TemporalDisjoint.
    def enterTemporalDisjoint(self, ctx:ProfilesParser.TemporalDisjointContext):
        pass

    # Exit a parse tree produced by ProfilesParser#TemporalDisjoint.
    def exitTemporalDisjoint(self, ctx:ProfilesParser.TemporalDisjointContext):
        pass


    # Enter a parse tree produced by ProfilesParser#greater.
    def enterGreater(self, ctx:ProfilesParser.GreaterContext):
        pass

    # Exit a parse tree produced by ProfilesParser#greater.
    def exitGreater(self, ctx:ProfilesParser.GreaterContext):
        pass


    # Enter a parse tree produced by ProfilesParser#smaller.
    def enterSmaller(self, ctx:ProfilesParser.SmallerContext):
        pass

    # Exit a parse tree produced by ProfilesParser#smaller.
    def exitSmaller(self, ctx:ProfilesParser.SmallerContext):
        pass


    # Enter a parse tree produced by ProfilesParser#quantity.
    def enterQuantity(self, ctx:ProfilesParser.QuantityContext):
        pass

    # Exit a parse tree produced by ProfilesParser#quantity.
    def exitQuantity(self, ctx:ProfilesParser.QuantityContext):
        pass


    # Enter a parse tree produced by ProfilesParser#general_set.
    def enterGeneral_set(self, ctx:ProfilesParser.General_setContext):
        pass

    # Exit a parse tree produced by ProfilesParser#general_set.
    def exitGeneral_set(self, ctx:ProfilesParser.General_setContext):
        pass


    # Enter a parse tree produced by ProfilesParser#conjunction_of_np.
    def enterConjunction_of_np(self, ctx:ProfilesParser.Conjunction_of_npContext):
        pass

    # Exit a parse tree produced by ProfilesParser#conjunction_of_np.
    def exitConjunction_of_np(self, ctx:ProfilesParser.Conjunction_of_npContext):
        pass


    # Enter a parse tree produced by ProfilesParser#disjunction_of_np.
    def enterDisjunction_of_np(self, ctx:ProfilesParser.Disjunction_of_npContext):
        pass

    # Exit a parse tree produced by ProfilesParser#disjunction_of_np.
    def exitDisjunction_of_np(self, ctx:ProfilesParser.Disjunction_of_npContext):
        pass


    # Enter a parse tree produced by ProfilesParser#AtomicExpr.
    def enterAtomicExpr(self, ctx:ProfilesParser.AtomicExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#AtomicExpr.
    def exitAtomicExpr(self, ctx:ProfilesParser.AtomicExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#DisjunctionExpr.
    def enterDisjunctionExpr(self, ctx:ProfilesParser.DisjunctionExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#DisjunctionExpr.
    def exitDisjunctionExpr(self, ctx:ProfilesParser.DisjunctionExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#FunctionExpr.
    def enterFunctionExpr(self, ctx:ProfilesParser.FunctionExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#FunctionExpr.
    def exitFunctionExpr(self, ctx:ProfilesParser.FunctionExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#SetExpr.
    def enterSetExpr(self, ctx:ProfilesParser.SetExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#SetExpr.
    def exitSetExpr(self, ctx:ProfilesParser.SetExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#ConjunctionExpr.
    def enterConjunctionExpr(self, ctx:ProfilesParser.ConjunctionExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#ConjunctionExpr.
    def exitConjunctionExpr(self, ctx:ProfilesParser.ConjunctionExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#AttributeExpr.
    def enterAttributeExpr(self, ctx:ProfilesParser.AttributeExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#AttributeExpr.
    def exitAttributeExpr(self, ctx:ProfilesParser.AttributeExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#AggregateExpr.
    def enterAggregateExpr(self, ctx:ProfilesParser.AggregateExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#AggregateExpr.
    def exitAggregateExpr(self, ctx:ProfilesParser.AggregateExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#ParenExpr.
    def enterParenExpr(self, ctx:ProfilesParser.ParenExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#ParenExpr.
    def exitParenExpr(self, ctx:ProfilesParser.ParenExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#PhraseExpr.
    def enterPhraseExpr(self, ctx:ProfilesParser.PhraseExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#PhraseExpr.
    def exitPhraseExpr(self, ctx:ProfilesParser.PhraseExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#QuantityExpr.
    def enterQuantityExpr(self, ctx:ProfilesParser.QuantityExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#QuantityExpr.
    def exitQuantityExpr(self, ctx:ProfilesParser.QuantityExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#StringExpr.
    def enterStringExpr(self, ctx:ProfilesParser.StringExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#StringExpr.
    def exitStringExpr(self, ctx:ProfilesParser.StringExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#VariableExpr.
    def enterVariableExpr(self, ctx:ProfilesParser.VariableExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#VariableExpr.
    def exitVariableExpr(self, ctx:ProfilesParser.VariableExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#TimeExpr.
    def enterTimeExpr(self, ctx:ProfilesParser.TimeExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#TimeExpr.
    def exitTimeExpr(self, ctx:ProfilesParser.TimeExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#PeriodExpr.
    def enterPeriodExpr(self, ctx:ProfilesParser.PeriodExprContext):
        pass

    # Exit a parse tree produced by ProfilesParser#PeriodExpr.
    def exitPeriodExpr(self, ctx:ProfilesParser.PeriodExprContext):
        pass


    # Enter a parse tree produced by ProfilesParser#period.
    def enterPeriod(self, ctx:ProfilesParser.PeriodContext):
        pass

    # Exit a parse tree produced by ProfilesParser#period.
    def exitPeriod(self, ctx:ProfilesParser.PeriodContext):
        pass


    # Enter a parse tree produced by ProfilesParser#phrase.
    def enterPhrase(self, ctx:ProfilesParser.PhraseContext):
        pass

    # Exit a parse tree produced by ProfilesParser#phrase.
    def exitPhrase(self, ctx:ProfilesParser.PhraseContext):
        pass


    # Enter a parse tree produced by ProfilesParser#noun_phrase.
    def enterNoun_phrase(self, ctx:ProfilesParser.Noun_phraseContext):
        pass

    # Exit a parse tree produced by ProfilesParser#noun_phrase.
    def exitNoun_phrase(self, ctx:ProfilesParser.Noun_phraseContext):
        pass


    # Enter a parse tree produced by ProfilesParser#verb_phrase.
    def enterVerb_phrase(self, ctx:ProfilesParser.Verb_phraseContext):
        pass

    # Exit a parse tree produced by ProfilesParser#verb_phrase.
    def exitVerb_phrase(self, ctx:ProfilesParser.Verb_phraseContext):
        pass


    # Enter a parse tree produced by ProfilesParser#type_name.
    def enterType_name(self, ctx:ProfilesParser.Type_nameContext):
        pass

    # Exit a parse tree produced by ProfilesParser#type_name.
    def exitType_name(self, ctx:ProfilesParser.Type_nameContext):
        pass


    # Enter a parse tree produced by ProfilesParser#article.
    def enterArticle(self, ctx:ProfilesParser.ArticleContext):
        pass

    # Exit a parse tree produced by ProfilesParser#article.
    def exitArticle(self, ctx:ProfilesParser.ArticleContext):
        pass



del ProfilesParser