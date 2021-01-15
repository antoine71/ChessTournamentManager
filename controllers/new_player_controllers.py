"""This module contains the controllers related to the creation of a new player"""

from models.player import Player, PlayerDataValidator

from views.general_views import ViewPrompt, ViewText

from controllers.database_management_controllers import ControllerSavePlayer


class ControllerNewPlayer:
    """This controller is called to create a new player and add it to the database.
    It will request the input data from the user, instantiate a Player object, add the player to the
    players Database object and save the new player to the TinyDB json file"""

    def __init__(self, database):
        self.database = database

    def run(self):

        player_data = []
        validator = PlayerDataValidator()
        prompt = (
            ('Nom (max. 50 caractères): ', validator.is_last_name_ok),
            ('Prénom (max. 50 caractères): ', validator.is_first_name_ok),
            ('Date de naissance (jj/mm/aaaa): ', validator.is_date_of_birth_ok),
            ('Sexe (m/f): ', validator.is_sex_ok),
            ('classement (entier positif): ', validator.is_ranking_ok)
        )
        for message, check_function in prompt:
            user_input = ViewPrompt(message).show()
            while not check_function(user_input):
                ViewText("Erreur de saisie, veuillez recommencer.").show()
                user_input = ViewPrompt(message).show()
            player_data.append(user_input)
        player = Player(*player_data)

        if player not in self.database:
            self.database.append(player)
            ViewText("Création du joueur terminée avec succès.").show()
            ControllerSavePlayer(player).run()
        else:
            ViewText("Erreur: le joueur existe déjà (même nom, prénom et date de naissance).").show()
