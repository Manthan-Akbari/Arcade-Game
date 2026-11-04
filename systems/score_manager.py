class ScoreManager:

    def __init__(self):
        self.scores={}

    def add_score(self,game_id,player_name,score):

        if game_id not in self.scores:
            self.scores[game_id]=[]

        self.scores[game_id].append({
            "player": player_name,
            "score": score
        })


    def get_score(self,game_id):

        if game_id not in self.scores:
            return []

        return self.scores[game_id]

    def get_leaderboard(self,game_id):

        scores=self.get_score(game_id)

        scores.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return scores