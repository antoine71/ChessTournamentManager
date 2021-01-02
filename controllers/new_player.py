from models import Player, PlayerDatabaseConverter
import controllers.database_management as dbm

from views import ViewPrompt, View


class ControllerNewPlayer:

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
        View("Création du joueur terminée avec succès.").show()
        dbm.ControllerSavePlayer(player).run()
