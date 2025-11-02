# Minesweeper Game

A classic Minesweeper implementation using Python and Tkinter.

## Features

- Full graphical user interface
- Left-click to reveal cells
- Right-click to place/remove flags
- Flood-fill revealing of empty cells
- Color-coded numbers
- Win/lose detection with emoji feedback
- Reset game functionality

## Controls

- **Left Click**: Reveal a cell
- **Right Click**: Place/remove a flag 🚩
- **Reset Button**: Start a new game

## Game Configuration

The game runs on a 9x9 grid with 10 mines. To modify these settings, you can adjust the following constants in `minesweeper.py`:

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
