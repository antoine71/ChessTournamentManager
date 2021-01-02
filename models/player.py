"""This module groups the classes related to the player models"""


class Player:
    """This class describes a player"""

    def __init__(self, last_name, first_name, date_of_birth, ranking):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.ranking = int(ranking)

    def __hash__(self):
        return hash((self.last_name, self.first_name, self.date_of_birth))

    def __eq__(self, other_player):
        return self.__dict__ == other_player.__dict__

    def __repr__(self):
        return "{} {}".format(self.first_name, self.last_name)