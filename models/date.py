class Date:

    def __init__(self, date_dd_mm_yyyy):
        self.date_string = date_dd_mm_yyyy
        self.day = int(date_dd_mm_yyyy[:2])
        self.month = int(date_dd_mm_yyyy[3:5])
        self.year = int(date_dd_mm_yyyy[6:])

    def __hash__(self):
        return hash(self.date_string)

    def __eq__(self, other):
        return self.date_string == other.date_string

    def __ne__(self, other):
        return self.date_string != other.date_string

    def __gt__(self, other):
        if self.year > other.year:
            return True
        elif self.year < other.year:
            return False
        else:
            if self.month > other.month:
                return True
            elif self.month < other.month:
                return False
            else:
                if self.day > other.day:
                    return True
                else:
                    return False

    def __ge__(self, other):
        return self > other or self == other

    def __lt__(self, other):
        return not self > other

    def __le__(self, other):
        return self < other or self == other

    def __repr__(self):
        return self.date_string