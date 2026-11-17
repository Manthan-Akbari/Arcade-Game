"""Top score bar and the centre message card."""
from . import settings as S
from .drawing import make_pen, draw_polygon, draw_rounded_rect

CARD_W, CARD_H = 170, 56
BOX_W, BOX_H = 540, 200

HINT = "Arrows / WASD  move   |   SPACE  pause   |   ESC  quit"


class HUD:

    def __init__(self, area):
        self._area = area
        self._cy = area.hud_top - S.HUD_HEIGHT / 2
        self._card_x = {"SCORE": -190, "BEST": 0, "LEVEL": 190}

        self._static = make_pen()
        self._values = {name: make_pen() for name in self._card_x}
        self._hint = make_pen()
        self._box = make_pen()
        self._text = make_pen()

        self._draw_panel()
        self._draw_cards()
        self.set_hint(HINT, S.TEXT_DIM)

    # ---- static parts ----------------------------------------------------
    def _draw_panel(self):
        a, p = self._area, self._static
        w2 = a.width / 2
        draw_polygon(p, [(-w2, a.hud_bottom), (w2, a.hud_bottom),
                         (w2, a.hud_top), (-w2, a.hud_top)], fill=S.HUD_BG)
        draw_polygon(p, [(-w2, a.hud_bottom), (w2, a.hud_bottom)],
                     outline=S.HUD_LINE, width=3)
        # title with a soft shadow
        for dx, dy, col in ((2, -2, "#06130d"), (0, 0, S.ACCENT)):
            p.goto(a.left + dx, self._cy - 20 + dy)
            p.color(col)
            p.write("SNAKE", font=(S.FONT, 34, "bold"))

    def _draw_cards(self):
        p = self._static
        for name, x in self._card_x.items():
            draw_rounded_rect(p, x - CARD_W / 2, self._cy - CARD_H / 2,
                              CARD_W, CARD_H, 12, S.CARD_BG, S.CARD_LINE, 2)
            p.goto(x, self._cy + 9)
            p.color(S.TEXT_DIM)
            p.write(name, align="center", font=(S.FONT, 10, "bold"))

    # ---- dynamic parts ---------------------------------------------------
    def update(self, score, best, level):
        data = {"SCORE": (score, S.TEXT_BRIGHT),
                "BEST": (best, S.GOLD),
                "LEVEL": (level, S.ACCENT)}
        for name, (value, color) in data.items():
            pen = self._values[name]
            pen.clear()
            pen.goto(self._card_x[name], self._cy - 26)
            pen.color(color)
            pen.write(str(value), align="center", font=(S.FONT, 22, "bold"))

    def set_hint(self, text, color):
        self._hint.clear()
        if self._area.width < 1250:
            return
        self._hint.goto(self._area.right, self._cy - 8)
        self._hint.color(color)
        self._hint.write(text, align="right", font=(S.FONT, 11, "bold"))

    # ---- message card ----------------------------------------------------
    def show_message(self, title, lines, accent=S.ACCENT, title_color=S.TEXT_BRIGHT):
        self.hide_message()
        cy = self._area.top - 24 - BOX_H / 2
        draw_rounded_rect(self._box, -BOX_W / 2, cy - BOX_H / 2, BOX_W, BOX_H,
                          22, "#0b241a", accent, 4)
        self._text.goto(0, cy + 8)
        self._text.color(title_color)
        self._text.write(title, align="center", font=(S.FONT, 34, "bold"))
        for i, line in enumerate(lines):
            self._text.goto(0, cy - 28 - i * 26)
            self._text.color(S.TEXT_DIM)
            self._text.write(line, align="center", font=(S.FONT, 15, "normal"))

    def hide_message(self):
        self._box.clear()
        self._text.clear()
