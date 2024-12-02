from typing import List, Optional, Tuple
from dataclasses import dataclass
from collections import deque

from utils import Coordinate, Direction, GameState


@dataclass(frozen=True)
class ResolutionState:
    pawns: List[Coordinate]
    cost: int
    previous_state: Optional["ResolutionState"] = None

    def __lt__(self, other: "ResolutionState") -> bool:
        return self.cost < other.cost

    def get_move_sequence(self) -> List[Tuple[int, int, int]]:
        """
        Reconstruct the sequence of moves from the state chain.
        :return: A list of moves in the format (pawn_id, target_x, target_y).
        """
        moves = []
        current = self
        while current.previous_state is not None:
            # Find what changed between current and previous state
            for pawn_id, (curr_pos, prev_pos) in enumerate(
                zip(current.pawns, current.previous_state.pawns)
            ):
                if curr_pos != prev_pos:
                    moves.append((pawn_id, curr_pos.x, curr_pos.y))
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
            string += (
                f"Move pawn {get_color_name(pawn_moved)} with a cost of {self.cost}:\n"
            )
        string += "\n".join(
            f"  Pawn {i}: ({pos.x}, {pos.y})" + (" <-" if i == pawn_moved else "")
            for i, pos in enumerate(self.pawns)
        )

        return string


def get_color_name(color_code):
    # Define color names for pawns
    colors = ["red", "green", "blue", "yellow"]
    return colors[color_code]


class AIPlayer:
    def __init__(self, state: "GameState"):
        self.name = "AI"
        self.state = state
        self.visited_positions = [[coords] for coords in self.state.pawns]

    def compute_choices(
        self, state: "ResolutionState", target_pawn_id: Optional[int] = None
    ) -> List[Tuple[int, int, int]]:
        """
        Compute all possible moves for the current state.
        :param state: The current state.
        :param target_pawn_id: If provided, only compute moves for this specific pawn.
        :return: A list of all possible moves in the format (pawn_id, target_x, target_y).
        """
        possible_moves = []
        pawn_ids = (
            [target_pawn_id] if target_pawn_id is not None else range(len(state.pawns))
        )

        for pawn_id in pawn_ids:
            for direction in Direction:
                target_coords = self._get_pawn_destination(state, pawn_id, direction)

                # Cond: target_coords != None AND (target_pawn_id != None => target_coords not in visited_positions[pawn_id])
                if target_coords is not None and (
                    target_pawn_id is None
                    or target_coords not in self.visited_positions[pawn_id]
                ):
                    possible_moves.append((pawn_id, target_coords.x, target_coords.y))
        return possible_moves

    def solve(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find a solution using a basic breadth-first search.
        :return: A list of moves in the format to reach the target. None if no solution is found. (pawn_id, target_x, target_y)
        """
        # Initialize queue and graph structure
        queue = deque([ResolutionState(pawns=self.state.pawns, cost=0)])
        # Get the target pawn id
        target_pawn_id = self.state.current_target[0]
        # Whether we are using the target pawn or not
        using_target_pawn = True
        # List of explored final states
        explored_states = []

        # Debug
        target_coords = self.get_chip_coordinates(*self.state.current_target)
        pawn_coords = self.state.pawns[target_pawn_id]
        print(
            "Target:",
            get_color_name(target_pawn_id),
            get_shape(self.state.current_target[1]),
            f"(at x={target_coords.x}, y={target_coords.y})",
            get_color_name(target_pawn_id),
            "pawn",
            f"(at x={pawn_coords.x}, y={pawn_coords.y})",
        )
        print(f"Starting search with {get_color_name(target_pawn_id)} pawn")

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
            for pawn_id, target_x, target_y in moves:
                has_valid_moves = True

                # Create new pawn positions list
                new_pawns = list(current_state.pawns)
                new_pawns[pawn_id] = Coordinate(x=target_x, y=target_y)

                # Track this position as visited for this pawn
                self.visited_positions[pawn_id].append(
                    Coordinate(x=target_x, y=target_y)
                )

                new_state = ResolutionState(
                    pawns=new_pawns,
                    cost=current_state.cost + 1,
                    previous_state=current_state,
                )

                queue.append(new_state)

            if not has_valid_moves:
                explored_states.append(current_state)

        print("Explored states:")
        for state in explored_states:
            print(state.get_move_sequence())
        return None

    def _is_solution(self, pawns: List[Coordinate]) -> bool:
        """
        Check if the target pawn has reached the target position.
        """
        target_pawn_id = self.state.current_target[0]
        target = self.get_chip_coordinates(*self.state.current_target)
        return pawns[target_pawn_id] == target

    def _get_pawn_destination(
        self,
        state: ResolutionState,
        pawn_id: int,
        direction: Direction,
        from_coords: Optional[Coordinate] = None,
    ) -> Optional[Coordinate]:
        """
        Get the destination coordinates for a pawn based on its direction.
        :param state: The current state.
        :param pawn_id: The id of the pawn.
        :param direction: The direction of the move (Direction enum).
        :param from_coords: A Coordinate to override the current position of the pawn used for mirror moves.
        :return: Target coordinates as a Coordinate or None if move is invalid.
        """
        pawn = state.pawns[pawn_id]
        if not pawn:
            return None

        current_coord = from_coords if from_coords else pawn
        x, y = current_coord.x, current_coord.y

        direction_deltas = {
            Direction.UP: (0, -1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
        }
        dx, dy = direction_deltas[direction]

        # Check if there's a wall in the current cell blocking movement in the current direction
        if self.state.walls[x][y][direction.value]:
            return Coordinate(x=x, y=y)

        # Move the pawn in the current direction until it hits a wall, another pawn or is reflected by a mirror
        while (
            0 <= x + dx < self.state.board_size and 0 <= y + dy < self.state.board_size
        ):
            x += dx
            y += dy

            # Check if the pawn is reflected by a mirror
            mirror = self.state.mirrors[x][y]
            if mirror[0] is not None:
                if pawn_id != mirror[0]:
                    continue
                new_direction = self._get_reflected_direction(direction, mirror[1])
                return self._get_pawn_destination(
                    state, pawn_id, new_direction, Coordinate(x=x, y=y)
                )

            # Check if the pawn is blocked by a wall
            if self.state.walls[x][y][direction.value]:
                return Coordinate(x=x, y=y)

            # Check if the pawn is blocked by another pawn
            if self._is_pawn_at(state, Coordinate(x=x, y=y)):
                return Coordinate(x=x - dx, y=y - dy)

        return Coordinate(x=x, y=y)

    @staticmethod
    def _is_pawn_at(state: ResolutionState, target_coords: Coordinate) -> bool:
        """
        Check if another pawn is at the target coordinates.
        :param target_coords: Coordinates to check.
        :return: True if a pawn is present, False otherwise.
        """
        return any(p == target_coords for p in state.pawns if p is not None)

    @staticmethod
    def _get_reflected_direction(direction: Direction, mirror_angle: int) -> Direction:
        """
        Get the new direction based on the mirror's angle.
        :param direction: Current direction of the pawn.
        :param mirror_angle: Angle of the mirror 45 (\) or 135 (/).
        :return: New direction after reflection.
        """
        reflection_map = {
            (Direction.UP, 45): Direction.LEFT,
            (Direction.UP, 135): Direction.RIGHT,
            (Direction.RIGHT, 135): Direction.UP,
            (Direction.RIGHT, 45): Direction.DOWN,
            (Direction.DOWN, 45): Direction.RIGHT,
            (Direction.DOWN, 135): Direction.LEFT,
            (Direction.LEFT, 45): Direction.UP,
            (Direction.LEFT, 135): Direction.DOWN,
        }
        if (direction, mirror_angle) not in reflection_map:
            raise ValueError(
                f"Invalid mirror angle or direction, got {direction}, {mirror_angle}"
            )
        return reflection_map[(direction, mirror_angle)]

    def get_chip_coordinates(self, color: int, chip: int) -> Coordinate:
        """
        Get the coordinates of a chip on the board.
        :param color: The color of the chip.
        :param chip: The chip number.
        :return: The coordinates of the chip. (x, y)
        """
        for x, col in enumerate(self.state.chips):
            for y, (c, ch) in enumerate(col):
                if c == color and ch == chip:
                    return Coordinate(x=x, y=y)
        raise ValueError(f"Chip {chip} of color {color} not found on the board.")


def get_shape(shape_code):
    # Define shape names
    shapes = ["circle", "square", "triangle", "star"]
    return shapes[shape_code]


if __name__ == "__main__":
    # Import GameRuntime for testing only
    from game_runtime import GameRuntime

    # Initialize GameRuntime
    runtime = GameRuntime()
    runtime.load_new_board()
    runtime.new_target()

    # Since GameBoard use grids with [y][x] indexing,
    # we need to adapt them by transposing the grids for [x][y] indexing.

    # Transpose the grids in GameState to use x, y indexing
    def transpose_grid(grid):
        return [list(col) for col in zip(*grid)]

    walls = transpose_grid(runtime.board.walls)
    mirrors = transpose_grid(runtime.board.mirrors)
    chips = transpose_grid(runtime.board.chips)

    # Extract data from GameRuntime to create GameState
    game_state = GameState(
        board_size=runtime.board.board_size,
        walls=walls,
        mirrors=mirrors,
        chips=chips,
        pawns=runtime.pawns,
        current_target=runtime.current_target,
    )

    # Initialize AIPlayer with GameState
    player = AIPlayer(game_state)

    # Solve the game
    solution = player.solve()
    print("Result:", solution, "\n")
