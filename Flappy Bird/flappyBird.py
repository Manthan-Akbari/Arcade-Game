import pygame
from pygame.locals import *
import random

pygame.init()


screen_width = 900
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 50

# font
font = pygame.font.SysFont("Bauhaus 93", 50)

# define colors
white = (255, 255, 255)

# define game variables
ground_scroll = 0
scroll_speed = 3
flying = False
game_over = False
pipe_gap = 200
pipe_frequency = 1700  # miliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# Load image
bg = pygame.image.load("BG.png")
ground_img = pygame.image.load("GR.png")
button_img = pygame.image.load("restart.png")


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    flappy.__vel = 0
    flappy.__clicked = False
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.__images = []
        self.__index = 0
        self.__counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"bird{num}.png").convert_alpha()
            self.__images.append(img)
        self.image = self.__images[self.__index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.__vel = 0
        self.__clicked = False

    def get_velocity(self):
        return self.__vel
 
    def set_velocity(self, vel):
        self.__vel = vel
 
    def get_clicked(self):
        return self.__clicked
 
    def set_clicked(self, clicked):
        self.__clicked = clicked
 
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def __animate(self):
        flap_cooldown = 7
        self.__counter += 1
        if self.__counter > flap_cooldown:
            self.__counter = 0
            self.__index += 1
            if self.__index >= len(self.__images):
                self.__index = 0
        self.image = self.__images[self.__index]

    def __apply_gravity(self):
        self.__vel += 0.5
        if self.__vel > 10:
            self.__vel = 10
        if self.rect.bottom < ground_y:
            self.rect.y += int(self.__vel)

    def update(self):
        # gravity
        if flying == True:
            self.__apply_gravity()

        if game_over == False:
            # Jump
            if pygame.mouse.get_pressed()[0] == 1 and self.__clicked == False:
                self.__clicked = True
                self.__vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.__clicked = False

            # handle animation
            self.__animate()

            # rotate the bird
            self.image = pygame.transform.rotate(
                self.__images[self.__index], self.__vel * -2.5
            )
        else:
            self.image = pygame.transform.rotate(self.__images[self.__index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect()

        self._position = position
        # position1 from top, -1 from bottom
        if self._position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if self._position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        if game_over == False:
            self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button:
    def __init__(self, x, y, image):
        self.__image = image
        self.rect = self.__image.get_rect()
        self.rect.topleft = (x, y)

    def get_image(self):
        return self.__image

    def draw(self):
        action = False
        # get mouuse position
        pos = pygame.mouse.get_pos()

        # check if mouse is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # draw button
        screen.blit(self.__image, (self.rect.x, self.rect.y))

        return action


ground_width = ground_img.get_width()
ground_y = screen_height - ground_img.get_height()

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

# restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)


run = True
while run:
    clock.tick(FPS)

    # Backgroud
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()

    # draw and scroll the ground
    screen.blit(ground_img, (ground_scroll, ground_y))
    screen.blit(ground_img, (ground_scroll + ground_width, ground_y))

    # chaeck score
    if len(pipe_group) > 0:
        if (
            bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right
            and pass_pipe == False
        ):
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 30)

    # look for coolision
    if (
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
        or flappy.rect.top < 0
    ):
        game_over = True

    # check if bird has hit the ground
    if flappy.rect.bottom > ground_y:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:

            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)

            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > ground_width:
            ground_scroll = 0

        pipe_group.update()

    # check for game over and reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            flying = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and flying == False
            and game_over == False
        ):
            flying = True

    pygame.display.update()
pygame.quit()
