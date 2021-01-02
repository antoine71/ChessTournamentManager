"""This module groups the classes related to the database models"""

from tinydb import TinyDB, Query

from models.tournament import Tournament, Round, Game
from models.player import Player


class PlayerDatabaseConverter:
    """This class converts Player objects to json and vice versa"""

    def __init__(self, db=TinyDB('players_db.json')):
        self.db = db

    def save_player(self, player):
        self.db.insert(player.__dict__)

    def load_database(self):
        return [Player(**item) for item in self.db]


class TournamentDatabaseConverter:
    """This class converts Tournament objects to json and vice versa"""

    def __init__(self, db=TinyDB('db_tournament.json')):
        self.db = db

    def save_tournament(self, tournament):

        self.db.upsert(
            {
                'name': tournament.name,
                'description': tournament.description,
                'start_date': tournament.start_date,
                'end_date': tournament.end_date,
                'number_of_rounds': tournament.number_of_rounds,
                'time_control': tournament.time_control,
                'players':
                    [
                        {
                            'last_name': player.last_name,
                            'first_name': player.first_name,
                            'date_of_birth': player.date_of_birth,
                            'ranking': player.ranking
                        }
                        for player in tournament.players
                    ],
                'rounds':
                    [
                        {
                            'name': round_.name,
                            'games':
                                [
                                    {
                                        'player1':
                                            {
                                                'last_name': game.pair[0].last_name,
                                                'first_name': game.pair[0].first_name,
                                                'date_of_birth': game.pair[0].date_of_birth,
                                                'ranking': game.pair[0].ranking
                                            },
                                        'player2':
                                            {
                                                'last_name': game.pair[1].last_name,
                                                'first_name': game.pair[1].first_name,
                                                'date_of_birth': game.pair[1].date_of_birth,
                                                'ranking': game.pair[1].ranking
                                            },
                                        'result': game.result
                                    }
                                    for game in round_.games
                                ]
                        }
                        for round_ in tournament.rounds
                    ]
            },
            Query().name == tournament.name
        )

    def load_database(self):
        return [self.load_tournament(tournament_json) for tournament_json in self.db]

    def load_tournament(self, tournament_json):
        tournament = Tournament(
            tournament_json['name'],
            tournament_json['description'],
            tournament_json['start_date'],
            tournament_json['end_date'],
            tournament_json['number_of_rounds'],
            tournament_json['time_control']
        )

        for player_data in tournament_json['players']:
            tournament.players.append(Player(**player_data))

        for round_ in tournament_json['rounds']:
            new_round = Round(tournament)
            for game_data in round_['games']:
                new_game = Game(Player(**game_data['player1']), Player(**game_data['player2']))
                new_game.update_result(game_data['result'])
                new_round.games.append(new_game)
            tournament.rounds.append(new_round)

        return tournament
