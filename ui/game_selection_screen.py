
import pygame
from game.game_registry import games
import os


class GameSelectionScreen:

    # OOP: Constructor
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app

        self.title_font = pygame.font.Font(None, 60)
        self.game_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 26)

        self.cards = []
        self.game_images = {}

        card_width = 270
        card_height = 215

        columns = 2
        gap_x = 30
        gap_y = 25

        start_x = 165
        start_y = 190

        # Load game images
        image_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "game_images"
        )

        for game in games:

            image_file = os.path.join(
                image_path,
                game["id"] + ".png"
            )

            try:
                image = pygame.image.load(image_file).convert_alpha()

                # OOP: Store each game's image using its ID
                self.game_images[game["id"]] = image

            except (pygame.error, FileNotFoundError):
                print(f"Image not found: {image_file}")
                self.game_images[game["id"]] = None

        # Create game cards
        for i, game in enumerate(games):

            row = i // columns
            column = i % columns

            x = start_x + column * (card_width + gap_x)
            y = start_y + row * (card_height + gap_y)

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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

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
                    break

    def draw(self):

        # ---------------- BACKGROUND ----------------

        self.screen.fill((12, 16, 30))

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
                self.screen.get_width() // 2 - title.get_width() // 2,
                70
            )
        )

        subtitle = pygame.font.Font(None, 25).render(
            f"Player: {self.app.player_name}",
            True,
            (120, 190, 255)
        )

        self.screen.blit(
            subtitle,
            (
                self.screen.get_width() // 2 - subtitle.get_width() // 2,
                135
            )
        )

        # ---------------- GAME CARDS ----------------

        mouse_pos = pygame.mouse.get_pos()

        for card in self.cards:

            rect = card["rect"]
            is_hovered = rect.collidepoint(mouse_pos)

            card_color = (32, 42, 68) if is_hovered else (24, 30, 50)
            border_color = (70, 180, 255) if is_hovered else (55, 65, 95)

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

            # ---------------- GAME IMAGE ----------------

            image_rect = pygame.Rect(
                rect.x + 15,
                rect.y + 15,
                rect.width - 30,
                105
            )

            pygame.draw.rect(
                self.screen,
                (18, 23, 40),
                image_rect,
                border_radius=12
            )

            game_image = self.game_images.get(card["id"])

            if game_image:

                # Scale image to fit without changing its aspect ratio
                image_copy = game_image.copy()
                image_copy.thumbnail(
                    (image_rect.width, image_rect.height),
                    pygame.transform.smoothscale
                )

                scaled_image = pygame.transform.smoothscale(
                    game_image,
                    (
                        image_rect.width,
                        image_rect.height
                    )
                )

                # Clip image to the image area
                old_clip = self.screen.get_clip()
                self.screen.set_clip(image_rect)

                self.screen.blit(
                    scaled_image,
                    image_rect
                )

                self.screen.set_clip(old_clip)

            else:

                # Fallback when image is unavailable
                icon_text = self.game_font.render(
                    card["name"],
                    True,
                    (70, 180, 255)
                )

                self.screen.blit(
                    icon_text,
                    icon_text.get_rect(center=image_rect.center)
                )

            # ---------------- GAME NAME ----------------

            game_text = self.game_font.render(
                card["name"],
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                game_text,
                game_text.get_rect(
                    center=(rect.centerx, rect.y + 137)
                )
            )

            # ---------------- PLAY BUTTON ----------------

            play_rect = pygame.Rect(
                rect.x + 60,
                rect.y + 165,
                150,
                38
            )

            button_color = (
                (70, 180, 255)
                if is_hovered
                else (45, 135, 220)
            )

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
                play_text.get_rect(center=play_rect.center)
            )

        pygame.display.flip()
