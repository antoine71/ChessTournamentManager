from operator import attrgetter

from tinydb import TinyDB, Query


class Database:

    def __init__(self, data=None):
        if data is None:
            data = []
        self.data = data

    def add_data(self, data):
        self.data.append(data)

    def sort_by(self, attribute, reverse_=False):
        self.data.sort(key=attrgetter(attribute), reverse=reverse_)

    def __iter__(self):
        return list.__iter__(self.data)

    def __repr__(self):
        return '\n'.join(str(data) for data in self.data)

    def __getitem__(self, index):
        return self.data[index]


class Player:

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


class Tournament:

    NUMBER_OF_PLAYERS = 4

    def __init__(self, name, description, start_date, end_date, number_of_rounds, time_control):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = int(number_of_rounds)
        self.players = []
        self.rounds = []
        self.time_control = time_control

    @property
    def status(self):
        if not self.rounds:
            return "pas encore commencé"
        elif [round_.status for round_ in self.rounds] == ["terminé"] * self.number_of_rounds:
            return "terminé"
        else:
            return "en cours"

    @property
    def score_table(self):
        return ScoreTable.aggregate(*[round_.score_table for round_ in self.rounds])

    def play_tournament(self):
        if not self.rounds:
            for i in range(self.number_of_rounds):
                self.rounds.append(Round(self))

    def start_new_round(self):
        new_round = Round(self)
        new_round.draw_games()
        self.rounds.append(new_round)

    def __repr__(self):
        return list.__repr__(list(self.__dict__.values()))


class Round:

    def __init__(self, tournament):
        self.tournament = tournament
        self.name = "round{}".format(len(self.tournament.rounds) + 1)
        self.games = []

    @property
    def status(self):
        if not self.games:
            return "pas encore commencé"
        elif [game.status for game in self.games] == ["terminé"] * len(self.games):
            return "terminé"
        else:
            return "en cours"

    @property
    def score_table(self):
        return ScoreTable.aggregate(*[game.score_table for game in self.games])

    def draw_games(self):
        self.games = [Game(self.tournament.players[i], self.tournament.players[i + int(Tournament.NUMBER_OF_PLAYERS / 2)])
                 for i in range(int(Tournament.NUMBER_OF_PLAYERS / 2))]

    def __repr__(self):
        return "\n".join([str(game) for game in self.games])


class Game:

    def __init__(self, player1, player2):
        self.pair = (player1, player2)
        self.result = 'nc'
        self.score_table = GameScoreTable(player1, player2)

    @property
    def status(self):
        if self.result == 'nc':
            return "pas encore commencé"
        else:
            return "terminé"

    def update_result(self, result):
        self.result = result
        self.update_score()

    def update_score(self):
        if self.result == '1':
            self.score_table.update_score_victory(self.pair[0])
        elif self.result == '2':
            self.score_table.update_score_victory(self.pair[1])
        elif self.result == 'n':
            self.score_table.update_score_draw(*self.pair)

    def __repr__(self):
        return self.score_table.__repr__()


class ScoreTable:

    def __init__(self, *players):
        self.score_table = {player: 0 for player in players}

    @classmethod
    def aggregate(cls, *score_tables):
        aggregated_score_table = cls()
        for score_table in score_tables:
            for player in score_table:
                if player in aggregated_score_table:
                    aggregated_score_table[player] += score_table[player]
                else:
                    aggregated_score_table[player] = score_table[player]
        return aggregated_score_table

    def __iter__(self):
        return dict.__iter__(self.score_table)

    def __getitem__(self, item):
        return self.score_table[item]

    def __setitem__(self, key, value):
        self.score_table[key] = value

    def __repr__(self):
        return self.score_table.__repr__()


class GameScoreTable(ScoreTable):

    def update_score_victory(self, player):
        self.score_table[player] += 1

    def update_score_draw(self, player1, player2):
        self.score_table[player1] += 0.5
        self.score_table[player2] += 0.5


class TournamentDatabaseConverter:

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


class PlayerDatabaseConverter:

    def __init__(self, db=TinyDB('players_db.json')):
        self.db = db

    def save_player(self, player):
        self.db.insert(player.__dict__)

