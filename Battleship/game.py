import tkinter as tk
from tkinter import messagebox
import random
import sys
from typing import final
 
BOARD_SIZE = 5
MAX_GUESSES = 15
 
HIDDEN = 'O'
HIT = 'X'
MISS = '-'
SHIP_SHOWN = 'S'
 
SCORE_FILE = "battleship_scores.txt"
 
# ---------- Arcade theme (change these to match the other games) ----------
BG = "#0b0f1a"
PANEL = "#151b2e"
NEON_CYAN = "#00f5ff"
NEON_PINK = "#ff2e97"
NEON_YELLOW = "#ffe600"
NEON_GREEN = "#39ff14"
GREY = "#5c6370"
FONT_TITLE = ("Courier New", 22, "bold")
FONT_TEXT = ("Courier New", 12, "bold")
FONT_CELL = ("Courier New", 16, "bold")
 
 
class Ship:
    total_ships = 0
 
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.is_sunk = False
        Ship.total_ships += 1
 
    def take_damage(self):
        self.size -= 1
        if self.size <= 0:
            self.is_sunk = True
 
    def get_points(self):
        return 10
 
    @staticmethod
    def is_valid_size(size):
        return size > 0
 
    @classmethod
    def slice_to_base(cls, derived_ship):
        return cls(derived_ship.name, derived_ship.size)
 
 
class Submarine(Ship):
    def __init__(self):
        super().__init__("Submarine", 1)
 
    def get_points(self):
        return 30
 
 
class Destroyer(Ship):
    def __init__(self):
        super().__init__("Destroyer", 1)
 
    def get_points(self):
        return 20
 
 
@final
class Carrier(Ship):
    def __init__(self):
        super().__init__("Carrier", 1)
 
    def get_points(self):
        return 40
 
 
class BattleshipBoard:
 
    class Coordinate:
        def __init__(self, row, col):
            self.row = row
            self.col = col
 
    def __init__(self, size):
        self.size = size
        self.__grid = [[HIDDEN for _ in range(size)] for _ in range(size)]
        self.__positions = {}
        self.fleet = [Submarine(), Destroyer(), Carrier()]
 
    def __lshift__(self, stream):
        stream.write(f"Board Data: {self.size}x{self.size}, Fleet size: {len(self.fleet)}\n")
        return stream
 
    def place_ships(self):
        for ship in self.fleet:
            while True:
                spot = self.Coordinate(random.randint(0, self.size - 1),
                                       random.randint(0, self.size - 1))
                key = (spot.row, spot.col)
                if key not in self.__positions:
                    self.__positions[key] = ship
                    break
 
    def fire(self, row, col):
        if self.__grid[row][col] != HIDDEN:
            return "repeat", None
        ship = self.__positions.get((row, col))
        if ship is None:
            self.__grid[row][col] = MISS
            return "miss", None
        self.__grid[row][col] = HIT
        ship.take_damage()
        return "hit", ship
 
    def all_sunk(self):
        return all(ship.is_sunk for ship in self.fleet)
 
    def unfound_ship_cells(self):
        return [key for key in self.__positions if self.__grid[key[0]][key[1]] == HIDDEN]
 
 
class Player:
    def __init__(self, name):
        self.name = name
        self.__score = 0
        self.guesses_left = MAX_GUESSES
 
    @property
    def score(self):
        return self.__score
 
    def add_score(self, points):
        self.__score += points
 
    def use_guess(self):
        self.guesses_left -= 1
 
    def reset(self):
        self.__score = 0
        self.guesses_left = MAX_GUESSES
 
 
class BattleshipGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini Battleship")
        self.configure(bg=BG)
        self.resizable(False, False)
 
        self.player = Player("Player")
        self.board = BattleshipBoard(BOARD_SIZE)
        self.buttons = []
 
        self.build_screen()
        self.new_round()
 
    def build_screen(self):
        tk.Label(self, text="MINI BATTLESHIP", font=FONT_TITLE,
                 bg=BG, fg=NEON_CYAN).pack(pady=(15, 5))
 
        self.info_label = tk.Label(self, text="", font=FONT_TEXT, bg=BG, fg=NEON_YELLOW)
        self.info_label.pack(pady=5)
 
        grid_frame = tk.Frame(self, bg=PANEL, padx=10, pady=10)
        grid_frame.pack(padx=20, pady=10)
 
        for r in range(BOARD_SIZE):
            row_buttons = []
            for c in range(BOARD_SIZE):
                btn = tk.Button(grid_frame, text=HIDDEN, font=FONT_CELL, width=4, height=2,
                                bg=BG, fg=NEON_CYAN, activebackground=NEON_CYAN,
                                command=lambda row=r, col=c: self.on_click(row, col))
                btn.grid(row=r, column=c, padx=3, pady=3)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
 
        self.message_label = tk.Label(self, text="", font=FONT_TEXT, bg=BG, fg=NEON_GREEN)
        self.message_label.pack(pady=5)
 
        bottom = tk.Frame(self, bg=BG)
        bottom.pack(pady=(5, 15))
        tk.Button(bottom, text="RESTART", font=FONT_TEXT, bg=NEON_PINK, fg=BG,
                  command=self.new_round).grid(row=0, column=0, padx=10)
        tk.Button(bottom, text="QUIT", font=FONT_TEXT, bg=GREY, fg=BG,
                  command=self.destroy).grid(row=0, column=1, padx=10)
 
    def new_round(self):
        self.board = BattleshipBoard(BOARD_SIZE)
        self.board.place_ships()
        self.player.reset()
        self.board << sys.stdout
 
        for row_buttons in self.buttons:
            for btn in row_buttons:
                btn.config(text=HIDDEN, bg=BG, fg=NEON_CYAN, state="normal")
 
        self.message_label.config(text="Find all 3 ships!")
        self.refresh_info()
 
    def refresh_info(self):
        ships_left = sum(1 for ship in self.board.fleet if not ship.is_sunk)
        self.info_label.config(
            text=f"Guesses: {self.player.guesses_left}   "
                 f"Score: {self.player.score}   Ships left: {ships_left}")
 
    def on_click(self, row, col):
        status, ship = self.board.fire(row, col)
        if status == "repeat":
            self.message_label.config(text="Already fired there!")
            return
 
        self.player.use_guess()
        btn = self.buttons[row][col]
 
        if status == "miss":
            btn.config(text=MISS, bg=GREY, fg=BG)
            self.message_label.config(text="Miss!")
        else:
            btn.config(text=HIT, bg=NEON_PINK, fg=BG)
            if ship.is_sunk:
                points = ship.get_points()
                self.player.add_score(points)
                self.message_label.config(text=f"You sunk the {ship.name}! +{points}")
            else:
                self.message_label.config(text="Hit!")
 
        self.refresh_info()
        self.check_game_over()
 
    def check_game_over(self):
        if self.board.all_sunk():
            bonus = self.player.guesses_left * 5
            self.player.add_score(bonus)
            self.refresh_info()
            self.finish(f"YOU WIN! Bonus for unused guesses: +{bonus}")
        elif self.player.guesses_left == 0:
            self.finish("OUT OF GUESSES! GAME OVER")
 
    def finish(self, text):
        for row, col in self.board.unfound_ship_cells():
            self.buttons[row][col].config(text=SHIP_SHOWN, bg=NEON_YELLOW, fg=BG)
        for row_buttons in self.buttons:
            for btn in row_buttons:
                btn.config(state="disabled")
 
        self.message_label.config(text=text)
        self.save_score()
 
        again = messagebox.askyesno(
            "Game Over", f"{text}\n\n{self.player.name}, your score: {self.player.score}\n\nPlay again?")
        if again:
            self.new_round()
        else:
            self.destroy()
 
    def save_score(self):
        with open(SCORE_FILE, "a") as file:
            file.write(f"{self.player.name},{self.player.score}\n")
 
 
if __name__ == "__main__":
    game = BattleshipGame()
    game.mainloop()
 

