"""This module contain the main controllers of the program"""

from controllers.new_player import ControllerNewPlayer
from controllers.new_tournament import ControllerNewTournament
from controllers.player_display import ControllerPlayerDatabase
from controllers.tournament_display import ControllerTournamentDatabase

from models.database import TournamentDatabaseConverter, PlayerDatabaseConverter

from views.general import ViewText, ViewPrompt


class ControllerMain:
    """The main controller is called
    It will load the players and tournament databases, and instantiate them in Database objects
    It will then instantiate a ControllerMainMenu"""

    def run(self):
        player_database = PlayerDatabaseConverter().load_database()
        tournament_database = TournamentDatabaseConverter().load_database()

        while True:
            ControllerMainMenu(player_database, tournament_database).run()


class ControllerCommandInterpreter:
    """This controller is called to collect a command from the user and call the controller associated with the
    command.
    This controller verifies if the user input is valid.
    The parameters are the following:
        message: it is a string that will be displayed on the screen, it shall contain the list of possible commands.
        commands: it is a dictionary.
                        the keys are the commands that the user shall type
                        the values are the controllers that shall be called by the commands. the controllers shall have
                        method run()
        return_to_menu: True command to implement a return to main menu command, False otherwise.
    """

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
        ViewText(self.message).show()
        user_command = ViewPrompt('Saississez votre commande : ').show()
        while not self.is_user_command_valid(user_command):
            user_command = ViewPrompt('Commande invalide. Veuillez réessayer : ').show()
        controller = self.commands[user_command]
        controller.run()


class ControllerMainMenu:
    """This controller is called to display the program main menu"""

    def __init__(self, player_database, tournament_database):
        self.player_database = player_database
        self.tournament_database = tournament_database

    def run(self):
        ViewText("Chess Tournament Manager - Menu principal.").show()
        ControllerCommandInterpreter(
            "\t(1) Ajouter un joueur\n"
            "\t(2) Ajouter un Tournoi\n"
            "\t(3) Voir les joueurs\n"
            "\t(4) Voir les tournois\n"
            "\t(q) Quitter le programme",
            {
                "1": ControllerNewPlayer(self.player_database),
                "2": ControllerNewTournament(self.tournament_database, self.player_database),
                "3": ControllerPlayerDatabase(self.player_database),
                "4": ControllerTournamentDatabase(self.tournament_database),
                "q": ControllerQuitProgram()

            },
            return_to_menu=False
        ).run()


class ControllerQuitProgram:

    def run(self):
        quit()
