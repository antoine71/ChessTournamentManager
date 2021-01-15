"""This module contains the controllers related to the operation of a tournament"""

import controllers.main_controllers as mc
from controllers.database_management_controllers import ControllerSaveTournament
import controllers.tournament_display_controllers as ctd

from views.general_views import ViewText
from views.tournament_views import ViewRoundResult


class ControllerPlayTournament:
    """This controller is called on a tournament that is not yet completed.
    It will allow the user to draw the games for each round and enter the results.
    After each update, the tournament TinyDB json file is updated."""

    def __init__(self, tournament, tournament_database):
        self.tournament = tournament
        self.tournament_database = tournament_database

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
                        round_.start()
                        ControllerSaveTournament(self.tournament).run()
                        continue
                    else:
                        if not round_.status == "matchs terminé, en attente de validation":
                            commands = {
                                    str(i + 1): ControllerEnterResults(round_.games[i])
                                    for i in range(len(round_.games))
                            }
                            commands.update({
                                    "s": ControllerSaveTournament(self.tournament)
                            })
                            mc.ControllerCommandInterpreter(
                                "(X) Entrer le résultat du match X\n"
                                "(s) Sauvegarder le tournoi",
                                commands
                            ).run()
                        else:
                            commands = {
                                str(i + 1): ControllerEnterResults(round_.games[i])
                                for i in range(len(round_.games))
                            }
                            commands.update({
                                "s": ControllerEndRound(self.tournament, round_)
                            })
                            mc.ControllerCommandInterpreter(
                                "(X) Entrer le résultat du match X\n"
                                "(s) Sauvegarder le tournoi et passer au round suivant",
                                commands
                            ).run()
                ViewRoundResult(round_).show()
        ViewText("Tournoi Terminé").show()
        mc.ControllerCommandInterpreter(
            "(r) Afficher le rapport de tournoi",
            {"r": ctd.ControllerTournamentReport(self.tournament, self.tournament_database)}
        ).run()


class ControllerEnterResults:
    """This controller is called to request the user to enter a game result"""
    def __init__(self, game):
        self.game = game

    def run(self):
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


class ControllerEndRound:
    """This controller is called to end the round"""

    def __init__(self, tournament, round_):
        self.tournament = tournament
        self.round_ = round_

    def run(self):
        self.round_.end()
        ControllerSaveTournament(self.tournament).run()
