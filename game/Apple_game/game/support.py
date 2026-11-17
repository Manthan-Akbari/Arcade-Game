
# support.py
# Settings, drawing functions and high-score file handling.

import os
import pygame


# ---------- SETTINGS ----------
WIDTH, HEIGHT = 900, 700

FPS = 60

START_LIVES = 3
MAX_LIVES = 5

POINTS_PER_LEVEL = 150


HIGHSCORE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "highscore.txt"
)


# ---------- COLOURS ----------
SKY_TOP = (90, 170, 235)
SKY_BOTTOM = (200, 235, 255)

GROUND = (86, 160, 80)

DARK_TEXT = (30, 40, 60)

WHITE = (255, 255, 255)
GOLD = (255, 200, 40)
RED = (220, 40, 50)


# ---------- HIGH SCORE FILE ----------
def load_highscore():

    try:
        with open(HIGHSCORE_FILE) as f:
            return int(f.read().strip())

    except (OSError, ValueError):
        return 0


def save_highscore(value):

    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(value))

    except OSError:
        pass


# ---------- DRAWING HELPERS ----------
def make_fonts():
    """Returns small, normal and big fonts."""

    return (
        pygame.font.SysFont("arial", 18, bold=True),
        pygame.font.SysFont("arial", 26, bold=True),
        pygame.font.SysFont("arial", 56, bold=True)
    )


def draw_text(
    surface,
    font,
    text,
    color,
    center=None,
    topleft=None
):

    image = font.render(text, True, color)

    rect = image.get_rect()

    if center:
        rect.center = center

    elif topleft:
        rect.topleft = topleft

    surface.blit(image, rect)


def draw_heart(surface, cx, cy, size, color):
    """A heart made using two circles and a triangle."""

    r = size // 4

    pygame.draw.circle(
        surface,
        color,
        (cx - r, cy - r // 2),
        r
    )

    pygame.draw.circle(
        surface,
        color,
        (cx + r, cy - r // 2),
        r
    )

    pygame.draw.polygon(
        surface,
        color,
        [
            (cx - 2 * r + 1, cy - r // 4),
            (cx + 2 * r - 1, cy - r // 4),
            (cx, cy + 2 * r)
        ]
    )


# ---------- BACKGROUND ----------
def make_sky():
    """Creates the background gradient once."""

    sky = pygame.Surface((WIDTH, HEIGHT))

    for y in range(HEIGHT):

        t = y / HEIGHT

        color = tuple(
            int(
                SKY_TOP[i] +
                (SKY_BOTTOM[i] - SKY_TOP[i]) * t
            )
            for i in range(3)
        )

        pygame.draw.line(
            sky,
            color,
            (0, y),
            (WIDTH, y)
        )

    return sky


def draw_ground(screen):

    pygame.draw.rect(
        screen,
        GROUND,
        (0, HEIGHT - 20, WIDTH, 20)
    )


# ---------- HUD ----------
def draw_hud(screen, fonts, score, lives):

    small, normal, _ = fonts

    draw_text(
        screen,
        normal,
        f"Score: {score.score}",
        DARK_TEXT,
        topleft=(20, 14)
    )

    draw_text(
        screen,
        normal,
        f"Level {score.level}",
        DARK_TEXT,
        center=(WIDTH // 2, 28)
    )

    draw_text(
        screen,
        small,
        f"Best: {score.best}",
        (150, 90, 0),
        center=(WIDTH // 2, 56)
    )

    for i in range(MAX_LIVES):

        color = (
            (235, 60, 90)
            if i < lives
            else (150, 160, 175)
        )

        draw_heart(
            screen,
            WIDTH - 30 - (MAX_LIVES - 1 - i) * 36,
            28,
            32,
            color
        )


# ---------- SCREEN CARD ----------
def _card(screen, width, height, accent):

    shade = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    shade.fill((10, 20, 40, 150))

    screen.blit(shade, (0, 0))

    box = pygame.Rect(0, 0, width, height)

    box.center = (WIDTH // 2, HEIGHT // 2)

    pygame.draw.rect(
        screen,
        (20, 40, 70),
        box,
        border_radius=24
    )

    pygame.draw.rect(
        screen,
        accent,
        box,
        4,
        border_radius=24
    )

    return box


# ---------- MENU SCREEN ----------
def draw_menu(screen, fonts, item_classes):

    small, normal, big = fonts

    box = _card(
        screen,
        720,
        340,
        (110, 210, 150)
    )

    draw_text(
        screen,
        big,
        "CATCH THE APPLES",
        WHITE,
        center=(box.centerx, box.top + 55)
    )

    draw_text(
        screen,
        small,
        "Move the basket with LEFT / RIGHT (or A / D).",
        (180, 210, 240),
        center=(box.centerx, box.top + 105)
    )

    y = box.top + 160

    for item_class in item_classes:

        item = item_class(0)

        item.x = box.left + 45
        item.y = y - 17

        item.draw(screen)

        draw_text(
            screen,
            small,
            item.label,
            WHITE,
            topleft=(box.left + 100, y - 14)
        )

        draw_text(
            screen,
            small,
            item.hint,
            (170, 200, 230),
            topleft=(box.left + 200, y - 14)
        )

        y += 50

    draw_text(
        screen,
        normal,
        "Press SPACE to start",
        (255, 220, 120),
        center=(box.centerx, box.bottom - 35)
    )


# ---------- GAME OVER SCREEN ----------
def draw_game_over(screen, fonts, score):

    _, normal, big = fonts

    accent = (
        GOLD
        if score.new_best
        else (230, 90, 90)
    )

    box = _card(
        screen,
        520,
        280,
        accent
    )

    title = (
        "NEW BEST SCORE!"
        if score.new_best
        else "GAME OVER"
    )

    draw_text(
        screen,
        big,
        title,
        accent,
        center=(box.centerx, box.top + 65)
    )

    draw_text(
        screen,
        normal,
        f"Score: {score.score}     Best: {score.best}",
        WHITE,
        center=(box.centerx, box.top + 135)
    )

    draw_text(
        screen,
        normal,
        "Press SPACE or ESC to return",
        (255, 220, 120),
        center=(box.centerx, box.top + 205)
    )
