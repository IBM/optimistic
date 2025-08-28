import antlr4

from ProfilesLexer import ProfilesLexer
from ProfilesParser import ProfilesParser
from ProfilesVisitor import ProfilesVisitor
from math_rep.constants import EXISTS_SYMBOL, FOR_ALL_SYMBOL, AND_SYMBOL, IMPLIES_SYMBOL, OR_SYMBOL, GE_SYMBOL, \
    LE_SYMBOL, NOT_EQUALS_SYMBOL
from eco_profiles.profiles_expr import Period, Time
from math_rep.expr import Atom, Attribute, MathVariable, Quantity, FormalContent, Aggregate, Between, GeneralSet, \
    StringTerm, SetMembership, Negation, Comparison, LogicalOperator, PredicateAppl, Quantifier, Predicate, \
    LogicalCombination, FunctionApplication, TEMPORAL_MEETS, TEMPORAL_MEETS_INV, TEMPORAL_BEFORE, \
    TEMPORAL_AFTER, TemporalOrder, TEMPORAL_OVERLAPS, TEMPORAL_DISJOINT, ComprehensionContainer, ComprehensionCondition, \
    TRUE_AS_QUANTITY
from math_rep.expression_types import MClassType, M_UNKNOWN, QualifiedName
from eco_profiles.profile_frame_constants import PROFILE_FRAME_NAME, profile_name

AGGREGATE_OPERATORS = {'sum': '+', 'product': '*'}

# Map LogicalOp1 to symbol
# Input is (smaller, greater, or-equals, negate)
# First two can't both be true; or-equals can be true only if smaller or greater
LOGICAL_OPS = {(False, False, False, False): '=',
               (False, False, False, True): NOT_EQUALS_SYMBOL,
               (False, True, False, False): '>',
               (False, True, False, True): LE_SYMBOL,
               (False, True, True, False): GE_SYMBOL,
               (False, True, True, True): '<',
               (True, False, False, False): '<',
               (True, False, False, True): GE_SYMBOL,
               (True, False, True, False): LE_SYMBOL,
               (True, False, True, True): '>'}

TYPES = {k: MClassType(profile_name(v)) for k, v in
         dict(leg='Leg', legs='Leg', duty='Duty', duties='Duty', pairing='Pairing', pairings='Pairing').items()}


def normalize_type(type_name):
    return TYPES.get(type_name.lower()) or M_UNKNOWN


class ParseError(ValueError):
    pass


class TempResult(FormalContent):
    def __init__(self, content):
        super().__init__()
        self.content = content

    def describe(self, parent_binding=None):
        return '[' + ','.join([c.describe() for c in self.content]) + ']'


class ProfileExtractor(ProfilesVisitor):
    def __init__(self):
        self.var_defs = []

    def push_var_def(self, var, vtype):
        loc = len(self.var_defs)
        self.var_defs.append((var, vtype))
        return loc

    def pop_var_defs(self, loc):
        del self.var_defs[loc:]

    def find_var_type(self, var):
        try:
            return next(vtype for v, vtype in reversed(self.var_defs) if v == var)
        except StopIteration:
            return M_UNKNOWN

    # following two methods used for testing
    def defaultResult(self):
        return TempResult([])

    def aggregateResult(self, aggregate, next_result):
        return TempResult(aggregate.content + [next_result])

    def visitNoun_phrase(self, ctx: ProfilesParser.Noun_phraseContext):
        article = ctx.article()
        result = Atom(M_UNKNOWN, [w.getText() for w in ctx.WORD()], article.getText() if article else None,
                      lexical_path=(PROFILE_FRAME_NAME,))
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitPhraseExpr(self, ctx: ProfilesParser.AtomicExprContext):
        noun_phrase = ctx.noun_phrase()
        result = self.visit(ctx.noun_phrase())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitAtomicExpr(self, ctx: ProfilesParser.AtomicExprContext):
        return self.visit(ctx.atomic_expr())

    def visitSingleAttribute(self, ctx: ProfilesParser.SingleAttributeContext):
        attr = self.visit(ctx.noun_phrase())
        container = self.visit(ctx.expr())
        result = Attribute(attr, container)
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitMultipleAttributes(self, ctx: ProfilesParser.MultipleAttributesContext):
        # FIXME: op not used???  Is this ever invoked (Text 5)?
        container = self.visit(ctx.expr())
        if ctx.cnp:
            op = AND_SYMBOL
            attrs = self.visit(ctx.cnp)
        else:
            op = OR_SYMBOL
            attrs = self.visit(ctx.dnp)
        result = Attribute(attrs, container)
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitVariableExpr(self, ctx: ProfilesParser.VariableExprContext):
        var = ctx.VARIABLE().getText()
        result = MathVariable(profile_name(var, self.find_var_type(var)))
        ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop)
        return result

    def visitProfile(self, ctx: ProfilesParser.ProfileContext):
        result = self.visit(ctx.condition())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitTemporalOp(self, ctx: ProfilesParser.TemporalOpContext):
        result = TemporalOrder(self.visit(ctx.expr(0)), self.visit(ctx.temporal_operator()), self.visit(ctx.expr(1)),
                               self.visit(ctx.expr(2)))
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitDisjunction(self, ctx: ProfilesParser.DisjunctionContext):
        result = LogicalOperator(OR_SYMBOL, [self.visit(c) for c in ctx.condition()])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitNegation(self, ctx: ProfilesParser.NegationContext):
        result = Negation(self.visit(ctx.condition()))
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitExistentialCond(self, ctx: ProfilesParser.ExistentialCondContext):
        result = self.visit(ctx.existential())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitIn(self, ctx: ProfilesParser.InContext):
        expr = self.visit(ctx.expr())
        negated = ctx.negate
        container = self.visit(ctx.general_set())
        in_expr = SetMembership(expr, container)
        # print('!!! In (no neg):', ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        text = ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop)
        if negated:
            result = Negation(in_expr)
            result.set_text(f'NOT {text}')
        else:
            result = in_expr
            result.set_text(text)
        return result

    def visitUniversalCond(self, ctx: ProfilesParser.UniversalCondContext):
        return self.visit(ctx.universal())

    def visitBetween(self, ctx: ProfilesParser.BetweenContext):
        value = self.visit(ctx.value)
        lb = self.visit(ctx.lower_bound)
        ub = self.visit(ctx.upper_bound)
        result = Between(value, lb, ub)
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitComparison(self, ctx: ProfilesParser.ComparisonContext):
        lhs = self.visit(ctx.expr(0))
        rhs = self.visit(ctx.expr(1))
        op = self.visit(ctx.comparison_operator())
        result = Comparison(lhs, op, rhs)
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitBindingExistentialWithDiff(self, ctx: ProfilesParser.BindingExistentialWithDiffContext):
        result = self.visit(ctx.binding_existential_with_diff())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitBinding_existential_with_diff(self, ctx: ProfilesParser.Binding_existential_with_diffContext):
        type_name = normalize_type(ctx.type_name().getText())
        vars = [profile_name(v.text, normalize_type(type_name)) for v in ctx.mvars]
        vars.reverse()
        compr = None
        container = self.visit(ctx.expr())
        # TODO: support let expressions to avoid duplication of container for multiple variables
        for var in vars:
            compr = ComprehensionContainer([var], container, compr)
        diff = ctx.diff is not None
        conditions = [PredicateAppl(Atom(normalize_type(type_name), ['*different*'],
                                         lexical_path=(PROFILE_FRAME_NAME,)),
                                    [MathVariable(v) for v in vars])] if diff else []
        if ctx.such_that():
            conditions.extend([self.visit(ctx.such_that())])
        if len(conditions) > 1:
            condition = LogicalOperator(AND_SYMBOL, conditions)
        elif conditions:
            condition = conditions[0]
        else:
            condition = TRUE_AS_QUANTITY
        result = Quantifier(EXISTS_SYMBOL, condition, container, unique=False)
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitBindingExistentialWithUnique(self, ctx: ProfilesParser.BindingExistentialWithUniqueContext):
        result = self.visit(ctx.binding_existential_with_unique())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitBinding_existential_with_unique(self, ctx: ProfilesParser.Binding_existential_with_uniqueContext):
        bindings = [self.visit(b) for b in ctx.binding_existential_with_unique1()]
        bindings.reverse()
        formula = self.visit(ctx.such_that())
        for b in bindings:
            formula = b.with_formula(formula)
        formula.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return formula

    def visitBinding_existential_with_unique1(self, ctx: ProfilesParser.Binding_existential_with_unique1Context):
        type_name = normalize_type(ctx.type_name().getText())
        var = ctx.VARIABLE().getText()
        container = ComprehensionContainer([profile_name(var, type_name)], self.visit(ctx.expr()))
        unique = bool(ctx.unique)
        # Note: this is only part of the expression, result can't be interpreted on its own!
        result = Quantifier(EXISTS_SYMBOL, TRUE_AS_QUANTITY, container, unique=unique)
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitBindingExistentialUnique(self, ctx: ProfilesParser.BindingExistentialUniqueContext):
        result = self.visit(ctx.binding_existential_unique())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitBinding_existential_unique(self, ctx: ProfilesParser.Binding_existential_uniqueContext):
        type_name = normalize_type(ctx.type_name().getText())
        var = ctx.VARIABLE().getText()
        container = ComprehensionContainer([profile_name(var, type_name)], self.visit(ctx.expr()))
        result = Quantifier(EXISTS_SYMBOL, TRUE_AS_QUANTITY, container, unique=True)
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitConjunction(self, ctx: ProfilesParser.ConjunctionContext):
        result = LogicalOperator(AND_SYMBOL, [self.visit(c) for c in ctx.condition()])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitIsConstant(self, ctx: ProfilesParser.IsConstantContext):
        result = Comparison(self.visit(ctx.expr()), NOT_EQUALS_SYMBOL if ctx.negate else '=',
                            self.visit(ctx.atomic_expr()))
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitPredicateAppl(self, ctx: ProfilesParser.PredicateApplContext):
        result = PredicateAppl(self.visit(ctx.predicate()), [self.visit(ctx.expr(0)), self.visit(ctx.expr(1))])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitUnaryPredAppl(self, ctx: ProfilesParser.UnaryPredApplContext):
        pospred = pred = self.visit(ctx.unary_predicate())
        if pred.negated:
            pospred = pred.to_positive()
        appl = PredicateAppl(pospred, [self.visit(ctx.expr())])
        if pred.negated:
            appl = Negation(appl)
        appl.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return appl

    def visitUnary_predicate(self, ctx: ProfilesParser.Unary_predicateContext):
        result = Predicate.from_atom(self.visit(ctx.phrase()), negated=ctx.negate is not None)
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitParenCond(self, ctx: ProfilesParser.ParenCondContext):
        result = self.visit(ctx.condition())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitAtomicPred(self, ctx: ProfilesParser.AtomicPredContext):
        atom = self.visit(ctx.phrase())
        result = Predicate(atom.words, article=atom.article, lexical_path=(PROFILE_FRAME_NAME,))
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitConjunctivePred(self, ctx: ProfilesParser.ConjunctivePredContext):
        result = LogicalCombination(AND_SYMBOL, [self.visit(p) for p in ctx.phrase()])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitDisjunctivePred(self, ctx: ProfilesParser.DisjunctivePredContext):
        result = LogicalCombination(OR_SYMBOL, [self.visit(p) for p in ctx.phrase()])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitFunctionApp(self, ctx: ProfilesParser.FunctionAppContext):
        func = ctx.function_name().op
        args = [self.visit(a) for a in ctx.expr()]
        result = FunctionApplication(profile_name(func.text), args)
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitPercentOf(self, ctx: ProfilesParser.PercentOfContext):
        result = FunctionApplication(profile_name('%*'),
                                     [Quantity(int(ctx.PERCENT().getText()[:-1]), '%'), self.visit(ctx.expr())])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitExistential(self, ctx: ProfilesParser.ExistentialContext):
        diff = ctx.diff is not None
        type_name = normalize_type(ctx.type_name().getText())
        vars = [v.getText() for v in ctx.VARIABLE()]
        container = self.visit(ctx.expr())
        conditions = [PredicateAppl(Atom(type_name, ['*different*'], lexical_path=(PROFILE_FRAME_NAME,)),
                                    [MathVariable(profile_name(v, type_name)) for v in vars])] if diff else []
        if ctx.such_that():
            conditions.extend([self.visit(ctx.such_that())])
        if len(conditions) > 1:
            formula = LogicalOperator(AND_SYMBOL, conditions)
        elif conditions:
            formula = conditions[0]
        else:
            formula = TRUE_AS_QUANTITY
        vars.reverse()
        for var in vars:
            formula = Quantifier(EXISTS_SYMBOL, formula,
                                 ComprehensionContainer([profile_name(var, type_name)], container))
        formula.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return formula

    def visitForAll(self, ctx: ProfilesParser.ForAllContext):
        diff = ctx.diff is not None
        type_name = normalize_type(ctx.type_name().getText()) if ctx.type_name() else M_UNKNOWN
        vars = [profile_name(v.getText(), type_name) for v in ctx.VARIABLE()]
        container = self.visit(ctx.expr())
        pre_conditions = [PredicateAppl(Atom(normalize_type(type_name), ['*different*'],
                                             lexical_path=(PROFILE_FRAME_NAME,)),
                                        [MathVariable(v) for v in vars])] if diff else []
        formula = self.visit(ctx.condition())
        if diff:
            pre_conditions.insert(0, PredicateAppl(Atom(normalize_type(type_name), ['*different*'],
                                                        lexical_path=(PROFILE_FRAME_NAME,)),
                                                   [MathVariable(profile_name(v, normalize_type(type_name))) for v in
                                                    vars]))
        if len(pre_conditions) > 1:
            pre_conditions = LogicalOperator(AND_SYMBOL, pre_conditions)
        elif pre_conditions:
            pre_conditions = pre_conditions[0]
        if pre_conditions:
            formula = LogicalOperator(IMPLIES_SYMBOL, [pre_conditions, formula])
        vars.reverse()
        for var in vars:
            formula = Quantifier(FOR_ALL_SYMBOL, formula,
                                 ComprehensionContainer([var], container))
        formula.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return formula

    def visitEvery(self, ctx: ProfilesParser.EveryContext):
        type_name = normalize_type(ctx.type_name().getText())
        var = ctx.VARIABLE().getText()
        container = self.visit(ctx.of_expr) if ctx.of_expr else self.visit(ctx.in_set)
        pred = self.visit(ctx.predicate())
        pred_appl = PredicateAppl(pred, [MathVariable(profile_name(var, type_name))])
        condition = self.visit(ctx.condition())
        if condition:
            formula = LogicalOperator(AND_SYMBOL, [pred_appl, condition])
        else:
            formula = pred_appl
        result = Quantifier(FOR_ALL_SYMBOL, formula, ComprehensionContainer([profile_name(var, type_name)], container))
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitAggregate(self, ctx: ProfilesParser.AggregateContext):
        operator = AGGREGATE_OPERATORS.get(ctx.op.text.lower())
        if not operator:
            raise ParseError(f'Improper aggregation type: {ctx.op().getText()}')
        collection = self.visit(ctx.collection)
        type_name = normalize_type(ctx.type_name().getText())
        var = ctx.VARIABLE().getText()
        pos = self.push_var_def(var, type_name)
        term = self.visit(ctx.term)
        if stn := ctx.such_that():
            st = ComprehensionCondition(self.visit(stn))
        else:
            st = None
        self.pop_var_defs(pos)
        result = Aggregate(operator, term, ComprehensionContainer([profile_name(var, type_name)], collection, rest=st))
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitSuch_that(self, ctx: ProfilesParser.Such_thatContext):
        result = self.visit(ctx.condition())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    # def visitTo_be(self, ctx: ProfilesParser.To_beContext):
    #     return super().visitTo_be(ctx)

    def visitComparisonOp1(self, ctx: ProfilesParser.ComparisonOp1Context):
        smaller = ctx.sm is not None
        greater = ctx.gr is not None
        or_eq = ctx.or_eq is not None
        negate = ctx.negate is not None
        result = LOGICAL_OPS[(smaller, greater, or_eq, negate)]
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitComparisonOp2(self, ctx: ProfilesParser.ComparisonOp2Context):
        smaller = ctx.sm is not None
        return LE_SYMBOL if smaller else GE_SYMBOL

    # def visitComparisonOp3(self, ctx: ProfilesParser.ComparisonOp3Context):
    #     return self.visit(ctx.eq_not_eq())

    def visitComparisonOp4(self, ctx: ProfilesParser.ComparisonOp4Context):
        return NOT_EQUALS_SYMBOL

    def visitEq_not_eq(self, ctx: ProfilesParser.Eq_not_eqContext):
        negate = ctx.negate is not None
        return NOT_EQUALS_SYMBOL if negate else '='

    def visitTemporalOrder(self, ctx: ProfilesParser.TemporalOrderContext):
        if ctx.immed is not None:
            result = TEMPORAL_MEETS if ctx.order.text == 'precedes' else TEMPORAL_MEETS_INV
        else:
            result = TEMPORAL_BEFORE if ctx.order.text == 'precedes' else TEMPORAL_AFTER
        return QualifiedName(result, lexical_path=(PROFILE_FRAME_NAME,))

    def visitTemporalOverlap(self, ctx: ProfilesParser.TemporalOverlapContext):
        return QualifiedName(TEMPORAL_OVERLAPS, lexical_path=(PROFILE_FRAME_NAME,))

    def visitTemporalDisjoint(self, ctx: ProfilesParser.TemporalDisjointContext):
        return QualifiedName(TEMPORAL_DISJOINT, lexical_path=(PROFILE_FRAME_NAME,))

    # def visitGreater(self, ctx: ProfilesParser.GreaterContext):
    #     return super().visitGreater(ctx)

    # def visitSmaller(self, ctx: ProfilesParser.SmallerContext):
    #     return super().visitSmaller(ctx)

    def visitQuantity(self, ctx: ProfilesParser.QuantityContext):
        num = ctx.NUMBER().getText()
        try:
            value = int(num)
        except ValueError:
            value = float(num)
        result = Quantity(value)
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitGeneral_set(self, ctx: ProfilesParser.General_setContext):
        result = GeneralSet([self.visit(e) for e in ctx.expr()])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitConjunction_of_np(self, ctx: ProfilesParser.Conjunction_of_npContext):
        result = LogicalCombination(AND_SYMBOL, [self.visit(a) for a in ctx.noun_phrase()])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitDisjunction_of_np(self, ctx: ProfilesParser.Disjunction_of_npContext):
        result = LogicalCombination(OR_SYMBOL, [self.visit(a) for a in ctx.noun_phrase()])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitStringExpr(self, ctx: ProfilesParser.StringExprContext):
        result = StringTerm(ctx.STRING().getText()[1:-1])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitFunctionExpr(self, ctx: ProfilesParser.FunctionExprContext):
        result = self.visit(ctx.function())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitTimeExpr(self, ctx: ProfilesParser.TimeExprContext):
        result = Time(ctx.TIME().getText())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitPeriodExpr(self, ctx: ProfilesParser.PeriodExprContext):
        result = self.visit(ctx.period())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitConjunctionExpr(self, ctx: ProfilesParser.ConjunctionExprContext):
        result = LogicalCombination(AND_SYMBOL, [self.visit(e) for e in ctx.expr()])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitDisjunctionExpr(self, ctx: ProfilesParser.DisjunctionExprContext):
        result = LogicalCombination(OR_SYMBOL, [self.visit(e) for e in ctx.expr()])
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitAttributeExpr(self, ctx: ProfilesParser.AttributeExprContext):
        result = self.visit(ctx.attribute())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitQuantityExpr(self, ctx: ProfilesParser.QuantityExprContext):
        result = self.visit(ctx.quantity())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitSetExpr(self, ctx: ProfilesParser.SetExprContext):
        result = self.visit(ctx.general_set())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitAggregateExpr(self, ctx: ProfilesParser.AggregateExprContext):
        result = self.visit(ctx.aggregate())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitParenExpr(self, ctx: ProfilesParser.ParenExprContext):
        result = self.visit(ctx.expr())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitPeriod(self, ctx: ProfilesParser.PeriodContext):
        result = Period(Time(ctx.TIME(0).getText()), Time(ctx.TIME(1).getText()))
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result

    def visitPhrase(self, ctx: ProfilesParser.PhraseContext):
        np = ctx.noun_phrase()
        if np:
            result = self.visit(np)
        else:
            result = self.visit(ctx.verb_phrase())
        result.set_text(ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop))
        return result


def parse(profile):
    """
    Analyze a textual description of a profile and create the corresponding formal structures.

    :param profile: text describing a profile according to the ANTLR grammar
    :return: a Condition object describing the input
    """
    # input_stream = antlr4.InputStream(profile)
    # lexer = ProfilesLexer(input_stream)
    # stream = antlr4.CommonTokenStream(lexer)
    # parser = ProfilesParser(stream)
    # tree = parser.profile()
    tree, parser = parse_profile_string(profile)
    extractor = ProfileExtractor()
    result = extractor.visit(tree)
    return result


def parse_profile_string(profile):
    input_stream = antlr4.InputStream(profile)
    lexer = ProfilesLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = ProfilesParser(stream)
    tree = parser.profile()
    return tree, parser


def parse_file(file_path):
    with open(file_path, 'r') as test_file:
        while True:
            try:
                profile = next(test_file).strip()
                ref = next(test_file).strip()
                print(f'Text: {profile}')
            except Exception:
                break
            result = parse(profile)
            print(f'Result: {result.describe()}')


if __name__ == '__main__':
    parse_file(r'/data/test-profiles.txt')
    # parse_file(r'D:\Yishai\ws\pycharm\eco-abstractions\data\test-profile.txt')
