import collections
import sys
import typing
from dataclasses import dataclass
from numbers import Real
from typing import Sequence, Set

from typing_extensions import dataclass_transform

from optimistic_client.meta.utils import memoize_method


class MTotalMapping(typing._GenericAlias, _root=True):
    def __getitem__(self, params):
        if self.__origin__ in (typing.Generic, typing.Protocol):
            # Can't subscript Generic[...] or Protocol[...].
            raise TypeError(f"Cannot subscript already-subscripted {self}")
        if not isinstance(params, tuple):
            params = (params,)
        msg = "Parameters to generic types must be types."
        params = tuple(typing._type_check(p, msg) for p in params)
        typing._check_generic(self, params)
        return typing._subs_tvars(self, self.__parameters__, params)


# FIXME: remove unused variables
# This type indicates a total function:
TotalFunction = Set
# This type indicates a partial function:
PartialFunction = Set
# This type indicates a total function as a mapping:
if sys.version_info[0] >= 3 and sys.version_info[1] >= 9:
    TotalMapping = typing._GenericAlias(collections.abc.Mapping, (typing.KT, typing.VT_co), name='TotalMapping')
elif sys.version_info[0] == 3 and sys.version_info[1] == 8:
    TotalMapping = MTotalMapping(collections.abc.Mapping, (typing.KT, typing.VT_co), name='TotalMapping')


def implies(p, q):
    return not p or q


def equals(a: Real, b: Real, epsilon: float = 1e-14):
    return abs(a - b) <= epsilon


@dataclass_transform()
class OptimizationProblem:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for name in dir(cls):
            if not name.startswith('__'):
                m = getattr(cls, name)
                if callable(m) and not hasattr(m, '**constraint**') and not hasattr(m, '**objective**'):
                    setattr(cls, name, memoize_method(m))
        dataclass(frozen=True)(
            cls)  # modifies cls, see https://docs.python.org/3/library/dataclasses.html#module-contents

    def check_constraints(self, check_only: Sequence[str] = None) -> Sequence[str]:
        """
        Call all methods marked with `@constraint`, return list of failures
        :return: sequence of names of methods that didn't return True
        """
        return [c for c in dir(self)
                if callable(m := getattr(self, c)) and getattr(m, '**constraint**', False)
                and (check_only is None or c in check_only)
                and not m()]

    def compute_objective(self, include_only: Sequence[str] = None) -> float:
        return sum(m() * w
                   for c in dir(self)
                   if callable(m := getattr(self, c))
                   and (include_only is None or c in include_only)
                   and (w := getattr(m, '**objective**', False)))
