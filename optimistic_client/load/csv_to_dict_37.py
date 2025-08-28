#
# The following implementation is to be used with python 3.7+
#
# We want to be able to load from a csv file, containing header row,
# a dictionary whose keys and values are typed and can be used by static
# type checker like `mypy`, and can be used by optimistic_client to check use the input data
# for it's schema
#
# Here we use `dataclass.dataclass` to allow us to define any loaded dictionary
# using inheritance, while enabling us to query for the dictionary structure
#
# Alos See:https://stackoverflow.com/questions/11665628/read-data-from-csv-file-and-transform-from-string-to-correct-data-type-includin
#
#
# Usage Example:
#  See ..\tests\test_csv_to_dict37.py

from dataclasses import fields, Field, asdict
from typing import Type, TypeVar, Any

T = TypeVar('T', bound='DictRecordTransform')


class DictRecordTransform:
    """ Generic base class for transforming dataclasses. """
    @classmethod
    def typeit(cls: Type[T], field: Field, dict_: dict) -> Any:
        """Apply the correct type into the dictionary value"""
        if field.type is bool:
            return dict_[field.name].strip().upper() == "TRUE"
        if field.type is str:
            return field.type(dict_[field.name]).strip()
        return field.type(dict_[field.name])

    @classmethod
    def transform(cls: Type[T], dict_: dict, to_dict=False) -> dict:
        """ Convert string values in given dictionary to corresponding type. """
        # for field in fields(cls):
        #     print(f'field name [{field.name}] type [{field.type}] value [{dict_[field.name]}] ')
        the_dict = {field.name: cls.typeit(field, dict_) for field in fields(cls)}
        if to_dict:
            return the_dict
        return cls(**the_dict)

