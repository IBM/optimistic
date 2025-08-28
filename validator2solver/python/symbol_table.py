from dataclasses import dataclass, field
from enum import Enum
from itertools import dropwhile, chain, product
from symtable import SymbolTable
from typing import Optional, Set, List

# File top-level frame

TOP_LEVEL_FRAME_NAME = '*module*'
MOCKUP_FRAME = '*mockup*'
PYTHON_BUILTIN_FRAME_NAME = '*python-builtins*'
CLASS_FRAME_PREFIX = 'Class '
FUNCTION_FRAME_PREFIX = 'Function '
COMPREHENSION_PREFIX = 'Comprehension_'
LIST_COMPREHENSION_PREFIX = f'{COMPREHENSION_PREFIX}List'
SET_COMPREHENSION_PREFIX = f'{COMPREHENSION_PREFIX}Set'
GEN_COMPREHENSION_PREFIX = f'{COMPREHENSION_PREFIX}Generator'
ROOT_LEXICAL_PATH = ''

_FRAME_KIND = {
    0: ['*Unknown*', 'UNKNOWN'],
    1: [PYTHON_BUILTIN_FRAME_NAME, 'BUILTIN'],
    2: [TOP_LEVEL_FRAME_NAME, 'MODULE'],
    3: [CLASS_FRAME_PREFIX, 'CLASS'],
    4: [FUNCTION_FRAME_PREFIX, 'FUNCTION'],
    5: [LIST_COMPREHENSION_PREFIX, 'COMPREHENSION_LIST'],
    6: [SET_COMPREHENSION_PREFIX, 'COMPREHENSION_SET'],
    7: [GEN_COMPREHENSION_PREFIX, 'COMPREHENSION_GEN'],
}

FrameKind = Enum(
    value='FrameKind',
    names=chain.from_iterable(
        product(v, [k]) for k, v in _FRAME_KIND.items()
    )
)


# class FrameKind(Enum):
#     UNKNOWN = 0
#     BUILTIN = 1
#     MODULE = 2
#     CLASS = 3
#     FUNCTION = 4
#     COMPREHENSION_LIST = 5
#     COMPREHENSION_SET = 6
#     COMPREHENSION_GEN = 7


@dataclass
class Variable:
    name: str
    type: Optional[str] = None

    def __hash__(self):
        return hash((self.name, self.type))

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.name == other.name and
                self.type == other.type
        )

    def describe(self) -> str:
        return f'{self.name}'


@dataclass
class Frame:
    name: str
    kind: FrameKind
    variables: Set[Variable] = field(default_factory=set)
    parent: 'Frame' = None
    children: List['Frame'] = field(default_factory=list)
    table: SymbolTable = None
    mockup: bool = False

    def __hash__(self):
        return hash((self.name, self.parent))

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.name == other.name
        )

    def describe(self) -> str:
        is_parent = self.parent.name if self.parent else 'None'
        suffix = f'{self.kind.name}-Mockup' if self.is_mockup() else f'{self.kind.name}'
        if len(self.variables) == 0:
            return f'Frame-{suffix} [{self.name} - Parent [{is_parent}] without local Variables'
        return f'Frame-{suffix} [{self.name}] - Parent [{is_parent}] : ({", ".join(sorted(v.describe() for v in list(self.variables)))})'

    def contains_variable(self, variable_name):
        return any(var.name == variable_name for var in self.variables)

    def contains_child(self, child):
        for ch in self.children:
            if ch.name == child.name:
                return ch
        return None

    def add_variables(self, variables):
        new_candidate = []
        for var in variables:
            if not self.contains_variable(var.name):
                new_candidate.append(var)
        self.variables = {*self.variables, *new_candidate}

    def find_variable(self, variable_name):
        return next((var for var in self.variables if var.name == variable_name),
                    None)

    def qualified_name(self):
        # if self.is_file():
        #     stripped = self.name.replace(TOP_LEVEL_FRAME_NAME, '').strip()
        #     return self.name.strip() if stripped == '' else stripped
        # if self.is_class():
        #     return self.name.replace(CLASS_FRAME_PREFIX, '').strip()
        # if self.is_function():
        #     return self.name.replace(FUNCTION_FRAME_PREFIX, '').strip()
        # if self.is_comprehension():
        #     if self.name.startswith(SET_COMPREHENSION_PREFIX):
        #         return self.name.replace(SET_COMPREHENSION_PREFIX, '').strip()
        #     if self.name.startswith(LIST_COMPREHENSION_PREFIX):
        #         return self.name.replace(LIST_COMPREHENSION_PREFIX, '').strip()
        #     if self.name.startswith(GEN_COMPREHENSION_PREFIX):
        #         return self.name.replace(GEN_COMPREHENSION_PREFIX, '').strip()
        # if self.is_mockup():
        #     return self.name.replace(MOCKUP_FRAME, '').strip()
        return self.name

    def module_name(self):
        root = self
        while root and not root.is_file():
            root = root.parent
        if root:
            return root.qualified_name()
        return ''

    def is_builtin(self):
        return self.kind == FrameKind.BUILTIN or self.name.lower().startswith(PYTHON_BUILTIN_FRAME_NAME)

    def is_file(self):
        return self.is_module()

    def is_module(self):
        return self.kind == FrameKind.MODULE or self.name.lower().startswith(TOP_LEVEL_FRAME_NAME)

    def is_class(self):
        return self.kind == FrameKind.CLASS or self.name.startswith(CLASS_FRAME_PREFIX)

    def is_function(self):
        return self.kind == FrameKind.FUNCTION or self.name.startswith(FUNCTION_FRAME_PREFIX)

    def is_comprehension(self):
        return self.kind == FrameKind.COMPREHENSION_SET or \
               self.kind == FrameKind.COMPREHENSION_GEN or \
               self.kind == FrameKind.COMPREHENSION_LIST or self.name.startswith(COMPREHENSION_PREFIX)

    def is_mockup(self):
        return self.mockup


@dataclass
class BindingScope:
    frame: Frame


def environment_path_of_var(var):
    return environment_path_from_frame(var.frame)


def environment_path_from_frame(frame):
    return lexical_path(frame, strip_builtin=False)


def lexical_path(frame, strip_builtin=False):
    """
    return tuple of frame qualified names ordered from leaf(exclusive) to root module(inclusive)
    """
    assert frame is not None
    path = []
    # frame = frame.parent
    while frame:
        name = frame.name if not frame.is_file() else frame.qualified_name()
        name = f'{frame.kind.name}{name}' if frame.is_class() or frame.is_function() or frame.is_comprehension() \
            else name
        if frame.is_builtin() and not strip_builtin:
            path.append(name)
        else:
            path.append(name)
        frame = frame.parent
    return tuple('' if len(path) == 0 else path)


def lexical_path_as_string(frame, strip_builtin=True):
    path = list(dropwhile(lambda s: s.startswith('*'), lexical_path(frame, strip_builtin)))
    return '.'.join(reversed(path)) if path and len(path) > 1 else '' if not len(path) else path[0]
