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
