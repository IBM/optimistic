import operator
from abc import ABC
from dataclasses import dataclass
from typing import Set, Tuple, FrozenSet

from optimistic_client.optimization import OptimizationProblem
from optimistic_client.meta.utils import builtin, memoize_method, constraint


class ResourceType:
    pass


@dataclass(frozen=True)
class Resource:
    type: ResourceType


class Activity:
    pass


@dataclass(frozen=True)
class Assignment:
    resource: Resource
    activity: Activity


@builtin
@dataclass(frozen=True)
class UniqueAssignment:
    """
    An assignment in which each resource has only one related activity
    """
    solution: Set[Assignment]

    @constraint
    @memoize_method
    def has_unique_assignment(self, wrt=('resource',)) -> bool:
        """"
        Constraint: the solution has unique assignments

        :param wrt: attributes of `Assignment` for which the activity should be unique
        """
        args = operator.attrgetter(*wrt)
        return all(args(a1) != args(a2) or a1.activity == a2.activity
                   for a1 in self.solution
                   for a2 in self.solution)

    @memoize_method
    @builtin
    def unique_assignment(self, resource: Resource, *args, wrt: Tuple = tuple()) -> Activity:
        """
        Return the unique activity assigned to the given resource
        """
        # defend against string wrt
        if isinstance(wrt, str):
            wrt = (wrt,)
        # get_wrt = lambda obj: () if len(wrt) == 0 else tuple(operator.attrgetter(a)(obj) for a in wrt)
        get_wrt = (lambda obj: tuple()) if len(wrt) == 0 else (operator.attrgetter(*wrt) if len(wrt) > 1 else
                                                               lambda obj: (operator.attrgetter(*wrt)(obj),))
        # assert self.has_unique_assignment()
        return next(a.activity for a in self.solution
                    if a.resource == resource and get_wrt(a) == args)


@dataclass(frozen=True)
class ResourceAllocationProblem(OptimizationProblem, ABC):
    solution: Set[Assignment]

    # TODO: remove, use UniqueAssignment instead
    @memoize_method
    @builtin
    def has_unique_assignment(self, wrt=('resource',)) -> bool:
        """"
        Constraint: the solution has unique assignments

        :param wrt: attributes of `Assignment` for which the activity should be unique
        """
        args = operator.attrgetter(*wrt)
        return all(args(a1) != args(a2) or a1.activity == a2.activity
                   for a1 in self.solution
                   for a2 in self.solution)

    # TODO: remove, use UniqueAssignment instead
    @memoize_method
    @builtin
    def unique_assignment(self, resource: Resource, *args, wrt: Tuple = tuple()) -> Activity:
        """
        Return the unique activity assigned to the given resource

        Precondition: self.has_unique_assignment()
        """
        get_wrt = (lambda obj: tuple()) if len(wrt) == 0 else (operator.attrgetter(*wrt) if len(wrt) > 1 else
                                                               lambda obj: (operator.attrgetter(*wrt)(obj),))
        assert self.has_unique_assignment()
        return next(a.activity for a in self.solution
                    if a.resource == resource and get_wrt(a) == args)

        # and all(getattr(a, attr) == arg for attr, arg in zip(wrt[1:], args)))
