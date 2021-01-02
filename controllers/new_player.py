"""This module contains the controllers related to the creation of a new player"""

from models.player import Player

from controllers.database_management import ControllerSavePlayer

from views.general import ViewPrompt, ViewText


class ControllerNewPlayer:
    """This controller is called to create a new player and add it to the database.
    It will request the input data from the user, instantiate a Player object, add the player to the
    players Database object and save the new player to the TinyDB json file"""

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
        self.database.append(player)
        ViewText("Création du joueur terminée avec succès.").show()
        ControllerSavePlayer(player).run()
