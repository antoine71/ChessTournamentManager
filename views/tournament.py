"""This module groups the views related to the tournaments"""

from operator import itemgetter

from views.general import ViewText

from utils.utils import resize_string


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
                "{}\t{}: {}".format(i + 1, player, score)
                for (i, (player, score)) in enumerate(sorted_score_table)
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

    def __init__(self, round_, mode_view_results=True):
        self.round_ = round_
        self.mode_view_results = mode_view_results

    def show(self):
        ViewText("\t{} - {}".format(self.round_.name, self.round_.status)).show()
        if not self.round_.games:
            ViewText("\t\tPas disponible").show()
        else:
            for i, game in enumerate(self.round_.games):
                ViewGameResult(i + 1, game, mode_view_results=self.mode_view_results).show()


class ViewGameResult:
    """This view displays the results a game on the screen"""

    def __init__(self, game_number, game, mode_view_results=True):
        self.game_number = game_number
        self.game = game
        self.mode_view_results = mode_view_results

    def show(self):
        match_result_string_output = "\t".join([
            resize_string("{}: {}".format(player, score), 30)
            for player, score in self.game.score_table.score_table.items()
        ])
        game_number_display = " {} ".format(self.game_number) if self.mode_view_results \
            else "({})".format(self.game_number)
        string_output = ''.join(
            [
                resize_string(game_number_display, 5),
                resize_string(self.game.status + ":", 22),
                match_result_string_output
            ]
        )
        ViewText(string_output).show()
