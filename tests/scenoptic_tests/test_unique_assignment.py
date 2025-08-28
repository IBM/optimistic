from dataclasses import dataclass
from typing import FrozenSet

from room_allocation.resource_allocation_bom import Assignment, UniqueAssignment, Activity, Resource, ResourceType


@dataclass(frozen=True)
class MyAssignment(Assignment):
    w1: int
    w2: int


@dataclass(frozen=True)
class S(UniqueAssignment):
    solution: FrozenSet[MyAssignment]


a1 = Activity()
a2 = Activity()
r1 = Resource(ResourceType())
r2 = Resource(ResourceType())
ma1 = MyAssignment(r1, a1, 1, 2)
ma1alt = MyAssignment(r1, a2, 1, 3)
ma2 = MyAssignment(r2, a2, 10, 20)
ma2alt = MyAssignment(r2, a1, 11, 21)
s = S(frozenset({ma1, ma2, ma1alt, ma2alt}))
assert s.has_unique_assignment(wrt=('w1', 'w2'))
assert s.unique_assignment(r1, 1, 2, wrt=('w1', 'w2')) is a1
assert s.unique_assignment(r1, 1, 3, wrt=('w1', 'w2')) is a2
assert s.unique_assignment(r2, 10, wrt=('w1',)) is a2
