import collections
import collections.abc
import csv
import json
import math
import numbers
from dataclasses import fields, is_dataclass
from functools import partial
from functools import reduce
from types import FunctionType
from typing import NewType, get_origin

from optimistic_client.load.load_utils import prepare_column_mapping, column_mapping


def read_json(file_name):
    with open(file_name) as input_file:
        data = json.load(input_file)
        # print(data)
        return data


def typeit(val):
    if isinstance(val, str):
        v = val.strip()
        if v.startswith('"') and v.endswith('"'):
            return f'{v}'
        return f'"{v}"'
    if isinstance(val, numbers.Number):
        return f'{val}'
    return f'{val}'


def typeit_csv_to_opl(val, field):
    """Apply the correct type into the dictionary value"""
    if field.type is bool:
        return val

    if hasattr(field.type, '__supertype__') and field.type.__supertype__ == str:
        v = val.strip()
        if v.startswith('"') and v.endswith('"'):
            return f'{v}'
        return f'"{v}"'

    if hasattr(field.type, '__supertype__') and field.type.__supertype__ == int:
        v = val.strip().strip('"')
        return int(v)

    if hasattr(field.type, '__supertype__') and field.type.__supertype__ == float:
        v = val.strip().strip('"')
        return float(v)

    if field.type is str:
        v = val.strip()
        if v.startswith('"') and v.endswith('"'):
            return f'{v}'
        return f'"{v}"'
    return field.type(val)


def is_number(n):
    is_anumber = True
    try:
        num = float(n)
        is_anumber = not math.isnan(num)
    except ValueError:
        is_anumber = False
    return is_anumber


def typeit_csv_to_obj(val, field):
    return typeit_new_type_or_primitive_to_obj(val, field.type)
    # """Apply the correct type into the dictionary value"""
    # if field.type is bool:
    #     the_val = val.strip()
    #     if is_number(the_val):
    #         return int(the_val) != 0
    #     else:
    #         return True if the_val.lower() == 'true' else False
    #
    # if hasattr(field.type, '__supertype__') and field.type.__supertype__ == str:
    #     return field.type(val).strip().strip('"')
    #
    # if hasattr(field.type, '__supertype__') and field.type.__supertype__ == int:
    #     v = val.strip().strip('"')
    #     return int(v)
    #
    # if hasattr(field.type, '__supertype__') and field.type.__supertype__ == float:
    #     v = val.strip().strip('"')
    #     return float(v)
    #
    # if field.type is str:
    #     return field.type(val).strip().strip('"')
    #
    # return field.type(val)


def typeit_new_type_or_primitive_to_obj(val, field_type):
    _field_type = field_type
    #
    #  Handles typing.NewType
    #
    if hasattr(field_type, '__supertype__'):
        while not isinstance(_field_type.__supertype__, type):
            _field_type = _field_type.__supertype__

    if hasattr(_field_type, '__supertype__') and _field_type.__supertype__ == str:
        _field_type = str

    if hasattr(_field_type, '__supertype__') and _field_type.__supertype__ == int:
        _field_type = int

    if hasattr(_field_type, '__supertype__') and _field_type.__supertype__ == float:
        _field_type = float

    if hasattr(_field_type, '__supertype__') and _field_type.__supertype__ == bool:
        _field_type = bool

    #
    #  Handles primitives
    #
    if _field_type is bool:
        the_val = val.strip().strip('"')
        if is_number(the_val):
            return int(the_val) != 0
        else:
            return True if the_val.lower() == 'true' else False

    if _field_type is str:
        return _field_type(val).strip().strip('"')

    return _field_type(val)


class Verify:
    def __init__(self, cls, attr):
        self._cls = cls
        self._attr = attr
        self._keys = None
        self._unique = {}
        self._duplicate = False
        self._single_column_fix = {}

    def check_unique(self, keys, index):
        t = tuple(keys)
        exists = self._unique.get(t)
        if exists is None:
            self._unique[t] = [index + 2]
        else:
            exists.append(index + 2)
            self._duplicate = True

    def single_csv_column_fix(self, requested_column, replaced_column):
        t = (requested_column, replaced_column)
        exists = self._single_column_fix.get(t)
        if exists is None:
            self._single_column_fix[t] = 1
        else:
            self._single_column_fix[t] = exists + 1

    def report(self):
        msg = ''
        name = self._cls._name if hasattr(self._cls, "_name") else self._attr

        if len(list(self._single_column_fix.keys())) == 0 and not self._duplicate:
            return msg

        if self._duplicate:
            msg += f'Field \"{self._attr}\" of type {name}'
            if self._keys:
                msg += f'\nkeys  = ({", ".join(self._keys)})'

            prefix = 'value' if name == 'Set' else 'domain'

            msg += f'\n' + "\n".join(
                f'{prefix} = {key[0] if len(key) == 1 else key}, records {",".join(str(r) for r in value)} are duplicates'
                for key, value in self._unique.items() if len(value) > 1) + "\n"

        if len(list(self._single_column_fix.keys())) > 0:
            msg += f'Field \"{self._attr}\"\n'
            msg += f'Single column CSV file with header not matching mapping still used'
            msg += f'\n' + "\n".join(
                f'Requested Mapping ({key[0]}) replaced with CSV column ({key[1]}) values {value} times'
                for key, value in self._single_column_fix.items()) + "\n"

        return msg


class DataGenerator:
    def __init__(self):
        self._verifiers = []

    def _verifier(self, cls, attr):
        verify = Verify(cls, attr)
        self._verifiers.append(verify)
        return verify

    def report(self):
        msg = '\n'.join(verify.report() for verify in self._verifiers if verify._duplicate or verify._single_column_fix)
        return msg

    def create_objects(self, cls, file_name, key_mapping=None, verify=None):
        if verify:
            the_keys = (field.name for field in fields(cls))
            verify._keys = the_keys

        with file_name.open(mode='r') as csv_file:
            header = [h.strip() for h in csv_file.readline().split(',')]
            trans = partial(self._transform, cls=cls, key_mapping=key_mapping, verify=verify)
            return tuple(map(trans, enumerate(csv.DictReader(csv_file, fieldnames=header))))

    def _transform(self, dict_, cls, key_mapping=None, verify=None):
        domain_mapping = self._prepare_mapping(key_mapping)
        the_dict = {field.name: typeit_csv_to_obj(dict_[1][self._column_mapping(field.name, domain_mapping)], field)
                    for field in fields(cls)}
        rs = cls(**the_dict)
        if verify:
            verify.check_unique([item for key, item in the_dict.items()], dict_[0])
        return rs

    def load_new_type_data(self, key: FunctionType, file_name, domain_mapping, verify=None):
        the_keys = (key,)
        return self._create_domain_key_mapping(the_keys, file_name, domain_mapping, verify)

    def load_data(self, cls, attr, file_name, column_mapping=None, strict=True):
        set_mapping = column_mapping.get('mapping', {}) if column_mapping else None
        key_mapping = column_mapping.get('domain_mapping', {}) if column_mapping else None
        value_mapping = column_mapping.get('range_mapping', {}) if column_mapping else None

        if cls.__annotations__ and \
                cls.__annotations__[attr] and \
                get_origin(cls.__annotations__[attr]):
            is_set = get_origin(cls.__annotations__[attr]) in \
                     (set, collections.abc.Set, collections.abc.Collection, collections.abc.MutableSet, frozenset)
            is_mapping = get_origin(cls.__annotations__[attr]) in \
                         (collections.abc.Mapping,)
            # is_total_mapping = cls.__annotations__[attr]._special is False \
            #                    and cls.__annotations__[attr]._name == 'TotalMapping'
            is_total_mapping = cls.__annotations__[attr]._name == 'TotalMapping'

            # is_solution = True if cls.__dataclass_fields__[attr].metadata \
            #                       and cls.__dataclass_fields__[attr].metadata.get('solution', False) else False
            verify = self._verifier(cls.__annotations__[attr], attr)

            if is_set:
                domain_keys = cls.__annotations__[attr].__args__[0]
                key_is_primitive, key_is_data_class, key_is_function, key_is_tuple = self._analyse_mapping(domain_keys)

                if key_is_tuple:
                    the_keys = domain_keys.__args__
                    set_objects = self._create_domain_key_mapping(the_keys, file_name, set_mapping, verify)
                elif key_is_function:
                    the_keys = (domain_keys,)
                    set_objects = self._create_domain_key_mapping(the_keys, file_name, set_mapping, verify)
                elif key_is_primitive and not key_is_data_class:
                    the_keys = (NewType(domain_keys.__name__, domain_keys),)
                    set_objects = self._create_domain_key_mapping(the_keys, file_name, set_mapping, verify)
                elif key_is_data_class:
                    set_objects = self.create_objects(domain_keys, file_name, set_mapping, verify)
                return set(set_objects)
            elif is_mapping:
                domain_keys = cls.__annotations__[attr].__args__[0]
                range_values = cls.__annotations__[attr].__args__[1]

                # Determine key characteristics
                key_is_primitive, key_is_data_class, key_is_function, key_is_tuple = self._analyse_mapping(domain_keys)
                # if key_is_data_class:
                #     raise Exception('Key as Dataclass  is not supported')

                # Determine value characteristics
                val_is_primitive, val_is_data_class, val_is_function, val_is_tuple = self._analyse_mapping(range_values)

                if key_is_tuple:
                    the_keys = domain_keys.__args__
                elif key_is_function:
                    the_keys = (domain_keys,)
                elif key_is_primitive and not key_is_data_class:
                    # the_keys = (NewType(self._column_mapping(domain_keys.__name__), domain_keys),)
                    the_keys = (NewType(domain_keys.__name__, domain_keys),)
                elif key_is_data_class:
                    the_keys = domain_keys

                if val_is_data_class:
                    if key_is_data_class:
                        total_mapping = self._create_domain_dataclass_to_range_dataclass(the_keys,
                                                                                         range_values,
                                                                                         file_name,
                                                                                         key_mapping,
                                                                                         value_mapping,
                                                                                         verify)
                    else:
                        total_mapping = self._create_total_domain_key_mapping_to_range_dataclass(the_keys,
                                                                                                 range_values,
                                                                                                 file_name,
                                                                                                 key_mapping,
                                                                                                 value_mapping,
                                                                                                 verify)
                elif val_is_function:
                    the_range = (range_values,)
                    if key_is_data_class:
                        total_mapping = self._create_domain_dataclass_to_range_value(the_keys,
                                                                                     the_range,
                                                                                     file_name,
                                                                                     key_mapping,
                                                                                     value_mapping,
                                                                                     verify)
                    else:
                        total_mapping = self._create_total_domain_key_mapping_to_range_value(the_keys,
                                                                                             the_range,
                                                                                             file_name,
                                                                                             key_mapping,
                                                                                             value_mapping,
                                                                                             verify)
                elif val_is_primitive and not val_is_data_class:
                    # alias_value = NewType(self._column_mapping(range_values.__name__), range_values)
                    alias_value = (NewType(range_values.__name__, range_values),)
                    if key_is_data_class:
                        total_mapping = self._create_domain_dataclass_to_range_value(the_keys,
                                                                                     alias_value,
                                                                                     file_name,
                                                                                     key_mapping,
                                                                                     value_mapping,
                                                                                     verify)
                    else:
                        total_mapping = self._create_total_domain_key_mapping_to_range_value(the_keys,
                                                                                             alias_value,
                                                                                             file_name,
                                                                                             key_mapping, value_mapping,
                                                                                             verify)
                elif val_is_tuple:
                    if strict:
                        raise Exception(f'Attribute ({attr}) with range ({range_values})  is not supported')
                    else:
                        the_range = range_values.__args__
                        if key_is_data_class:
                            total_mapping = self._create_domain_dataclass_to_range_value(the_keys,
                                                                                         the_range,
                                                                                         file_name,
                                                                                         key_mapping,
                                                                                         value_mapping,
                                                                                         verify)
                        else:
                            total_mapping = self._create_total_domain_key_mapping_to_range_value(the_keys,
                                                                                                 the_range,
                                                                                                 file_name,
                                                                                                 key_mapping,
                                                                                                 value_mapping,
                                                                                                 verify)

                # result_dict = reduce(lambda a, b: {**a, **b}, list_of_dicts)
                return total_mapping
        else:
            verify = self._verifier(cls.__annotations__[attr], attr)
            domain_keys = cls.__annotations__[attr]
            # This is the case were a data class field is a single record
            key_is_primitive, key_is_data_class, key_is_function, key_is_tuple = \
                self._analyse_mapping(cls.__annotations__[attr])

            if key_is_tuple:
                the_keys = domain_keys.__args__
                set_objects = self._create_domain_key_mapping(the_keys, file_name, set_mapping, verify)
            elif key_is_function:
                the_keys = (domain_keys,)
                set_objects = self._create_domain_key_mapping(the_keys, file_name, set_mapping, verify)
            elif key_is_primitive and not key_is_data_class:
                the_keys = (NewType(domain_keys.__name__, domain_keys),)
                set_objects = self._create_domain_key_mapping(the_keys, file_name, set_mapping, verify)
            elif key_is_data_class:
                set_objects = self.create_objects(domain_keys, file_name, set_mapping, verify)
            return set_objects[0]

    @staticmethod
    def _analyse_mapping(element):
        is_primitive = isinstance(element, type)
        is_data_class = is_dataclass(element)
        is_function = isinstance(element, FunctionType)
        is_tuple = get_origin(element) is tuple if not is_function and not is_primitive else False
        return is_primitive, is_data_class, is_function, is_tuple

    def _create_domain_dataclass_to_range_dataclass(self,
                                                    keys_cls,
                                                    value_cls,
                                                    file_name,
                                                    key_mapping=None,
                                                    value_mapping=None,
                                                    verify=None):
        if verify:
            the_keys = (field.name for field in fields(keys_cls))
            verify._keys = the_keys
        domain_dataclass_trans = partial(self._transform,
                                         cls=keys_cls,
                                         key_mapping=key_mapping)
        range_dataclass_trans = partial(self._transform,
                                        cls=value_cls,
                                        key_mapping=value_mapping)
        with file_name.open(mode='r') as csv_file:
            header = [h.strip() for h in csv_file.readline().split(',')]
            trans = partial(self._transform_dataclass_to_dataclass,
                            domain_dataclass_trans=domain_dataclass_trans,
                            range_dataclass_trans=range_dataclass_trans,
                            verify=verify)
            return reduce(lambda a, b: {**a, **b}, map(trans, enumerate(csv.DictReader(csv_file, fieldnames=header))))

    @staticmethod
    def _transform_dataclass_to_dataclass(dict_,
                                          domain_dataclass_trans,
                                          range_dataclass_trans,
                                          verify=None):
        the_dict = {domain_dataclass_trans(dict_): range_dataclass_trans(dict_)}
        if verify:
            verify.check_unique(the_dict, dict_[0])
        return the_dict

    def _create_domain_dataclass_to_range_value(self,
                                                keys_cls,
                                                map_value,
                                                file_name,
                                                key_mapping=None,
                                                value_mapping=None,
                                                verify=None):
        if verify:
            the_keys = (field.name for field in fields(keys_cls))
            verify._keys = the_keys
        domain_dataclass_trans = partial(self._transform,
                                         cls=keys_cls,
                                         key_mapping=key_mapping)
        with file_name.open(mode='r') as csv_file:
            header = [h.strip() for h in csv_file.readline().split(',')]
            trans = partial(self._transform_dataclass_to_key,
                            values=map_value,
                            domain_dataclass_trans=domain_dataclass_trans,
                            value_mapping=value_mapping,
                            verify=verify)
            return reduce(lambda a, b: {**a, **b}, map(trans, enumerate(csv.DictReader(csv_file, fieldnames=header))))

    def _transform_dataclass_to_key(self,
                                    dict_,
                                    values,
                                    domain_dataclass_trans,
                                    value_mapping=None,
                                    verify=None):
        range_mapping = self._prepare_mapping(value_mapping)

        if len(values) > 1:
            dict_values = tuple(
                typeit_new_type_or_primitive_to_obj(dict_[1][self._column_mapping(value.__name__, range_mapping)],
                                                    value)
                for value in values)
        else:
            dict_values = typeit_new_type_or_primitive_to_obj(
                dict_[1][self._column_mapping(values[0].__name__, range_mapping)], values[0])

        the_dict = {domain_dataclass_trans(dict_): dict_values}
        if verify:
            verify.check_unique(the_dict, dict_[0])
        return the_dict

    def _create_total_domain_key_mapping_to_range_dataclass(self, keys, map_value, file_name, key_mapping=None,
                                                            value_mapping=None,
                                                            verify=None):
        if verify:
            verify_mapping = self._prepare_mapping(key_mapping)
            the_keys = (self._column_mapping(key.__name__, verify_mapping) for key in keys)
            verify._keys = the_keys
        dataclass_trans = partial(self._transform,
                                  cls=map_value,
                                  key_mapping=value_mapping)
        with file_name.open(mode='r') as csv_file:
            header = [h.strip() for h in csv_file.readline().split(',')]
            trans = partial(self._transform_key_to_dataclass,
                            keys=keys,
                            dataclass_trans=dataclass_trans,
                            key_mapping=key_mapping,
                            verify=verify)
            return reduce(lambda a, b: {**a, **b}, map(trans, enumerate(csv.DictReader(csv_file, fieldnames=header))))

    def _transform_key_to_dataclass(self, dict_, keys, dataclass_trans, key_mapping=None, verify=None):
        domain_mapping = self._prepare_mapping(key_mapping)
        if len(keys) > 1:
            dict_key = tuple(
                typeit_new_type_or_primitive_to_obj(dict_[1][self._column_mapping(key.__name__, domain_mapping)], key)
                for key in keys)
        else:
            dict_key = typeit_new_type_or_primitive_to_obj(
                dict_[1][self._column_mapping(keys[0].__name__, domain_mapping)], keys[0])
        the_dict = {dict_key: dataclass_trans(dict_)}
        if verify:
            verify.check_unique(the_dict, dict_[0])
        return the_dict

    def _create_domain_key_mapping(self, keys, file_name, key_mapping=None, verify=None):
        if verify:
            verify_mapping = self._prepare_mapping(key_mapping)
            the_keys = (self._column_mapping(key.__name__, verify_mapping) for key in keys)
            verify._keys = the_keys
        with file_name.open(mode='r') as csv_file:
            header = [h.strip() for h in csv_file.readline().split(',')]
            trans = partial(self._transform_domain,
                            keys=keys,
                            key_mapping=key_mapping,
                            verify=verify)
            return tuple(map(trans, enumerate(csv.DictReader(csv_file, fieldnames=header))))

    def _transform_domain(self, dict_, keys, key_mapping=None, verify=None):
        domain_mapping = self._prepare_mapping(key_mapping)
        if len(keys) > 1:
            rs = tuple(
                typeit_new_type_or_primitive_to_obj(dict_[1][self._column_mapping(key.__name__, domain_mapping)], key)
                for key in keys)
        else:
            num_of_columns = len(list(dict_[1].keys()))
            if num_of_columns == 1:
                requested_key = self._column_mapping(keys[0].__name__, domain_mapping)
                if requested_key in dict_[1]:
                    rs = typeit_new_type_or_primitive_to_obj(dict_[1][requested_key], keys[0])
                else:
                    # Assume the header does not match the key, but
                    # since this is single column file, we take the values as is,
                    # relaxing the demand from user to provide mapping from the field to the CSV column
                    for existing_key in dict_[1].keys():
                        verify.single_csv_column_fix(requested_key, existing_key)
                        rs = typeit_new_type_or_primitive_to_obj(dict_[1][existing_key], keys[0])

            else:
                rs = typeit_new_type_or_primitive_to_obj(
                    dict_[1][self._column_mapping(keys[0].__name__, domain_mapping)], keys[0])

        if verify:
            if len(keys) > 1:
                verify.check_unique(rs, dict_[0])
            else:
                verify.check_unique((rs,), dict_[0])
        return rs

    def _create_total_domain_key_mapping_to_range_value(self, keys, map_value, file_name, key_mapping=None,
                                                        value_mapping=None, verify=None):
        if verify:
            verify_mapping = self._prepare_mapping(key_mapping)
            the_keys = (self._column_mapping(key.__name__, verify_mapping) for key in keys)
            verify._keys = the_keys
        with file_name.open(mode='r') as csv_file:
            header = [h.strip() for h in csv_file.readline().split(',')]
            trans = partial(self._transform_key_to_key,
                            keys=keys,
                            values=map_value,
                            key_mapping=key_mapping,
                            value_mapping=value_mapping,
                            verify=verify)
            return reduce(lambda a, b: {**a, **b}, map(trans, enumerate(csv.DictReader(csv_file, fieldnames=header))))

    def _transform_key_to_key(self, dict_, keys, values, key_mapping=None, value_mapping=None, verify=None):
        domain_mapping = self._prepare_mapping(key_mapping)
        range_mapping = self._prepare_mapping(value_mapping)
        if len(keys) > 1:
            dict_key = \
                tuple(
                    typeit_new_type_or_primitive_to_obj(dict_[1][self._column_mapping(key.__name__, domain_mapping)],
                                                        key)
                    for key in keys)
        else:
            dict_key = typeit_new_type_or_primitive_to_obj(
                dict_[1][self._column_mapping(keys[0].__name__, domain_mapping)], keys[0])

        if len(values) > 1:
            dict_values = tuple(
                typeit_new_type_or_primitive_to_obj(dict_[1][self._column_mapping(value.__name__, range_mapping)],
                                                    value)
                for value in values)
        else:
            dict_values = typeit_new_type_or_primitive_to_obj(
                dict_[1][self._column_mapping(values[0].__name__, range_mapping)], values[0])

        # the_dict = {
        #     dict_key: typeit_new_type_or_primitive_to_obj(dict_[1][self._column_mapping(values.__name__, range_mapping)], values)}
        the_dict = {dict_key: dict_values}
        if verify:
            verify.check_unique(the_dict, dict_[0])
        return the_dict

    @staticmethod
    def _prepare_mapping(the_mapping):
        return prepare_column_mapping(the_mapping)

    @staticmethod
    def _column_mapping(field, mapping=None):
        return column_mapping(field, mapping)


def describe_total_mapping(cls, field=None):
    if not field:
        list(_describe_total_mapping(cls, f) for f in cls.__annotations__.keys())
    else:
        _describe_total_mapping(cls, field)


def _describe_total_mapping(cls, field):
    def _analyze(elem):
        is_function = isinstance(elem, FunctionType)
        print(f'5-Is Function :  {is_function}')
        is_primitive = isinstance(elem, type)
        is_user_primitive = is_primitive and elem not in (str, int, float, bool)
        is_data_class = is_dataclass(elem)
        print(f'5-Is Primitive:  {is_primitive}')
        print(f'5-Is USER Primitive:  {is_user_primitive}')
        print(f'5-Is DataClass:  {is_data_class}')

        is_tuple = get_origin(elem) is tuple if not is_function and not is_primitive else False
        print(f'5-Is Tuple    :  {is_tuple}')
        if not is_tuple:
            print(f'5-Name        :  {elem.__name__}')

        print(f'5c            :  {dir(elem)}')
        print(f'5d-The Class  :  {type(elem)}')
        if is_tuple:
            print(f'7-Tuple Items :  {elem.__args__}')

        if is_primitive and not is_data_class:
            print(f'8-Class Name  : {elem.__name__}')

    print(f'{cls.__name__}::{field}  -- Total Mapping description:\n')
    print(f'1-class dir              :  {dir(cls)}')
    annotation_field = cls.__annotations__[field]
    print(f'2-class field annotations:  {annotation_field}')
    print(f'2a-class field type      :  {type(annotation_field)}')
    if get_origin(annotation_field):
        is_set = get_origin(annotation_field) in \
                 (set, collections.abc.Set, collections.abc.Collection, collections.abc.MutableSet, frozenset)
        is_mapping = get_origin(annotation_field) in \
                     (collections.abc.Mapping,)
        # is_total_mapping = annotation_field._special is False and annotation_field._name == 'TotalMapping'
        is_total_mapping = annotation_field._name == 'TotalMapping'
        print(f'2b-Is Set:  {is_set}')
        print(f'2c-Is Mapping:  {is_mapping}')
        print(f'2d-Is Total Mapping:  {is_total_mapping}')
        # print(f'3:  {dir(cls.__annotations__[field])}')
        print(f'4-Field items            :  {annotation_field.__args__}')
        print(f'\nMap Keys:   {annotation_field.__args__[0]}')
        _analyze(annotation_field.__args__[0])
        if len(annotation_field.__args__) > 1:
            print(f'\nMap Values:  {annotation_field.__args__[1]}')
            _analyze(annotation_field.__args__[1])
    else:
        _analyze(annotation_field)
    print("\n")
