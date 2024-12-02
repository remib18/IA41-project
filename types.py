from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
