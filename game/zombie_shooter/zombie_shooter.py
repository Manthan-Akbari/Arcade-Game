"""Zombie Shooter adapted for the Multi Game Arcade project."""

import math
import random
import pygame

from game.base_game import Game as BaseGame

FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (236, 236, 238)
GRAY = (150, 155, 165)
FLOOR = (24, 26, 31)
GRID = (31, 34, 40)
RED = (214, 48, 49)
GREEN = (86, 190, 110)
YELLOW = (250, 204, 21)
ZOMBIE_GREEN = (96, 140, 84)
PLAYER_BLUE = (70, 130, 210)

# Weapon settings
RIFLE_DAMAGE = 20
RIFLE_FIRE_RATE = 9
RIFLE_BULLET_SPEED = 1000
RIFLE_SPREAD = 0.05

# Zombie settings
ZOMBIE_RADIUS = 14
ZOMBIE_HEALTH = 60
ZOMBIE_DAMAGE = 10
ZOMBIE_POINTS = 10


class Player:
    # OOP: Constructor - stores the player's position and health.
    def __init__(self, width, height):
        self.x = width / 2
        self.y = height / 2
        self.width = width
        self.height = height
        self.radius = 16
        self.speed = 240
        self.max_health = 100
        self.health = self.max_health
        self.angle = 0
        self.shoot_timer = 0

    def move(self, keys, dt):
        dx = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(
            keys[pygame.K_a] or keys[pygame.K_LEFT]
        )
        dy = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(
            keys[pygame.K_w] or keys[pygame.K_UP]
        )

        length = math.hypot(dx, dy)
        if length > 0:
            self.x += dx / length * self.speed * dt
            self.y += dy / length * self.speed * dt

        self.x = max(self.radius, min(self.width - self.radius, self.x))
        self.y = max(self.radius, min(self.height - self.radius, self.y))

    def aim(self, mouse_pos):
        self.angle = math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x)

    def shoot(self, bullets):
        if self.shoot_timer <= 0:
            angle = self.angle + random.uniform(-RIFLE_SPREAD, RIFLE_SPREAD)
            bx = self.x + math.cos(self.angle) * 28
            by = self.y + math.sin(self.angle) * 28
            bullets.append(Bullet(bx, by, angle))
            self.shoot_timer = 1 / RIFLE_FIRE_RATE

    def update(self, dt):
        self.shoot_timer -= dt

    def draw(self, screen):
        pygame.draw.circle(
            screen, PLAYER_BLUE, (int(self.x), int(self.y)), self.radius
        )
        pygame.draw.circle(
            screen, BLACK, (int(self.x), int(self.y)), self.radius, 2
        )
        end = (
            self.x + math.cos(self.angle) * 30,
            self.y + math.sin(self.angle) * 30,
        )
        pygame.draw.line(screen, (60, 60, 60), (self.x, self.y), end, 6)


class Bullet:
    # OOP: Each bullet stores its own movement and lifetime.
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * RIFLE_BULLET_SPEED
        self.vy = math.sin(angle) * RIFLE_BULLET_SPEED
        self.radius = 3
        self.life = 1.3
        self.alive = True

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        if self.life <= 0:
            self.alive = False

    def draw(self, screen):
        pygame.draw.circle(
            screen, YELLOW, (int(self.x), int(self.y)), self.radius
        )


class Zombie:
    # OOP: Each zombie manages its own movement and attack cooldown.
    def __init__(self, width, height, wave):
        self.x, self.y = random.choice([
            (random.uniform(0, width), -30),
            (width + 30, random.uniform(0, height)),
            (random.uniform(0, width), height + 30),
            (-30, random.uniform(0, height)),
        ])
        self.radius = ZOMBIE_RADIUS
        self.speed = random.uniform(55, 80)
        self.health = ZOMBIE_HEALTH * (1 + 0.06 * (wave - 1))
        self.attack_timer = 0
        self.alive = True

    def update(self, dt, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            self.x += dx / distance * self.speed * dt
            self.y += dy / distance * self.speed * dt

        self.attack_timer -= dt
        if (
            distance <= self.radius + player.radius + 3
            and self.attack_timer <= 0
        ):
            player.health -= ZOMBIE_DAMAGE
            self.attack_timer = 0.8

    def draw(self, screen):
        pos = (int(self.x), int(self.y))
        pygame.draw.circle(screen, ZOMBIE_GREEN, pos, self.radius)
        pygame.draw.circle(screen, BLACK, pos, self.radius, 2)
        pygame.draw.circle(screen, RED, (pos[0] - 5, pos[1] - 3), 3)
        pygame.draw.circle(screen, RED, (pos[0] + 5, pos[1] - 3), 3)


class ZombieShooter(BaseGame):
    # OOP: Inherits the common game interface used by GameManager.
    def __init__(self, screen, player_name):
        super().__init__(screen, player_name)
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.big_font = pygame.font.SysFont("arial", 72, bold=True)
        self.reset()

    def reset(self):
        self.player = Player(self.width, self.height)
        self.bullets = []
        self.zombies = []
        self.score = 0
        self.kills = 0
        self.wave = 0
        self.to_spawn = 0
        self.spawn_timer = 0
        self.wave_pause = 2.0

    def draw_text(self, message, font, color, x, y, center=True):
        image = font.render(message, True, color)
        rect = (
            image.get_rect(center=(x, y))
            if center
            else image.get_rect(topleft=(x, y))
        )
        self.screen.blit(image, rect)

    def update_waves(self, dt):
        if self.to_spawn > 0:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.zombies.append(
                    Zombie(self.width, self.height, self.wave)
                )
                self.to_spawn -= 1
                self.spawn_timer = max(0.25, 0.9 - 0.05 * self.wave)
        elif not self.zombies:
            self.wave_pause -= dt
            if self.wave_pause <= 0:
                self.wave += 1
                self.to_spawn = 6 + 4 * self.wave
                self.wave_pause = 3.0

    def check_bullet_hits(self):
        for bullet in self.bullets:
            for zombie in self.zombies:
                distance = math.hypot(
                    bullet.x - zombie.x, bullet.y - zombie.y
                )
                if distance <= bullet.radius + zombie.radius:
                    zombie.health -= RIFLE_DAMAGE
                    bullet.alive = False
                    if zombie.health <= 0:
                        zombie.alive = False
                        self.score += ZOMBIE_POINTS
                        self.kills += 1
                    break

    def update(self, dt):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        self.player.move(keys, dt)
        self.player.aim(mouse_pos)
        self.player.update(dt)

        if pygame.mouse.get_pressed()[0]:
            self.player.shoot(self.bullets)

        self.update_waves(dt)

        for bullet in self.bullets:
            bullet.update(dt)
        for zombie in self.zombies:
            zombie.update(dt, self.player)

        self.check_bullet_hits()

        self.bullets = [bullet for bullet in self.bullets if bullet.alive]
        self.zombies = [zombie for zombie in self.zombies if zombie.alive]

    def draw_background(self):
        self.screen.fill(FLOOR)
        for x in range(0, self.width, 50):
            pygame.draw.line(self.screen, GRID, (x, 0), (x, self.height))
        for y in range(0, self.height, 50):
            pygame.draw.line(self.screen, GRID, (0, y), (self.width, y))

    def draw_hud(self):
        pygame.draw.rect(self.screen, (45, 48, 56), (20, 20, 200, 22))
        health_width = int(
            200 * max(0, self.player.health) / self.player.max_health
        )
        pygame.draw.rect(
            self.screen, GREEN, (20, 20, health_width, 22)
        )
        pygame.draw.rect(self.screen, BLACK, (20, 20, 200, 22), 2)

        self.draw_text(
            f"Player: {self.player_name}", self.font, WHITE, 20, 52, False
        )
        self.draw_text(
            f"Score: {self.score}", self.font, WHITE, 20, 80, False
        )
        self.draw_text(
            f"Wave: {self.wave}", self.font, WHITE,
            self.width - 140, 20, False
        )
        remaining = self.to_spawn + len(self.zombies)
        self.draw_text(
            f"Zombies left: {remaining}", self.font, WHITE,
            self.width - 240, 50, False
        )
        self.draw_text(
            "Rifle | Ammo: unlimited", self.font, GRAY,
            20, self.height - 36, False
        )

        if self.to_spawn == 0 and not self.zombies:
            self.draw_text(
                f"Wave {self.wave + 1} incoming...",
                self.font, YELLOW, self.width // 2, 100
            )

    def draw_crosshair(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(
            self.screen, WHITE,
            (mouse_x - 10, mouse_y), (mouse_x + 10, mouse_y), 2
        )
        pygame.draw.line(
            self.screen, WHITE,
            (mouse_x, mouse_y - 10), (mouse_x, mouse_y + 10), 2
        )

    def draw(self):
        self.draw_background()
        for zombie in self.zombies:
            zombie.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_hud()
        self.draw_crosshair()

    def draw_game_over(self):
        self.draw()
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        self.draw_text(
            "YOU DIED", self.big_font, RED, self.width // 2, 190
        )
        stats = [
            f"Score: {self.score}",
            f"Zombies killed: {self.kills}",
            f"Wave reached: {self.wave}",
        ]
        for index, line in enumerate(stats):
            self.draw_text(
                line, self.font, WHITE,
                self.width // 2, 290 + index * 35
            )
        self.draw_text(
            "Returning to arcade...", self.font, YELLOW,
            self.width // 2, 470
        )

    def run(self):
        """Run the game and return its score to the arcade."""
        running = True
        game_over = False
        game_over_timer = 1.5
        previous_mouse_visibility = pygame.mouse.get_visible()
        pygame.mouse.set_visible(False)

        try:
            while running:
                dt = min(self.clock.tick(FPS) / 1000, 0.05)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # Pass the close event back to the main arcade loop.
                        pygame.event.post(event)
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False

                if not running:
                    break

                if not game_over:
                    self.update(dt)
                    if self.player.health <= 0:
                        game_over = True
                else:
                    game_over_timer -= dt
                    if game_over_timer <= 0:
                        running = False

                if game_over:
                    self.draw_game_over()
                else:
                    self.draw()

                pygame.display.flip()

        finally:
            # Restore the cursor even if the game exits unexpectedly.
            pygame.mouse.set_visible(previous_mouse_visibility)

        return self.score
