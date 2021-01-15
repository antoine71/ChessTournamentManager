"""This module groups the classes related to the display of lists of objects"""

from views.general_views import ViewText

from operator import attrgetter

from utils.utils import resize_string


class ViewDatabase:
    """This view displays the content of a Database object as a table on the screen. The constructor parameters are
    as follows
        database (list): a list of objects, player or tournaments object typically for this program
        title (string): the title that will be displayed on top of the table
        attributes (list): the list of attribute names (as strings) of the object that shall be displayed
        selection_mode (bool): True will display brackets around the item number to highlight that the item number
        can be used as a command
        sort_by_attribute (string): the attribute that shall be used to sort the table"""

    def __init__(self, database, title, *attributes, headers=[], selection_mode=True, sort_by_attribute="name",
                 sort_order=True):
        self.database = database
        self.title = title
        self.attributes = attributes
        self.headers = headers
        self.selection_mode = selection_mode
        self.sort_by_attribute = sort_by_attribute
        self.sort_order = sort_order

    def show(self):
        ViewText(self.title).show()
        if not self.database:
            headers_string_output = "La base de données est vide."
            data_list_string_output = ""
        else:
            self.database.sort(key=attrgetter(self.sort_by_attribute), reverse=self.sort_order)
            if self.headers:
                headers_string_output = " " * 6 \
                                        + "".join([resize_string(header, 25).upper() for header in self.headers])\
                                        + "\n"
            else:
                headers_string_output = ""
            data_list_string_output = "\n".join(
                [
                    resize_string(self.highlight_command(i + 1), 6)
                    + "".join([resize_string(str(getattr(data, attribute)), 25)
                               for attribute in self.attributes])
                    for i, data in enumerate(self.database)
                ])

        ViewText(headers_string_output + data_list_string_output).show()

    def highlight_command(self, command):
        if self.selection_mode:
            return "({})".format(command)
        else:
            return "{}".format(command)


class ViewDatabaseDetails:
    """This view displays the attributes and values of a Tournament object"""

    def __init__(self, title, database_object, fields, object_attributes):
        self.title = title
        self.database_object = database_object
        self.fields = fields
        self.object_attributes = object_attributes

    def show(self):
        ViewText(self.title).show()
        string_output = "\n".join(["\t{} : {}".format(field, self.database_object.__getattribute__(attribute))
                                   for field, attribute in tuple(zip(self.fields, self.object_attributes))])
        ViewText(string_output).show()
