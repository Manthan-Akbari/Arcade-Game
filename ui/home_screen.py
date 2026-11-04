import pygame


class HomeScreen:

    # OOP: Constructor
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app

        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 42)
        self.small_font = pygame.font.Font(None, 24)

        self.play_button = pygame.Rect(
            325, 410, 250, 75
        )

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.play_button.collidepoint(event.pos):
                self.app.current_screen = "player"

    def draw(self):

        # ---------------- BACKGROUND ----------------

        self.screen.fill((12, 16, 30))

        # Decorative circles
        pygame.draw.circle(
            self.screen,
            (25, 35, 65),
            (80, 100),
            70
        )

        pygame.draw.circle(
            self.screen,
            (30, 25, 65),
            (820, 150),
            90
        )

        pygame.draw.circle(
            self.screen,
            (20, 55, 70),
            (850, 620),
            100
        )

        pygame.draw.circle(
            self.screen,
            (45, 25, 65),
            (60, 620),
            80
        )

        # ---------------- MAIN CARD ----------------

        card = pygame.Rect(
            150, 100, 600, 500
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

        # Title shadow
        title_shadow = self.title_font.render(
            "MULTI GAME",
            True,
            (5, 8, 15)
        )

        self.screen.blit(
            title_shadow,
            (self.screen.get_width() // 2 -
             title_shadow.get_width() // 2 + 3, 168)
        )

        title = self.title_font.render(
            "MULTI GAME",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (
                self.screen.get_width() // 2 -
                title.get_width() // 2,
                160
            )
        )

        arcade_text = self.title_font.render(
            "ARCADE",
            True,
            (70, 180, 255)
        )

        self.screen.blit(
            arcade_text,
            (
                self.screen.get_width() // 2 -
                arcade_text.get_width() // 2,
                225
            )
        )

        # ---------------- SUBTITLE ----------------

        subtitle = self.subtitle_font.render(
            "PLAY  •  COMPETE  •  BEAT YOUR SCORE",
            True,
            (175, 185, 205)
        )

        self.screen.blit(
            subtitle,
            (
                self.screen.get_width() // 2 -
                subtitle.get_width() // 2,
                315
            )
        )

        # ---------------- PLAY BUTTON ----------------

        mouse_pos = pygame.mouse.get_pos()

        if self.play_button.collidepoint(mouse_pos):

            # Outer glow
            glow_rect = self.play_button.inflate(14, 14)

            pygame.draw.rect(
                self.screen,
                (35, 90, 150),
                glow_rect,
                border_radius=16
            )

            button_color = (70, 180, 255)

        else:
            button_color = (45, 135, 220)

        pygame.draw.rect(
            self.screen,
            button_color,
            self.play_button,
            border_radius=14
        )

        # Button highlight
        highlight = pygame.Rect(
            self.play_button.x,
            self.play_button.y,
            self.play_button.width,
            8
        )

        pygame.draw.rect(
            self.screen,
            (120, 210, 255),
            highlight,
            border_radius=8
        )

        play_text = self.button_font.render(
            "▶  PLAY",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            play_text,
            (
                self.play_button.centerx -
                play_text.get_width() // 2,
                self.play_button.centery -
                play_text.get_height() // 2
            )
        )

        # ---------------- FOOTER ----------------

        footer = self.small_font.render(
            "MULTI GAME ARCADE",
            True,
            (100, 110, 135)
        )

        self.screen.blit(
            footer,
            (
                self.screen.get_width() // 2 -
                footer.get_width() // 2,
                650
            )
        )

        pygame.display.flip()