"""The snake (inherits from Player)."""
import turtle

from . import settings as S
from .drawing import lerp_color
from .player import Player

HEAD_SCALE = S.CELL / 22
BODY_SCALE = S.CELL / 22 * 0.95

HEADINGS = {(1, 0): 0, (0, -1): 90, (-1, 0): 180, (0, 1): 270}


class Snake(Player):
    START_LENGTH = 3

    def __init__(self, area, name="Player"):
        super().__init__(name)                
        self.__area = area                    
        self.__cells = []                     
        self.__segments = []                  
        self.__direction = (1, 0)
        self.__next_direction = (1, 0)
        self.__pending_growth = 0
        self.reset()

    # ---- read-only info --------------------------------------------------
    @property
    def head_cell(self):
        return self.__cells[0]

    @property
    def cells(self):
        return tuple(self.__cells)

    @property
    def length(self):
        return len(self.__cells)

    # ---- building the turtles -------------------------------------------
    def __new_segment(self, index):
        t = turtle.Turtle(visible=False)
        t.speed(0)
        t.penup()
        if index == 0:
            t.shape("snake_head")
            t.shapesize(HEAD_SCALE, HEAD_SCALE, 1)
        else:
            t.shape("snake_body")
            t.shapesize(BODY_SCALE, BODY_SCALE, 1)
            base = lerp_color(S.SNAKE_BODY_START, S.SNAKE_BODY_END, min(index / 30, 1))
            if index % 2 == 0:                       # subtle scale pattern
                base = lerp_color(base, "#ffffff", 0.12)
            t.color(S.SNAKE_BODY_LINE, base)
        t.hideturtle()
        return t

    def __render(self):
        while len(self.__segments) < len(self.__cells):
            self.__segments.append(self.__new_segment(len(self.__segments)))
        for seg, cell in zip(self.__segments, self.__cells):
            seg.goto(self.__area.to_xy(cell))
            seg.showturtle()
        for seg in self.__segments[len(self.__cells):]:
            seg.hideturtle()
        self.__segments[0].setheading(HEADINGS[self.__direction])

    #  behaviour -
    def reset(self):
        c, r = self.__area.center_cell
        self.__cells = [(c - i, r) for i in range(self.START_LENGTH)]
        self.__direction = (1, 0)
        self.__next_direction = (1, 0)
        self.__pending_growth = 0
        self.__render()

    def set_direction(self, dx, dy):
        """Ignore a 180 degree turn."""
        if (dx, dy) == (-self.__direction[0], -self.__direction[1]):
            return
        self.__next_direction = (dx, dy)

    def move(self):                           # method overriding
        self.__direction = self.__next_direction
        dx, dy = self.__direction
        c, r = self.__cells[0]
        self.__cells.insert(0, self.__area.wrap(c + dx, r + dy))
        if self.__pending_growth > 0:
            self.__pending_growth -= 1
        else:
            self.__cells.pop()
        self.__render()

    def grow(self, amount=1):
        self.__pending_growth += amount

    def collision(self):
        return self.__cells[0] in self.__cells[1:]

    def set_visible(self, visible):
        for seg in self.__segments[:len(self.__cells)]:
            seg.showturtle() if visible else seg.hideturtle()
