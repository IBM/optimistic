from dataclasses import dataclass

from typing import NewType

ResourceType = NewType('ResourceType', str)
Activity = NewType('Activity', str)


@dataclass(frozen=True)
class Resource:
    type: ResourceType


@dataclass(frozen=True)
class Assignment:
    resource: Resource
    activity: Activity
