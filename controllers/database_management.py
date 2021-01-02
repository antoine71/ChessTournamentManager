"""This module groups all the controllers related to the management of the TinyDB database"""

from models.database import PlayerDatabaseConverter, TournamentDatabaseConverter

from views.general import ViewText


class ControllerSaveTournament:
    """This controller is called to save a tournament to the database"""

    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        TournamentDatabaseConverter().save_tournament(self.tournament)
        ViewText("Sauvegarde de la base de données Tournoi.").show()


class ControllerSavePlayer:
    """This controller is called to save a player to the database"""

    def __init__(self, player):
        self.player = player

    def run(self):
        PlayerDatabaseConverter().save_player(self.player)
        ViewText("Sauvegarde de la base de données Joueurs.").show()