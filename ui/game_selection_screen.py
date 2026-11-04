import pygame
from game.game_registry import games


class GameSelectionScreen:

    # OOP: Constructor
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app

        self.title_font = pygame.font.Font(None, 60)
        self.game_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 26)

        self.cards = []

        card_width = 240
        card_height = 280

        columns = 3
        gap = 25

        start_x = 60
        start_y = 210

        for i, game in enumerate(games):

            row = i // columns
            column = i % columns

            x = start_x + column * (card_width + gap)
            y = start_y + row * (card_height + gap)

            card = pygame.Rect(
                x,
                y,
                card_width,
                card_height
            )

            self.cards.append({
                "rect": card,
                "id": game["id"],
                "name": game["name"]
            })

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            for card in self.cards:

                if card["rect"].collidepoint(event.pos):

                    score = self.app.game_manager.start_game(
                        card["id"],
                        self.app.player_name
                    )

                    print("Final Score:", score)

                    self.app.score_manager.add_score(
                        card["id"],
                        self.app.player_name,
                        score
                    )

                    self.app.save_manager.save_scores(
                        self.app.score_manager.scores
                    )

                    self.app.game_over_screen.set_result(
                        card["id"],
                        score
                    )

                    self.app.current_screen = "game_over"

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
            (850, 130),
            90
        )

        # ---------------- TITLE ----------------

        title = self.title_font.render(
            "SELECT YOUR GAME",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (
                self.screen.get_width() // 2 -
                title.get_width() // 2,
                70
            )
        )

        subtitle = pygame.font.Font(
            None,
            25
        ).render(
            f"Player: {self.app.player_name}",
            True,
            (120, 190, 255)
        )

        self.screen.blit(
            subtitle,
            (
                self.screen.get_width() // 2 -
                subtitle.get_width() // 2,
                135
            )
        )

        # ---------------- GAME CARDS ----------------

        mouse_pos = pygame.mouse.get_pos()

        for card in self.cards:

            rect = card["rect"]

            is_hovered = rect.collidepoint(mouse_pos)

            # Card background

            if is_hovered:

                card_color = (32, 42, 68)
                border_color = (70, 180, 255)

            else:

                card_color = (24, 30, 50)
                border_color = (55, 65, 95)

            pygame.draw.rect(
                self.screen,
                card_color,
                rect,
                border_radius=18
            )

            pygame.draw.rect(
                self.screen,
                border_color,
                rect,
                width=2,
                border_radius=18
            )

            # ---------------- GAME ICON AREA ----------------

            icon_rect = pygame.Rect(
                rect.x + 15,
                rect.y + 15,
                rect.width - 30,
                120
            )

            pygame.draw.rect(
                self.screen,
                (18, 23, 40),
                icon_rect,
                border_radius=12
            )

            # Simple controller icon

            pygame.draw.circle(
                self.screen,
                (70, 180, 255),
                icon_rect.center,
                35
            )

            pygame.draw.circle(
                self.screen,
                (18, 23, 40),
                icon_rect.center,
                25
            )

            # ---------------- GAME NAME ----------------

            game_text = self.game_font.render(
                card["name"],
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                game_text,
                (
                    rect.centerx -
                    game_text.get_width() // 2,
                    rect.y + 155
                )
            )

            # ---------------- PLAY BUTTON ----------------

            play_rect = pygame.Rect(
                rect.x + 45,
                rect.y + 205,
                150,
                45
            )

            if is_hovered:

                button_color = (70, 180, 255)

            else:

                button_color = (45, 135, 220)

            pygame.draw.rect(
                self.screen,
                button_color,
                play_rect,
                border_radius=10
            )

            play_text = self.button_font.render(
                "PLAY",
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                play_text,
                (
                    play_rect.centerx -
                    play_text.get_width() // 2,
                    play_rect.centery -
                    play_text.get_height() // 2
                )
            )

        pygame.display.flip()