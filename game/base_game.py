class Game:


    def __init__(self,screen,player_name):
        self.screen=screen
        self.player_name=player_name
        self.score=0

    def run(self):
        raise NotImplementedError

    def get_score(self):
        return self.score