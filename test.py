import pygame

pygame.init()

screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("TEST")

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.display.flip()

pygame.quit()