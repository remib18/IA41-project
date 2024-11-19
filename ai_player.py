from typing import List, Tuple, Optional
from game_runtime import GameRuntime
from dataclasses import dataclass
from collections import deque

from game_window import GameWindow


@dataclass(frozen=True)
class ResolutionState:
    pawns: List[Tuple[int, int]]
    cost: int
    previous_state: Optional["ResolutionState"] = None

    def __lt__(self, other: "ResolutionState") -> bool:
        return self.cost < other.cost

    def get_move_sequence(self) -> List[Tuple[int, int, int]]:
        """
        Reconstruct the sequence of moves from the state chain.
        :return: A list of moves in the format (pawn_id, target_y, target_x).
        """
        moves = []
        current = self
        while current.previous_state is not None:
            # Find what changed between current and previous state
            for pawn_id, (curr_pos, prev_pos) in enumerate(
                zip(current.pawns, current.previous_state.pawns)
            ):
                if curr_pos != prev_pos:
                    moves.append((pawn_id, curr_pos[0], curr_pos[1]))
                    break
            current = current.previous_state
        return list(reversed(moves))

    def __str__(self):
        pawn_moved = None

        if self.previous_state:
            for i, (curr_pos, prev_pos) in enumerate(
                zip(self.pawns, self.previous_state.pawns)
            ):
                if curr_pos != prev_pos:
                    pawn_moved = i
                    break

        string = "\n\n"

        if pawn_moved is None:
            string += "Initial state:\n"
        else:
            string += f"Move pawn {GameWindow.get_color_name(pawn_moved)} with a cost of {self.cost}:\n"
        string += "\n".join(
            f"  Pawn {i}: {pos}" + (" <-" if i == pawn_moved else "")
            for i, pos in enumerate(self.pawns)
        )

        return string


class AIPlayer:
    def __init__(self, runtime: "GameRuntime"):
        self.name = "AI"
        self.runtime = runtime
        self.visited_positions = [[coords] for coords in runtime.pawns]

    def compute_choices(
        self, state: "ResolutionState", target_pawn_id: Optional[int] = None
    ) -> List[Tuple[int, int, int]]:
        """
        Compute all possible moves for the current runtime state.
        :param state: The current state of the game.
        :param target_pawn_id: If provided, only compute moves for this specific pawn.
        :return: A list of all possible moves in the format (pawn_id, target_y, target_x).
        """
        possible_moves = []
        pawn_ids = (
            [target_pawn_id] if target_pawn_id is not None else range(len(state.pawns))
        )

        for pawn_id in pawn_ids:
            for direction in range(4):
                target_coords = self._get_pawn_destination(state, pawn_id, direction)

                # Cond: target_coords != None AND (target_pawn_id != None => target_coords not in visited_positions[pawn_id])
                if target_coords is not None and (
                    target_pawn_id is None
                    or target_coords not in self.visited_positions[pawn_id]
                ):
                    possible_moves.append((pawn_id, target_coords[0], target_coords[1]))
        return possible_moves

    def solve(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find a solution using a basic breadth-first search.
        :return: A list of moves in the format to reach the target. None if no solution is found. (pawn_id, target_y, target_x)
        """
        # Initialize queue and graph structure
        queue = deque([ResolutionState(pawns=runtime.pawns, cost=0)])
        # Get the target pawn id
        target_pawn_id = self.runtime.current_target[0]
        # Whether we are using the target pawn or not
        using_target_pawn = True
        # List of explored final states
        explored_states = []

        # Debug (TODO: Remove)
        coords = self.runtime.board.get_chip_coordinates(*self.runtime.current_target)
        print(
            "Target:",
            GameWindow.get_color_name(target_pawn_id),
            GameWindow.get_shape(self.runtime.current_target[1]),
            "pawn",
            f"(at x={coords[1]}, y={coords[0]})",
        )
        print(f"Starting search with {GameWindow.get_color_name(target_pawn_id)} pawn")

        while queue:
            current_state = queue.popleft()

            # Check if we've reached the target
            if self._is_solution(current_state.pawns):
                return current_state.get_move_sequence()

            # Compute all possible moves
            moves = self.compute_choices(
                current_state, target_pawn_id if using_target_pawn else None
            )
            has_valid_moves = False

            # Try all possible moves
            for pawn_id, target_y, target_x in moves:
                has_valid_moves = True

                # Create new pawn positions list
                new_pawns = list(current_state.pawns)
                new_pawns[pawn_id] = (target_y, target_x)

                # Track this position as visited for this pawn
                self.visited_positions[pawn_id].append((target_y, target_x))

                new_state = ResolutionState(
                    pawns=new_pawns,
                    cost=current_state.cost + 1,
                    previous_state=current_state,
                )

                queue.append(new_state)

            if not has_valid_moves:
                explored_states.append(current_state)

            # If we've tried all possible moves with the target pawn and no solution was found, try with all pawns
            """if len(queue) == 0 and using_target_pawn:
                print(
                    "No solution found with target pawn, trying with all other pawns..."
                )
                using_target_pawn = False
                queue = deque([self.state])"""

        print("Explored states:")
        for state in explored_states:
            print(state.get_move_sequence())
        return None

    def _is_solution(self, pawns: List[Tuple[int, int]]) -> bool:
        """
        Check if the target pawn has reached the target position.
        """
        target_pawn_id = self.runtime.current_target[0]
        target = self.runtime.board.get_chip_coordinates(*self.runtime.current_target)
        return pawns[target_pawn_id] == target

    def _get_pawn_destination(
        self,
        state: ResolutionState,
        pawn_id: int,
        direction: int,
        from_coords: Optional[Tuple[int, int]] = None,
    ) -> Optional[Tuple[int, int]]:
        """
        Get the destination coordinates for a pawn based on its direction.
        :param state: The current state of the game.
        :param pawn_id: The id of the pawn.
        :param direction: The direction of the move (0: up, 1: right, 2: down, 3: left).
        :param from_coords: A tuple to override the current position of the pawn used for mirror moves.
        :return: Target coordinates as a tuple (target_y, target_x) or None if move is invalid.
        """
        pawn = state.pawns[pawn_id]
        board = self.runtime.board

        if not pawn or not board:
            return None

        y, x = from_coords if from_coords else pawn
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        dy, dx = directions[direction]

        # Check if there's a wall in the current cell blocking movement in the current direction
        if board.walls[y][x][direction]:
            return y, x

        # Move the pawn in the current direction until it hits a wall, another pawn or is reflected by a mirror
        while 0 <= y + dy < board.board_size and 0 <= x + dx < board.board_size:
            y, x = y + dy, x + dx

            # Check if the pawn is reflected by a mirror
            if (mirror := board.mirrors[y][x])[0] is not None:
                if pawn_id != mirror[0]:
                    continue
                new_direction = self._get_reflected_direction(direction, mirror[1])
                return self._get_pawn_destination(state, pawn_id, new_direction, (y, x))

            # Check if the pawn is blocked by a wall
            if board.walls[y][x][direction]:
                return y, x

            # Check if the pawn is blocked by another pawn
            if self._is_pawn_at(state, (y, x)):
                return y - dy, x - dx

        return y, x

    @staticmethod
    def _is_pawn_at(state: ResolutionState, target_coords: Tuple[int, int]) -> bool:
        """
        Check if another pawn is at the target coordinates.
        :param target_coords: Coordinates to check.
        :return: True if a pawn is present, False otherwise.
        """
        return any(p == target_coords for p in state.pawns if p is not None)

    @staticmethod
    def _get_reflected_direction(direction: int, mirror_angle: int) -> int:
        """
        Get the new direction based on the mirror's angle.
        :param direction: Current direction of the pawn.
        :param mirror_angle: Angle of the mirror (45, 135).
        :return: New direction after reflection.
        """
        reflection_map = {
            (0, 45): 3,
            (0, 135): 1,
            (1, 135): 0,
            (1, 45): 2,
            (2, 45): 1,
            (2, 135): 3,
            (3, 45): 0,
            (3, 135): 2,
        }
        if (direction, mirror_angle) not in reflection_map:
            raise ValueError(
                f"Invalid mirror angle or direction, got {direction}, {mirror_angle}"
            )
        return reflection_map[(direction, mirror_angle)]


if __name__ == "__main__":
    runtime = GameRuntime()
    runtime.load_new_board()
    while True:
        try:
            runtime.new_target()
        except Exception:  # No more targets available
            break
        player = AIPlayer(runtime)
        print("Result:", player.solve(), "\n")
