import controllers.main_controllers as mc
from controllers.database_management import ControllerSaveTournament
import controllers.tournament_display as ctd

from views import View, ViewRoundResult


class ControllerPlayTournament:

    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        self.tournament.play_tournament()
        View("Démarrage du tournoi").show()
        for round_ in self.tournament.rounds:
            if round_.status == "terminé":
                ViewRoundResult(round_).show()
            else:
                while round_.status != "terminé":
                    ViewRoundResult(round_).show()
                    if round_.status == "pas encore commencé":
                        mc.ControllerNavigation(
                            "(t) Procéder au tirage des matchs",
                            {"t": ControllerDrawGames(round_)}
                        ).run()
                        ControllerSaveTournament(self.tournament).run()
                        continue
                    else:
                        mc.ControllerNavigation(
                            "(X) Entrer le résultat du match X",
                            {
                                str(i): ControllerEnterResults(round_.games[i])
                                for i in range(len(round_.games))
                            }
                        ).run()
                        ControllerSaveTournament(self.tournament).run()
                ViewRoundResult(round_).show()
        View("Tournoi Terminé").show()
        mc.ControllerNavigation(
            "(r) Afficher le rapport de tournoi",
            {"r": ctd.ControllerTournamentReport(self.tournament)}
        ).run()


class ControllerEnterResults:

    def __init__(self, game):
        self.game = game

    def run(self):
        if self.game.status == "terminé":
            View("Le match est déja joué.").show()
        else:
            View("{} VS {}".format(self.game.pair[0], self.game.pair[1])).show()
            mc.ControllerNavigation(
                "(1 / n / 2) Entrez le résultat\n",
                {
                    "1": ControllerUpdateResult(self.game, "1"),
                    "n": ControllerUpdateResult(self.game, "n"),
                    "2": ControllerUpdateResult(self.game, "2"),
                }).run()


class ControllerUpdateResult:

    def __init__(self, game, result):
        self.game = game
        self.result = result

    def run(self):
        self.game.update_result(self.result)


class ControllerDrawGames:

    def __init__(self, round_):
        self.round_ = round_

    def run(self):
        self.round_.draw_games()