import operator
from typing import Set, Tuple, Any
from dataclasses import dataclass
from optimistic_client.meta.utils import constraint, memoize_method, builtin, rename_attr


# def unique_assignment_attribute(resource='resource', activity='activity'):
#     return rename_attr(resource=resource, activity=activity)

def assignment(resource='resource', activity='activity', as_data_class=False):
    """
    Use the decorator to add access to instance attributes, using the assignment semantics Resource & Activity
    This will enable the unique assignment algorithms to access the specific solution and do the necessary computations
    The decorator, may also convert the class to be an IMMUTABLE dataclass
    """

    def deco(cls):
        _cls = dataclass(cls, unsafe_hash=True, frozen=True) if as_data_class else cls
        return rename_attr(resource=resource, activity=activity)(_cls)

    return deco


@builtin
def has_unique_assignment(obj, wrt=('resource',)) -> bool:
    """"
    Constraint: the solution has unique assignments

    :param wrt: attributes of `Assignment` for which the activity should be unique
    """
    args = operator.attrgetter(*wrt)
    return all(args(a1) != args(a2) or a1.activity == a2.activity
               for a1 in getattr(obj, 'solution')
               for a2 in getattr(obj, 'solution'))


@builtin
def non_unique_assignment(obj, wrt=('resource',)) -> Set[Tuple[Any, ...]]:
    args = operator.attrgetter(*wrt)
    # return tuple((a1, a2)
    #              for a1 in getattr(obj, 'solution')
    #              for a2 in getattr(obj, 'solution')
    #              if not (args(a1) != args(a2) or a1.activity == a2.activity))
    return set(tuple(sorted(sorted((a1, a2), key=lambda sol: sol.resource), key=lambda sol: sol.activity))
               for a1 in getattr(obj, 'solution')
               for a2 in getattr(obj, 'solution')
               if not (args(a1) != args(a2) or a1.activity == a2.activity))


@builtin
def unique_assignment(objs, resource: Any, *args, wrt: Tuple = tuple()) -> Any:
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
    return next(a.activity for a in getattr(objs, 'solution')
                if a.resource == resource and get_wrt(a) == args)


class UniqueAssignment:
    """
    An assignment in which each resource has only one related activity
    """

    @constraint
    @memoize_method
    def has_unique_assignment(self, wrt=('resource',)) -> bool:
        return has_unique_assignment(self, wrt)

    @memoize_method
    @builtin
    def unique_assignment(self, resource: Any, *args, wrt: Tuple = tuple()) -> Any:
        return unique_assignment(self, resource, wrt=wrt) if len(args) == 0 \
            else unique_assignment(self, resource, *args, wrt)

    @memoize_method
    @builtin
    def non_unique_assignment(self, wrt=('resource',)):
        return non_unique_assignment(self, wrt)
