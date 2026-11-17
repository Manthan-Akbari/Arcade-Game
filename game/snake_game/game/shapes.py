
import math
from turtle import Shape

from .settings import (SNAKE_HEAD, SNAKE_HEAD_LINE)


def _circle(cx, cy, r, n=18):
    return [(cx + r * math.cos(2 * math.pi * i / n),
             cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _snake_head():
    shape = Shape("compound")

    # forked tongue (drawn first so the head covers its base)
    tongue = [(-0.8, 9), (-0.8, 15), (-3, 18), (0, 16.2),
              (3, 18), (0.8, 15), (0.8, 9)]
    shape.addcomponent(tongue, "#ff4d6d", "#ff4d6d")

    # head with a pointed snout
    head = [(0, 12), (5, 10), (9, 5), (10, -1), (8, -7), (4, -10),
            (0, -10.5), (-4, -10), (-8, -7), (-10, -1), (-9, 5), (-5, 10)]
    shape.addcomponent(head, SNAKE_HEAD, SNAKE_HEAD_LINE)

    # diamond pattern on top of the head
    shape.addcomponent([(0, 6), (3, 0), (0, -6), (-3, 0)], "#7fb800", "#7fb800")

    # eyes  pupils
    for side in (-1, 1):
        shape.addcomponent(_circle(side * 5.5, 4, 3.4), "white", "#3a5a00")
        shape.addcomponent(_circle(side * 5.5, 5.2, 1.7), "#111111", "#111111")
        shape.addcomponent(_circle(side * 1.8, 9.2, 0.8), "#2f4a00", "#2f4a00")
    return shape


def _snake_body():
    return Shape("polygon", _circle(0, 0, 11.5, 22))


def _apple():
    shape = Shape("compound")
    shape.addcomponent(_circle(0, -1, 8.5, 24), "#e63946", "#9d0208")
    shape.addcomponent(_circle(-3.5, 2.5, 2.2, 10), "#ff9aa2", "#ff9aa2")
    shape.addcomponent([(-0.8, 6), (0.8, 6), (1.2, 11), (-0.2, 11)],
                       "#6b4226", "#6b4226")
    shape.addcomponent([(1, 8.5), (5, 11.5), (8.5, 9.5), (5, 7)],
                       "#52b788", "#2d6a4f")
    return shape


def register_shapes(screen):
    screen.register_shape("snake_head", _snake_head())
    screen.register_shape("snake_body", _snake_body())
    screen.register_shape("apple", _apple())
