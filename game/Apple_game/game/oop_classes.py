
# oop_classes.py
# OOP concepts:
# GameObject -> Basket, FallingItem, FloatingText (Inheritance)
# FallingItem -> Apple, Heart (Inheritance + Polymorphism)
# Score (Encapsulation)
# Game (Composition)

import random
import pygame

from . import support as S
from game.base_game import Game as BaseGame


# ---------- 1. PARENT CLASS ----------
class GameObject:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def center(self):
        return (
            int(self.x + self.width / 2),
            int(self.y + self.height / 2)
        )

    def update(self):
        pass

    def draw(self, screen):
        pass


# ---------- 2. CHILD CLASSES ----------
class Basket(GameObject):

    def __init__(self):
        super().__init__(
            S.WIDTH // 2 - 55,
            S.HEIGHT - 80,
            110,
            46
        )
        self.speed = 9

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed

        self.x = max(
            0,
            min(S.WIDTH - self.width, self.x)
        )

    def draw(self, screen):
        r = self.get_rect()

        points = [
            (r.left, r.top),
            (r.right, r.top),
            (r.right - 14, r.bottom),
            (r.left + 14, r.bottom)
        ]

        pygame.draw.polygon(screen, (170, 105, 50), points)
        pygame.draw.polygon(screen, (110, 65, 30), points, 3)


class FloatingText(GameObject):
    """Text like +10 that floats up and disappears."""

    def __init__(self, text, pos, color, font):
        super().__init__(pos[0], pos[1], 0, 0)

        self.image = font.render(text, True, color)
        self.life = 40

    def update(self):
        self.y -= 1.5
        self.life -= 1

    def draw(self, screen):
        screen.blit(
            self.image,
            self.image.get_rect(center=(self.x, self.y))
        )


# ---------- 3. FALLING ITEM CLASS ----------
class FallingItem(GameObject):

    label = "Item"
    hint = ""
    SIZE = 34

    def __init__(self, speed):
        super().__init__(
            random.randint(0, S.WIDTH - self.SIZE),
            -self.SIZE,
            self.SIZE,
            self.SIZE
        )

        self.speed = speed

    def update(self):
        self.y += self.speed

    def is_off_screen(self):
        return self.y > S.HEIGHT - 20

    def on_catch(self, game):
        pass

    def on_miss(self, game):
        pass


# ---------- 4. APPLE CLASS ----------
class Apple(FallingItem):

    label = "Apple"
    hint = "+10 points. Miss it and you lose a life!"

    def on_catch(self, game):
        game.add_points(10, self.center())

    def on_miss(self, game):
        game.lose_life(self.center())

    def draw(self, screen):
        cx, cy = self.center()

        pygame.draw.circle(
            screen, S.RED, (cx, cy + 1), 15
        )

        pygame.draw.circle(
            screen, (255, 150, 160), (cx - 5, cy - 4), 4
        )

        pygame.draw.line(
            screen, (100, 60, 30),
            (cx, cy - 13), (cx + 2, cy - 21), 3
        )

        pygame.draw.ellipse(
            screen, (60, 170, 80),
            (cx + 2, cy - 22, 12, 7)
        )


# ---------- 5. HEART CLASS ----------
class Heart(FallingItem):

    label = "Heart"
    hint = "+1 life (you can have up to 5)."

    def on_catch(self, game):
        game.gain_life(self.center())

    def draw(self, screen):
        cx, cy = self.center()

        S.draw_heart(
            screen, cx, cy + 2, 40, (255, 90, 120)
        )


ITEM_TYPES = [Apple, Heart]


# ---------- 6. SCORE CLASS ----------
# Encapsulation: score data is stored in private variables.
class Score:

    def __init__(self):
        self._score = 0
        self._best = S.load_highscore()
        self._new_best = False

    @property
    def score(self):
        return self._score

    @property
    def best(self):
        return self._best

    @property
    def new_best(self):
        return self._new_best

    @property
    def level(self):
        return self._score // S.POINTS_PER_LEVEL + 1

    def add(self, points):
        self._score += points

        if self._score > self._best:
            self._best = self._score
            self._new_best = True

    def reset(self):
        self._score = 0
        self._new_best = False

    def save(self):
        S.save_highscore(self._best)


# ---------- 7. MAIN GAME CLASS ----------
# Inheritance: Game extends the arcade's BaseGame.
# Composition: Game manages Basket, Score, Apple, Heart and FloatingText.
class Game(BaseGame):

    def __init__(self, screen, player_name):
        super().__init__(screen, player_name)

        # Reuse the arcade's existing screen.
        self.screen = screen
        self.player_name = player_name

        pygame.font.init()

        self.clock = pygame.time.Clock()
        self.fonts = S.make_fonts()
        self.sky = S.make_sky()

        self.score = Score()
        self.basket = Basket()

        self.items = []
        self.texts = []

        self.lives = S.START_LIVES
        self.last_spawn = 0

        self.state = "menu"
        self.running = True

    def start_new_game(self):
        self.basket = Basket()
        self.items = []
        self.texts = []

        self.score.reset()
        self.lives = S.START_LIVES

        self.last_spawn = pygame.time.get_ticks()
        self.state = "playing"

    # Called when an apple is caught.
    def add_points(self, points, pos):
        self.score.add(points)

        self.texts.append(
            FloatingText(
                f"+{points}",
                pos,
                (255, 255, 255),
                self.fonts[1]
            )
        )

    # Called when an apple is missed.
    def lose_life(self, pos):
        self.lives -= 1

        self.texts.append(
            FloatingText(
                "MISSED!",
                pos,
                (255, 90, 90),
                self.fonts[1]
            )
        )

    # Called when a heart is caught.
    def gain_life(self, pos):
        self.lives = min(
            S.MAX_LIVES,
            self.lives + 1
        )

        self.texts.append(
            FloatingText(
                "+1 LIFE",
                pos,
                (255, 120, 150),
                self.fonts[1]
            )
        )

    # ---------- EVENT HANDLING ----------
    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_SPACE:

                    if self.state == "menu":
                        self.start_new_game()

                    elif self.state == "over":
                        self.running = False

    # ---------- GAME UPDATE ----------
    def update(self):

        if self.state != "playing":
            return

        self.basket.update()

        # Spawn new items.
        now = pygame.time.get_ticks()

        if now - self.last_spawn > max(
            380,
            1000 - (self.score.level - 1) * 70
        ):

            speed = min(
                9,
                3 + (self.score.level - 1) * 0.6
            )

            item_class = random.choices(
                ITEM_TYPES,
                weights=[85, 15]
            )[0]

            self.items.append(item_class(speed))
            self.last_spawn = now

        # Basket collision area.
        catch_area = pygame.Rect(
            int(self.basket.x) + 6,
            int(self.basket.y),
            98,
            22
        )

        # Update falling items.
        for item in self.items[:]:

            item.update()

            if item.get_rect().colliderect(catch_area):

                self.items.remove(item)

                # Polymorphism: Apple and Heart respond differently.
                item.on_catch(self)

            elif item.is_off_screen():

                self.items.remove(item)
                item.on_miss(self)

        # Update floating messages.
        for floating_text in self.texts[:]:

            floating_text.update()

            if floating_text.life <= 0:
                self.texts.remove(floating_text)

        # Game over condition.
        if self.lives <= 0:

            self.state = "over"
            self.score.save()

    # ---------- DRAWING ----------
    def draw(self):

        self.screen.blit(self.sky, (0, 0))

        S.draw_ground(self.screen)

        # Polymorphism: each object has its own draw method.
        for obj in self.items + [self.basket] + self.texts:
            obj.draw(self.screen)

        S.draw_hud(
            self.screen,
            self.fonts,
            self.score,
            self.lives
        )

        if self.state == "menu":

            S.draw_menu(
                self.screen,
                self.fonts,
                ITEM_TYPES
            )

        elif self.state == "over":

            S.draw_game_over(
                self.screen,
                self.fonts,
                self.score
            )

        pygame.display.flip()

    # ---------- GAME LOOP ----------
    def run(self):

        while self.running:

            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(S.FPS)

        # Return final score to the arcade GameManager.
        return self.score.score
