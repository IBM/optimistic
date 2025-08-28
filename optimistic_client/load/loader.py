import csv
from functools import partial
from dataclasses import fields

from optimistic_client.load.csv_to_dict_38 import transform
from optimistic_client.load.load_utils import is_data_class
from optimistic_client.load.knoweldge_class_generator import DataGenerator


def loadCsv(fileName, cls):
    """
    Loads CSV file into a dataclass, requires that each
    input class (`cls`) inherit from `DictRecordTransform` in package `optimistic_client.load.csv_to_dict_37`
    """
    with open(fileName, newline='') as file:
        # return tuple(cls.transform(row) for row in csv.DictReader(file))
        return tuple(map(cls.transform, csv.DictReader(file)))


def loadCsvAsTypeDict(fileName, cls):
    """
    Loads CSV file into a class that inherits from `typing.TypeDict`
    This enables us to define the type of each key/value of a dictionary.
    """
    with open(fileName, newline='') as file:
        # return tuple(cls.transform(row) for row in csv.DictReader(file))
        trans = partial(transform, typed_dict=cls)
        return tuple(map(trans, csv.DictReader(file)))


def create_problem_instance(cls,
                            input_files,
                            column_mappings=None):
    _constructor = {}
    _generator = DataGenerator()

    if is_data_class(cls):
        for field in fields(cls):
            _constructor[field.name] = _generator.load_data(cls,
                                                            field.name,
                                                            input_files.get(field.name),
                                                            column_mapping=column_mappings.get(field.name))

        print(
            f'Create Problem Instance \"{cls.__name__}\":\n Data Loader Report:\n{_generator.report() or " Data is Ok"}\n')
        _problem = cls(**_constructor)
    else:
        _problem = cls()
    return _problem
