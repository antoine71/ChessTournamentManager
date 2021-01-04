"""This module contains the controllers related to the creation of a new tournament"""

import controllers.main_controllers as mc
from controllers.database_management import ControllerSaveTournament

from models.tournament import Tournament, TournamentDataValidator

from views.general import ViewPrompt, ViewText
from views.database import ViewDatabase

import utils


class ControllerNewTournament:
    """This controller is called to create a new tournament.
    It will request the input data from the user, instantiate a Tournament object, add the tournament to the
    tournaments Database object and save the new tournament to the TinyDB json file"""

    def __init__(self, tournament_database, player_database):
        self.tournament_database = tournament_database
        self.player_database = player_database

    def run(self):
        tournament_data = []
        validator = TournamentDataValidator()
        prompt = (
            ('Nom (max. 50 caractères): ', validator.is_name_ok),
            ('Description (max. 50 caractères): ', validator.is_description_ok),
            ('Lieu (max. 50 caractères): ', validator.is_place_ok),
            ('Date de début (jj/mm/aaaa): ', validator.is_start_date_ok),
            ('Date de fin (jj/mm/aaaa): ', validator.is_end_date_ok),
            ('Nombre de rounds:  (entier positif, par défaut: 4): ', validator.is_number_of_rounds_ok),
            ('Contrôle du temps (blitz / bullet / coup rapide): ', validator.is_time_control_ok)
        )
        for message, check_function in prompt:
            user_input = ViewPrompt(message).show()
            while not check_function(user_input):
                ViewText("Erreur de saisie, veuillez recommencer.").show()
                user_input = ViewPrompt(message).show()
            tournament_data.append(user_input)
        tournament = Tournament(*tournament_data)

        if tournament not in self.tournament_database:
            tournament.players = ControllerChoosePlayer(self.player_database).run()
            self.tournament_database.append(tournament)
            ViewText("Création du tournoi terminée avec succès.").show()
            ControllerSaveTournament(tournament).run()
        else:
            ViewText("Erreur: le tournoi existe déjà (même nom, dates, contrôle du temps.").show()


class ControllerChoosePlayer:
    """This controller is called to offer the user the possibility to select a player from the players database.
    It will offer to select all the players needed to create the tournament, and return the list of players"""

    def __init__(self, player_database):
        self.player_database = player_database

    def run(self):
        ViewDatabase(
            self.player_database,
            "Sélection des joueurs:",
            "last_name", "first_name", "date_of_birth", "ranking",
            sort_by_attribute="last_name",
            sort_order=False
        ).show()
        tournament_players = []
        while len(tournament_players) < Tournament.NUMBER_OF_PLAYERS:
            mc.ControllerCommandInterpreter(
                "(X) Choisir un joueur par son numéro",
                {
                    str(i + 1): ControllerAddPlayer(tournament_players, self.player_database[i])
                    for i in range(len(self.player_database))
                }
            ).run()
        return tournament_players


class ControllerAddPlayer:
    """This controller is called when a player has been selected, to verify if the selection is valid and add
    the players to the list of players"""

    def __init__(self, tournament_players_list, player):
        self.tournament_players_list = tournament_players_list
        self.player = player

    def run(self):
        if self.player in self.tournament_players_list:
            ViewText("Saisie non valide, {} {} est déjà inscrit au tournoi"
                     .format(self.player.first_name, self.player.last_name)).show()
        else:
            self.tournament_players_list.append(self.player)
            ViewText("{} {} est inscrit au tournoi."
                     .format(self.player.first_name, self.player.last_name)).show()
