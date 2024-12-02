from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
