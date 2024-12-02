from typing import List, Tuple, Optional
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


@dataclass
class GameState:
    board_size: int
    walls: List[List[Tuple[bool, bool, bool, bool]]]
    mirrors: List[List[Tuple[Optional[int], Optional[int]]]]
    chips: List[List[Tuple[Optional[int], Optional[int]]]]
    pawns: List[Coordinate]
    current_target: Tuple[int, int]


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
