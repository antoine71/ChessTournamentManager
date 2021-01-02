from tinydb import TinyDB

from controllers.new_player import ControllerNewPlayer
from controllers.new_tournament import ControllerNewTournament
from controllers.player_display import ControllerPlayerDatabase
from controllers.tournament_display import ControllerTournamentDatabase

from models import Database, Player, TournamentDatabaseConverter

from views import View, ViewPrompt


class ControllerMain:

    def run(self):
        player_database = Database()
        tournament_database = Database()

        players_db = TinyDB("players_db.json")
        for item in players_db:
            player_database.add_data(Player(**item))

        tournament_db = TinyDB("db_tournament.json")
        for tournament_json in tournament_db:
            tournament_database.add_data(TournamentDatabaseConverter().load_tournament(tournament_json))

        while True:
            ControllerMainMenu(player_database, tournament_database).run()


class ControllerNavigation:

    def __init__(self, message, commands, return_to_menu=True):
        self.commands = commands
        if return_to_menu:
            self.commands['m'] = ControllerMain()
            self.message = "(m) Retour au menu principal" if not message else message + "\n(m) Retour au menu principal"
        else:
            self.message = message

    def is_user_command_valid(self, user_command):
        return user_command in self.commands

    def run(self):
        View(self.message).show()
        user_command = ViewPrompt('Saississez votre commande : ').show()
        while not self.is_user_command_valid(user_command):
            user_command = ViewPrompt('Commande Invalide. Veuillez réessayer : ').show()
        controller = self.commands[user_command]
        controller.run()


class ControllerMainMenu:

    def __init__(self, player_database, tournament_database):
        self.player_database = player_database
        self.tournament_database = tournament_database

    def run(self):
        View("Chess Tournament Manager - Menu principal.").show()
        ControllerNavigation(
            "\t(1) Ajouter un joueur\n"
            "\t(2) Ajouter un Tournoi\n"
            "\t(3) Voir les joueurs\n"
            "\t(4) Voir les tournois",
            {
                '1': ControllerNewPlayer(self.player_database),
                '2': ControllerNewTournament(self.tournament_database, self.player_database),
                '3': ControllerPlayerDatabase(self.player_database),
                '4': ControllerTournamentDatabase(self.tournament_database)
            },
            return_to_menu=False
        ).run()
