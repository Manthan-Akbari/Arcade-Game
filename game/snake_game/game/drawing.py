"""Small drawing helpers shared by the UI classes."""
import math
import turtle


def make_pen():
    """A hidden turtle used only for drawing."""
    pen = turtle.Turtle(visible=False)
    pen.speed(0)
    pen.penup()
    pen.hideturtle()
    return pen


def rounded_rect_points(x, y, w, h, r, steps=6):
    """Points of a rounded rectangle whose bottom-left corner is (x, y)."""
    corners = [
        (x + w - r, y + r, -90),
        (x + w - r, y + h - r, 0),
        (x + r, y + h - r, 90),
        (x + r, y + r, 180),
    ]
    points = []
    for cx, cy, start in corners:
        for i in range(steps + 1):
            a = math.radians(start + 90 * i / steps)
            points.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return points


def draw_polygon(pen, points, fill=None, outline=None, width=1):
    pen.penup()
    pen.goto(points[0])
    pen.color(outline or fill or "white", fill or "white")
    pen.pensize(width)
    pen.pendown()
    if fill:
        pen.begin_fill()
    for p in points[1:]:
        pen.goto(p)
    pen.goto(points[0])
    if fill:
        pen.end_fill()
    pen.penup()


def draw_rounded_rect(pen, x, y, w, h, r, fill=None, outline=None, width=2):
    draw_polygon(pen, rounded_rect_points(x, y, w, h, r), fill, outline, width)


def lerp_color(c1, c2, t):
    """Blend two '#rrggbb' colours (t = 0 -> c1, t = 1 -> c2)."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    mixed = [round(a[i] + (b[i] - a[i]) * t) for i in range(3)]
    return "#{:02x}{:02x}{:02x}".format(*mixed)
