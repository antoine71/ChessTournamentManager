import re


def is_date_format_dd_mm_yyyy(date):
    """Return true if the format of the date is dd/yy/mmmm"""
    regex_date_dd_mm_yyyy = r"^((0[1-9])|[12][0-9]|(3[01]))\/((0[1-9])|(1[012]))\/((19|20)\d{2})$"
    return re.match(regex_date_dd_mm_yyyy, date) is not None


def is_positive_integer(number):
    """return True if the parameter is a positive  integer, whether it is passed to the function as a string or int
    or float"""
    if isinstance(number, int):
        return number >= 0
    elif isinstance(number, float):
        return number % 1 == 0 and number >= 0
    elif isinstance(number, str):
        if number.isdigit():
            return int(number) >= 0 and float(number) % 1 == 0
        else:
            return False
    else:
        return False


def check_string_length(string, length=50):
    """Return true is the length of the string is less than or equal to the specified length"""
    return isinstance(string, str) and len(string) <= length


def resize_string(string, size):
    """Return a string of the specified size"""
    if len(string) < size:
        blanks_size = size - len(string)
        blanks_string = " " * blanks_size
        return string + blanks_string
    else:
        return string
