"""This module contains the models related to the tournaments"""


class Tournament:
    """This class describes a tournament"""

    NUMBER_OF_PLAYERS = 4

    def __init__(self, name, description, start_date, end_date, number_of_rounds, time_control):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = int(number_of_rounds)
        self.players = []
        self.rounds = []
        self.time_control = time_control

    @property
    def status(self):
        if not self.rounds:
            return "pas encore commencé"
        elif [round_.status for round_ in self.rounds] == ["terminé"] * self.number_of_rounds:
            return "terminé"
        else:
            return "en cours"

    @property
    def score_table(self):
        return ScoreTable.aggregate(*[round_.score_table for round_ in self.rounds])

    def play_tournament(self):
        if not self.rounds:
            for i in range(self.number_of_rounds):
                self.rounds.append(Round(self))

    def start_new_round(self):
        new_round = Round(self)
        new_round.draw_games()
        self.rounds.append(new_round)

    def __repr__(self):
        return list.__repr__(list(self.__dict__.values()))


class Round:
    """This class describes a round"""

    def __init__(self, tournament):
        self.tournament = tournament
        self.name = "round{}".format(len(self.tournament.rounds) + 1)
        self.games = []

    @property
    def status(self):
        if not self.games:
            return "pas encore commencé"
        elif [game.status for game in self.games] == ["terminé"] * len(self.games):
            return "terminé"
        else:
            return "en cours"

    @property
    def score_table(self):
        return ScoreTable.aggregate(*[game.score_table for game in self.games])

    def draw_games(self):
        self.games = [Game(self.tournament.players[i], self.tournament.players[i + int(Tournament.NUMBER_OF_PLAYERS / 2)])
                 for i in range(int(Tournament.NUMBER_OF_PLAYERS / 2))]

    def __repr__(self):
        return "\n".join([str(game) for game in self.games])


class Game:
    """This class describes a game"""

    def __init__(self, player1, player2):
        self.pair = (player1, player2)
        self.result = 'nc'
        self.score_table = GameScoreTable(player1, player2)

    @property
    def status(self):
        if self.result == 'nc':
            return "pas encore commencé"
        else:
            return "terminé"

    def update_result(self, result):
        self.result = result
        self.update_score()

    def update_score(self):
        if self.result == '1':
            self.score_table.update_score_victory(self.pair[0])
        elif self.result == '2':
            self.score_table.update_score_victory(self.pair[1])
        elif self.result == 'n':
            self.score_table.update_score_draw(*self.pair)

    def __repr__(self):
        return self.score_table.__repr__()


class ScoreTable:
    """This class describes the score"""

    def __init__(self, *players):
        self.score_table = {player: 0 for player in players}

    @classmethod
    def aggregate(cls, *score_tables):
        """This method is called to generate a score table based on the combination of other score tables
        (eg. the score table of a round based on the aggregation of games score table of the tournament score table
        based on the aggregation of round tables)."""

        aggregated_score_table = cls()
        for score_table in score_tables:
            for player in score_table:
                if player in aggregated_score_table:
                    aggregated_score_table[player] += score_table[player]
                else:
                    aggregated_score_table[player] = score_table[player]
        return aggregated_score_table

    def __iter__(self):
        return dict.__iter__(self.score_table)

    def __getitem__(self, item):
        return self.score_table[item]

    def __setitem__(self, key, value):
        self.score_table[key] = value

    def __repr__(self):
        return self.score_table.__repr__()


class GameScoreTable(ScoreTable):
    """This class describes the score for a single game"""

    def update_score_victory(self, player):
        self.score_table[player] += 1

    def update_score_draw(self, player1, player2):
        self.score_table[player1] += 0.5
        self.score_table[player2] += 0.5


