from dataclasses import dataclass
from typing import NewType, Set

from optimistic_client.meta.utils import metadata, constraint, count
from optimistic_client.optimization import OptimizationProblem

KT1 = NewType('KT1', str)
KT2 = NewType('KT2', str)

IT1 = NewType('IT1', int)
IT2 = NewType('IT2', int)
FT1 = NewType('FT1', float)
FT2 = NewType('FT2', float)
ST1 = NewType('ST1', str)
ST2 = NewType('ST2', str)


@dataclass
class Inputs:
    k1: KT1 = metadata(primary_key=True)
    k2: KT2 = metadata(primary_key=True)
    s1: ST1


@dataclass
class BoolRep1:
    k1: KT1 = metadata(primary_key=True)
    k2: KT2 = metadata(primary_key=True)
    out_str: ST1


@dataclass
class TestOptimizationProblem(OptimizationProblem):
    input: Set[Inputs]
    solution: Set[BoolRep1]

    def all_k1(self):
        return {inp.k1 for inp in self.input}

    def all_k2(self):
        return {inp.k2 for inp in self.input}

    @constraint
    def c_bool1(self):
        # FIXME!!!! this is translated erroneously, missing condition on set membership
        return all(count(s for s in self.solution if s.k1 == k1 and s.k2 == k2) == 2
                   for k1 in self.all_k1()
                   for k2 in self.all_k2())

    @constraint
    def c_bool2(self):
        # FIXME!!!! this is translated erroneously, missing condition on set membership
        return all(s.out_str == 'a' for s in self.solution)
