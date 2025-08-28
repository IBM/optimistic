from validator2solver.optimistic_factory import add_frame
from validator2solver.python.python_builtins import create_builtin_frame
from validator2solver.python.symbol_table import Frame, FrameKind, Variable


def add_import_frame(builtin=None, do_examples=False):
    buitlin_frame = builtin if builtin else create_builtin_frame()
    buitlin_frame = add_python_builtin_frame(buitlin_frame)
    buitlin_frame = add_optimistic_frames(buitlin_frame)
    if do_examples:
        buitlin_frame = add_room_allocation_frame(buitlin_frame)
    return buitlin_frame


def add_python_builtin_frame(builtin=None):
    buitlin_frame = builtin if builtin else create_builtin_frame()

    module_frame = add_frame(buitlin_frame, Frame(name=f'itertools', kind=FrameKind.MODULE,
                                                  variables={Variable('tee'), Variable('chain')}))
    class_frame = add_frame(module_frame, Frame(name='chain', kind=FrameKind.CLASS))
    add_frame(class_frame, Frame(name='from_iterable', kind=FrameKind.FUNCTION))

    module_frame = add_frame(buitlin_frame, Frame(name=f'datetime', kind=FrameKind.MODULE,
                                                  variables={Variable('datetime')}))
    add_frame(module_frame, Frame(name='datetime', kind=FrameKind.CLASS))

    module_frame = add_frame(buitlin_frame, Frame(name=f'operator', kind=FrameKind.MODULE,
                                                  variables={Variable('attrgetter')}))

    module_frame = add_frame(buitlin_frame, Frame(name=f'abc', kind=FrameKind.MODULE,
                                                  variables={Variable('ABC')}))
    add_frame(module_frame, Frame(name='ABC', kind=FrameKind.CLASS))

    module_frame = add_frame(buitlin_frame, Frame(name=f'typing', kind=FrameKind.MODULE,
                                                  variables={Variable('Sequence'),
                                                             Variable('Collection'),
                                                             Variable('Mapping'),
                                                             Variable('Set'),
                                                             Variable('Any'),
                                                             Variable('Tuple'),
                                                             Variable('NewType'),
                                                             Variable('FrozenSet')}))
    add_frame(module_frame, Frame(name='Sequence', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='Collection', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='Mapping', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='Set', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='Any', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='Tuple', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='NewType', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='FrozenSet', kind=FrameKind.CLASS))

    # FIXME:? putting this remark here for future reference
    #       The following can replace typing.Mapping in python 3.9, make sure that when searching for frame
    #       when using "typing.Mapping" in problem model, we get "typing.Mapping" instance frame
    #       and not the "collections.abc.Mapping" frame,
    #       This has happened when the following declarations of collection.abc.Mapping is declared before
    #        "typing.Mapping" declaration in the above lines.
    #       Adding the following after the "typing" above declaration solved the search algorithm issue,
    #       but this may appear in future changes
    module_first_frame = add_frame(buitlin_frame, Frame(name=f'collections', kind=FrameKind.MODULE,
                                                        variables={Variable('abc')}))
    module_frame = add_frame(module_first_frame, Frame(name=f'abc', kind=FrameKind.MODULE,
                                                       variables={Variable('Mapping')}))
    add_frame(module_frame, Frame(name='Mapping', kind=FrameKind.CLASS))

    add_frame(buitlin_frame, Frame(name=f'math', kind=FrameKind.MODULE,
                                   variables={Variable('ceil'), Variable('pow')}))

    module_frame = add_frame(buitlin_frame, Frame(name=f'dataclasses', kind=FrameKind.MODULE,
                                                  variables={Variable('dataclass'), Variable('Field'),
                                                             Variable('field'), Variable('fields'),
                                                             Variable('asdict')
                                                             }))
    add_frame(module_frame, Frame(name='Field', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='dataclass', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='field', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='fields', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='addict', kind=FrameKind.FUNCTION))

    return buitlin_frame


def add_optimistic_frames(builtin=None):
    buitlin_frame = builtin if builtin else create_builtin_frame()

    module_first_frame = add_frame(buitlin_frame, Frame(name=f'optimistic_client', kind=FrameKind.MODULE,
                                                        variables={Variable('optimization')}))
    module_frame = add_frame(module_first_frame, Frame(name=f'optimization', kind=FrameKind.MODULE,
                                                       variables={Variable('OptimizationProblem'),
                                                                  # FIXME: remove unused variables
                                                                  Variable('TotalFunction'),
                                                                  Variable('PartialFunction'),
                                                                  Variable('TotalMapping'),
                                                                  Variable('implies'),
                                                                  Variable('equals')}))
    add_frame(module_frame, Frame(name='TotalFunction', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='PartialFunction', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='TotalMapping', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='implies', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='equals', kind=FrameKind.FUNCTION))

    class_frame = add_frame(module_frame, Frame(name='OptimizationProblem', kind=FrameKind.CLASS,
                                                variables={Variable('check_constraints'),
                                                           Variable('compute_objective')}))
    add_frame(class_frame, Frame(name='check_constraints', kind=FrameKind.FUNCTION))
    add_frame(class_frame, Frame(name='compute_objective', kind=FrameKind.FUNCTION))

    module_first_frame = add_frame(buitlin_frame, Frame(name=f'optimistic_client', kind=FrameKind.MODULE,
                                                        variables={Variable('unique_assignment')}))
    module_frame = add_frame(module_first_frame, Frame(name=f'unique_assignment', kind=FrameKind.MODULE,
                                                       variables={Variable('UniqueAssignment'),
                                                                  Variable('assignment')}))
    add_frame(module_frame, Frame(name='assignment', kind=FrameKind.FUNCTION))
    class_frame = add_frame(module_frame, Frame(name='UniqueAssignment', kind=FrameKind.CLASS,
                                                variables={Variable('has_unique_assignment'),
                                                           Variable('unique_assignment'),
                                                           Variable('non_unique_assignment')}))
    add_frame(class_frame, Frame(name='has_unique_assignment', kind=FrameKind.FUNCTION))
    add_frame(class_frame, Frame(name='unique_assignment', kind=FrameKind.FUNCTION))
    add_frame(class_frame, Frame(name='non_unique_assignment', kind=FrameKind.FUNCTION))

    module_first_frame = add_frame(buitlin_frame, Frame(name=f'optimistic_client', kind=FrameKind.MODULE,
                                                        variables={Variable('unique_solution')}))
    module_frame = add_frame(module_first_frame, Frame(name=f'unique_solution', kind=FrameKind.MODULE,
                                                       variables={Variable('unique_solution'),
                                                                  Variable('solution_attribute')}))

    add_frame(module_frame, Frame(name='unique_solution', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='solution_attribute', kind=FrameKind.FUNCTION))

    module_first_frame = add_frame(buitlin_frame, Frame(name=f'optimistic_client', kind=FrameKind.MODULE,
                                                        variables={Variable('meta')}))
    module_second_frame = add_frame(module_first_frame, Frame(name=f'meta', kind=FrameKind.MODULE,
                                                              variables={Variable('utils'),
                                                                         Variable('infrastructure')}))
    module_frame = add_frame(module_second_frame, Frame(name=f'utils', kind=FrameKind.MODULE,
                                                        variables={Variable('count'),
                                                                   Variable('memoize_method'),
                                                                   Variable('metadata'),
                                                                   Variable('builtin'),
                                                                   Variable('constraint'),
                                                                   Variable('minimize'),
                                                                   Variable('maximize'),
                                                                   Variable('record'),
                                                                   Variable('solution_variable')}))
    add_frame(module_frame, Frame(name='count', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='memoize_method', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='metadata', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='builtin', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='constraint', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='minimize', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='maximize', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='record', kind=FrameKind.FUNCTION))
    add_frame(module_frame, Frame(name='solution_variable', kind=FrameKind.FUNCTION))

    module_frame = add_frame(module_second_frame, Frame(name=f'infrastructure', kind=FrameKind.MODULE,
                                                        variables={Variable('KeepMembersMixin')}))
    class_frame = add_frame(module_frame, Frame(name='KeepMembersMixin', kind=FrameKind.CLASS,
                                                variables={Variable('members')}))
    add_frame(module_second_frame, module_frame)
    add_frame(module_frame, class_frame)
    add_frame(class_frame, Frame(name='members', kind=FrameKind.FUNCTION))

    return buitlin_frame


def add_room_allocation_frame(builtin=None):
    buitlin_frame = builtin if builtin else create_builtin_frame()

    module_first_frame = add_frame(buitlin_frame, Frame(name=f'optimistic_examples', kind=FrameKind.MODULE,
                                                        variables={Variable('room_allocation')}))
    module_second_frame = add_frame(module_first_frame, Frame(name=f'room_allocation', kind=FrameKind.MODULE,
                                                              variables={Variable('room_allocation_bom_2'),
                                                                         Variable('resource_allocation_bom'),
                                                                         Variable('resource_allocation_bom_2')}))
    module_frame = add_frame(module_second_frame, Frame(name=f'room_allocation_bom_2', kind=FrameKind.MODULE,
                                                        variables={Variable('EmployeeType'), Variable('OfficeType')}))
    add_frame(module_frame, Frame(name='EmployeeType', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='OfficeType', kind=FrameKind.CLASS, variables={Variable('members')}))

    module_frame = add_frame(module_second_frame, Frame(name=f'resource_allocation_bom', kind=FrameKind.MODULE,
                                                        variables={Variable('Resource'), Variable('Assignment')}))
    add_frame(module_frame, Frame(name='Resource', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='Assignment', kind=FrameKind.CLASS))

    module_frame = add_frame(module_second_frame, Frame(name=f'resource_allocation_bom_2', kind=FrameKind.MODULE,
                                                        variables={Variable('Resource'), Variable('Assignment')}))
    add_frame(module_frame, Frame(name='Resource', kind=FrameKind.CLASS))
    add_frame(module_frame, Frame(name='Assignment', kind=FrameKind.CLASS))

    return buitlin_frame
