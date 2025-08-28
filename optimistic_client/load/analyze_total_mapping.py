import itertools
from dataclasses import fields, is_dataclass, Field, astuple
from typing import get_args

from optimistic_client.load.knoweldge_class_generator import DataGenerator
from optimistic_client.load.load_utils import is_solution, is_data_class, is_function, is_tuple, is_set, is_mapping, \
    is_total_mapping, is_primitive, is_bounded_primitive, is_unbounded_primitive, prepare_column_mapping, \
    column_mapping
from optimistic_client.load.loader import create_problem_instance


class AnalyzeInfo:
    def __init__(self, name):
        self.name = name
        self.fields = set()
        self.field_keys = {}
        self.unique_required_types = set()
        self.discarded_field_keys = {}
        self.missing_domain_keys = {}
        self.extra_domain_keys = {}

    def is_active(self):
        return len(self.discarded_field_keys) > 0 or len(self.unique_required_types) > 0


class AnalyzeTotalMapping:
    def __init__(self, cls, input_files, column_mappings, verbose=False):
        self._cls = cls
        self._input_files = input_files
        self._column_mappings = column_mappings
        self._verbose = verbose
        self._gen = DataGenerator()
        self._sources = {}
        self._domain = {}

        self._total_mapping_info = AnalyzeInfo('TotalMapping')
        self._mapping_info = AnalyzeInfo('Mapping')
        self._set_info = AnalyzeInfo('Set')
        self._all_required_types = set()

        self._total_mappings = {}
        self._total_mappings_required_types = set()
        self._discarded_total_mappings = {}
        self._missing_domain_keys = {}
        self._extra_domain_keys = {}

        self._analyze_complete = False

    def analyze(self, cls_instance=None):
        self._check_prerequisite()
        self._identify_field_keys_by_collection_type()
        self._prepare_required_fields_sources()
        self._compute_domains()
        self._verify(cls_instance)
        self._analyze_complete = True

    def _check_prerequisite(self):
        err_msg = []
        warn_msg = []
        for field in fields(self._cls):
            if not self._input_files.get(field.name):
                err_msg.append(f'{field.name}')
            if not self._column_mappings.get(field.name):
                warn_msg.append(f'{field.name}')
        if warn_msg:
            print(f'Warning: column mapping may be missing for the following fields: \"{", ".join(warn_msg)}\"')
        if err_msg:
            print(f'ERROR: missing input files for fields: V{", ".join(err_msg)}\"')
            raise AttributeError(f'Missing Input Files: \"{", ".join(err_msg)}\"')

    def _identify_field_keys_by_collection_type(self):
        """
        Identify the dataclass fields which are defined as `TotalMapping`,
        For each such field extract all the domain `NewType` attributes
        """
        for field in fields(self._cls):
            info = None
            if is_total_mapping(field):
                info = self._total_mapping_info
            elif is_mapping(field):
                info = self._mapping_info
            elif is_set(field):
                info = self._set_info

            if info:
                info.fields.add(field)
                domain_keys = get_args(field.type)[0]
                add_keys, discard_keys = self._analyze_required_types(domain_keys)
                if discard_keys:
                    info.discarded_field_keys[field] = discard_keys
                else:
                    if add_keys:
                        info.field_keys[field] = add_keys
                    for key in add_keys:
                        info.unique_required_types.add(key)
                        self._all_required_types.add(key)

    def _analyze_required_types(self, keys):
        """
        Step through the item hierarchy to get all the leaf `NewType` of the
        `TotalMapping` domain
        We assume the root call, passes into keys, the domain (i.e. args[0]) of `TotalMapping` object
        In case the domain consists of `NewType` attributes, it registers them
        Recursive calls, may occur in case the domain is:
            - typing.Tuple
        """
        required_keys = []
        discarded_keys = []
        if is_data_class(keys):
            for field in fields(keys):
                if is_function(field.type):
                    required_keys.append(field.type)
                elif is_bounded_primitive(field):
                    required_keys.append(bool)
                elif is_unbounded_primitive(field):
                    # i.e. element in (str, float, int):
                    # Any other primitive key, can not be supported
                    # The entire total mapping can not be checked
                    discarded_keys.append((keys, f'{keys.__name__}.{field.name}', field.type.__name__))
        elif is_function(keys):
            required_keys.append(keys)
        elif is_tuple(keys):
            tuple_keys = get_args(keys)
            for index, key in enumerate(tuple_keys):
                if is_data_class(key):
                    discarded_keys.append((keys, keys._name, key.__name__))
                else:
                    add_keys, add_discarded_keys = self._analyze_required_types(key)
                    for sub_key in add_keys:
                        required_keys.append(sub_key)
                    for discard_sub_key in add_discarded_keys:
                        discarded_keys.append(
                            (keys,
                             f'{keys._name}.Index[{index}]{"." + discard_sub_key[1] if discard_sub_key[1] else ""}',
                             discard_sub_key[2]))
        elif is_bounded_primitive(keys):
            required_keys.append(bool)
        elif is_unbounded_primitive(keys):
            # i.e. element in (str, float, int):
            # Any other primitive key, can not be supported
            # The entire total mapping can not be checked
            discarded_keys.append((keys, "", keys.__name__))
        else:
            return None
        return tuple(required_keys), tuple(discarded_keys)

    def _prepare_required_fields_sources(self):
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
            if is_solution(field):
                # Only Input variables contribute to domain
                continue
            args, domain_mapping, range_mapping = self._fetch_root_column_mappings(field)
            if args:
                sources = self._resolve_argument_mapping_and_sources(args[0], domain_mapping)
                self._load_new_type_source(sources, self._input_files[field.name])

                if len(args) > 1:
                    sources = self._resolve_argument_mapping_and_sources(args[1], range_mapping)
                    self._load_new_type_source(sources, self._input_files[field.name])

    def _load_new_type_source(self, sources, input_file):
        for key, mapping in sources:
            if key is bool:
                data = {True, False}
            else:
                data = self._gen.load_new_type_data(key,
                                                    input_file,
                                                    mapping,
                                                    verify=None)
            source = self._sources.get(key.__name__, set())
            source.update(set(data))
            self._sources[key.__name__] = source

    def _resolve_argument_mapping_and_sources(self, element, mapping, map_already_iterable=False):
        """
        Determine for each element the set of required NewType sources to load,
        and their corresponding mapping
        """
        original_mapping = mapping if mapping else {}
        original_mapping = original_mapping if map_already_iterable else prepare_column_mapping(mapping)
        sources = []
        if is_function(element) or is_bounded_primitive(element):
            if element in self._all_required_types:
                map_value = column_mapping(element.__name__, original_mapping)
                resolved_mapping = {}
                if map_value:
                    resolved_mapping[element.__name__] = map_value
                sources.append((element, resolved_mapping))

        if is_data_class(element):
            for field in fields(element):
                if field.type in self._all_required_types:
                    # The field type is required one.
                    # Update the mapping:
                    #  - If the field name key exists in the original input mapping, then use the original mapping
                    #  - Otherwise, the mapping may not exists, so in case of loading dataclass key
                    #        we use the datacalss field name, we map the field type name to the dataclass field name
                    map_value = column_mapping(field.name, original_mapping)
                    resolved_mapping = {field.type.__name__: map_value or field.name}
                    sources.append((field.type, resolved_mapping))

        if is_tuple(element):
            # In root Mapping/TotalMapping a domain or range of type Tuple
            # may hold NewType, primitive only,
            for sub_args in get_args(element):
                sub_sources = self._resolve_argument_mapping_and_sources(sub_args,
                                                                         original_mapping,
                                                                         map_already_iterable=True)
                sources = [*sources, *sub_sources]

        if is_unbounded_primitive(element):
            # argument of primitive types e.g. (int, float, str) are unbounded
            # we ignore them for now
            # However, for bool, we do consider, during the actual comparisons.
            pass

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
            # This is Primitive which is not dataclass (i.e. builtin(int,str,float,bool)
            pass
        return args, domain_mapping, range_mapping

    def _compute_domains(self):
        for info in (self._total_mapping_info, self._mapping_info, self._set_info):
            if info.is_active():
                for field, values in info.field_keys.items():
                    ordered_domain_sources = []
                    for source in values:
                        ordered_domain_sources.append(self._sources[source.__name__])
                    if len(ordered_domain_sources) > 1:
                        self._domain[field.name] = sorted(set(itertools.product(*ordered_domain_sources)))
                    else:
                        self._domain[field.name] = sorted(set(ordered_domain_sources[0]))

    def _verify(self, cls_instance=None):
        _problem = cls_instance
        if not _problem:
            _problem = create_problem_instance(self._cls,
                                               self._input_files,
                                               self._column_mappings)
        # if self._verbose:
        #     print(f'Instance [{_problem.__class__.__name__}], loaded data fields:')
        #     for field in fields(type(_problem)):
        #         print(f'  {field.name}: {getattr(_problem, field.name)}')
        #     print()
        for info in (self._total_mapping_info, self._mapping_info, self._set_info):
            if info.is_active():
                for field, domain_types in info.field_keys.items():
                    missing_domain, extra_domain = [], []
                    instance_data = getattr(_problem, field.name)
                    domain_keys = get_args(field.type)[0]
                    if is_function(domain_keys) or is_tuple(domain_keys):
                        missing_domain = sorted(self._domain[field.name] - instance_data.keys())
                        extra_domain = sorted(instance_data.keys() - self._domain[field.name])

                    if is_data_class(domain_keys):
                        instance_row_data = set()
                        if "Set" == info.name:
                            for instance in instance_data:
                                instance_row_data.add(astuple(instance))
                        else:
                            for instance in instance_data.keys():
                                instance_row_data.add(astuple(instance))
                        missing_domain = sorted(set(self._domain[field.name]) - instance_row_data)
                        extra_domain = sorted(instance_row_data - set(self._domain[field.name]))

                    info.missing_domain_keys[field.name] = missing_domain
                    info.extra_domain_keys[field.name] = extra_domain

    def report(self):
        sl = '\"'
        if not self._analyze_complete:
            print(f'Problem \"{self._cls.__name__}]\" report requires to first call analyze() method')
        else:
            for info in (self._total_mapping_info, self._mapping_info, self._set_info):
                if info.is_active():
                    name = info.name
                    if self._verbose:
                        print(f'Analyze {name} of \"{self._cls.__name__}\":')
                        print(
                            f' {name}:        {[f"{key.name}: " + ",".join(elem.__name__ for elem in values) for key, values in info.field_keys.items()]}')

                        _unique_required_types = {key.__name__ for key in info.unique_required_types}
                        if info.unique_required_types:
                            required_types_msg = ",".join(sorted(_unique_required_types))
                        print(
                            f' {name} Types:  {required_types_msg if info.unique_required_types else "[]"}')

                        _sources = f'{[f"{key}: {sorted(value)}" for key, value in self._sources.items() if key in _unique_required_types]}'
                        _domains = dict()
                        _fields_names = []
                        for field in info.fields:
                            _fields_names.append(field.name)
                        for field in sorted(_fields_names):
                            _domains.update(
                                {key: sorted(value) for key, value in self._domain.items() if key == field})

                        print(f' Sources:             {_sources}')
                        print(f' Domain:              {_domains}')
                        print()

                    print(f'{name}, Domain validation results:')
                    for field, key_values in info.field_keys.items():
                        key_names = ", ".join(iter(key.__name__ for key in key_values))
                        missing_domain = info.missing_domain_keys[field.name]
                        extra_domain = info.extra_domain_keys[field.name]
                        msg = f'  Domain of {sl}{field.name}{sl} field is '
                        if missing_domain:
                            msg += f'{"missing mandatory" if "TotalMapping" == name else "missing (optional)"}'
                        else:
                            msg += 'complete'
                        msg += f'{" and without extra keys" if not missing_domain and not extra_domain else ""}'
                        msg += f'{f" {len(missing_domain)} keys {sl}{key_names}{sl} with values: {missing_domain}" if missing_domain else ""}'
                        print(msg)
                        if extra_domain:
                            print(
                                f'  Domain of \"{field.name}\" field has {len(extra_domain)} extra keys \"{key_names}\" with values: {extra_domain}')

                    print()
                    if info.discarded_field_keys:
                        print(
                            f'Discard {name} domain validation, due to invalid attribute types:')
                    for field, discarded_keys in info.discarded_field_keys.items():
                        discard_attr_msg = ", ".join(
                            f'{discard[1] + "." if discard[1] else ""}{discard[2]}' for discard in discarded_keys)
                        print(f'  Cannot determine domain for \"{field.name}\", '
                              f'due to key violations: \"{discard_attr_msg}\"')
