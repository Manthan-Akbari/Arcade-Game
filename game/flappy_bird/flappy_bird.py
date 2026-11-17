from pathlib import Path
import random
import threading

import pygame

from game.base_game import Game
from game.flappy_bird.FBThreading import GameStats, monitor_task


class Bird(pygame.sprite.Sprite):
    # OOP: Inheritance - Bird is a Pygame Sprite.
    def __init__(self, x, y, asset_dir):
        super().__init__()
        self.images = [
            pygame.image.load(str(asset_dir / f"bird{i}.png")).convert_alpha()
            for i in range(1, 4)
        ]
        self.image_index = 0
        self.animation_counter = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def flap(self):
        self.velocity = -10

    def update(self, flying, game_over, ground_y):
        if flying and self.rect.bottom < ground_y:
            self.velocity = min(self.velocity + 0.5, 10)
            self.rect.y += int(self.velocity)

        if not game_over:
            self.animation_counter += 1
            if self.animation_counter > 7:
                self.animation_counter = 0
                self.image_index = (self.image_index + 1) % len(self.images)

            self.image = pygame.transform.rotate(
                self.images[self.image_index], self.velocity * -2.5
            )
        else:
            self.image = pygame.transform.rotate(
                self.images[self.image_index], -90
            )


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, asset_dir, pipe_gap):
        super().__init__()
        self.image = pygame.image.load(str(asset_dir / "pipe.png")).convert_alpha()
        self.rect = self.image.get_rect()

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - pipe_gap // 2)
        else:
            self.rect.topleft = (x, y + pipe_gap // 2)

    def update(self, game_over, scroll_speed):
        if not game_over:
            self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class FlappyBirdGame(Game):
    # OOP: Inheritance - uses the common Game interface expected by GameManager.
    def __init__(self, screen, player_name):
        super().__init__(screen, player_name)

        self.asset_dir = Path(__file__).resolve().parent / "assets"
        self.width, self.height = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.fps = 50

        self.white = (255, 255, 255)
        self.font = pygame.font.SysFont("Bauhaus 93", 50)
        self.small_font = pygame.font.SysFont("Bauhaus 93", 28)

        self.background = pygame.image.load(
            str(self.asset_dir / "BG.png")
        ).convert()
        self.ground_image = pygame.image.load(
            str(self.asset_dir / "GR.png")
        ).convert_alpha()

        self.ground_width = self.ground_image.get_width()
        self.ground_y = self.height - self.ground_image.get_height()

        self.scroll_speed = 3
        self.ground_scroll = 0
        self.pipe_gap = 200
        self.pipe_frequency = 1700
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency

        self.flying = False
        self.game_over = False
        self.pass_pipe = False
        self.running = True

        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.bird = Bird(100, self.height // 2, self.asset_dir)
        self.bird_group.add(self.bird)

        # Threading: background monitor saves the game's personal high score.
        project_root = Path(__file__).resolve().parents[2]
        highscore_path = project_root / "data" / "flappy_bird_highscore.txt"
        self.stats = GameStats(highscore_path)
        self.stop_event = threading.Event()
        self.monitor = threading.Thread(
            target=monitor_task,
            args=(self.stats, self.stop_event),
            name="FlappyStatsMonitor",
            daemon=True
        )

    def reset_game(self):
        self.pipe_group.empty()
        self.bird.rect.x = 100
        self.bird.rect.y = self.height // 2
        self.bird.velocity = 0
        self.score = 0
        self.pass_pipe = False
        self.flying = False
        self.game_over = False
        self.ground_scroll = 0
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Put QUIT back so the main Arcade App can process it.
                pygame.event.post(event)
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if not self.game_over:
                        self.flying = True
                        self.bird.flap()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_over:
                    # The Arcade has its own Play Again button.
                    self.running = False
                else:
                    self.flying = True
                    self.bird.flap()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.bird_group.draw(self.screen)
        self.pipe_group.draw(self.screen)

        self.screen.blit(self.ground_image, (self.ground_scroll, self.ground_y))
        self.screen.blit(
            self.ground_image,
            (self.ground_scroll + self.ground_width, self.ground_y)
        )

        score_image = self.font.render(str(self.score), True, self.white)
        self.screen.blit(
            score_image,
            (self.width // 2 - score_image.get_width() // 2, 25)
        )

        _, best_score = self.stats.snapshot()
        best_image = self.small_font.render(
            f"BEST: {best_score}", True, self.white
        )
        self.screen.blit(best_image, (20, 20))

        if not self.flying and not self.game_over:
            instruction = self.small_font.render(
                "CLICK OR PRESS SPACE TO FLY", True, self.white
            )
            self.screen.blit(
                instruction,
                (self.width // 2 - instruction.get_width() // 2, self.height // 2 + 100)
            )

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 115))
            self.screen.blit(overlay, (0, 0))

            title = self.font.render("GAME OVER", True, self.white)
            hint = self.small_font.render(
                "CLICK OR PRESS ESC TO RETURN", True, self.white
            )
            self.screen.blit(
                title,
                (self.width // 2 - title.get_width() // 2, self.height // 2 - 60)
            )
            self.screen.blit(
                hint,
                (self.width // 2 - hint.get_width() // 2, self.height // 2 + 5)
            )

        pygame.display.flip()

    def update(self):
        self.bird_group.update(self.flying, self.game_over, self.ground_y)
        self.pipe_group.update(self.game_over, self.scroll_speed)

        # Score increases after the bird completely passes a pipe.
        pipes = self.pipe_group.sprites()
        if pipes:
            first_pipe = pipes[0]
            if (
                self.bird.rect.left > first_pipe.rect.left
                and self.bird.rect.right < first_pipe.rect.right
                and not self.pass_pipe
            ):
                self.pass_pipe = True

            if self.pass_pipe and self.bird.rect.left > first_pipe.rect.right:
                self.score += 1
                self.pass_pipe = False

        self.stats.update_score(self.score)

        # Collision detection.
        if (
            pygame.sprite.spritecollide(self.bird, self.pipe_group, False)
            or self.bird.rect.top < 0
            or self.bird.rect.bottom > self.ground_y
        ):
            self.game_over = True
            self.flying = False

        if not self.game_over and self.flying:
            now = pygame.time.get_ticks()
            if now - self.last_pipe > self.pipe_frequency:
                pipe_height = random.randint(-100, 100)
                pipe_y = self.height // 2 + pipe_height

                bottom_pipe = Pipe(
                    self.width, pipe_y, -1, self.asset_dir, self.pipe_gap
                )
                top_pipe = Pipe(
                    self.width, pipe_y, 1, self.asset_dir, self.pipe_gap
                )

                self.pipe_group.add(bottom_pipe, top_pipe)
                self.last_pipe = now

            self.ground_scroll -= self.scroll_speed
            if abs(self.ground_scroll) > self.ground_width:
                self.ground_scroll = 0

    def run(self):
        # Start the background thread only when the game actually starts.
        self.monitor.start()

        try:
            while self.running:
                self.clock.tick(self.fps)
                self.handle_events()

                if not self.game_over:
                    self.update()

                self.draw()

                # Once game over is displayed, wait for a key/mouse action
                # before returning to the Arcade's Game Over screen.
                if self.game_over:
                    continue

        finally:
            # Threading: signal the worker and wait for a clean shutdown.
            self.stop_event.set()
            self.monitor.join()

        return self.score
