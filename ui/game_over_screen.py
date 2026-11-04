import pygame


class GameOverScreen:

    # OOP: Constructor
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app

        self.title_font = pygame.font.Font(None, 75)
        self.score_font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 25)

        self.play_again_button = pygame.Rect(
            300, 420, 300, 55
        )

        self.leaderboard_button = pygame.Rect(
            300, 490, 300, 55
        )

        self.home_button = pygame.Rect(
            300, 560, 300, 55
        )

        self.score = 0
        self.game_id = ""

    def set_result(self, game_id, score):

        self.game_id = game_id
        self.score = score

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            # ---------------- PLAY AGAIN ----------------

            if self.play_again_button.collidepoint(event.pos):

                score = self.app.game_manager.start_game(
                    self.game_id,
                    self.app.player_name
                )

                self.app.score_manager.add_score(
                    self.game_id,
                    self.app.player_name,
                    score
                )

                self.app.save_manager.save_scores(
                    self.app.score_manager.scores
                )

                self.set_result(
                    self.game_id,
                    score
                )

            # ---------------- LEADERBOARD ----------------

            elif self.leaderboard_button.collidepoint(event.pos):

                self.app.leaderboard_screen.set_game(
                    self.game_id
                )

                self.app.current_screen = "leaderboard"

            # ---------------- HOME ----------------

            elif self.home_button.collidepoint(event.pos):

                self.app.current_screen = "home"

    def draw(self):

        # ---------------- BACKGROUND ----------------

        self.screen.fill((12, 16, 30))

        # Decorative circles

        pygame.draw.circle(
            self.screen,
            (25, 35, 65),
            (70, 100),
            70
        )

        pygame.draw.circle(
            self.screen,
            (30, 25, 65),
            (830, 150),
            90
        )

        pygame.draw.circle(
            self.screen,
            (20, 55, 70),
            (850, 620),
            100
        )

        # ---------------- MAIN CARD ----------------

        card = pygame.Rect(
            150, 80, 600, 540
        )

        pygame.draw.rect(
            self.screen,
            (24, 30, 50),
            card,
            border_radius=25
        )

        pygame.draw.rect(
            self.screen,
            (55, 65, 95),
            card,
            width=2,
            border_radius=25
        )

        # ---------------- GAME OVER ----------------

        title = self.title_font.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (
                self.screen.get_width() // 2 -
                title.get_width() // 2,
                125
            )
        )

        # ---------------- PLAYER NAME ----------------

        player_text = self.small_font.render(
            f"PLAYER  •  {self.app.player_name}",
            True,
            (150, 170, 195)
        )

        self.screen.blit(
            player_text,
            (
                self.screen.get_width() // 2 -
                player_text.get_width() // 2,
                205
            )
        )

        # ---------------- SCORE ----------------

        score_label = self.small_font.render(
            "YOUR SCORE",
            True,
            (120, 190, 255)
        )

        self.screen.blit(
            score_label,
            (
                self.screen.get_width() // 2 -
                score_label.get_width() // 2,
                255
            )
        )

        score_text = self.score_font.render(
            str(self.score),
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            score_text,
            (
                self.screen.get_width() // 2 -
                score_text.get_width() // 2,
                285
            )
        )

        # ---------------- BUTTON FUNCTION ----------------

        mouse_pos = pygame.mouse.get_pos()

        buttons = [
            (
                self.play_again_button,
                "PLAY AGAIN"
            ),
            (
                self.leaderboard_button,
                "LEADERBOARD"
            ),
            (
                self.home_button,
                "HOME"
            )
        ]

        for button, text in buttons:

            if button.collidepoint(mouse_pos):

                button_color = (70, 180, 255)

            else:

                button_color = (45, 135, 220)

            pygame.draw.rect(
                self.screen,
                button_color,
                button,
                border_radius=10
            )

            button_text = self.button_font.render(
                text,
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                button_text,
                (
                    button.centerx -
                    button_text.get_width() // 2,
                    button.centery -
                    button_text.get_height() // 2
                )
            )

        pygame.display.flip()