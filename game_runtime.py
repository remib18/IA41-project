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
        """
        # List of reachable targets without moving any other pawn
        reachable_targets = [
            # (color, chip)
            (1, 0),  # Green - Circle
            (1, 2),  # Green - Triangle
            (2, 2),  # Blue - Triangle
            (2, 3),  # Blue - Star
            (3, 0),  # Yellow - Circle
            (3, 1),  # Yellow - Square
            (3, 2),  # Yellow - Triangle
            (3, 3),  # Yellow - Star
        ]

        # Remove targets that have been selected before
        reachable_targets = [
            target for target in reachable_targets if target not in self.targets_history
        ]

        # If no target is available, set the current target to None
        if not reachable_targets:
            self.current_target = None
            raise Exception(
                "No more targets available"
            )  # TODO: remove when app flow is implemented
            return

        # Random selected reachable target
        self.current_target = random.choice(reachable_targets)
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
