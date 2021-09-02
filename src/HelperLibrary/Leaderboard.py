from src.HelperLibrary.Game import Game
from src.HelperLibrary.StorageFunctions import StorageFunctions


class Leaderboard:
    def __init__(self, users_table_name="users", games_table_name="games"):
        self.users_table = users_table_name
        self.games_table = games_table_name

    @staticmethod
    def form_game_object(game_record):
        game = Game(game_record[1], game_record[2])
        game.player_one_score = game_record[3]
        game.player_two_score = game_record[4]
        game.winner = game_record[5]
        return game

    def get_records(self):
        all_games = StorageFunctions(self.games_table).retrieve(["winner"], [None], negative=True)
        potential_high_scores = []
        for game_record in all_games:
            game = self.form_game_object(game_record)
            if game.winner == game.player_one:
                potential_high_scores.append([game.player_one, game.player_one_score])
            else:
                potential_high_scores.append([game.player_two, game.player_two_score])
        high_scores = sorted(potential_high_scores, key=lambda x: x[1], reverse=True)[:5]
        return high_scores

    def format_records(self, high_scores):
        for high_score in high_scores:
            high_score[0] = StorageFunctions(self.users_table).retrieve(["id"], [high_score[0]])[0][1]
        return high_scores
