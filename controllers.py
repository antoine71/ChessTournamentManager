from tinydb import TinyDB

from models import Database, Player, Tournament, TournamentDatabaseConverter, PlayerDatabaseConverter
from views import View, ViewPrompt, ViewChoosePlayer, ViewDatabase, ViewScoreTable, ViewTournamentResult, \
    ViewTournamentDetails, ViewRoundResult


class Controller:

    def run(self):
        pass


class ControllerMain(Controller):

    def run(self):
        player_database = Database()
        tournament_database = Database()

        players_db = TinyDB("players_db.json")
        for item in players_db:
            player_database.add_data(Player(**item))

        tournament_db = TinyDB("db_tournament.json")
        for tournament_json in tournament_db:
            tournament_database.add_data(TournamentDatabaseConverter().load_tournament(tournament_json))

        menu_view = View(
            """Menu:
            (1) Ajouter un joueur
            (2) Ajouter un Tournoi
            (3) Voir les joueurs
            (4) Voir les tournois"""
        )
        command_prompt_view = ViewPrompt('Saississez votre commande : ')

        while True:
            ControllerView(menu_view).run()
            user_command = ControllerView(command_prompt_view).run()
            controller = ControllerMainMenu(user_command, player_database, tournament_database).run()
            controller.run()


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


class ControllerMainMenu(Controller):

    def __init__(self, user_command, player_database, tournament_database):
        self.user_command = user_command
        self.commands = {
            '1': ControllerNewPlayer(player_database),
            '2': ControllerNewTournament(tournament_database, player_database),
            '3': ControllerPlayerDatabase(player_database),
            '4': ControllerTournamentDatabase(tournament_database)
        }

    def run(self):
        return self.commands[self.user_command]


class ControllerView(Controller):

    def __init__(self, view):
        self.view = view

    def run(self):
        return self.view.show()


class ControllerNavigation:

    def __init__(self, message, commands, return_to_menu=True):
        self.commands = commands
        if return_to_menu:
            self.commands['m'] = Controller()
            self.message = "(m) Retour au menu principal" if not message else message + "\n(m) Retour au menu principal"
        else:
            self.message = message

    def is_user_command_valid(self, user_command):
        return user_command in self.commands

    def run(self):
        View(self.message).show()
        user_command = ControllerView(ViewPrompt('Saississez votre commande : ')).run()
        while not self.is_user_command_valid(user_command):
            user_command = ControllerView(ViewPrompt('Commande Invalide. Veuillez réessayer : ')).run()
        controller = self.commands[user_command]
        controller.run()


class ControllerPlayerDatabase:

    def __init__(self, player_database, sort_by_attribute="last_name"):
        self.player_database = player_database
        self.sort_by_attribute = sort_by_attribute

    def run(self):
        view = ViewDatabase(self.player_database,
                            "Base de données des Joueurs",
                            'last_name', 'first_name', 'date_of_birth', 'ranking',
                            selection_mode=False, sort_by_attribute=self.sort_by_attribute)
        view.show()

        ControllerNavigation(
            "(n) Trier par nom de famille\n"
            "(c) Trier par classement",
            {
                'n': ControllerPlayerDatabase(self.player_database, sort_by_attribute="last_name"),
                'c': ControllerPlayerDatabase(self.player_database, sort_by_attribute="ranking")
            },
        ).run()


class ControllerTournamentDatabase:

    def __init__(self, tournament_database):
        self.tournament_database = tournament_database

    def run(self):
        view = ViewDatabase(self.tournament_database,
                            "Base de données des Tournois",
                            'name', 'start_date', 'end_date')
        view.show()

        ControllerNavigation(
            "(X) Saississez le numéro d'un tournmoi pour afficher le rapport du tournoi",
            {
                str(i): ControllerTournamentReport(self.tournament_database[i])
                for i in range(len(self.tournament_database.data))
            }).run()


class ControllerTournamentReport:

    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        ViewTournamentDetails("Détails du Tournoi", self.tournament).show()
        ViewDatabase(
            Database(self.tournament.players),
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
        ControllerNavigation(commands_message, commands_list).run()


class ControllerDrawGames:

    def __init__(self, round_):
        self.round_ = round_

    def run(self):
        self.round_.draw_games()


class ControllerPlayTournament(Controller):

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
                        ControllerNavigation(
                            "(t) Procéder au tirage des matchs",
                            {"t": ControllerDrawGames(round_)}
                        ).run()
                        ControllerSaveTournament(self.tournament).run()
                        continue
                    else:
                        ControllerNavigation(
                            "(X) Entrer le résultat du match X",
                            {
                                str(i): ControllerEnterResults(round_.games[i])
                                for i in range(len(round_.games))
                            }
                        ).run()
                        ControllerSaveTournament(self.tournament).run()
                ViewRoundResult(round_).show()
        View("Tournoi Terminé").show()
        ControllerNavigation(
            "(r) Afficher le rapport de tournoi",
            {"r": ControllerTournamentReport(self.tournament)}
        ).run()


class ControllerEnterResults(Controller):

    def __init__(self, game):
        self.game = game

    def run(self):
        if self.game.status == "terminé":
            View("Le match est déja joué.").show()
        else:
            ControllerView(View("{} VS {}".format(self.game.pair[0], self.game.pair[1]))).run()
            ControllerNavigation(
                "(1 / n / 2) Entrez le résultat\n"
                "(a) Annuler",
                {
                    "1": ControllerUpdateResult(self.game, "1"),
                    "n": ControllerUpdateResult(self.game, "n"),
                    "2": ControllerUpdateResult(self.game, "2"),
                    "a": Controller()
                }).run()


class ControllerUpdateResult:

    def __init__(self, game, result):
        self.game = game
        self.result = result

    def run(self):
        self.game.update_result(self.result)


class ControllerNewPlayer(Controller):

    def __init__(self, database):
        self.database = database

    def run(self):
        player = Player(*[ViewPrompt(variable).show() for variable in
                          [
                              'Nom : ',
                              'Prénom : ',
                              'Date de naissance : ',
                              'classement : '
                          ]])
        self.database.add_data(player)
        PlayerDatabaseConverter().save_player(player)
        View("Création du joueur terminée avec succès.").show()
        return self.database


class ControllerNewTournament(Controller):

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
            ControllerNavigation(
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
