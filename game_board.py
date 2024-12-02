from typing import List, Tuple, Union

from utils import Coordinate


class GameBoard:
    def __init__(
        self,
        board_size: int = 16,
        number_of_colors: int = 4,
        number_of_chips: int = 4,
        number_of_mirrors: int = 2,
        walls=None,
        chips=None,
        mirrors=None,
        initial_pawns_position=None,
    ):
        # Prevent unexpected values => TODO: Enable user defined values
        if (
            board_size != 16
            or number_of_colors != 4
            or number_of_chips != 4
            or (number_of_mirrors != 2 and number_of_mirrors != 0)
        ):
            raise ValueError(
                "Only the default values are currently supported. You can only disable or enable mirrors."
            )

        self.board_size = board_size
        self.number_of_colors = number_of_colors
        self.number_of_chips = number_of_chips
        self.number_of_mirrors = number_of_mirrors
        self.walls: List[List[Tuple[bool, bool, bool, bool]]] = []
        self.chips: List[List[Tuple[Union[int, None], Union[int, None]]]] = []
        self.mirrors: List[List[Tuple[Union[int, None], Union[int, None]]]] = []

        # Generate the walls, chips and mirrors for the board
        self.walls = self.generate_walls()
        self.chips = self.generate_chips()
        self.mirrors = self.generate_mirrors()
        self.initial_pawns_position = self.set_initial_pawns_position()

    def get_chip_coordinates(self, color: int, chip: int) -> Coordinate:
        """
        Get the coordinates of a chip on the board.
        :param color: The color of the chip.
        :param chip: The chip number.
        :return: The coordinates of the chip. (y, x)
        """
        for y, row in enumerate(self.chips):
            for x, (c, ch) in enumerate(row):
                if c == color and ch == chip:
                    return Coordinate(x=x, y=y)
        raise ValueError(f"Chip {chip} of color {color} not found on the board.")

    def generate_walls(self) -> List[List[Tuple[bool, bool, bool, bool]]]:
        """
        Generate the walls for a board based on the given parameters.

        :return: a board grid with the walls from a cell perspective (north, east, south, west)
        """

        # Generate a board grid with no walls
        board = [
            [(False, False, False, False) for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]

        # Compute the center zone span (regardless if even or odd board size)
        is_even = self.board_size % 2 == 0
        center = self.board_size // 2
        center_start = center - 1
        center_end = center if is_even else center + 1

        # Add walls around the center zone
        for row in range(center_start, center_end + 1):
            for col in range(center_start, center_end + 1):
                # Add walls if on the border of the center zone
                if row == center_start:
                    # Add a north wall
                    board[row][col] = (
                        True,
                        board[row][col][1],
                        board[row][col][2],
                        board[row][col][3],
                    )
                    # Add a south wall to the above cell
                    if row - 1 >= 0:
                        board[row - 1][col] = (
                            board[row - 1][col][0],
                            board[row - 1][col][1],
                            True,
                            board[row - 1][col][3],
                        )
                if row == center_end:
                    # Add a south wall
                    board[row][col] = (
                        board[row][col][0],
                        board[row][col][1],
                        True,
                        board[row][col][3],
                    )
                    # Add a north wall to the below cell
                    if row + 1 < self.board_size:
                        board[row + 1][col] = (
                            True,
                            board[row + 1][col][1],
                            board[row + 1][col][2],
                            board[row + 1][col][3],
                        )
                if col == center_start:
                    # Add a west wall
                    board[row][col] = (
                        board[row][col][0],
                        board[row][col][1],
                        board[row][col][2],
                        True,
                    )
                    # Add an east wall to the left cell
                    if col - 1 >= 0:
                        board[row][col - 1] = (
                            board[row][col - 1][0],
                            True,
                            board[row][col - 1][2],
                            board[row][col - 1][3],
                        )
                if col == center_end:
                    # Add an east wall
                    board[row][col] = (
                        board[row][col][0],
                        True,
                        board[row][col][2],
                        board[row][col][3],
                    )
                    # Add a west wall to the right cell
                    if col + 1 < self.board_size:
                        board[row][col + 1] = (
                            board[row][col + 1][0],
                            board[row][col + 1][1],
                            board[row][col + 1][2],
                            True,
                        )

        # Walls around the board
        for row in range(self.board_size):
            end = self.board_size - 1
            if row == 0:
                # Add a north wall
                for col in range(self.board_size):
                    board[row][col] = (
                        True,
                        board[row][col][1],
                        board[row][col][2],
                        board[row][col][3],
                    )
            if row == end:
                # Add a south wall
                for col in range(self.board_size):
                    board[row][col] = (
                        board[row][col][0],
                        board[row][col][1],
                        True,
                        board[row][col][3],
                    )
            # Add a west wall
            board[row][0] = (board[row][0][0], board[row][0][1], board[row][0][2], True)
            # Add an east wall
            board[row][end] = (
                board[row][end][0],
                True,
                board[row][end][2],
                board[row][end][3],
            )

        # Generate a pre-defined board walls declaration => TODO: Generate random walls
        horizontal = [
            (1, 10),
            (2, 0),
            (2, 6),
            (2, 12),
            (3, 2),
            (4, 3),
            (4, 15),
            (5, 5),
            (5, 8),
            (5, 13),
            (8, 4),
            (8, 11),
            (8, 15),
            (9, 0),
            (9, 14),
            (12, 6),
            (12, 10),
            (13, 9),
            (14, 3),
        ]
        vertical = [
            (0, 4),
            (0, 8),
            (1, 9),
            (2, 6),
            (2, 12),
            (3, 11),
            (4, 2),
            (5, 7),
            (6, 4),
            (5, 13),
            (8, 10),
            (9, 4),
            (10, 14),
            (12, 6),
            (13, 5),
            (13, 9),
            (14, 2),
            (15, 5),
            (15, 12),
        ]

        # Write the walls into the board
        for row, col in horizontal:
            board[row][col] = (
                board[row][col][0],
                board[row][col][1],
                True,
                board[row][col][3],
            )
            if row < self.board_size - 1:
                board[row + 1][col] = (
                    True,
                    board[row + 1][col][1],
                    board[row + 1][col][2],
                    board[row + 1][col][3],
                )
        for row, col in vertical:
            board[row][col] = (
                board[row][col][0],
                True,
                board[row][col][2],
                board[row][col][3],
            )
            if col < self.board_size - 1:
                board[row][col + 1] = (
                    board[row][col + 1][0],
                    board[row][col + 1][1],
                    board[row][col + 1][2],
                    True,
                )

        return board

    def generate_chips(self) -> List[List[Tuple[Union[int, None], Union[int, None]]]]:
        """
        Generate the chips for a board based on the given parameters.

        :return: a board grid with the chips from a cell perspective (color, chip)
        """
        # Generate a pre-defined board chips declaration => TODO: Generate random chips
        chips_positions = [
            [(1, 10), (4, 3), (10, 14), (14, 3)],  # Red
            [(3, 12), (4, 2), (13, 6), (13, 10)],  # Green
            [(2, 6), (2, 12), (8, 11), (12, 6)],  # Blue
            [(6, 5), (6, 13), (9, 4), (13, 9)],  # Yellow
        ]

        # Map the chips to the board grid
        board = [
            [(None, None) for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]
        for color, chips_of_color in enumerate(chips_positions):
            for chip, (y, x) in enumerate(chips_of_color):
                board[y][x] = (color, chip)

        return board

    def generate_mirrors(self) -> List[List[Tuple[Union[int, None], Union[int, None]]]]:
        """
        Generate the mirrors for a board based on the given parameters.

        Note: forwards mirrors angle is 135°, backwards mirrors angle is 45°

        :return: a board grid with the mirrors (colors, angle) from a cell perspective
        """
        if self.number_of_mirrors == 0:
            return [
                [(None, None) for _ in range(self.board_size)]
                for _ in range(self.board_size)
            ]

        # Generate a pre-defined board mirrors declaration => TODO: Generate random mirrors
        mirrors_positions = [
            [(2, 14, 45), (11, 8, 135)],  # Red
            [(3, 9, 45), (11, 1, 135)],  # Green
            [(1, 4, 135), (14, 13, 45)],  # Blue
            [(3, 6, 135), (10, 7, 45)],  # Yellow
        ]

        # Map the mirrors to the board grid
        board = [
            [(None, None) for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]
        for color, mirrors_of_color in enumerate(mirrors_positions):
            for _chip, (y, x, angle) in enumerate(mirrors_of_color):
                board[y][x] = (color, angle)

        return board

    def set_initial_pawns_position(self) -> List[Coordinate]:
        """
        Set the initial position of the pawns on the board.

        :return: a list of Coordinate with the initial position of the pawns
        """
        # Generate a pre-defined board pawns declaration => TODO: Generate random pawns
        pawns_positions = [
            (5, 1),  # Red
            (10, 12),  # Green
            (12, 1),  # Blue
            (4, 14),  # Yellow
        ]
        return [Coordinate(x=x, y=y) for y, x in pawns_positions]

    def get_seed(self) -> str:
        """
        Get the seed for the current board configuration.
        :return: The seed for the current board configuration
        """
        # Converting board properties to hexadecimal values
        hex_board_size = format(self.board_size, "x")
        hex_number_of_colors = format(self.number_of_colors, "x")
        hex_number_of_chips = format(self.number_of_chips, "x")
        hex_number_of_mirrors = format(self.number_of_mirrors, "x")

        # Serialize walls, chips, mirrors, and pawns in custom format
        hex_walls = ";".join(
            [
                f"{i},{j},{wall}"
                for i, row in enumerate(self.walls)
                for j, cell in enumerate(row)
                for wall, exists in enumerate(cell)
                if exists
            ]
        )
        hex_chips = ";".join(
            [
                f"{i},{j},{color},{chip}"
                for i, row in enumerate(self.chips)
                for j, (color, chip) in enumerate(row)
                if color is not None
            ]
        )
        hex_mirrors = ";".join(
            [
                f"{i},{j},{color},{angle}"
                for i, row in enumerate(self.mirrors)
                for j, (color, angle) in enumerate(row)
                if color is not None
            ]
        )
        hex_pawns = ";".join(
            [f"{coord.y},{coord.x}" for coord in self.initial_pawns_position]
        )

        # Combine all into a single string with separators
        seed_string = f"{hex_board_size}-{hex_number_of_colors}-{hex_number_of_chips}-{hex_number_of_mirrors}|{hex_walls}|{hex_chips}|{hex_mirrors}|{hex_pawns}"
        return seed_string

    @staticmethod
    def from_seed(seed: str) -> "GameBoard":
        """
        Generate a board from a given seed.
        :param seed: The seed to generate the board from.
        :return: A board object.
        """
        # Split the seed into its components
        parts = seed.split("|")
        main_parts = parts[0].split("-")

        board_size = int(main_parts[0], 16)
        number_of_colors = int(main_parts[1], 16)
        number_of_chips = int(main_parts[2], 16)
        number_of_mirrors = int(main_parts[3], 16)

        # Deserialize walls, chips, mirrors, and pawns
        walls = [
            [(False, False, False, False) for _ in range(board_size)]
            for _ in range(board_size)
        ]
        for wall_entry in parts[1].split(";"):
            if wall_entry:
                i, j, wall = map(int, wall_entry.split(","))
                walls[i][j] = tuple(
                    True if w == wall else walls[i][j][w] for w in range(4)
                )

        chips = [[(None, None) for _ in range(board_size)] for _ in range(board_size)]
        for chip_entry in parts[2].split(";"):
            if chip_entry:
                i, j, color, chip = map(int, chip_entry.split(","))
                chips[i][j] = (color, chip)

        mirrors = [[(None, None) for _ in range(board_size)] for _ in range(board_size)]
        for mirror_entry in parts[3].split(";"):
            if mirror_entry:
                i, j, color, angle = map(int, mirror_entry.split(","))
                mirrors[i][j] = (color, angle)

        initial_pawns_position = []
        for pawn_entry in parts[4].split(";"):
            if pawn_entry:
                y, x = map(int, pawn_entry.split(","))
                initial_pawns_position.append(Coordinate(x=x, y=y))

        return GameBoard(
            board_size=board_size,
            number_of_colors=number_of_colors,
            number_of_chips=number_of_chips,
            number_of_mirrors=number_of_mirrors,
            walls=walls,
            chips=chips,
            mirrors=mirrors,
            initial_pawns_position=initial_pawns_position,
        )

    @staticmethod
    def get_random():
        """
        Generate a random board.
        :return: A board object.
        """
        # TODO: Implement random board generation
        return GameBoard()


if __name__ == "__main__":
    # Create a board
    board = GameBoard()

    # Get the seed for the board
    seed = board.get_seed()
    print(f"Seed: {seed}")

    # Create a new board from the seed
    new_board = GameBoard.from_seed(seed)

    # Check if the new board is the same as the original one
    assert new_board.get_seed() == seed
    print("The board was successfully generated from the seed.")
