"""Score, level and a high score that is saved between runs."""
from . import settings as S


class Score:

    def __init__(self, path=S.HIGHSCORE_FILE):
        self._path = path
        self._score = 0
        self._highscore = self._load()
        self._new_best = False

    # ---- properties ------------------------------------------------------
    @property
    def score(self):
        return self._score

    @property
    def highscore(self):
        return self._highscore

    @property
    def level(self):
        return self._score // S.POINTS_PER_LEVEL + 1

    @property
    def new_best(self):
        return self._new_best

    # ---- behaviour -------------------------------------------------------
    def increase(self, points=S.POINTS_PER_FOOD):
        self._score += points
        if self._score > self._highscore:
            self._highscore = self._score
            self._new_best = True

    def reset(self):
        self._score = 0
        self._new_best = False

    def save(self):
        try:
            with open(self._path, "w") as f:
                f.write(str(self._highscore))
        except OSError:
            pass

    def _load(self):
        try:
            with open(self._path) as f:
                return int(f.read().strip())
        except (OSError, ValueError):
            return 0
