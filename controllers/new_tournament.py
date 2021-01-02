import controllers.main_controllers as mc
from controllers.database_management import ControllerSaveTournament

from models import Tournament

from views import ViewPrompt, View, ViewDatabase


class ControllerNewTournament:

    def __init__(self, tournament_database, player_database):
        self.tournament_database = tournament_database
        self.player_database = player_database

    def run(self):
        tournament = Tournament(*[ViewPrompt(variable).show() for variable in
                                  [
                                      'Nom : ',
                                      'Description : ',
                                      'Date de début : ',
                                      'date de fin : ',
                                      'Nombre de rounds: ',
                                      'Controle du temps: '
                                  ]])
        tournament.players = ControllerChoosePlayer(self.player_database).run()
        self.tournament_database.add_data(tournament)
        ControllerSaveTournament(tournament).run()
        View("Création du tournoi terminée avec succès.").show()
        return self.tournament_database


class ControllerChoosePlayer:

    def __init__(self, player_database):
        self.player_database = player_database

    def run(self):
        ViewDatabase(
            self.player_database,
            "Sélection des joueurs:",
            "last_name", "first_name", "date_of_birth", "ranking",
            sort_by_attribute="last_name"
        ).show()
        tournament_players = []
        while len(tournament_players) < Tournament.NUMBER_OF_PLAYERS:
            mc.ControllerNavigation(
                "(X) Choisir un joueur par son numéro",
                {
                    str(i): ControllerAddPlayer(tournament_players, self.player_database.data[i])
                    for i in range(len(self.player_database.data))
                }
            ).run()
        return tournament_players


class ControllerAddPlayer:

    def __init__(self, tournament_players_list, player):
        self.tournament_players_list = tournament_players_list
        self.player = player

    def run(self):
        if self.player in self.tournament_players_list:
            View("Saisie non valide, {} {} est déjà inscrit au tournoi"
                 .format(self.player.first_name, self.player.last_name)).show()
        else:
            self.tournament_players_list.append(self.player)
            View("{} {} est inscrit au tournoi."
                 .format(self.player.first_name, self.player.last_name)).show()
