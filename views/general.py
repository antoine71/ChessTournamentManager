"""This module groups the general views"""


class ViewText:
    """This view displays a text string on the screen"""

    def __init__(self, data):
        self.data = data

    def show(self):
        print(self.data, end="\n\n")


class ViewPrompt(ViewText):
    """This view displays a prompt invite on the screen and returns the user input"""

    def show(self):
        user_command = input(self.data)
        print("")
        return user_command


