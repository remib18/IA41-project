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
    """
    The size of the grid of the game board. (`board_size` x `board_size`)
    """

    walls: List[List[Tuple[bool, bool, bool, bool]]]
    """
    A grid representing each cell of the game board. Each cell has a tuple of 4 booleans representing the walls
    in the following order: (up, right, down, left).
    The grid must have the size of `board_size` x `board_size` and a cell in the grid must be accessible by `walls[x][y]`.
    """

    mirrors: List[List[Tuple[Optional[int], Optional[int]]]]
    """
    A grid representing each cell of the game board. Each cell has a tuple of 2 integers representing the mirrors.
    The grid must have the size of `board_size` x `board_size` and a cell in the grid must be accessible by `mirrors[x][y]`.
    The first integer represents the mirror color (0: red, 1: green, 2: blue, 3: yellow).
    The second integer represents the mirror angle(45: \, 135: /).
    If the cell has no mirror, the tuple is (None, None).
    """

    chips: List[List[Tuple[Optional[int], Optional[int]]]]
    """
    A grid representing each cell of the game board. Each cell has a tuple of 2 integers representing the chips.
    The grid must have the size of `board_size` x `board_size` and a cell in the grid must be accessible by `chips[x][y]`.
    The first integer represents the chip color (0: red, 1: green, 2: blue, 3: yellow).
    The second integer represents the chip shape (0: circle, 1: square, 2: triangle, 3: star).
    If the cell has no chip, the tuple is (None, None).
    """

    pawns: List[Coordinate]
    """
    A list of coordinates representing the pawns in the game.
    The list must be ordered by the color of the pawns in the following order: red, green, blue, yellow.
    Exemple:
    ```py
    [
        Coordinate(0, 0),  // Pawn red is at x=0, y=0
        Coordinate(0, 1),  // Pawn green is at x=0, y=1
        Coordinate(0, 2),  // Pawn blue is at x=0, y=2
        Coordinate(0, 3),  // Pawn yellow is at x=0, y=3
    ]
    ```
    """

    current_target: Tuple[int, int]
    """
    The current target of the game. The target is a tuple of 2 integers representing the target color and shape.
    The first integer represents the target color (0: red, 1: green, 2: blue, 3: yellow).
    The second integer represents the target shape (0: circle, 1: square, 2: triangle, 3: star).
    """


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
