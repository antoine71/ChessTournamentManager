"""This module contains the models related to the tournaments"""
import datetime

import utils.utils as utils
from models.date import Date\

from operator import attrgetter, itemgetter


class Tournament:
    """This class describes a tournament"""

    NUMBER_OF_PLAYERS = 8

    def __init__(self, name, description, place, start_date, end_date, number_of_rounds, time_control):
        self.name = name
        self.description = description
        self.place = place
        self.start_date = Date(start_date)
        self.end_date = Date(end_date)
        if number_of_rounds == "":
            self.number_of_rounds = 4
        else:
            self.number_of_rounds = int(number_of_rounds)
        self.players = []
        self.rounds = []
        self.time_control = time_control
        self.saved = False

    @property
    def games(self):
        games = []
        for round_ in self.rounds:
            for game in round_.games:
                games.append(game)
        return games

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

    def __hash__(self):
        return hash((self.name, self.start_date, self.end_date, self.time_control))

    def __eq__(self, other_tournament):
        return (self.name, self.start_date, self.end_date, self.time_control) == \
               (other_tournament.name, other_tournament.start_date, other_tournament.end_date,
                other_tournament.time_control)

    def __repr__(self):
        return list.__repr__(list(self.__dict__.values()))


class TournamentDataValidator:
    """This class contains methods used to validate parameters before creating a Tournament object"""

    def is_name_ok(self, name):
        return utils.check_string_length(name, 50)

    def is_description_ok(self, description):
        return utils.check_string_length(description, 100)

    def is_place_ok(self, place):
        return utils.check_string_length(place, 50)

    def is_start_date_ok(self, start_date):
        return utils.is_date_format_dd_mm_yyyy(start_date)

    def is_end_date_ok(self, end_date):
        return utils.is_date_format_dd_mm_yyyy(end_date)

    def is_number_of_rounds_ok(self, number_of_rounds):
        if number_of_rounds == "":
            return True
        else:
            return utils.is_positive_integer(number_of_rounds)

    def is_time_control_ok(self, time_control):
        return time_control == "blitz" or time_control == "bullet" or time_control == "coup rapide"


class Round:
    """This class describes a round"""

    def __init__(self, tournament):
        self.tournament = tournament
        self.name = "round{}".format(len(self.tournament.rounds) + 1)
        self.games = []
        self.start_time = datetime.datetime(1970, 1, 1)
        self.end_time = datetime.datetime(1970, 1, 1)
        self.end_confirmation = False

    @property
    def status(self):
        if not self.games:
            return "pas encore commencé"
        elif [game.status for game in self.games] == ["terminé"] * len(self.games) and self.end_confirmation:
            return "terminé"
        elif [game.status for game in self.games] == ["terminé"] * len(self.games):
            return "matchs terminé, en attente de validation"
        else:
            return "en cours"

    @property
    def score_table(self):
        return ScoreTable.aggregate(*[game.score_table for game in self.games])

    def draw_games(self):
        upper_list, lower_list = self.sort_player_for_draw()
        while upper_list:
            i = 0
            while Game(upper_list[0], lower_list[i]) in self.tournament.games:
                i += 1
            self.games.append(Game(upper_list.pop(0), lower_list.pop(i)))

    def sort_player_for_draw(self):
        players_list = self.tournament.players
        players_list.sort(key=attrgetter("ranking"), reverse=True)

        try:
            players_list_scores = [(player, self.tournament.score_table[player]) for player in players_list]
        except KeyError:
            players_list_scores = [(player, 0) for player in players_list]

        players_list_scores.sort(key=itemgetter(1), reverse=True)

        upper_list = [players_list_scores[i][0] for i in range(int(len(players_list) / 2))]
        lower_list = [players_list_scores[i][0] for i in range(int(len(players_list) / 2), len(players_list))]
        return upper_list, lower_list

    def start(self):
        self.start_time = datetime.datetime.now()

    def end(self):
        self.end_time = datetime.datetime.now()

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

    def __hash__(self):
        p1, p2 = self.pair
        return hash((p1, p2)) + hash((p2, p1))

    def __eq__(self, other):
        p1, p2 = self.pair
        other_p1, other_p2 = other.pair
        return (p1, p2) == (other_p2, other_p1) or (p1, p2) == (other_p2, other_p1)


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
        self.score_table[player] = 1

    def update_score_draw(self, player1, player2):
        self.score_table[player1] = 0.5
        self.score_table[player2] = 0.5
