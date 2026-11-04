import pygame


class PlayerScreen:

    # OOP: Constructor
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app

        self.title_font = pygame.font.Font(None, 60)
        self.subtitle_font = pygame.font.Font(None, 28)
        self.input_font = pygame.font.Font(None, 38)
        self.button_font = pygame.font.Font(None, 38)

        self.input_box = pygame.Rect(
            275, 320, 350, 60
        )

        self.start_button = pygame.Rect(
            325, 420, 250, 65
        )

        self.player_name = ""
        self.active = False

    def handle_event(self, event):

        try:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.input_box.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

                if self.start_button.collidepoint(event.pos):

                    if not self.player_name.strip():
                        print("Error: Player name cannot be empty")
                        return

                    self.app.player_name = self.player_name.strip()
                    self.app.current_screen = "game_selection"

            if event.type == pygame.KEYDOWN and self.active:

                if event.key == pygame.K_BACKSPACE:

                    self.player_name = self.player_name[:-1]

                elif event.key == pygame.K_RETURN:

                    if not self.player_name.strip():
                        print("Error: Player name cannot be empty")
                        return

                    self.app.player_name = self.player_name.strip()
                    self.app.current_screen = "game_selection"

                else:

                    if len(self.player_name) < 15:

                        try:
                            self.player_name += event.unicode

                        except Exception as e:
                            print("Error while entering name:", e)

        except Exception as e:

            print("Player input error:", e)
            
    def draw(self):

#background

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

#main card

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

#title

        title = self.title_font.render(
            "ENTER YOUR NAME",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (
                self.screen.get_width() // 2 -
                title.get_width() // 2,
                155
            )
        )

        subtitle = self.subtitle_font.render(
            "Your score will be saved to the leaderboard",
            True,
            (170, 180, 200)
        )

        self.screen.blit(
            subtitle,
            (
                self.screen.get_width() // 2 -
                subtitle.get_width() // 2,
                225
            )
        )



        if self.active:
            border_color = (70, 180, 255)
        else:
            border_color = (70, 80, 105)

        pygame.draw.rect(
            self.screen,
            (16, 21, 36),
            self.input_box,
            border_radius=10
        )

        pygame.draw.rect(
            self.screen,
            border_color,
            self.input_box,
            width=2,
            border_radius=10
        )

        if self.player_name:

            name_text = self.input_font.render(
                self.player_name,
                True,
                (255, 255, 255)
            )

        else:

            name_text = self.subtitle_font.render(
                "Enter your name...",
                True,
                (100, 110, 130)
            )

        self.screen.blit(
            name_text,
            (
                self.input_box.x + 20,
                self.input_box.y + 15
            )
        )

#start button

        mouse_pos = pygame.mouse.get_pos()

        if self.start_button.collidepoint(mouse_pos):

            button_color = (70, 180, 255)

        else:

            button_color = (45, 135, 220)

        pygame.draw.rect(
            self.screen,
            button_color,
            self.start_button,
            border_radius=12
        )

        start_text = self.button_font.render(
            "START",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            start_text,
            (
                self.start_button.centerx -
                start_text.get_width() // 2,
                self.start_button.centery -
                start_text.get_height() // 2
            )
        )

        # ---------------- FOOTER ----------------

        footer = self.subtitle_font.render(
            "MAX 15 CHARACTERS",
            True,
            (90, 100, 120)
        )

        self.screen.blit(
            footer,
            (
                self.screen.get_width() // 2 -
                footer.get_width() // 2,
                540
            )
        )

        pygame.display.flip()