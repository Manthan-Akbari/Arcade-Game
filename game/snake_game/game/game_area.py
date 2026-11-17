"""The window, the grid and the play-field background."""
import random
import turtle
import tkinter as tk

from . import settings as S
from .drawing import make_pen, draw_polygon
from .shapes import register_shapes


class GameArea:

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Snake Game")
        self.screen.bgcolor(S.BG_COLOR)
        self.screen.setup(width=1.0, height=1.0)     # use the whole screen
        self.screen.tracer(0)
        self._maximize()
        register_shapes(self.screen)
        self._measure()
        self._draw_background()

    # ---- window ----------------------------------------------------------
    def _maximize(self):
        try:
            root = self.screen.getcanvas().winfo_toplevel()
            try:
                root.state("zoomed")                  # Windows
            except tk.TclError:
                root.attributes("-zoomed", True)      # Linux
            root.update()
        except Exception:
            pass                                      # macOS: setup() is enough
        self.screen.update()

    def _measure(self):
        self.width = max(self.screen.window_width(), 800)
        self.height = max(self.screen.window_height(), 600)

        self.cols = int((self.width - 2 * S.FIELD_MARGIN) // S.CELL)
        self.rows = int((self.height - S.HUD_HEIGHT - 2 * S.FIELD_MARGIN) // S.CELL)

        field_w = self.cols * S.CELL
        field_h = self.rows * S.CELL

        self.hud_top = self.height / 2
        self.hud_bottom = self.hud_top - S.HUD_HEIGHT

        spare = self.height - S.HUD_HEIGHT - field_h
        self.left = -field_w / 2
        self.right = field_w / 2
        self.top = self.hud_bottom - spare / 2
        self.bottom = self.top - field_h

    def _draw_background(self):
        pen = make_pen()
        f = S.CELL
        # base colour
        draw_polygon(pen, [(self.left, self.bottom), (self.right, self.bottom),
                           (self.right, self.top), (self.left, self.top)],
                     fill=S.FIELD_A)
        # checkerboard
        tile = turtle.Turtle()
        tile.speed(0)
        tile.penup()
        tile.shape("square")
        tile.shapesize(f / 20, f / 20, 1)
        tile.color(S.FIELD_B)
        for r in range(self.rows):
            for c in range(self.cols):
                if (c + r) % 2 == 0:
                    tile.goto(self.to_xy((c, r)))
                    tile.stamp()
        tile.hideturtle()
        # glowing border
        pad = 3
        draw_polygon(pen, [(self.left - pad, self.bottom - pad),
                           (self.right + pad, self.bottom - pad),
                           (self.right + pad, self.top + pad),
                           (self.left - pad, self.top + pad)],
                     outline=S.FIELD_BORDER, width=5)

    # ---- grid helpers ----------------------------------------------------
    def to_xy(self, cell):
        c, r = cell
        return (self.left + (c + 0.5) * S.CELL, self.top - (r + 0.5) * S.CELL)

    def wrap(self, c, r):
        return (c % self.cols, r % self.rows)

    @property
    def center_cell(self):
        return (self.cols // 2, self.rows // 2)

    def random_free_cell(self, occupied):
        taken = set(occupied)
        free = [(c, r) for c in range(self.cols) for r in range(self.rows)
                if (c, r) not in taken]
        return random.choice(free) if free else None

    def update(self):
        self.screen.update()
