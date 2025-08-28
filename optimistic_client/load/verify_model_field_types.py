from dataclasses import fields
from typing import get_args

from inflection import camelize

from optimistic_client.load.load_utils import is_solution, is_data_class, is_primitive, is_unbounded_primitive, \
    is_user_primitive, is_tuple, is_function, is_set, is_mapping, is_total_mapping, is_typing, is_not_supported_builtins
from optimistic_client.optimization import OptimizationProblem


class LexicalPath:
    def __init__(self, field):
        self._field = field
        self._path = []

    def add(self, element):
        self._path.append(element)
        return self

    def field(self):
        return self._field

    def path(self, drop_field=False):
        if len(self._path) > 0:
            _msg = '' if drop_field else f'{self._field.name}'
            for index, key in enumerate(self._path):
                _sep = "" if drop_field and not index else "."
                _msg += f'{_sep}{self._name(key)}'
        else:
            _msg = ''
        return _msg

    def last(self):
        if not self._path:
            return self._field.name
        return self._name(self._path[-1])

    @staticmethod
    def _name(key):
        if hasattr(key, '_field_type') or hasattr(key, 'name'):
            return key.name
        elif is_typing(key) and not is_function(key):
            return key._name
        else:
            return key.__name__

    def copy(self):
        cpp = LexicalPath(self._field)
        for p in self._path:
            cpp.add(p)
        return cpp


class VerifyModelFieldTypes:
    def __init__(self, cls, column_mappings=None):
        self._cls = cls
        self._report = []
        self._solution_exists = False
        self._column_mappings = column_mappings
        self._verbose = True

    def verify(self):
        rs = self._check_is_class_data_class()
        if rs:
            self._check_solution_exists()
            self._check_root_input_and_solution()

    def _check_is_class_data_class(self):
        """
        The class model must be a dataclass,
        any field consisting of domain or range whose type is another class must be a record/dataclass
        """
        _msg = f'' if is_data_class(
            self._cls) else f'"{self._cls.__module__}.{self._cls.__name__}" not a dataclass\n' \
                            f'   Possible Fix: Inherit from "{OptimizationProblem.__module__}.{OptimizationProblem.__name__}"'
        if _msg:
            self._report.append(_msg)
        return is_data_class(self._cls)

    def _check_solution_exists(self):
        for field in fields(self._cls):
            if is_solution(field):
                return True
        _msg = f'"{self._cls.__module__}.{self._cls.__name__}" is missing one or more solution field(s)\n' \
               f'  Possible Fix:\n' \
               f'    A. import necessary package:\n' \
               f'          from optimistic_client.meta.utils import solution_variable\n' \
               f'    B. Select one or more fields and declare it as a solution:\n' \
               f'          selected: ... = solution_variable()'
        self._report.append(_msg)
        return False

    def _check_root_input_and_solution(self):
        for field in fields(self._cls):
            lexical_path = LexicalPath(field)
            # self._check2(field.type, lexical_path, is_domain=True, is_root=True)
            self._check(field.type, lexical_path, is_root=True)

    def _check(self, element, lexical, is_root=False):
        self._verify_primitive(element, lexical)
        self._verify_function(element, lexical)
        if is_tuple(element):
            if is_root:
                _msg = f'Field "{lexical.field().name}" use of Tuple as main type is forbidden\n' \
                       f'  Possible Fix:\n' \
                       f'     Refer to the documentation'
                self._report.append(_msg)
        self._verify_tuple(element, lexical)
        self._verify_data_class(element, lexical)
        self._verify_set(element, lexical)
        self._verify_mapping(element, lexical)
        self._verify_illegal_use_of_primitives(element, lexical)

    def _verify_primitive(self, element, lexical):
        """
        primitive types may only be:
         - builtin "int", "str", "float" , "bool"

        Note, here we also check that class declaration are decorated with @record,
        since a "class" is also builtin primitive, and we can use them, as long they are @record s
        """
        if is_primitive(element):
            if is_user_primitive(element):
                _msg = f'Field "{lexical.field().name}"{f" key {lexical.path()}" if lexical.path() else ""} cannot refer to regular class definitions "{element.__name__}"\n' \
                       f'  Possible Fix:  Convert the class to a problem @record\n' \
                       f'    A. import necessary package:\n' \
                       f'          from optimistic_client.meta.utils import record\n' \
                       f'    B. decorate the class:\n' \
                       f'          @record\n' \
                       f'          class {element.__name__}:\n' \
                       f'          ...'
                self._report.append(_msg)

            if is_not_supported_builtins(element):
                _msg = f'Field "{lexical.field().name}" must only use either NewType or primitive types str, float, int, or bool\n' \
                       f'  Possible Fix:\n' \
                       f'    Change "{element.__name__}" type of "{lexical.path() or lexical.field().name}"'
                self._report.append(_msg)

    def _verify_function(self, element, lexical):
        """
        functions are typing.NewType,
        They can inherit from each other, as long the resolved type may be:
            - only builtin "int", "str", "float" , "bool"
        """
        if is_function(element):
            _lexical = lexical.copy()
            _lexical.add(element)
            _field_type = element.__supertype__
            while not isinstance(_field_type, type):
                _lexical.add(_field_type)
                _field_type = _field_type.__supertype__
            if _field_type not in (str, float, int, bool):
                _msg = f'Field "{_lexical.field().name}" must use defined NewType variables having primitive types str, float, int, or bool\n' \
                       f'  Possible Fix:\n' \
                       f'     Change "{_field_type.__name__}" type of attribute "{_lexical.path()}"'
                self._report.append(_msg)

    def _verify_data_class(self, element, lexical):
        """
        Dataclass record fields may be:
            - primitive types (bounded or unbounded)
            - typing.NewTypes
        """
        _lexical = lexical
        if is_data_class(element):
            _lexical.add(element)
            for field in fields(element):
                if is_data_class(field.type):
                    _msg = f'Field "{_lexical.field().name}", cannot use @record types for a field in a @record\n' \
                           f' @record fields can only use primitive or NewType types\n' \
                           f' "{_lexical.path()}.{field.name}" field type is @record "{field.type.__name__}"\n' \
                           f'  Possible Fix:\n' \
                           f'     Change "{element.__name__}.{field.name}" to a valid field type'
                    self._report.append(_msg)
                    continue

                _sub_type_error = ""
                if is_set(field.type):
                    _sub_type_error = 'Set'
                if is_mapping(field.type):
                    _sub_type_error = 'Mapping'
                if is_total_mapping(field.type):
                    _sub_type_error = 'TotalMapping'
                if is_tuple(field.type):
                    _sub_type_error = 'Tuple'
                if _sub_type_error:
                    _msg = f'Field "{_lexical.field().name}" cannot set "@record" field type to {_sub_type_error}\n' \
                           f' @record fields can only use primitive or NewType types\n' \
                           f' "{_lexical.path()}.{field.name}" field type is {field.type._name}\n' \
                           f'  Possible Fix:\n' \
                           f'     Change "{element.__name__}.{field.name}" to a valid field type'
                    self._report.append(_msg)
                    continue

                self._verify_primitive(field.type, _lexical.copy().add(field))
                self._verify_function(field.type, _lexical.copy().add(field))

    def _verify_tuple(self, element, lexical):
        """
        Tuple elements may be one or more of:
            - Primitive types (bounded or unbounded)
            - typing.NewType
        """
        if is_tuple(element):
            for index, sub_args in enumerate(get_args(element)):
                if is_data_class(sub_args):
                    _msg = f'Field "{lexical.field().name}" cannot use @record key inside a Tuple\n' \
                           f'  Tuple elements can only use primitive or NewType types\n' \
                           f'  "{lexical.path() or lexical.field().name}[{index}]" field type is @record "{sub_args.__name__}"\n' \
                           f'  Possible Fix:\n' \
                           f'     Do not use "{sub_args.__name__}" field type inside a Tuple'
                    self._report.append(_msg)
                    continue
                _sub_type_error = ""
                if is_set(sub_args):
                    _sub_type_error = 'Set'
                if is_mapping(sub_args):
                    _sub_type_error = 'Mapping'
                if is_total_mapping(sub_args):
                    _sub_type_error = 'TotalMapping'
                if _sub_type_error:
                    _msg = f'Field "{lexical.field().name}" cannot use {_sub_type_error} inside a Tuple\n' \
                           f'  Tuple elements can only use primitive or NewType types\n' \
                           f'  Possible Fix:\n' \
                           f'     Do not use {_sub_type_error} at index {index}'
                    self._report.append(_msg)
                    continue

                self._verify_primitive(sub_args, lexical.copy())
                self._verify_function(sub_args, lexical.copy())

    def _verify_set(self, element, lexical):
        """
        "typing.Set" elements may be:
          - primitive types (bounded or unbounded)
          - typing.NewType
          - a @record class
        """
        if is_set(element):
            for index, sub_arg in enumerate(get_args(element)):
                if is_tuple(sub_arg):
                    _msg = f'Field "{lexical.field().name}" use of Tuple inside a Set is forbidden\n' \
                           f'  Valid types in a Set are NewType, @record, or primitive\n' \
                           f'  Possible Fix:\n' \
                           f'    Change the type to a valid type'
                    self._report.append(_msg)
                    continue
                self._verify_primitive(sub_arg, lexical.copy())
                self._verify_function(sub_arg, lexical.copy())
                self._verify_data_class(sub_arg, lexical.copy())

    def _verify_mapping(self, element, lexical):
        """
        typing.Mapping(or TotalMapping) Domain elements may be:
            - primitive types
            - typing.NewTypes
            - a @record class,
            - typing.Tuple

        typing.Mapping(or TotalMapping) range elements may be:
            - primitive types
            - typing.NewTypes
            - a @record class,
        """
        if is_mapping(element):
            for index, sub_arg in enumerate(get_args(element)):
                is_domain = 0 == index
                d_o_r = "range" if index else "domain"

                _sub_type_error = ""
                if is_set(sub_arg):
                    _sub_type_error = 'Set'
                if is_mapping(sub_arg):
                    _sub_type_error = 'Mapping'
                if is_total_mapping(sub_arg):
                    _sub_type_error = 'TotalMapping'
                if _sub_type_error:
                    _msg = f'Field "{lexical.field().name}" cannot use {_sub_type_error} inside a "{LexicalPath._name(element)}" {d_o_r}\n' \
                           f'  Possible Fix:\n' \
                           f'      Do not use {_sub_type_error} type as part of the {d_o_r}'
                    self._report.append(_msg)
                    continue

                if is_tuple(sub_arg) and not is_domain:
                    _msg = f'Field "{lexical.field().name}" cannot use Tuple inside "{LexicalPath._name(element)}" range\n' \
                           f'  Possible Fix:\n' \
                           f'      Do not use Tuple as part of the {d_o_r}'
                    self._report.append(_msg)
                    continue

                self._verify_primitive(sub_arg, lexical.copy())
                self._verify_function(sub_arg, lexical.copy())
                self._verify_data_class(sub_arg, lexical.copy())
                self._verify_tuple(sub_arg, lexical.copy().add(element).add(sub_arg))

    def _parse_attr_type_exmp(self, attr):
        cam_attr = camelize(attr)
        postfix = ""
        if attr == cam_attr:
            postfix = "_"
        return f'{cam_attr}{postfix}'

    def _verify_illegal_use_of_primitives(self, element, lexical):
        _lexical = lexical
        if is_solution(_lexical.field()) or is_total_mapping(element):
            field_origin = ''
            if is_solution(_lexical.field()) and is_total_mapping(element):
                field_origin = "Total Mapping Solution field"
            elif is_solution(_lexical.field()):
                field_origin = "Solution field"
            elif is_total_mapping(element):
                field_origin = "Total Mapping field"

            if is_primitive(element) and is_unbounded_primitive(element):
                _msg = self._illegel_primitive_msg(lexical=_lexical,
                                                   field_name=_lexical.field().name,
                                                   field_type=element.__name__,
                                                   field_origin=field_origin,
                                                   mapping_d_or_r=None,
                                                   mapping_class=None,
                                                   attr_def=None,
                                                   attr_exmp=None)
                self._report.append(_msg)

            if is_data_class(element):
                for field in fields(element):
                    if is_primitive(field.type) and is_unbounded_primitive(field.type):
                        _lexical = lexical.copy().add(field)
                        _msg = self._illegel_primitive_msg(lexical=_lexical,
                                                           field_name=_lexical.field().name,
                                                           field_type=field.type.__name__,
                                                           field_origin=field_origin,
                                                           mapping_d_or_r=None,
                                                           mapping_class=None,
                                                           attr_def=None,
                                                           attr_exmp=None)
                        self._report.append(_msg)

            if is_set(element):
                for index, sub_arg in enumerate(get_args(element)):
                    if is_tuple(sub_arg):
                        continue
                    if is_data_class(sub_arg):
                        _local_lexical = lexical.copy().add(sub_arg)
                        for field in fields(sub_arg):
                            if is_primitive(field.type) and is_unbounded_primitive(field.type):
                                _lexical = _local_lexical.copy().add(field)
                                _msg = self._illegel_primitive_msg(lexical=_lexical,
                                                                   field_name=_lexical.field().name,
                                                                   field_type=field.type.__name__,
                                                                   field_origin=field_origin,
                                                                   mapping_d_or_r=None,
                                                                   mapping_class=None,
                                                                   attr_def=None,
                                                                   attr_exmp=None)
                                self._report.append(_msg)

                    if is_primitive(sub_arg) and is_unbounded_primitive(sub_arg):
                        attr_exmp = f'                   {_lexical.last()}: Set[{self._parse_attr_type_exmp(_lexical.last())}]'
                        _msg = self._illegel_primitive_msg(lexical=_lexical,
                                                           field_name=_lexical.field().name,
                                                           field_type=sub_arg.__name__,
                                                           field_origin=field_origin,
                                                           mapping_d_or_r=None,
                                                           mapping_class=None,
                                                           attr_def=None,
                                                           attr_exmp=attr_exmp)
                        self._report.append(_msg)

            if is_mapping(element):
                domain_arg = get_args(element)[0]
                _lexical = lexical.copy()

                if is_primitive(domain_arg) and is_unbounded_primitive(domain_arg):
                    attr_exmp = f'                   {_lexical.last()}: {LexicalPath._name(element)}[{self._parse_attr_type_exmp(_lexical.last())},...]'
                    _msg = self._illegel_primitive_msg(lexical=_lexical,
                                                       field_name=_lexical.field().name,
                                                       field_type=domain_arg.__name__,
                                                       field_origin=field_origin,
                                                       mapping_d_or_r='domain',
                                                       mapping_class=LexicalPath._name(element),
                                                       attr_def=None,
                                                       attr_exmp=attr_exmp)
                    self._report.append(_msg)

                if is_data_class(domain_arg):
                    _local_lexical = lexical.copy().add(domain_arg)
                    for field in fields(domain_arg):
                        if is_primitive(field.type) and is_unbounded_primitive(field.type):
                            _lexical = _local_lexical.copy().add(field)
                            attr_exmp = f'                   class {LexicalPath._name(domain_arg)}:\n' \
                                        f'                         {_lexical.last()}: {self._parse_attr_type_exmp(_lexical.last())}'
                            _msg = self._illegel_primitive_msg(lexical=_lexical,
                                                               field_name=_lexical.field().name,
                                                               field_type=field.type.__name__,
                                                               field_origin=field_origin,
                                                               mapping_d_or_r='domain',
                                                               mapping_class=LexicalPath._name(element),
                                                               attr_def=None,
                                                               attr_exmp=attr_exmp)
                            self._report.append(_msg)

                if is_tuple(domain_arg):
                    _lexical = lexical.copy()
                    _cur_keys = ""
                    for index, sub_args in enumerate(get_args(domain_arg)):
                        key_add = False
                        if is_primitive(sub_args) and is_unbounded_primitive(sub_args):
                            # _lexical = _local_lexical.copy().add(sub_args)
                            _next_key = f'T_{index}'
                            _cur_keys += ", " + _next_key if _cur_keys else _next_key
                            key_add = True
                            _attr_def = f'              {_next_key} = NewType("{_next_key}", {sub_args.__name__})\n'
                            attr_exmp = f'                     {_lexical.field().name}: {LexicalPath._name(element)}' \
                                        f'[Tuple[{_cur_keys} ....]'
                            _msg = self._illegel_primitive_msg(lexical=_lexical,
                                                               field_name=_lexical.field().name,
                                                               field_type=sub_args.__name__,
                                                               field_origin=field_origin,
                                                               mapping_d_or_r='domain',
                                                               mapping_class="",
                                                               attr_def=_attr_def,
                                                               attr_exmp=attr_exmp)
                            self._report.append(_msg)
                        if not key_add:
                            _cur_keys += ", " + LexicalPath._name(sub_args) if _cur_keys else LexicalPath._name(
                                sub_args)

    def _illegel_primitive_msg(self,
                               lexical,
                               field_name,
                               field_type,
                               field_origin,
                               mapping_d_or_r=None,
                               mapping_class=None,
                               attr_def=None,
                               attr_exmp=None):
        _lexical = lexical

        part_of_mapping = ''
        if mapping_d_or_r:
            sl = '"'
            part_of_mapping = f' part of {sl + mapping_class + sl + " " if mapping_class else ""}{mapping_d_or_r}'

        _msg = f'{field_origin} "{field_name}" cannot accept unbounded types "{field_type}"{part_of_mapping}\n'

        _msg += f'  Possible Fix:\n' \
                f'     Change attribute "{f"{_lexical.path()}" if lexical.path() else _lexical.field().name}" type by defining a new type\n' \
                f'     A. import necessary package:\n' \
                f'            from typing import NewType\n' \
                f'     B. declare global variable\n' \
                f'             <variable> = NewType(\"variable\", {field_type})\n' \
                f'             where "variable" has a semantics that is part of the problem model\n' \
                f'             e.g.\n'

        if attr_def:
            _msg += attr_def + "\n"
        else:
            _msg += f'              {camelize(_lexical.last())} = NewType("{camelize(_lexical.last())}", {field_type})\n'
        _msg += f'              and update attribute type:\n'

        if attr_exmp:
            _msg += attr_exmp
        else:
            _msg += f'                   {_lexical.last()}: {self._parse_attr_type_exmp(_lexical.last())}'

        return _msg

    def report(self):
        _msg = ""
        for msg in self._report:
            _msg += f'{msg}\n\n'

        print(f'Verify "{self._cls.__name__}" static field types:')
        if _msg:
            print(f'{"=" * 50}\n{_msg}')
        else:
            print(f'  Verification passed\n')
