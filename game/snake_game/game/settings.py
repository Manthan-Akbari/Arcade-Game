"""Central place for sizes, speeds, colours and fonts."""
import os

# ---- Layout -------------------------------------------------------------
CELL = 30            # size of one grid cell in pixels
HUD_HEIGHT = 88      # height of the top score bar
FIELD_MARGIN = 16    # minimum gap around the play field

# ---- Gameplay -----------------------------------------------------------
BASE_DELAY = 130     # ms between moves at level 1
MIN_DELAY = 55       # fastest speed
SPEEDUP_PER_LEVEL = 7
POINTS_PER_FOOD = 10
POINTS_PER_LEVEL = 50

HIGHSCORE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "highscore.txt"
)

# ---- Colours ------------------------------------------------------------
BG_COLOR = "#0d1f17"
HUD_BG = "#10291f"
HUD_LINE = "#1f6b4a"
CARD_BG = "#16382a"
CARD_LINE = "#2f8f64"

FIELD_A = "#173f2e"
FIELD_B = "#1b4735"
FIELD_BORDER = "#58e08b"

TEXT_DIM = "#8fc9a7"
TEXT_BRIGHT = "#f4fff8"
ACCENT = "#58e08b"
GOLD = "#ffd166"
DANGER = "#ff6b6b"

SNAKE_HEAD = "#a7e22e"
SNAKE_HEAD_LINE = "#4c7a00"
SNAKE_BODY_START = "#8ad13a"
SNAKE_BODY_END = "#2d9c5a"
SNAKE_BODY_LINE = "#1d6b3a"

# ---- Fonts --------------------------------------------------------------
FONT = "Arial"
