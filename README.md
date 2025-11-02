# Minesweeper Game

A classic Minesweeper implementation using Python and Tkinter.

## Features

- Full graphical user interface
- Three difficulty levels
- Left-click to reveal cells
- Right-click to place/remove flags
- Flood-fill revealing of empty cells
- Color-coded numbers
- Win/lose detection

## Controls

- **Left Click**: Reveal a cell
- **Right Click**: Place/remove a flag
- **Reset Button**: Start a new game

## Difficulty Settings

The game comes with three preset difficulty levels:

- **Easy**: 9x9 grid with 10 mines
- **Medium**: 16x16 grid with 40 mines

To change the difficulty, modify the following constants in `minesweeper.py`:

```python
GAME_WIDTH = 9    # Width of the grid
GAME_HEIGHT = 9   # Height of the grid
NUM_MINES = 10    # Number of mines
```

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)

## Running the Game

```bash
python minesweeper.py
```

## Game Rules

1. The board contains hidden mines
2. Numbers reveal how many mines are adjacent to that cell
3. Use these numbers to deduce where mines are
4. Flag all mines and reveal all safe cells to win
5. Revealing a mine results in game over

## Implementation Details

The game is split into two main classes:

- `MinesweeperGame`: Handles game logic and state
- `MinesweeperApp`: Manages the GUI and user interactions

## License

This project is available as open source under the terms of the MIT License.
