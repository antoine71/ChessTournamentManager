"""This module groups the classes related to the database models"""

from tinydb import TinyDB, Query

from models.tournament import Tournament, Round, Game
from models.player import Player

from datetime import datetime


class PlayerDatabaseConverter:
    """This class converts Player objects to json and vice versa"""

    def __init__(self, db=TinyDB('database/db.json'), table="players"):
        self.players_table = db.table(table)

    def save_player(self, player):
        self.players_table.upsert(
            {
                "last_name": player.last_name,
                "first_name": player.first_name,
                "date_of_birth": str(player.date_of_birth),
                "sex": player.sex,
                "ranking": player.ranking
            },
            (Query().last_name == player.last_name)
            & (Query().first_name == player.first_name)
            & (Query().date_of_birth == str(player.date_of_birth))
        )

    def load_database(self):
        return [Player(**item) for item in self.players_table]

    def delete_player(self, player):
        self.players_table.remove((Query().last_name == player.last_name)
                                  & (Query().first_name == player.first_name)
                                  & (Query().date_of_birth == str(player.date_of_birth)))


class TournamentDatabaseConverter:
    """This class converts Tournament objects to json and vice versa"""

    def __init__(self, db=TinyDB('database/db.json'), table="tournaments"):
        self.tournaments_table = db.table(table)

    def save_tournament(self, tournament):

        self.tournaments_table.upsert(
            {
                'name': tournament.name,
                'description': tournament.description,
                'place': tournament.place,
                'start_date': str(tournament.start_date),
                'end_date': str(tournament.end_date),
                'number_of_rounds': tournament.number_of_rounds,
                'time_control': tournament.time_control,
                'players':
                    [
                        {
                            'last_name': player.last_name,
                            'first_name': player.first_name,
                            'date_of_birth': str(player.date_of_birth),
                            'sex': player.sex,
                            'ranking': player.ranking
                        }
                        for player in tournament.players
                    ],
                'rounds':
                    [
                        {
                            'name': round_.name,
                            'start':
                                {
                                    'y': round_.start_time.year,
                                    'mo': round_.start_time.month,
                                    'd': round_.start_time.day,
                                    'h': round_.start_time.hour,
                                    'mi': round_.start_time.minute
                                },
                            'end':
                                {

                                    'y': round_.end_time.year,
                                    'mo': round_.end_time.month,
                                    'd': round_.end_time.day,
                                    'h': round_.end_time.hour,
                                    'mi': round_.end_time.minute
                                },
                            'games':
                                [
                                    {
                                        'player1':
                                            {
                                                'last_name': game.pair[0].last_name,
                                                'first_name': game.pair[0].first_name,
                                                'date_of_birth': str(game.pair[0].date_of_birth),
                                                'sex': game.pair[0].sex,
                                                'ranking': game.pair[0].ranking
                                            },
                                        'player2':
                                            {
                                                'last_name': game.pair[1].last_name,
                                                'first_name': game.pair[1].first_name,
                                                'date_of_birth': str(game.pair[1].date_of_birth),
                                                'sex': game.pair[1].sex,
                                                'ranking': game.pair[1].ranking
                                            },
                                        'result': game.result
                                    }
                                    for game in round_.games
                                ],
                            'end_confirmation': round_.end_confirmation
                        }
                        for round_ in tournament.rounds
                    ]
            },
            Query().name == tournament.name
        )

    def delete_tournament(self, tournament):
        self.tournaments_table.remove(
            (Query().name == tournament.name) &
            (Query().start_date == str(tournament.start_date)) &
            (Query().end_date == str(tournament.end_date)) &
            (Query().time_control == tournament.time_control)
        )

    def load_database(self):
        return [self.load_tournament(tournament_json) for tournament_json in self.tournaments_table]

    def load_tournament(self, tournament_json):
        tournament = Tournament(
            tournament_json['name'],
            tournament_json['description'],
            tournament_json['place'],
            tournament_json['start_date'],
            tournament_json['end_date'],
            tournament_json['number_of_rounds'],
            tournament_json['time_control']
        )

        for player_data in tournament_json['players']:
            tournament.players.append(Player(**player_data))

        for round_ in tournament_json['rounds']:
            new_round = Round(tournament)
            new_round.start_time = datetime(
                round_['start']['y'],
                round_['start']['mo'],
                round_['start']['d'],
                round_['start']['h'],
                round_['start']['mi'],
            )
            new_round.end_time = datetime(
                round_['end']['y'],
                round_['end']['mo'],
                round_['end']['d'],
                round_['end']['h'],
                round_['end']['mi'],
            )
            new_round.end_confirmation = round_['end_confirmation']
            for game_data in round_['games']:
                new_game = Game(Player(**game_data['player1']), Player(**game_data['player2']))
                new_game.update_result(game_data['result'])
                new_round.games.append(new_game)
            tournament.rounds.append(new_round)

        return tournament
