"""The apple."""
import math
import turtle

from . import settings as S

BASE_SCALE = S.CELL / 18


class Food:

    def __init__(self, area):
        self._area = area
        self._cell = (0, 0)                  # protected
        self._turtle = turtle.Turtle(visible=False)
        self._turtle.speed(0)
        self._turtle.penup()
        self._turtle.shape("apple")
        self._turtle.setheading(90)          # keep the stem pointing up
        self._turtle.shapesize(BASE_SCALE, BASE_SCALE, 1)
        self._turtle.hideturtle()

    def place(self, occupied):
        cell = self._area.random_free_cell(occupied)
        if cell is not None:
            self._cell = cell
            self._turtle.goto(self._area.to_xy(cell))

    def consumed(self, head_cell):
        return head_cell == self._cell

    def pulse(self, phase):
        scale = BASE_SCALE * (1 + 0.09 * math.sin(phase))
        self._turtle.shapesize(scale, scale, 1)

    def show(self):
        self._turtle.showturtle()

    def hide(self):
        self._turtle.hideturtle()
