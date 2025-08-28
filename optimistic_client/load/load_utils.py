import collections
import collections.abc
from dataclasses import is_dataclass, Field
from types import FunctionType
from typing import get_origin


def is_primitive(field_type) -> bool:
    element = _get_dataclass_field_type(field_type)
    return isinstance(element, type)


def is_unbounded_primitive(field_type) -> bool:
    element = _get_dataclass_field_type(field_type)
    return is_primitive(element) and element in (str, int, float)


def is_bounded_primitive(field_type) -> bool:
    element = _get_dataclass_field_type(field_type)
    return is_primitive(element) and element in (bool,)


def is_data_class(field_type) -> bool:
    element = _get_dataclass_field_type(field_type)
    return is_dataclass(element)


def is_not_supported_builtins(field_type):
    element = _get_dataclass_field_type(field_type)
    return element in (complex, list, tuple, range, bytes, set, frozenset, dict)


def is_user_primitive(field_type) -> bool:
    element = _get_dataclass_field_type(field_type)
    return is_primitive(element) and not is_data_class(element) \
           and element not in (str, int, float, bool) \
           and not is_not_supported_builtins(field_type)


def is_typing(field_type) -> bool:
    """
    Checks if the type is one defined from the `typing` module
    - NewType
    - _GenericAlias: Set, Mapping, TotalMapping
    - Tuple
    """
    return is_function(field_type) or get_origin(field_type)


def is_function(field_type) -> bool:
    """
    We assume that if True, the dataclass field is a `typing.NewType` , which is a function
    """
    element = _get_dataclass_field_type(field_type)
    return isinstance(element, FunctionType)


def is_tuple(field_type) -> bool:
    """
    If the dataclass field is not function or user/primitive,
    We assume that it can be any other:
        - `typing.Tuple`,
        - or any other `typing._GenericAlias` object
    """
    element = _get_dataclass_field_type(field_type)
    return get_origin(element) is tuple if not is_function(element) and not is_primitive(element) else False


def is_set(field_type) -> bool:
    """
    If the dataclass field is not function or user/primitive, or a `typing.Tuple`
    We assume that it can be any other:
        - One of `typing._GenericAlias` SET object
    """
    element = _get_dataclass_field_type(field_type)
    return get_origin(element) in \
           (set, collections.abc.Set, collections.abc.Collection, collections.abc.MutableSet, frozenset)


def is_mapping(field_type) -> bool:
    """
    If the dataclass field is not function or user/primitive, or a `typing.Tuple`
    We assume that it can be any other:
        - One of `typing._GenericAlias` Mapping object
    """
    element = _get_dataclass_field_type(field_type)
    return get_origin(element) in \
           (collections.abc.Mapping,)


def is_total_mapping(field_type) -> bool:
    element = _get_dataclass_field_type(field_type)
    return is_mapping(element) and 'TotalMapping' == element._name


def is_solution(element: Field) -> bool:
    if isinstance(element, Field):
        return True if getattr(element, 'metadata', {}).get('solution', False) else False


def _get_dataclass_field_type(is_field_type):
    if isinstance(is_field_type, Field):
        return is_field_type.type
    return is_field_type


def prepare_column_mapping(the_mapping):
    """
    Converts user define mapping into internal structure,
    where entries either in the domain or range mappings, that have multiple values
    are converted into iterator, so that successive access to the same field fetch the next value:

    examples:
        Problem Dataclass:
            Id = NewType('tz', str)
            Age = NewType('age', int)

            class ExampleProblem(OptimizationProblem):
               students_score: Mapping[Tuple[str, str, Id, Id, Age], int]

        Column Mapping:
                "students_score": {
                        "domain_mapping": {
                            "str": ["name", "family"],
                            "tz": ["id", "passport"]
                        },
                        "range_mapping": {
                            "int": "score"
                        }
                    },

    Here, we need to iterate over the first two `str` keys in the Tuple,
    and than the `Id` NewType, where each access the a different column in the file
    """
    if not the_mapping:
        return None
    rs = {}
    for key, value in the_mapping.items():
        if isinstance(value, (list, set, tuple)):
            rs[key] = {'value': iter(value),
                       'column': value}
        else:
            rs[key] = {'value': iter((value,)),
                       'column': value}
    return rs


def column_mapping(field, mapping=None):
    """
    For certain field fetches the next column mapping,
    """
    if not mapping:
        return field
    else:
        try:
            m = mapping.get(field)
            if m:
                value = next(m['value'])
                return value
        except:
            msg = f'Attribute ({field}) missing column mapping , already used {mapping.get(field, field)["column"]}'
            raise Exception(msg)

        if field in (int.__name__, str.__name__, float.__name__, bool.__name__):
            msg = f' Primitive Attribute \"{field}\" is missing column mapping'
            raise Exception(msg)

        # No mapping, use the given field
        return field


def fetch_root_column_mapping(field: Field, input_mapping):
    if not input_mapping:
        return None, None
    domain_mapping, range_mapping = None, None
    if is_function(field) or is_dataclass(field):
        domain_mapping = self._column_mappings.get(field.name, {}).get('mapping', None)
        range_mapping = None
    elif is_set(field):
        domain_mapping = self._column_mappings.get(field.name, {}).get('mapping', None)
        range_mapping = None
    elif is_mapping(field):
        domain_mapping = self._column_mappings.get(field.name, {}).get('domain_mapping', None)
        range_mapping = self._column_mappings.get(field.name, {}).get('range_mapping', None)
    elif is_tuple(field):
        # If tuple, we don't accept Tuple at the root, only inside a mapping
        pass
    elif is_primitive(field) and not is_data_class(field):
        domain_mapping = self._column_mappings.get(field.name, {}).get('mapping', None)
        range_mapping = None
    return domain_mapping, range_mapping
