from dataclasses import fields, is_dataclass, Field
from typing import get_args, NewType

from optimistic_client.load.knoweldge_class_generator import DataGenerator
from optimistic_client.load.load_utils import is_data_class, is_function, is_tuple, is_set, is_mapping, \
    is_primitive, is_bounded_primitive, is_unbounded_primitive, prepare_column_mapping, \
    column_mapping
from optimistic_client.load.verify_model_field_types import LexicalPath


class VerifyColumnMapping:
    def __init__(self, cls, input_files, column_mappings, verbose=False):
        self._cls = cls
        self._input_files = input_files
        self._column_mappings = column_mappings
        self._report = {}
        self._verbose = verbose
        self._gen = DataGenerator()
        self._missing_input_files = []
        self._missing_column = []
        self._analyze_complete = False
        self._exception_raised = False

    def verify(self, cls_instance=None) -> bool:
        self._check_prerequisite()
        if self._missing_input_files:
            self._analyze_complete = True
            self._exception_raised = True
            return
        self._verify_input_sources()
        self._analyze_complete = True
        return not self._exception_raised

    def _append_report(self, field, msg):
        _report_msg = self._report.get(field, [])
        _report_msg.append(msg)
        self._report[field] = _report_msg

    def _check_prerequisite(self):
        for field in fields(self._cls):
            if not self._input_files.get(field.name):
                self._missing_input_files.append(field.name)
            if not self._column_mappings.get(field.name):
                self._missing_column.append(field.name)

        if self._missing_input_files:
            _msg = f' ERROR: Following fields are missing mandatory input files\n'
            _msg += f'  "{", ".join(field for field in self._missing_input_files)}"\n'
            self._append_report("Prerequisite", _msg)

        if self._missing_column:
            _msg = f' WARNING: Following fields may require column mapping:\n'
            _msg += f'  "{", ".join(field for field in self._missing_column)}"\n'
            self._append_report("Prerequisite", _msg)

    def _verify_input_sources(self):
        """
        Here, we iterate on the fields of the main optimization problem dataclass
        We can expect fields of types:
         -  typing.Mapping or (typing.)TotalMapping, with one of the following sub-fields:
                -  typing.Tuple (card: 1), with sub-fields:
                        - typing.NewType (card: *)
                        - (unbounded)/primitives (not-dataclass) (card: *)
                -  typing.NewType (card: 1)
                -  record/dataclass (card:1)
                - (unbounded)/primitives (not-dataclass) - int,float, str, bool  (card: 1)
         -  typing.Set, with one of the following sub-fields:
                -  NewType (card: 1)
                -  record/dataclass (card: 1)
                - (unbounded)/primitives (not-dataclass)  (card: 1)
         -  record/dataclass (card: 1)
         -  (unbounded)/primitives (not-dataclass)- int,float, str, bool (card: 1)
         -  typing.NewType (card: 1)
        """
        for field in fields(self._cls):
            lexical_path = LexicalPath(field)
            args, domain_mapping, range_mapping = self._fetch_root_column_mappings(field)
            if args:
                sources = self._resolve_argument_mapping_and_sources(args[0], domain_mapping, lexical_path,
                                                                     is_domain=True)
                self._load_new_type_source(sources, self._input_files[field.name], is_domain=True)

                if len(args) > 1:
                    sources = self._resolve_argument_mapping_and_sources(args[1], range_mapping, lexical_path,
                                                                         is_domain=False)
                    self._load_new_type_source(sources, self._input_files[field.name], is_domain=False)

    def _load_new_type_source(self, sources, input_file, is_domain):
        for key, mapping, data_source_mapping, lexical in sources:
            try:
                data = self._gen.load_new_type_data(key,
                                                    input_file,
                                                    mapping,
                                                    verify=None)
            except:
                _key = '' if data_source_mapping else LexicalPath._name(key)
                _path = f'{lexical.path(drop_field=True)}.' if lexical.path(drop_field=True) else ""
                if data_source_mapping:
                    _path = f'{lexical.path(drop_field=True)}' if lexical.path(drop_field=True) else ""
                    record_key, record_value = [(key, value) for key, value in data_source_mapping.items()][0]
                    _msg = f' {"Domain" if is_domain else "Range"} Path: "{_path}{_key}"' \
                           f' Used mapping: {data_source_mapping}' \
                           f' Input File: {input_file.name},' \
                           f' Error: Mapping is missing @record field name "{record_key}" or wrong column value "{record_value}"\n'
                else:
                    _path = f'{lexical.path(drop_field=True)}.' if lexical.path(drop_field=True) else ""
                    _msg = f' {"Domain" if is_domain else "Range"} Path: "{_path}{_key}"' \
                           f' Existing Mapping: {mapping}' \
                           f' Input File: {input_file.name},' \
                           f' Error: Wrong or missing column name\n'
                self._append_report(lexical.field().name, _msg)
                self._exception_raised = True

    def _resolve_argument_mapping_and_sources(self, element, mapping, lexical, is_domain, map_already_iterable=False):
        """
        Determine for each element the set of required NewType sources to load,
        and their corresponding mapping
        """
        original_mapping = mapping if mapping else {}
        original_mapping = original_mapping if map_already_iterable else prepare_column_mapping(mapping)
        sources = []

        _lexical = lexical.copy()
        try:
            if is_function(element) or is_bounded_primitive(element) or is_unbounded_primitive(element):
                map_value = column_mapping(element.__name__, original_mapping)
                resolved_mapping = {}
                if map_value:
                    resolved_mapping[element.__name__] = map_value
                sources.append((element, resolved_mapping, {}, _lexical.copy()))

            if is_data_class(element):
                _lexical.add(element)
                for field in fields(element):
                    # The field type is required one.
                    # Update the mapping:
                    #  - If the field name key exists in the original input mapping, then use the original mapping
                    #  - Otherwise, the mapping may not exists, so in case of loading dataclass key
                    #        we use the datacalss field name, we map the field type name to the dataclass field name
                    map_value = column_mapping(field.name, original_mapping)
                    resolved_mapping = {field.type.__name__: map_value or field.name}
                    ds_mapping = {field.name: map_value or field.name}
                    sources.append((field.type, resolved_mapping, ds_mapping, _lexical.copy().add(field)))

            if is_tuple(element):
                # In root Mapping/TotalMapping a domain or range of type Tuple
                # may hold NewType, primitive only,
                for index, sub_args in enumerate(get_args(element)):
                    sub_sources = self._resolve_argument_mapping_and_sources(sub_args,
                                                                             original_mapping,
                                                                             _lexical.copy().add(
                                                                                 NewType(f'[{index}]', int)),
                                                                             is_domain=is_domain,
                                                                             map_already_iterable=True)
                    sources = [*sources, *sub_sources]
        except:
            _existing_mapping = mapping.get(element.__name__, {})
            if not _existing_mapping:
                _error = f'missing column mapping'
            else:
                _error = f'column name array is too short missing one or more entries'
            _path = f'{lexical.path(drop_field=True)}.' if lexical.path(drop_field=True) else ""
            _msg = f' {"Domain" if is_domain else "Range"} Path: "{_path}{LexicalPath._name(element)}"' \
                   f' Used mapping: {{\'{element.__name__}\': {_existing_mapping.get("column", "")}}}' \
                   f' Error: {_error}\n'
            self._append_report(_lexical.field().name, _msg)
            self._exception_raised = True

        return sources

    def _fetch_root_column_mappings(self, field: Field):
        domain_mapping, range_mapping, args = None, None, None
        if is_function(field) or is_dataclass(field):
            args = (field.type,)
            domain_mapping = self._column_mappings.get(field.name, {}).get('mapping', None)
            range_mapping = None
        elif is_set(field):
            args = get_args(field.type)
            domain_mapping = self._column_mappings.get(field.name, {}).get('mapping', None)
            range_mapping = None
        elif is_mapping(field):
            args = get_args(field.type)
            domain_mapping = self._column_mappings.get(field.name, {}).get('domain_mapping', None)
            range_mapping = self._column_mappings.get(field.name, {}).get('range_mapping', None)
        elif is_tuple(field):
            # If tuple, we don't accept Tuple at the root, only inside a mapping
            pass
        elif is_primitive(field) and not is_data_class(field):
            args = (field.type,)
            domain_mapping = self._column_mappings.get(field.name, {}).get('mapping', None)
            range_mapping = None
        return args, domain_mapping, range_mapping

    def report(self):
        sl = '\"'
        if not self._analyze_complete:
            print(
                f' Problem \"{self._cls.__name__}]\" column verification report requires to first call verify() method')
        else:
            _msg = ""
            for key, messages in self._report.items():
                if "Prerequisite" == key:
                    _msg = f'"{key}" check:\n'
                else:
                    _msg = f'Field "{key}" failed:\n'
                for msg in messages:
                    _msg += f'{msg}'

            print(f'Verify "{self._cls.__name__}" column types:')
            if _msg:
                print(f'{"=" * 50}\n{_msg}')
            else:
                print(f'  Verification passed\n')
