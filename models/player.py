"""This module groups the classes related to the player models"""

import utils.utils as utils

from models.date import Date


class Player:
    """This class describes a player"""

    def __init__(self, last_name, first_name, date_of_birth, sex, ranking):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = Date(date_of_birth)
        self.sex = sex
        self.ranking = int(ranking)

    def update_ranking(self, new_ranking):
        self.ranking = int(new_ranking)

    def __hash__(self):
        return hash((self.last_name, self.first_name, self.date_of_birth))

    def __eq__(self, other_player):
        return (self.last_name, self.first_name, self.date_of_birth) == \
               (other_player.last_name, other_player.first_name, other_player.date_of_birth)

    def __repr__(self):
        return "{} {}".format(self.first_name, self.last_name)


class PlayerDataValidator:
    """This class contains methods used to validate parameters before creating a Player object"""

    def is_last_name_ok(self, last_name):
        return utils.check_string_length(last_name, 50)

    def is_first_name_ok(self, first_name):
        return utils.check_string_length(first_name, 50)

    def is_date_of_birth_ok(self, date_of_birth):
        return utils.is_date_format_dd_mm_yyyy(date_of_birth)

    def is_sex_ok(self, sex):
        return sex == "m" or sex == "f"

    def is_ranking_ok(self, ranking):
        return utils.is_positive_integer(ranking)
