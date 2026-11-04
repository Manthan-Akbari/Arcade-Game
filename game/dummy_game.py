import pygame
from game.base_game import Game

class DummyGame(Game):


    def run(self):

        running=True
        font=pygame.font.Font(None,50)
        while running:

            for event in pygame.event.get():

                if event.type==pygame.QUIT:
                    running=False
                if event.type==pygame.KEYDOWN:

                    if event.key==pygame.K_SPACE:
                        self.score+=1
                    if event.key==pygame.K_ESCAPE:
                        running =False

            self.screen.fill((30,30,30))

            text=font.render(
                f"{self.player_name} | Score: {self.score}",
                True,
                (255,255,255)
            )

            self.screen.blit(text,(200,300))

            pygame.display.flip()
        return self.score
