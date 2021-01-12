"""This module groups the class related to the display of players"""

import controllers.main_controllers as mc
from controllers.play_tournament_controllers import ControllerPlayTournament
from controllers.database_management_controllers import ControllerDeleteTournament

from views.database_views import ViewDatabase, ViewDatabaseDetails
from views.tournament_views import ViewScoreTable, ViewTournamentResult


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
            "supprimer " + str(i + 1): ControllerDeleteTournament(self.tournament_database[i],
                                                                  self.tournament_database)
            for i in range(len(self.tournament_database))
        }
        commands.update({
                str(i + 1): ControllerTournamentReport(self.tournament_database[i], self.tournament_database)
                for i in range(len(self.tournament_database))
            }
        )

        mc.ControllerCommandInterpreter(
            "(X) Afficher le rapport du tournoi numéro X",
            commands
        ).run()


class ControllerTournamentReport:
    """This class manages the display of the tournament report"""

    def __init__(self, tournament, tournament_database):
        self.tournament = tournament
        self.tournament_database = tournament_database

    def run(self):
        ViewDatabaseDetails(
            "Détails du Tournoi",
            self.tournament,
            ["Nom", "Description", "Lieu", "Date de début", "Date de fin", "Nombre de rounds",
             "Contrôle du temps", "Status"],
            ["name", "description", "place", "start_date", "end_date", "number_of_rounds",
             "time_control", "status"]
        ).show()
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
            commands_list = {"j": ControllerPlayTournament(self.tournament, self.tournament_database)}
        else:
            commands_message = ""
            commands_list = {}

        commands_message += "\n(supprimer) Supprimer le tournoi de la base de donnée"
        commands_list['supprimer'] = ControllerDeleteTournament(self.tournament, self.tournament_database)

        mc.ControllerCommandInterpreter(commands_message, commands_list).run()
