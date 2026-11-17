import os
import threading


class GameStats:
    # OOP: Encapsulation - shared score data is protected by a Lock.
    def __init__(self, highscore_file):
        self.highscore_file = highscore_file
        self.__lock = threading.Lock()
        self.__score = 0
        self.__high_score = self.__load_high_score()

    def __load_high_score(self):
        try:
            with open(self.highscore_file, "r", encoding="utf-8") as file:
                return int(file.read().strip() or 0)
        except (OSError, ValueError):
            return 0

    def update_score(self, score):
        # Only one thread can update/read these values at a time.
        with self.__lock:
            self.__score = score
            if score > self.__high_score:
                self.__high_score = score

    def snapshot(self):
        with self.__lock:
            return self.__score, self.__high_score


def monitor_task(stats, stop_event):
    """Background thread: persist a new high score without blocking gameplay."""
    saved_best = -1

    while not stop_event.is_set():
        current_score, best_score = stats.snapshot()

        if best_score != saved_best:
            try:
                os.makedirs(os.path.dirname(stats.highscore_file), exist_ok=True)
                with open(stats.highscore_file, "w", encoding="utf-8") as file:
                    file.write(str(best_score))
                saved_best = best_score
            except OSError as error:
                print("Could not save Flappy Bird high score:", error)

        stop_event.wait(1)
