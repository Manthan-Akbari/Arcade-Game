import pygame


class LeaderboardScreen:

    # OOP: Constructor
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app

        self.title_font = pygame.font.Font(None, 65)
        self.heading_font = pygame.font.Font(None, 30)
        self.text_font = pygame.font.Font(None, 30)
        self.score_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 32)

        self.home_button = pygame.Rect(
            350, 620, 200, 50
        )

        self.game_id = ""

    def set_game(self, game_id):

        self.game_id = game_id

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.home_button.collidepoint(event.pos):

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
            (830, 120),
            90
        )

        # ---------------- MAIN CARD ----------------

        card = pygame.Rect(
            120, 55, 660, 550
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

        # ---------------- TITLE ----------------

        title = self.title_font.render(
            "LEADERBOARD",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (
                self.screen.get_width() // 2 -
                title.get_width() // 2,
                80
            )
        )

        # ---------------- GAME NAME ----------------

        game_name = self.game_id.replace(
            "_", " "
        ).upper()

        game_text = self.heading_font.render(
            game_name,
            True,
            (70, 180, 255)
        )

        self.screen.blit(
            game_text,
            (
                self.screen.get_width() // 2 -
                game_text.get_width() // 2,
                145
            )
        )

        # ---------------- HEADER ----------------

        header_rect = pygame.Rect(
            165, 190, 570, 45
        )

        pygame.draw.rect(
            self.screen,
            (18, 23, 40),
            header_rect,
            border_radius=8
        )

        rank_text = self.heading_font.render(
            "RANK",
            True,
            (130, 145, 170)
        )

        player_text = self.heading_font.render(
            "PLAYER",
            True,
            (130, 145, 170)
        )

        score_text = self.heading_font.render(
            "SCORE",
            True,
            (130, 145, 170)
        )

        self.screen.blit(
            rank_text,
            (190, 202)
        )

        self.screen.blit(
            player_text,
            (310, 202)
        )

        self.screen.blit(
            score_text,
            (620, 202)
        )

        # ---------------- LEADERBOARD DATA ----------------

        leaderboard = self.app.score_manager.get_leaderboard(
            self.game_id
        )

        y = 250

        for index, entry in enumerate(leaderboard[:8]):

            row = pygame.Rect(
                165,
                y,
                570,
                40
            )

            # Highlight top 3

            if index == 0:

                row_color = (42, 42, 30)

            elif index == 1:

                row_color = (35, 38, 45)

            elif index == 2:

                row_color = (42, 32, 28)

            else:

                row_color = (18, 23, 40)

            pygame.draw.rect(
                self.screen,
                row_color,
                row,
                border_radius=8
            )

            # Rank

            rank = index + 1

            if rank == 1:
                rank_display = "1."
            elif rank == 2:
                rank_display = "2."
            elif rank == 3:
                rank_display = "3."
            else:
                rank_display = f"{rank}."

            rank_surface = self.text_font.render(
                rank_display,
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                rank_surface,
                (195, y + 7)
            )

            # Player

            player_surface = self.text_font.render(
                entry["player"],
                True,
                (235, 240, 250)
            )

            self.screen.blit(
                player_surface,
                (310, y + 7)
            )

            # Score

            score_surface = self.score_font.render(
                str(entry["score"]),
                True,
                (70, 180, 255)
            )

            self.screen.blit(
                score_surface,
                (
                    620,
                    y + 5
                )
            )

            y += 45

        # ---------------- NO SCORES ----------------

        if len(leaderboard) == 0:

            no_score = self.text_font.render(
                "No scores yet. Be the first!",
                True,
                (120, 135, 160)
            )

            self.screen.blit(
                no_score,
                (
                    self.screen.get_width() // 2 -
                    no_score.get_width() // 2,
                    330
                )
            )

        # ---------------- HOME BUTTON ----------------

        mouse_pos = pygame.mouse.get_pos()

        if self.home_button.collidepoint(mouse_pos):

            button_color = (70, 180, 255)

        else:

            button_color = (45, 135, 220)

        pygame.draw.rect(
            self.screen,
            button_color,
            self.home_button,
            border_radius=10
        )

        home_text = self.button_font.render(
            "HOME",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            home_text,
            (
                self.home_button.centerx -
                home_text.get_width() // 2,
                self.home_button.centery -
                home_text.get_height() // 2
            )
        )

        pygame.display.flip()