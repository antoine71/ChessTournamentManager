"""This module groups the controllers related to the display of players"""

import controllers.main_controllers as mc
from controllers.database_management_controllers import ControllerDeletePlayer, ControllerSavePlayer

from models.player import PlayerDataValidator

from views.database_views import ViewDatabase, ViewDatabaseDetails
from views.general_views import ViewText, ViewPrompt


class ControllerPlayerDatabase:
    """This class manages the display of the list of players"""

    def __init__(self, player_database, sort_by_attribute="last_name", sort_order=False,
                 title="Base de données des Joueurs"):
        self.player_database = player_database
        self.sort_by_attribute = sort_by_attribute
        self.sort_order = sort_order
        self.title = title

    def run(self):
        view = ViewDatabase(self.player_database,
                            self.title,
                            'last_name', 'first_name', 'date_of_birth', 'sex', 'ranking',
                            headers=[
                                "Nom de famille",
                                "Prénom",
                                "Date de naissance",
                                "Sexe",
                                "Classement"
                            ],
                            selection_mode=True,
                            sort_by_attribute=self.sort_by_attribute,
                            sort_order=self.sort_order)
        view.show()

        commands = {
            str(i + 1): ControllerPlayerReport(self.player_database[i], self.player_database)
            for i in range(len(self.player_database))
        }
        commands.update(
            {
                'n': ControllerPlayerDatabase(self.player_database, sort_by_attribute="last_name",
                                              title=self.title),
                'c': ControllerPlayerDatabase(self.player_database, sort_by_attribute="ranking", sort_order=True,
                                              title=self.title)
            }
        )

        mc.ControllerCommandInterpreter(
            "(n) Trier par nom de famille\n"
            "(c) Trier par classement\n"
            "(X) Afficher le joueur numéro X",
            commands
        ).run()


class ControllerPlayerReport:
    """This class manages the display the player data as a report"""

    def __init__(self, player, player_database):
        self.player = player
        self.player_database = player_database

    def run(self):
        ViewDatabaseDetails(
            "Détails du Joueur",
            self.player,
            ["Nom de Famille", "Prénom", "Date de naissance", "Sexe", "Classement"],
            ["last_name", "first_name", "date_of_birth", "sex", "ranking"]
        ).show()

        mc.ControllerCommandInterpreter(
            "(c) Mettre à jour le classement\n"
            "(supprimer) Supprimer le joueur de la base de données",
            {
                "c": ControllerUpdateRanking(self.player),
                "supprimer": ControllerDeletePlayer(self.player, self.player_database)
            }
        ).run()


class ControllerUpdateRanking:
    """This class is called to update the ranking of a player"""

    def __init__(self, player):
        self.player = player

    def run(self):
        validator = PlayerDataValidator()
        user_input = ViewPrompt("Veuillez saisir le nouveau classement (entier positif): ").show()
        while not validator.is_ranking_ok(user_input):
            ViewText("Erreur de saisie, veuillez recommencer.").show()
            user_input = ViewPrompt("Veuillez saisir le nouveau classement (entier positif): ").show()
        self.player.update_ranking(user_input)
        ViewText("Le classement du joueur {} {} a été modifié (nouveau classement: {})".format(
            self.player.first_name,
            self.player.last_name,
            self.player.ranking
        )).show()
        ControllerSavePlayer(self.player).run()
