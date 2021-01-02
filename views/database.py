"""This module groups the classes related to the display of lists of objects"""

from views.general import ViewText

from operator import attrgetter


class ViewDatabase:
    """This view displays the content of a Database object as a table on the screen. The constructor parameters are
    as follows
        database (list): a list of objects, player or tournaments object typically for this program
        title (string): the title that will be displayed on top of the table
        attributes (list): the list of attribute names (as strings) of the object that shall be displayed
        selection_mode (bool): True will display brackets around the item number to highlight that the item number
        can be used as a command
        sort_by_attribute (string): the attribute that shall be used to sort the table"""

    def __init__(self, database, title, *attributes, selection_mode=True, sort_by_attribute="name"):
        self.database = database
        self.title = title
        self.attributes = attributes
        self.selection_mode = selection_mode
        self.sort_by_attribute = sort_by_attribute

    def show(self):
        ViewText(self.title).show()
        self.database.sort(key=attrgetter(self.sort_by_attribute))
        data_list_string_output = "\n".join(
            [
                self.highlight_command(i) + "\t".join([str(data.__dict__[attribute]) for attribute in self.attributes])
                for i, data in enumerate(self.database)
            ])
        ViewText(data_list_string_output).show()

    def highlight_command(self, command):
        if self.selection_mode:
            return "({})\t".format(command)
        else:
            return "{}\t".format(command)
