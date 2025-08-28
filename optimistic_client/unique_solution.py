from dataclasses import dataclass

from optimistic_client.meta.utils import constraint, memoize_method, rename_attr
from optimistic_client.unique_assignment import has_unique_assignment, unique_assignment, non_unique_assignment


def unique_solution(sol='solution', as_data_class=False):
    """
    The decorator prepare full solution class,
    - Add a data descriptor for accessing the `solution` masked instance attribute
    - Add Method to check
      - has_unique_assignment()
      - unique_assignment()
      - non_unique_assignment()
    """

    def deco(cls):
        _cls = dataclass(cls, unsafe_hash=True, frozen=True) if as_data_class else cls
        setattr(_cls, has_unique_assignment.__name__, constraint(memoize_method(has_unique_assignment)))
        setattr(_cls, unique_assignment.__name__, memoize_method(unique_assignment))
        setattr(_cls, non_unique_assignment.__name__, memoize_method(non_unique_assignment))
        return rename_attr(solution=sol)(_cls)

    return deco


def solution_attribute(sol='solution', as_data_class=False):
    """
    The decorator adds data descriptor for accessing the `solution` masked instance attribute
    The decorator, may also convert the class to be an IMMUTABLE dataclass
    """

    def deco(cls):
        _cls = dataclass(cls, unsafe_hash=True, frozen=True) if as_data_class else cls
        return rename_attr(solution=sol)(_cls)

    return deco
