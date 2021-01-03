"""This module contains the controllers related to the operation of a tournament"""

import controllers.main_controllers as mc
from controllers.database_management import ControllerSaveTournament
import controllers.tournament_display as ctd

from views.general import ViewText
from views.tournament import ViewRoundResult


class ControllerPlayTournament:
    """This controller is called on a tournament that is not yet completed.
    It will allow the user to draw the games for each round and enter the results.
    After each update, the tournament TinyDB json file is updated."""

    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        self.tournament.play_tournament()
        ViewText("Démarrage du tournoi").show()
        for round_ in self.tournament.rounds:
            if round_.status == "terminé":
                ViewRoundResult(round_).show()
            else:
                while round_.status != "terminé":
                    ViewRoundResult(round_, mode_view_results=False).show()
                    if round_.status == "pas encore commencé":
                        mc.ControllerCommandInterpreter(
                            "(t) Procéder au tirage des matchs",
                            {"t": ControllerDrawGames(round_)}
                        ).run()
                        ControllerSaveTournament(self.tournament).run()
                        continue
                    else:
                        mc.ControllerCommandInterpreter(
                            "(X) Entrer le résultat du match X",
                            {
                                str(i + 1): ControllerEnterResults(round_.games[i])
                                for i in range(len(round_.games))
                            }
                        ).run()
                        ControllerSaveTournament(self.tournament).run()
                ViewRoundResult(round_).show()
        ViewText("Tournoi Terminé").show()
        mc.ControllerCommandInterpreter(
            "(r) Afficher le rapport de tournoi",
            {"r": ctd.ControllerTournamentReport(self.tournament)}
        ).run()


class ControllerEnterResults:
    """This controller is called to request the user to enter a game result"""
    def __init__(self, game):
        self.game = game

    def run(self):
        if self.game.status == "terminé":
            ViewText("Le match est déja joué.").show()
        else:
            ViewText("{} VS {}".format(self.game.pair[0], self.game.pair[1])).show()
            mc.ControllerCommandInterpreter(
                "(1 / n / 2) Entrez le résultat\n",
                {
                    "1": ControllerUpdateResult(self.game, "1"),
                    "n": ControllerUpdateResult(self.game, "n"),
                    "2": ControllerUpdateResult(self.game, "2"),
                }).run()


class ControllerUpdateResult:
    """This controller is called to update the game results on the Game object"""

    def __init__(self, game, result):
        self.game = game
        self.result = result

    def run(self):
        self.game.update_result(self.result)


class ControllerDrawGames:
    """This controller is called to draw the games from a Round object"""

    def __init__(self, round_):
        self.round_ = round_

    def run(self):
        self.round_.draw_games()
