from dataclasses import dataclass


@dataclass
class RoomType:
    max_occupancy: int


@dataclass
class Floor:
    designator: str


@dataclass
class Room:
    designator: str
    type: RoomType
    floor: Floor
