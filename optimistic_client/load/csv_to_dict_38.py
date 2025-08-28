#
# The following implementation is to be used with python 3.8+
#
# We want to be able to load from a csv file, containing header row,
# a dictionary whose keys and values are typed and can be used by static
# type checker like `mypy`, and can be used by optimistic_client to check use the input data
# for it's schema
#
# Here we use `typing.TypedDict` to allow us declare a dictionary type that expects all of its
# instances to have a certain set of keys, where each key is associated with a value of a consistent type.
#
# Alos See:https://stackoverflow.com/questions/11665628/read-data-from-csv-file-and-transform-from-string-to-correct-data-type-includin
#
#
# Usage Example:
#  See ..\tests\test_csv_to_dict38.py

from typing import Any


def typeit(field: type, value: str) -> Any:
    """Apply the correct type into the dictionary value"""
    if field is bool:
        return value.strip().upper() == "TRUE"
    if field is str:
        return value.strip()
    return field(value)


def transform(dict_, typed_dict) -> dict:
    """ Convert values in given dictionary to corresponding types in TypedDict . """
    fields = typed_dict.__annotations__
    return {name: typeit(fields[name], value) for name, value in dict_.items()}
