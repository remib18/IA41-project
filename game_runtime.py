import random
from typing import List, Tuple, Optional

from game_board import GameBoard


class GameRuntime:
    """
    This is the class that will be used to run Rasende Roboter game, also known as Ricochet Robots.
    """

    def __init__(self):
        self.board: Optional["GameBoard"] = None
        self.pawns: List[Tuple[int, int]] = []
        self.current_target: Optional[Tuple[int, int]] = None
        self.targets_history: List[Tuple[int, int]] = []
        self.boards_history: List[str] = []

    def new_target(self) -> None:
        """
        Generates a new random target for the game.
        The new target has not been selected before.
        Shape of the target: (color, chip)
        Set to none if no target is available.
        ""
        random_color = random.randint(0, self.board.number_of_colors - 1)
        random_chip = random.randint(0, self.board.number_of_chips - 1)

        # Check if the target has been selected before
        if (random_color, random_chip) in self.targets_history:
            return self.new_target()

        self.current_target = (random_color, random_chip)
        self.targets_history.append(self.current_target)
        """
        self.current_target = (0, 1)
        self.targets_history.append(self.current_target)

    def load_new_board(self) -> None:
        """
        Load a new board to the game.
        """
        new_board = GameBoard.get_random()

        # Check if the board has been selected before
        if new_board.get_seed() in self.boards_history:
            return self.load_new_board()

        self.board = new_board
        self.boards_history.append(self.board.get_seed())
        self.pawns = self.board.initial_pawns_position
