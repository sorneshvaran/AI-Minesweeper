import random
import os
import time
import tkinter as tk
from tkinter import messagebox

class MinesweeperGame:
    """
    Represents the Minesweeper game environment.
    This class knows where all the mines are.
    """
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.visible_board = [['U' for _ in range(width)] for _ in range(height)]
        self.game_over = False
        self.win = False
        self._place_mines()
        self._calculate_numbers()

    def _place_mines(self):
        """Randomly places mines on the board."""
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            if self.board[x][y] != -1:
                self.board[x][y] = -1
                mines_placed += 1

    def _calculate_numbers(self):
        """Calculates the numbers for all non-mine cells."""
        for x in range(self.height):
            for y in range(self.width):
                if self.board[x][y] == -1:
                    continue
                
                mine_count = 0
                for neighbor_x, neighbor_y in self._get_neighbors(x, y):
                    if self.board[neighbor_x][neighbor_y] == -1:
                        mine_count += 1
                self.board[x][y] = mine_count

    def _get_neighbors(self, x, y):
        """Helper to get all valid 8-directional neighbors."""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    neighbors.append((nx, ny))
        return neighbors

    def reveal(self, x, y):
        """
        User 'clicks' this cell. Returns the result.
        - Returns 'mine' if it's a mine.
        - Returns 'safe' if it's safe.
        - Returns None if the cell can't be revealed.
        """
        if self.visible_board[x][y] != 'U':
            return None # Can't reveal a flagged or already-revealed cell

        if self.board[x][y] == -1:
            self.game_over = True
            self.win = False
            self.visible_board[x][y] = '*'
            return 'mine'
        
        number = self.board[x][y]
        self.visible_board[x][y] = str(number)

        # Flood-fill if a '0' is revealed
        if number == 0:
            for nx, ny in self._get_neighbors(x, y):
                if self.visible_board[nx][ny] == 'U':
                    self.reveal(nx, ny)
        
        self._check_win_condition()
        return 'safe'

    def toggle_flag(self, x, y):
        """Toggles a flag on an unrevealed cell."""
        if self.visible_board[x][y] == 'U':
            self.visible_board[x][y] = 'F'
        elif self.visible_board[x][y] == 'F':
            self.visible_board[x][y] = 'U'

    def _check_win_condition(self):
        """Checks if the player has won."""
        revealed_count = 0
        for x in range(self.height):
            for y in range(self.width):
                # Count all revealed, non-mine cells
                if self.visible_board[x][y] != 'U' and self.visible_board[x][y] != 'F':
                    revealed_count += 1
        
        if revealed_count == (self.width * self.height) - self.num_mines:
            self.game_over = True
            self.win = True
    

class MinesweeperApp:
    """
    The main Tkinter application class.
    This creates the GUI and handles user clicks.
    """
    def __init__(self, root, width, height, num_mines):
        self.root = root
        self.width = width
        self.height = height
        self.num_mines = num_mines

        self.root.title("Minesweeper")
        
        # Define colors for numbers
        self.colors = {
            '1': '#0000FF', '2': '#008000', '3': '#FF0000',
            '4': '#00008B', '5': '#8B0000', '6': '#008B8B',
            '7': '#000000', '8': '#808080'
        }
        
        # --- Control Frame ---
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=5)
        
        self.reset_button = tk.Button(self.control_frame, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=10)
        
        # --- Game Frame ---
        self.game_frame = tk.Frame(root, bg="white")
        self.game_frame.pack()
        
        self.setup_game()

    def setup_game(self):
        """Initializes the game state, AI, and GUI grid."""
        # Clear old widgets if any
        for widget in self.game_frame.winfo_children():
            widget.destroy()
            
        self.game = MinesweeperGame(self.width, self.height, self.num_mines)
        
        # 2D list to hold the button widgets
        self.buttons = []
        for r in range(self.height):
            row_list = []
            for c in range(self.width):
                # Create a button for each cell
                btn = tk.Button(self.game_frame, text=" ", width=2, height=1, 
                                font=("Arial", 14, "bold"),
                                relief="raised")
                
                # Bind left-click and right-click events
                # Use a lambda to pass the specific row (r) and col (c)
                btn.bind("<Button-1>", lambda event, r=r, c=c: self.on_left_click(r, c))
                btn.bind("<Button-3>", lambda event, r=r, c=c: self.on_right_click(r, c))
                
                btn.grid(row=r, column=c)
                row_list.append(btn)
            self.buttons.append(row_list)

    def on_left_click(self, r, c):
        """Handles a user left-click on a cell."""
        if self.game.game_over:
            return

        result = self.game.reveal(r, c)
        self.update_gui()

        if self.game.game_over:
            self.show_game_over()

    def on_right_click(self, r, c):
        """Handles a user right-click to flag a cell."""
        if self.game.game_over:
            return
        
        self.game.toggle_flag(r, c)
        self.update_gui()

    def reset_game(self):
        """Resets the game to a new, fresh board."""
        self.setup_game()

    def update_gui(self):
        """Redraws the entire button grid based on the game's visible_board."""
        for r in range(self.height):
            for c in range(self.width):
                val = self.game.visible_board[r][c]
                btn = self.buttons[r][c]
                
                if val == 'U':
                    btn.config(text=" ", state="normal", relief="raised")
                elif val == 'F':
                    btn.config(text="🚩", state="normal", relief="raised")
                elif val == '*':
                    btn.config(text="💣", state="disabled", relief="sunken", bg="red")
                elif val.isdigit():
                    if val == '0':
                        btn.config(text=" ", state="disabled", relief="sunken", bg="#ddd")
                    else:
                        btn.config(text=val, state="disabled", relief="sunken", 
                                   disabledforeground=self.colors[val], bg="#ddd")

    def show_game_over(self):
        """Displays the final game result and disables the board."""
        # Disable all buttons
        for r in range(self.height):
            for c in range(self.width):
                self.buttons[r][c].config(state="disabled")
        
        # Reveal all mines if the player lost
        if not self.game.win:
            for r in range(self.height):
                for c in range(self.width):
                    if self.game.board[r][c] == -1 and self.game.visible_board[r][c] != 'F':
                        self.buttons[r][c].config(text="💣", bg="#aaa")

        if self.game.win:
            messagebox.showinfo("Game Over", "🎉 YOU WIN! 🎉")
        else:
            messagebox.showerror("Game Over", "💀 YOU LOST 💀")

            
# --- Run the Game ---
if __name__ == "__main__":
    # Settings: (width, height, num_mines)
    # Easy: (9, 9, 10)
    # Medium: (16, 16, 40)
    GAME_WIDTH = 9
    GAME_HEIGHT = 9
    NUM_MINES = 10
    
    root = tk.Tk()
    app = MinesweeperApp(root, GAME_WIDTH, GAME_HEIGHT, NUM_MINES)
    root.mainloop()

