"""This module groups the controllers related to the display of players"""

import controllers.main_controllers as mc

from views.database import ViewDatabase


class ControllerPlayerDatabase:
    """This class manages the display of the list of players"""

    def __init__(self, player_database, sort_by_attribute="last_name"):
        self.player_database = player_database
        self.sort_by_attribute = sort_by_attribute

    def run(self):
        view = ViewDatabase(self.player_database,
                            "Base de données des Joueurs",
                            'last_name', 'first_name', 'date_of_birth', 'ranking',
                            selection_mode=True, sort_by_attribute=self.sort_by_attribute)
        view.show()

        mc.ControllerCommandInterpreter(
            "(n) Trier par nom de famille\n"
            "(c) Trier par classement",
            {
                'n': ControllerPlayerDatabase(self.player_database, sort_by_attribute="last_name"),
                'c': ControllerPlayerDatabase(self.player_database, sort_by_attribute="ranking")
            },
        ).run()
