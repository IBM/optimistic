import functools
from dataclasses import field, dataclass
from functools import wraps

from typing_extensions import dataclass_transform


def different(*args):
    """
    Determine if all args are different

    :param args: immutable args (can be included in a set)
    :return: True iff all args are different
    """
    return len(set(args)) == len(args)


def unique_element(s):
    """
    Return unique element of s if there is only one, otherwise return None

    :param s: sequence of elements
    :return: unique element if exists, otherwise None
    """
    try:
        element = next(s)
    except StopIteration:
        return None
    try:
        next(s)
    except StopIteration:
        return element
    return None


def count(seq):
    return sum(1 for e in seq)


def builtin(func):
    """
    Decorator to indicate that this is a builtin function or method, whose code shouldn't be analyzed.
    """
    setattr(func, '**builtin**', True)
    return func


def memoize_method(func):
    """
    Decorator to memoize previous results of func
    """
    memory = {}

    @wraps(func)
    def memoized(*args, **kwargs):
        if (result := memory.get((id(args[0]), *args[1:], imkw := tuple(sorted(kwargs.items()))))) is not None:
            return result
        result = func(*args, **kwargs)
        memory[(id(args[0]), *args[1:], imkw)] = result
        return result

    return memoized


def _add_property_proxy(cls, attr_name, proxied_attr):
    def get_attr(self):
        return getattr(self, proxied_attr)

    def set_attr(self, value):
        setattr(self, proxied_attr, value)

    prop = property(get_attr, set_attr)
    setattr(cls, attr_name, prop)


@builtin
def rename_attr(**kargs):
    """
    The decorator enables us to add a property descriptor that adds access to the original word using new key mask
    It does that by adding attributes to the class as data descriptors
    that in turn call the instance __dict__ to get the instance attributes values
    """

    def deco(cls):
        for key, word in kargs.items():
            if word in vars(cls) or (cls.__annotations__ and word in cls.__annotations__.keys()):
                _add_property_proxy(cls, key, word)
            else:
                raise AttributeError(f'Attribute [{word}] is missing in class [{cls.__name__}]')
        return cls

    return deco


@builtin
def metadata(primary_key=False, domain=False, solution=False):
    return field(metadata=dict(primary_key=primary_key, domain=domain, solution=solution))


@builtin
def constraint(method):
    """
    Decorator to indicate that this method is a constraint in an optimization problem
    """
    setattr(method, '**constraint**', True)
    return method


@builtin
def minimize(method=None, *, weight=1):
    """
    Decorator to indicate that this method is an objective to be minimized in an optimization problem

    :param method: method returning objective to be minimized
    :param weight: weight of this objective
    """
    if method is None:
        return functools.partial(minimize, weight=weight)
    setattr(method, '**objective**', weight)
    return method


@builtin
def maximize(method=None, *, weight=1):
    """
    Decorator to indicate that this method is an objective to be maximized in an optimization problem

    :param method: method returning objective to be maximized
    :param weight: weight of this objective
    """
    if method is None:
        return functools.partial(maximize, weight=weight)
    setattr(method, '**objective**', -weight)
    return method


@dataclass_transform()
def record(cls_decl):
    return dataclass(frozen=True)(cls_decl)


def solution_variable():
    return metadata(solution=True)
