from tinydb import TinyDB

from models import Database, Player, Tournament, TournamentDatabaseConverter, PlayerDatabaseConverter
from views import View, ViewPrompt, ViewChoosePlayer

from operator import itemgetter


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

    def run(self, commands, user_command):
        controller = commands[user_command]
        return controller


class ControllerPlayerDatabase:

    def __init__(self, player_database, sort_by="last_name", reverse_=False):
        self.player_database = player_database
        self.player_database.sort_by(sort_by, reverse_)

    def run(self):
        ControllerView(View("Base de données des joueurs")).run()
        players_list_string_output = "\n".join(
            [
                "{}, {} - Né(e) le {} - Classement: {}".format(
                    player.last_name,
                    player.first_name,
                    player.date_of_birth,
                    player.ranking
                )
                for player in self.player_database
            ]
        )
        ControllerView(View(players_list_string_output)).run()
        ControllerView(View(
            """Commandes:
            (n) Trier par nom de famille
            (c) Trier par classement
            (m) Retour au menu"""
        )).run()
        user_command = ControllerView(ViewPrompt('Saississez votre commande : ')).run()
        controller = ControllerNavigation().run(
            {
                'n': ControllerPlayerDatabase(self.player_database, sort_by="last_name", reverse_=False),
                'c': ControllerPlayerDatabase(self.player_database, sort_by="ranking", reverse_=True),
                'm': Controller(),
            },
            user_command)
        controller.run()


class ControllerTournamentDatabase:

    def __init__(self, tournament_database):
        self.tournament_database = tournament_database

    def run(self):
        ControllerView(View("Base de données des tournois")).run()
        tournament_list_string_output = "\n".join(
            [
                "({}) - {} - du {} au {} - Contrôle du temps: {} - status: {}".format(
                    i,
                    tournament.name,
                    tournament.start_date,
                    tournament.end_date,
                    tournament.time_control,
                    tournament.status
                )
                for i, tournament in enumerate(self.tournament_database)
            ]
        )
        ControllerView(View(tournament_list_string_output)).run()
        ControllerView(View(
            """Commandes:
            Saississez le numéro d'un tournoi pour afficher les détails ou
            (m) Revenir au menu principal"""
        )).run()
        user_command = ControllerView(ViewPrompt('Saississez votre commande : ')).run()
        if user_command.isdigit():
            controller = ControllerTournamentDetailNavigation(self.tournament_database, int(user_command)).run()
        else:
            controller = ControllerNavigation().run(
                {
                    'm': Controller(),
                },
                user_command)
        controller.run()


class ControllerTournamentDetailNavigation:

    def __init__(self, tournament_database, tournament_number):
        self.tournament_database = tournament_database
        self.tournament_number = tournament_number

    def run(self):
        return ControllerTournamentDetail(self.tournament_database[self.tournament_number])


class ControllerTournamentDetail:

    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        ControllerView(View("Détails du tournoi:")).run()
        string_output = "\n".join([
            "\tNom : {}".format(self.tournament.name),
            "\tDescription : {}".format(self.tournament.description),
            "\tDate de début : {}".format(self.tournament.start_date),
            "\tDate de fin : {}".format(self.tournament.end_date),
            "\tNombre de rounds : {}".format(self.tournament.number_of_rounds),
            "\tContrôle du temps : {}".format(self.tournament.time_control),
            "\tStatus : {}".format(self.tournament.status),
        ])
        ControllerView(View(string_output)).run()
        ControllerView(View("Joueurs engagés:")).run()
        for player in self.tournament.players:
            ControllerPlayerDetail(player).run()
        ControllerView(View("Classement:")).run()
        ControllerScoreTable(self.tournament.score_table).run()
        ControllerView(View("Résultats des matchs:")).run()
        if not self.tournament.rounds:
            ControllerView(View("\tPas disponible")).run()
        else:
            for round_ in self.tournament.rounds:
                ControllerRoundDetail(round_).run()
        user_command = ControllerView(ViewPrompt('Saississez votre commande : ')).run()
        if user_command == "p":
            ControllerPlayTournament(self.tournament).run()


class ControllerScoreTable:

    def __init__(self, score_table):
        self.score_table = score_table

    def run(self):
        if not self.score_table.score_table:
            string_output = "\tPas disponible"
        else:
            sorted_score_table = sorted(self.score_table.score_table.items(), key=itemgetter(1), reverse=True)
            string_output = "\n".join([
                "\t{}: {}".format(player, score)
                for player, score in sorted_score_table
            ])
        ControllerView(View(string_output)).run()


class ControllerPlayerDetail:

    def __init__(self, player):
        self.player = player

    def run(self):
        string_output = "\t{}, {} - Né(e) le {} - Classement: {}".format(
                self.player.last_name,
                self.player.first_name,
                self.player.date_of_birth,
                self.player.ranking
        )
        ControllerView(View(string_output)).run()


class ControllerRoundDetail:

    def __init__(self, round_):
        self.round_ = round_

    def run(self):
        ControllerView(View("\t{} - {}".format(self.round_.name, self.round_.status))).run()
        if not self.round_.games:
            ControllerView(View("\t\tPas disponible")).run()
        else:
            for game in self.round_.games:
                ControllerGameDetail(game).run()


class ControllerGameDetail:

    def __init__(self, game):
        self.game = game

    def run(self):
        match_result_string_output = "\t".join([
            "\t\t{}: {}".format(player, score)
            for player, score in self.game.score_table.score_table.items()
        ])
        string_output = ' - '.join([self.game.status, match_result_string_output])
        ControllerView(View(string_output)).run()


class ControllerPlayTournament(Controller):

    def __init__(self, tournament):
        self.tournament = tournament

    def run(self):
        self.tournament.play_tournament()
        ControllerView(View("Démarrage du tournoi")).run()
        for round_ in self.tournament.rounds:
            if round_.status == "terminé":
                ControllerRoundDetail(round_).run()
            else:
                while round_.status != "terminé":
                    ControllerRoundDetail(round_).run()
                    if round_.status == "pas encore commencé":
                        user_command = ControllerView(ViewPrompt('(t) Procéder au tirage des matchs : ')).run()
                        if user_command == "t":
                            round_.draw_games()
                            ControllerSaveTournament(self.tournament).run()
                            continue
                    else:
                        user_command = ControllerView(ViewPrompt('Entrez le résultat du match (numéro du match) : ')).run()
                        ControllerEnterResults(round_.games[int(user_command) - 1]).run()
                        ControllerSaveTournament(self.tournament).run()
                ControllerRoundDetail(round_).run()
        ControllerView(View("Tournoi Terminé")).run()
        user_command = ControllerView(ViewPrompt('(r) Afficher le rapport de tournoi ou (m) menu: ')).run()
        if user_command == "r":
            ControllerTournamentDetail(self.tournament).run()
        else:
            Controller().run()


class ControllerEnterResults(Controller):

    def __init__(self, game):
        self.game = game

    def run(self):
        ControllerView(View("{} VS {}".format(self.game.pair[0], self.game.pair[1]))).run()
        user_command = ControllerView(ViewPrompt('Entrez le résultat (1 / 2 / n) : ')).run()
        self.game.update_result(user_command)


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
        return self.tournament_database


class ControllerChoosePlayer:

    def __init__(self, player_database):
        self.player_database = player_database

    def run(self):
        ControllerView(ViewChoosePlayer(self.player_database)).run()
        tournament_players = []
        while len(tournament_players) < Tournament.NUMBER_OF_PLAYERS:
            user_command = int(ControllerView(ViewPrompt('Choisissez un joueur : ')).run())
            tournament_players.append(self.player_database.data[user_command])
        return tournament_players
