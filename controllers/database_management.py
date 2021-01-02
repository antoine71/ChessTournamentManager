from models import TournamentDatabaseConverter, PlayerDatabaseConverter

from views import View


class ControllerSaveTournament:

    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        TournamentDatabaseConverter().save_tournament(self.tournament)
        View("Sauvegarde de la base de données Tournoi.").show()


class ControllerSavePlayer:

    def __init__(self, player):
        self.player = player

    def run(self):
        PlayerDatabaseConverter().save_player(self.player)
        View("Sauvegarde de la base de données Joueurs.").show()