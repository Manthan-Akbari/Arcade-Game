from game.game_registry import games


class GameManager:

    def __init__(self,screen):
        self.screen=screen

    def start_game(self,game_id,player_name):

        for game_data in games:

            if game_data["id"]==game_id:

                game_class=game_data["class"]

                game=game_class(
                    self.screen,
                    player_name
                )

                score=game.run()

                return score
        return 0

