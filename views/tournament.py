"""This module groups the views related to the tournaments"""

from operator import itemgetter

from views.general import ViewText


class ViewTournamentDetails:
    """This view displays the attributes and values of a Tournament object"""

    def __init__(self, title, tournament):
        self.title = title
        self.tournament = tournament

    def show(self):
        ViewText(self.title).show()
        string_output = "\n".join([
            "\tNom : {}".format(self.tournament.name),
            "\tDescription : {}".format(self.tournament.description),
            "\tDate de début : {}".format(self.tournament.start_date),
            "\tDate de fin : {}".format(self.tournament.end_date),
            "\tNombre de rounds : {}".format(self.tournament.number_of_rounds),
            "\tContrôle du temps : {}".format(self.tournament.time_control),
            "\tStatus : {}".format(self.tournament.status),
        ])
        ViewText(string_output).show()


class ViewScoreTable:
    """This view displays a ScoreTable object on the screen"""

    def __init__(self, title, score_table):
        self.title = title
        self.score_table = score_table

    def show(self):
        ViewText(self.title).show()
        if not self.score_table.score_table:
            string_output = "\tPas disponible"
        else:
            sorted_score_table = sorted(self.score_table.score_table.items(), key=itemgetter(1), reverse=True)
            string_output = "\n".join([
                "\t{}: {}".format(player, score)
                for player, score in sorted_score_table
            ])
        ViewText(string_output).show()


class ViewTournamentResult:
    """This view displays the results of each game of each round of a tournament on the screen"""

    def __init__(self, title, tournament):
        self.title = title
        self.tournament = tournament

    def show(self):
        ViewText(self.title).show()
        if not self.tournament.rounds:
            ViewText("\tPas disponible").show()
        else:
            for round_ in self.tournament.rounds:
                ViewRoundResult(round_).show()


class ViewRoundResult:
    """This view displays the results of each game of a round on the screen"""

    def __init__(self, round_):
        self.round_ = round_

    def show(self):
        ViewText("\t{} - {}".format(self.round_.name, self.round_.status)).show()
        if not self.round_.games:
            ViewText("\t\tPas disponible").show()
        else:
            for game in self.round_.games:
                ViewGameResult(game).show()


class ViewGameResult:
    """This view displays the results a game on the screen"""

    def __init__(self, game):
        self.game = game

    def show(self):
        match_result_string_output = "\t".join([
            "\t\t{}: {}".format(player, score)
            for player, score in self.game.score_table.score_table.items()
        ])
        string_output = ' - '.join([self.game.status, match_result_string_output])
        ViewText(string_output).show()