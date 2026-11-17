"""SnakeGame: ties every class together and runs the main loop."""
import time
import turtle
import tkinter as tk

from . import settings as S
from .food import Food
from .game_area import GameArea
from .hud import HUD, HINT
from .score import Score
from .snake import Snake


class SnakeGame:

    def __init__(self):
        self.area = GameArea()
        self.snake = Snake(self.area)
        self.player = self.snake              # Player reference to Snake
        self.food = Food(self.area)
        self.score = Score()
        self.hud = HUD(self.area)

        self.state = "ready"                  # ready | running | paused | over
        self._phase = 0.0

        self._bind_keys()
        self._new_round()

    # ---- keyboard --------------------------------------------------------
    def _bind_keys(self):
        screen = self.area.screen
        screen.listen()
        keys = {
            ("Up", "w", "W"): (0, -1),
            ("Down", "s", "S"): (0, 1),
            ("Left", "a", "A"): (-1, 0),
            ("Right", "d", "D"): (1, 0),
        }
        for names, (dx, dy) in keys.items():
            for name in names:
                screen.onkeypress(lambda dx=dx, dy=dy: self._turn(dx, dy), name)
        screen.onkeypress(self._space, "space")
        screen.onkeypress(self._space, "p")
        screen.onkeypress(screen.bye, "Escape")

    def _turn(self, dx, dy):
        if self.state == "over":
            return
        if self.state == "ready":
            self.state = "running"
            self.hud.hide_message()
            self.food.show()
        if self.state == "running":
            self.snake.set_direction(dx, dy)

    def _space(self):
        if self.state == "running":
            self.state = "paused"
            self.hud.set_hint("PAUSED  -  press SPACE to resume", S.GOLD)
        elif self.state == "paused":
            self.state = "running"
            self.hud.set_hint(HINT, S.TEXT_DIM)
        elif self.state == "over":
            self._new_round()

    # ---- rounds ----------------------------------------------------------
    def _new_round(self):
        self.snake.reset()
        self.snake.set_visible(True)
        self.score.reset()
        self.food.place(self.snake.cells)
        self.food.hide()
        self.state = "ready"
        self.hud.set_hint(HINT, S.TEXT_DIM)
        self._refresh_hud()
        self.hud.show_message(
            "SNAKE",
            ["Eat apples, grow longer, don't bite yourself!",
             "Press an arrow key or WASD to start"],
        )

    def _game_over(self):
        self.state = "over"
        self.score.save()
        for _ in range(3):                     # quick blink
            self.snake.set_visible(False)
            self.area.update()
            time.sleep(0.12)
            self.snake.set_visible(True)
            self.area.update()
            time.sleep(0.12)
        self.snake.set_visible(False)
        self.food.hide()

        if self.score.new_best:
            title, color, accent = "NEW HIGH SCORE!", S.GOLD, S.GOLD
        else:
            title, color, accent = "GAME OVER", S.DANGER, S.DANGER
        self.hud.show_message(
            title,
            [f"Score: {self.score.score}      Best: {self.score.highscore}",
             "Press SPACE to play again"],
            accent=accent, title_color=color,
        )

    def _refresh_hud(self):
        self.hud.update(self.score.score, self.score.highscore, self.score.level)

    def _eat(self):
        self.snake.grow()
        self.score.increase()
        self.food.place(self.snake.cells)
        self._refresh_hud()

    # ---- main loop (timer based, so the window stays responsive) ---------
    def _delay(self):
        return max(S.MIN_DELAY, S.BASE_DELAY - (self.score.level - 1) * S.SPEEDUP_PER_LEVEL)

    def _tick(self):
        try:
            if self.state == "running":
                self.snake.move()
                if self.snake.collision():
                    self._game_over()
                elif self.food.consumed(self.snake.head_cell):
                    self._eat()
            self.area.update()
            self.area.screen.ontimer(self._tick, self._delay())
        except (turtle.Terminator, tk.TclError):
            pass

    def _animate(self):
        try:
            if self.state == "running":
                self._phase += 0.35
                self.food.pulse(self._phase)
                self.area.update()
            self.area.screen.ontimer(self._animate, 40)
        except (turtle.Terminator, tk.TclError):
            pass

    def run(self):
        self.area.update()
        self._tick()
        self._animate()
        try:
            self.area.screen.mainloop()
        except (turtle.Terminator, tk.TclError):
            pass
