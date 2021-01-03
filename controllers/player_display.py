"""This module groups the controllers related to the display of players"""

import controllers.main_controllers as mc
from controllers.database_management import ControllerDeletePlayer

from views.database import ViewDatabase


class ControllerPlayerDatabase:
    """This class manages the display of the list of players"""

    def __init__(self, player_database, sort_by_attribute="last_name", sort_order=False):
        self.player_database = player_database
        self.sort_by_attribute = sort_by_attribute
        self.sort_order = sort_order

    def run(self):
        view = ViewDatabase(self.player_database,
                            "Base de données des Joueurs",
                            'last_name', 'first_name', 'date_of_birth', 'ranking',
                            selection_mode=True,
                            sort_by_attribute=self.sort_by_attribute,
                            sort_order=self.sort_order)
        view.show()

        commands = {
            "supprimer " + str(i + 1): ControllerDeletePlayer(self.player_database[i], self.player_database)
            for i in range(len(self.player_database))
        }
        commands.update(
            {
                'n': ControllerPlayerDatabase(self.player_database, sort_by_attribute="last_name"),
                'c': ControllerPlayerDatabase(self.player_database, sort_by_attribute="ranking", sort_order=True)
            }
        )

        mc.ControllerCommandInterpreter(
            "(n) Trier par nom de famille\n"
            "(c) Trier par classement\n"
            "(supprimer X) Supprimer le joueur",
            commands
        ).run()
