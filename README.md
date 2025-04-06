# Master 1 AI Project: Rasende Roboter Game Solver

This project serves as an introduction to AI game-solving techniques. It represents my initial draft before integrating work with the rest of the team.

We selected *Rasende Roboter* for its challenging gameplay mechanics, particularly the strategic movement of multiple pawns required to solve each challenge.

See [the final implementation](https://github.com/remib18/RasendeRoboter).

## Project Overview

### Current Features

- The project currently supports a single board configuration.
- The solving feature is still under development and not yet integrated into the UI.
- A mirror mechanic has been implemented, adding an extra layer of complexity. This feature can be easily disabled if needed (see the [Documentation](#documentation) section).

### Objectives

The project's primary objectives are:
1. Generate and manage game boards.
2. Develop AI to solve challenges efficiently.
3. Provide a user interface for interactive gameplay.

## Progress

### 1. Board Generation
- ✅ Static board generation (can be extended to generate random boards).
- ✅ Seed system to allow board regeneration.
- ❌ Random board generation with validation to avoid unsolvable scenarios (e.g., verifying solution existence).

### 2. Game Runtime
- ✅ Generate new targets and boards once challenges are solved.
- ✅ Manage game state transitions.
- ❌ Make this file the project entrypoint that runs the ui and AI components.

### 3. Game Window (UI)
- ✅ Basic board display.
- ❌ Player input to compete against the AI.
- ❌ Visual display of player/AI solutions.
- ❌ Support for additional shapes and colors for complex boards.

### 4. AI Player
- ✅ Data structure to store resolution states.
- ✅ Compute all possible moves for a given board and target.
- ✅ Implement pawn movement, including wall and mirror interactions.
- ✅ Detect solutions.
- ✅ Basic solving algorithm for simple scenarios (e.g., requiring 1-2 pawn movements).
- ❌ Advanced solving algorithm for complex, solvable cases.

## Installation

To run the project, ensure you have Python 3 installed with the following dependencies:

- **PyQt6** (version 6.7.1 or higher)

### How to Run

For now, the project components must be executed separately:

```bash
# Run the board UI
python ./game_window.py

# Run the game-solving algorithm
python ./ai_player.py
```

Once fully integrated, the project can be launched using:

```bash
python ./game_runtime.py
```

## Documentation

### Enabling/Disabling the Mirror Mechanic

To enable or disable the mirror feature, edit the `get_random` method in the `GameBoard` class (located in `game_board.py`).

- **Disable mirrors:** Set `number_of_mirrors=0`.
- **Enable mirrors:** Specify the number of mirrors per color (currently supports `0` or `2`).

Example:

```python
@staticmethod
def get_random():
    """
    Generate a random board.
    :return: A board object.
    """
    # Disable mirrors
    return GameBoard(number_of_mirrors=0)
    
    # Enable mirrors
    return GameBoard(number_of_mirrors=2)
```

## Authors

- [@remib18](https://www.github.com/remib18)
