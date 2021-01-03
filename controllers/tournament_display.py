"""This module groups the class related to the display of players"""

import controllers.main_controllers as mc
from controllers.database_management import ControllerDeleteTournament
from controllers.play_tournament import ControllerPlayTournament
from controllers.database_management import ControllerDeleteTournament

from views.database import ViewDatabase
from views.tournament import ViewTournamentDetails, ViewScoreTable, ViewTournamentResult


class ControllerTournamentDatabase:
    """This class manages the display of the list of tournaments"""

    def __init__(self, tournament_database):
        self.tournament_database = tournament_database

    def run(self):
        view = ViewDatabase(self.tournament_database,
                            "Base de données des Tournois",
                            'name', 'start_date', 'end_date', 'status',
                            sort_by_attribute="start_date",
                            sort_order=True)
        view.show()

        commands = {
            "supprimer " + str(i + 1): ControllerDeleteTournament(self.tournament_database[i], self.tournament_database)
            for i in range(len(self.tournament_database))
        }
        commands.update({
                str(i + 1): ControllerTournamentReport(self.tournament_database[i])
                for i in range(len(self.tournament_database))
            }
        )

        mc.ControllerCommandInterpreter(
            "(X) Saississez le numéro d'un tournoi pour afficher le rapport du tournoi\n"
            "(supprimer X) Supprimer le tournoi",
            commands
        ).run()


class ControllerTournamentReport:
    """This class manages the display of the tournament report"""

    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        ViewTournamentDetails("Détails du Tournoi", self.tournament).show()
        ViewDatabase(
            self.tournament.players,
            "Liste des joueurs engagés",
            'last_name', 'first_name', 'date_of_birth', 'ranking',
            selection_mode=False,
            sort_by_attribute="last_name"
        ).show()
        ViewScoreTable("Classement:", self.tournament.score_table).show()
        ViewTournamentResult("Résultats du Tournoi:", self.tournament).show()

        if self.tournament.status != "terminé":
            commands_message = "(j) Jouer / reprendre le tournoi"
            commands_list = {"j": ControllerPlayTournament(self.tournament)}
        else:
            commands_message = ""
            commands_list = {}

        mc.ControllerCommandInterpreter(commands_message, commands_list, ).run()
