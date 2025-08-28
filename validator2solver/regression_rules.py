from math_rep.constants import FOR_ALL_SYMBOL
from math_rep.expr import Quantifier, RangeExpr, Quantity, MathVariable, \
    m_and, DefinedBy, TRUE_AS_QUANTITY
from rewriting.patterns import ClassPattern, Bindings
from rewriting.rules import RewriteRule
from validator2solver.domain_analysis import DomainTable


class ForAllToConjunction(RewriteRule):
    def __init__(self, domain_table: DomainTable):
        self.domain_table = domain_table

    pattern = Quantifier[FOR_ALL_SYMBOL]

    def transform_single(self, obj: Quantifier, bindings: Bindings):
        container = obj.container
        # TODO: extend to multiple vars?
        if len(container.vars) != 1:
            return obj
        var = container.vars[0]
        domain = self.domain_table.ensure_info(MathVariable(var)).appl_info.domain
        if not isinstance(domain, RangeExpr):
            return obj
        return m_and(*[obj.formula.substitute({var: Quantity(i)})
                       for i in range(domain.start, domain.stop)])


class EliminateDefinedBy(RewriteRule):
    pattern = ClassPattern(DefinedBy)

    def transform_single(self, obj, bindings: Bindings):
        return TRUE_AS_QUANTITY
