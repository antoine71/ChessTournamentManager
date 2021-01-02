from operator import itemgetter


class View:

    def __init__(self, data):
        self.data = data

    def show(self):
        print(self.data, end="\n\n")


class ViewPrompt(View):

    def show(self):
        user_command = input(self.data)
        print("")
        return user_command


class ViewChoosePlayer(View):

    def show(self):
        for i, player in enumerate(self.data):
            print(f"({i}) {player}")


class ViewDatabase:

    def __init__(self, database, title, *parameters, selection_mode=True, sort_by_attribute="name"):
        self.database = database
        self.title = title
        self.parameters = parameters
        self.selection_mode = selection_mode
        self.sort_by_attribute = sort_by_attribute

    def show(self):
        View(self.title).show()
        self.database.sort_by(self.sort_by_attribute)
        data_list_string_output = "\n".join(
            [
                self.link(i) + "\t".join([str(data.__dict__[parameter]) for parameter in self.parameters])
                for i, data in enumerate(self.database)
            ])
        View(data_list_string_output).show()

    def link(self, command):
        if self.selection_mode:
            return "({})\t".format(command)
        else:
            return "{}\t".format(command)


class ViewTournamentDetails:

    def __init__(self, title, tournament):
        self.title = title
        self.tournament = tournament

    def show(self):
        View(self.title).show()
        string_output = "\n".join([
            "\tNom : {}".format(self.tournament.name),
            "\tDescription : {}".format(self.tournament.description),
            "\tDate de début : {}".format(self.tournament.start_date),
            "\tDate de fin : {}".format(self.tournament.end_date),
            "\tNombre de rounds : {}".format(self.tournament.number_of_rounds),
            "\tContrôle du temps : {}".format(self.tournament.time_control),
            "\tStatus : {}".format(self.tournament.status),
        ])
        View(string_output).show()


class ViewScoreTable:

    def __init__(self, title, score_table):
        self.title = title
        self.score_table = score_table

    def show(self):
        View(self.title).show()
        if not self.score_table.score_table:
            string_output = "\tPas disponible"
        else:
            sorted_score_table = sorted(self.score_table.score_table.items(), key=itemgetter(1), reverse=True)
            string_output = "\n".join([
                "\t{}: {}".format(player, score)
                for player, score in sorted_score_table
            ])
        View(string_output).show()


class ViewTournamentResult:

    def __init__(self, title, tournament):
        self.title = title
        self.tournament = tournament

    def show(self):
        View(self.title).show()
        if not self.tournament.rounds:
            View("\tPas disponible").show()
        else:
            for round_ in self.tournament.rounds:
                ViewRoundResult(round_).show()


class ViewRoundResult:

    def __init__(self, round_):
        self.round_ = round_

    def show(self):
        View("\t{} - {}".format(self.round_.name, self.round_.status)).show()
        if not self.round_.games:
            View("\t\tPas disponible").show()
        else:
            for game in self.round_.games:
                ViewGameResult(game).show()


class ViewGameResult:

    def __init__(self, game):
        self.game = game

    def show(self):
        match_result_string_output = "\t".join([
            "\t\t{}: {}".format(player, score)
            for player, score in self.game.score_table.score_table.items()
        ])
        string_output = ' - '.join([self.game.status, match_result_string_output])
        View(string_output).show()