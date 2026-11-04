import pygame
from ui.home_screen import HomeScreen
from ui.player_screen import PlayerScreen
from ui.game_selection_screen import GameSelectionScreen
from game.game_manager import GameManager
from systems.score_manager import ScoreManager
from systems.save_manager import SaveManager
from ui.game_over_screen import GameOverScreen
from ui.leaderboard_screen import LeaderboardScreen
class App:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((900, 700))
        pygame.display.set_caption("Multi Game Arcade")
        self.home_screen=HomeScreen(self.screen,self)
        self.player_screen=PlayerScreen(self.screen,self)
        self.game_selection_screen = GameSelectionScreen(self.screen,self)
        self.game_manager=GameManager(self.screen)
        self.score_manager=ScoreManager()#composition
        self.save_manager=SaveManager()
        self.game_over_screen=GameOverScreen(self.screen,self)
        self.leaderboard_screen=LeaderboardScreen(self.screen,self)
        saved_scores=self.save_manager.load_scores()
        self.score_manager.scores=saved_scores
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_name=""
        self.current_screen="home"

    def run(self):
        print("inside app.run")
        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if self.current_screen == "home":
                    self.home_screen.handle_event(event)

                elif self.current_screen == "player":
                    self.player_screen.handle_event(event)
                elif self.current_screen == "game_selection":
                    self.game_selection_screen.handle_event(event)
                elif self.current_screen == "game_over":
                    self.game_over_screen.handle_event(event)
                elif self.current_screen == "leaderboard":
                    self.leaderboard_screen.handle_event(event)            
                

            if self.current_screen=="home":
                self.home_screen.draw()

            elif self.current_screen == "player":
                self.player_screen.draw()

            elif self.current_screen == "game_selection":
                self.game_selection_screen.draw()

            elif self.current_screen=="game_over":
                self.game_over_screen.draw()
            elif self.current_screen=="leaderboard":
                self.leaderboard_screen.draw()
            self.clock.tick(60)

        pygame.quit()