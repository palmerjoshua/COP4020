"""
Joshua Palmer
COP 4020
Python Homework 1
22 March 2016

This is a helper script. It is not meant to be run directly.
Instead, its contents are meant to be imported by the main homework script.

Contents:

1. Pretty Printer - This is a handy print function that makes printing dictionaries and other containers a little more readable.
2. make_pretty - A decorator used to separate my homework's output into logical sections and make it look nicer in the console.
"""

try:
    import pprint
except ImportError:
    pp = None  # this should never happen, but who knows
else:
    pp = pprint.PrettyPrinter(indent=4)  # makes dictionaries look nicer when printed to the console


def make_pretty(title):
    """This decorator is used to print a header and footer around my output. Instead of littering every function with the same
       prints, prepending them with this decorator will automatically add them for me.
       :param title - The title of the section that will be printed. Can be any string."""

    length = 20  # length of each side of the header
    symbol = "#"  # the symbol used to print the header
    bottom_length = 2 + 2*length + len(title)  # length of the footer

    def decorator(func):
        def wrapper():
            print(symbol*length, title, symbol*length)  # print header
            func()  # call original function
            print(symbol*bottom_length)  # print footer
            print()  # print blank line
        return wrapper
    return decorator

if __name__ == '__main__':
    msg = "Warning: This is just a helper script and is not meant to be run alone.\n" \
          "         It is meant to be imported and not run directly. For the homework\n" \
          "         assignment, run palmerjoshua2013_PyHomework1.py."
    print(msg)
