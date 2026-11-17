import random
import pygame
from typing import final

from game.base_game import Game as BaseGame

BOARD_SIZE = 5
MAX_GUESSES = 15

HIDDEN = "O"
HIT = "X"
MISS = "-"
SHIP_SHOWN = "S"

BG = (11, 15, 26)
PANEL = (21, 27, 46)
NEON_CYAN = (0, 245, 255)
NEON_PINK = (255, 46, 151)
NEON_YELLOW = (255, 230, 0)
NEON_GREEN = (57, 255, 20)
GREY = (92, 99, 112)
WHITE = (235, 240, 250)


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

    def place_ships(self):
        for ship in self.fleet:
            while True:
                spot = self.Coordinate(
                    random.randint(0, self.size - 1),
                    random.randint(0, self.size - 1)
                )
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

    def cell_value(self, row, col):
        return self.__grid[row][col]

    def is_ship_at(self, row, col):
        return (row, col) in self.__positions


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


class BattleshipGame(BaseGame):
    """Mini Battleship adapted to run inside the Pygame arcade."""

    def __init__(self, screen, player_name):
        super().__init__(screen, player_name)

        self.screen = screen
        self.player = Player(player_name)
        self.width, self.height = screen.get_size()

        self.title_font = pygame.font.Font(None, 58)
        self.info_font = pygame.font.Font(None, 27)
        self.cell_font = pygame.font.Font(None, 48)
        self.message_font = pygame.font.Font(None, 28)
        self.help_font = pygame.font.Font(None, 23)

        self.cell_size = min(88, (self.height - 250) // BOARD_SIZE)
        self.board_size_px = self.cell_size * BOARD_SIZE
        self.board_x = (self.width - self.board_size_px) // 2
        self.board_y = 185

        self.message = "Find all 3 ships!"
        self.game_over = False
        self.game_over_message = ""
        self.running = True

        self.new_round()

    def new_round(self):
        self.board = BattleshipBoard(BOARD_SIZE)
        self.board.place_ships()
        self.player.reset()
        self.message = "Find all 3 ships!"
        self.game_over = False
        self.game_over_message = ""

    def draw_text(self, text, font, color, center):
        surface = font.render(text, True, color)
        self.screen.blit(surface, surface.get_rect(center=center))

    def get_cell_rect(self, row, col):
        return pygame.Rect(
            self.board_x + col * self.cell_size,
            self.board_y + row * self.cell_size,
            self.cell_size - 5,
            self.cell_size - 5
        )

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = self.get_cell_rect(row, col)
                value = self.board.cell_value(row, col)

                if self.game_over and value == HIDDEN and self.board.is_ship_at(row, col):
                    value = SHIP_SHOWN

                if value == HIT:
                    color, text_color = NEON_PINK, BG
                elif value == MISS:
                    color, text_color = GREY, WHITE
                elif value == SHIP_SHOWN:
                    color, text_color = NEON_YELLOW, BG
                else:
                    color, text_color = PANEL, NEON_CYAN

                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                pygame.draw.rect(
                    self.screen, NEON_CYAN, rect, width=2, border_radius=8
                )
                self.draw_text(value, self.cell_font, text_color, rect.center)

    def draw(self):
        self.screen.fill(BG)
        self.draw_text(
            "MINI BATTLESHIP", self.title_font, NEON_CYAN,
            (self.width // 2, 48)
        )

        ships_left = sum(1 for ship in self.board.fleet if not ship.is_sunk)
        info = (
            f"Player: {self.player.name}   "
            f"Guesses: {self.player.guesses_left}   "
            f"Score: {self.player.score}   Ships: {ships_left}"
        )
        self.draw_text(
            info, self.info_font, NEON_YELLOW, (self.width // 2, 115)
        )

        self.draw_board()
        self.draw_text(
            self.message, self.message_font,
            NEON_GREEN if self.game_over else WHITE,
            (self.width // 2, self.board_y + self.board_size_px + 30)
        )

        if self.game_over:
            self.draw_text(
                self.game_over_message, self.message_font, NEON_YELLOW,
                (self.width // 2, self.height - 75)
            )
            help_text = "Press R to play again  |  ESC to return"
        else:
            help_text = "Click a cell to fire  |  Press ESC to return"

        self.draw_text(
            help_text, self.help_font, GREY,
            (self.width // 2, self.height - 30)
        )

    def handle_click(self, position):
        if self.game_over:
            return

        mouse_x, mouse_y = position
        board_right = self.board_x + self.board_size_px
        board_bottom = self.board_y + self.board_size_px

        if not (self.board_x <= mouse_x < board_right and
                self.board_y <= mouse_y < board_bottom):
            return

        col = (mouse_x - self.board_x) // self.cell_size
        row = (mouse_y - self.board_y) // self.cell_size

        if row >= BOARD_SIZE or col >= BOARD_SIZE:
            return

        status, ship = self.board.fire(row, col)
        if status == "repeat":
            self.message = "Already fired there!"
            return

        self.player.use_guess()

        if status == "miss":
            self.message = "Miss!"
        elif ship.is_sunk:
            points = ship.get_points()
            self.player.add_score(points)
            self.message = f"You sunk the {ship.name}! +{points}"
        else:
            self.message = "Hit!"

        self.check_game_over()

    def check_game_over(self):
        if self.board.all_sunk():
            bonus = self.player.guesses_left * 5
            self.player.add_score(bonus)
            self.finish(f"YOU WIN! Unused guesses bonus: +{bonus}")
        elif self.player.guesses_left == 0:
            self.finish("OUT OF GUESSES! GAME OVER")

    def finish(self, message):
        self.game_over = True
        self.game_over_message = message
        self.message = f"Final score: {self.player.score}"

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.event.post(event)
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r and self.game_over:
                        self.new_round()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            self.draw()
            pygame.display.flip()
            clock.tick(60)

        self.score = self.player.score
        return self.score

# Standalone testing entry point.
# When this file is imported by the arcade, this block will not execute.
if __name__ == "__main__":
    pygame.init()

    standalone_screen = pygame.display.set_mode((900, 700))
    pygame.display.set_caption("Mini Battleship")

    standalone_game = BattleshipGame(standalone_screen, "Player")
    standalone_game.run()

    # Pygame is shut down only for standalone execution.
    pygame.quit()

