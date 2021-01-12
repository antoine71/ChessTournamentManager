"""This module groups all the controllers related to the management of the TinyDB database"""

from models.database import PlayerDatabaseConverter, TournamentDatabaseConverter

from views.general_views import ViewText


class ControllerSaveTournament:
    """This controller is called to save a tournament to the database"""

    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        TournamentDatabaseConverter().save_tournament(self.tournament)
        ViewText("Sauvegarde de la base de données Tournoi.").show()


class ControllerDeleteTournament:

    def __init__(self, tournament, tournament_database):
        self.tournament = tournament
        self.tournament_database = tournament_database

    def run(self):
        TournamentDatabaseConverter().delete_tournament(self.tournament)
        self.tournament_database.remove(self.tournament)
        ViewText("Le tournoi \"{}\" a été supprimé de la base de données.".format(self.tournament.name)).show()


class ControllerSavePlayer:
    """This controller is called to save a player to the database"""

    def __init__(self, player):
        self.player = player

    def run(self):
        PlayerDatabaseConverter().save_player(self.player)
        ViewText("Sauvegarde de la base de données Joueurs.").show()


class ControllerDeletePlayer:

    def __init__(self, player, player_database):
        self.player = player
        self.player_database = player_database

    def run(self):
        PlayerDatabaseConverter().delete_player(self.player)
        self.player_database.remove(self.player)
        ViewText("Le joueur {} {} a été supprimé de la base de données.".format(self.player.first_name,
                                                                                self.player.last_name)).show()
