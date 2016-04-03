# region HEADER
"""
Joshua Palmer
COP 4020
Python Homework 2
April 5, 2016
"""
# endregion


# region IMPORTS
import numpy as np
import pandas as pd
import pprint
# endregion


# region HELPER CLASSES
class MyDict(dict):
    """This is a simple subclass of the built in dictionary. The only added functionality is that it can be used with
    the subtraction operator, e.g.

       md = MyDict({'a': 1, 'b': 2})
     no_a = md - 'a'         # result: {'b': 2}
     no_b = md - 'b'         # result: {'a': 1}
    empty = md - ['a', 'b']  # result: {}

    """
    def __sub__(self, other):
        """
        :param other - a key or iterable container of keys to remove from the original dictionary.
        :return copy of self minus the key/value pair(s) specified by other"""
        is_container = hasattr(other, '__iter__') and type(other) is not str
        if not is_container:
            other = {other}
        return self._set_filter_(other)

    def _set_filter_(self, other):
        to_delete = set(other.keys()) if type(other) is dict else set(other)
        to_keep = set(self.keys()) - to_delete
        return {k: self[k] for k in to_keep}


class LABELS:
    states = "States"
    shows = "Shows"
    viewers = "Viewers"
    sum_ = "Sum"
    total = "Total"
    maximum = "Max"
    minimum = "Min"
    percent = "Percent"
    max_pct = "Max %"
    min_pct = "Min %"
    favorite = "Favorite"

    @staticmethod
    def ordered():
        return LABELS._label_generator(LABELS.states, LABELS.shows, LABELS.viewers)

    @staticmethod
    def ordered_stats():
        return LABELS._label_generator(LABELS.maximum, LABELS.minimum, LABELS.total, LABELS.percent)

    @staticmethod
    def _label_generator(*labels):
        for label in labels:
            yield label
# endregion


# region GLOBAL VARIABLES
pp = pprint.PrettyPrinter(indent=4)
RAW_DATA = []
data = MyDict()
# endregion


# region HELPER FUNCTIONS
def _save_data(lines):  # question 2
    """
    Saves the file data to a raw list of csv, and to a dictionary,
    e.g. {'States': [...], 'Shows': [...], 'Viewers: [...]}
    :param lines: list of lines from an input file, i.e. results of ifile.readlines()
    :return: None; this function saves global data
    """
    global RAW_DATA, data
    RAW_DATA = [[item for item in line.split(",")] for line in lines]
    data = MyDict({label: list(set(line[i] for line in RAW_DATA))
                  if label != LABELS.viewers else [line[i] for line in RAW_DATA]
                  for i, label in enumerate(LABELS.ordered())})


def load():
    with open('show_results.txt', 'r') as ifile:
        try:
            lines = [line.rstrip() for line in ifile.readlines()]
        except FileNotFoundError:
            print("Could not find input file.")
        else:
            _save_data(lines)


def _print_dict(particular_dict=None, pretty=True):
    print_fn = pp.pprint if pretty else print
    to_print = particular_dict or data
    for label, lst in to_print.items():
        print(label+":", end=' ')
        print_fn(lst)


def _get_viewers_by_state():
    return _get_viewers_(LABELS.states, LABELS.shows, False)


def _get_viewers_by_show():
    return _get_viewers_(LABELS.shows, LABELS.states, False)


def _get_viewers_(outer_label, inner_label, include_total=True):
    """
    Converts the raw data into a nested dictionary.
    :param outer_label: Specifies the outer keys, i.e. the columns (either states or shows)
    :param inner_label: Specifies the inner keys, i.e. the rows
    :param include_total: If True, add an extra "Total" column
    :return: dictionary of viewer data
    """
    viewers = {outer: {inner: 0 for inner in data[inner_label]} for outer in data[outer_label]}
    if include_total:
        viewers[LABELS.total] = {inner: 0 for inner in data[inner_label]}
    for line in RAW_DATA:
        state, show, view = line[0], line[1], int(line[2])
        (outer, inner) = (state, show) if outer_label == LABELS.states else (show, state)
        viewers[outer][inner] += view
        if include_total:
            viewers[LABELS.total][inner] += view
    return viewers


def _get_show_stats():
    """
    Generates more statistics about each show, such as:
    1. Max number of viewers
    2. Min number of viewers
    3. Total number of viewers
    4. Percentage of viewers
    :return: dictionary of viewer data
    """
    stats = {label: {show: 0 for show in data[LABELS.shows]} for label in LABELS.ordered_stats()}
    by_show = _get_viewers_by_show()
    total_viewers = sum(int(i) for i in data[LABELS.viewers])
    for show in by_show:
        stats[LABELS.maximum][show] = max(by_show[show].values())
        stats[LABELS.minimum][show] = min(by_show[show].values())
        stats[LABELS.total][show] = sum(val for val in by_show[show].values())
        stats[LABELS.percent][show] = "{:2.2f}".format((stats[LABELS.total][show] / total_viewers) * 100)
    return stats


def make_pretty(title):
    """This decorator is used to print a header and footer around my output. Instead of littering every
       function with the same prints, prepending them with this decorator will automatically add them for me.
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
# endregion


# region NUMPY ARRAYS
@make_pretty("NUMPY ARRAY (whole)")
def create_numpy_array():  # questions 3-4
    """
    Converts raw data to a numpy array, and prints it.
    :return: None
    """
    global RAW_DATA
    if RAW_DATA:
        n_array = np.array(RAW_DATA)
        pp.pprint(n_array)


@make_pretty("SEPARATED REGULAR ARRAYS")
def div_arrays_reg():  # questions 5-6
    """
    Prints the raw data, sorted by state, show, and viewer count.
    Since the data were separated at the beginning, all that's left to do is print them.
    :return: None
    """
    _print_dict(data, False)


@make_pretty("SEPARATED NUMPY ARRAYS")
def div_arrays_np():  # questions 7-8
    """
    Same as div_arrays_reg, except the separated arrays are cast into numpy arrays
    :return: None
    """
    global data
    n_arrays = {label: np.array(lst) for label, lst in data.items()}
    _print_dict(n_arrays)


@make_pretty("SORTED ARRAYS")
def sort_arrays():  # questions 9-12
    """
    Sorts 'states' and 'shows', casts each item in 'viewers' to an integer, and prints all three lists.
    :return: None
    """
    global data
    viewers = LABELS.viewers
    data_copy = MyDict({label: sorted(lst) if label != viewers else [int(i) for i in lst]
                   for label, lst in data.items()})
    count = sum(i for i in data_copy[viewers])
    _print_dict(data_copy - viewers)
    print(LABELS.sum_ + ":", count)
# endregion


# region DATA FRAMES
@make_pretty("DATA FRAMES")
def data_frames():  # questions 13-17
    """
    Creates two data frames and prints them. Also calculates the max and min percentages, and prints my favorite show.
    :return: None
    """
    viewer_frame = pd.DataFrame.from_dict(_get_viewers_by_state())
    stats_frame = pd.DataFrame.from_dict(_get_show_stats())[[lb for lb in LABELS.ordered_stats()]]

    print(viewer_frame, end="\n\n")
    print(stats_frame, end="\n\n")

    max_percent = max(float(i) for i in stats_frame[LABELS.percent].values)
    min_percent = min(float(i) for i in stats_frame[LABELS.percent].values)

    print(LABELS.max_pct+':', max_percent)
    print(LABELS.min_pct+':', min_percent)
    print(LABELS.favorite+':', 'Game of Thrones')
# endregion


def main():
    load()
    create_numpy_array()
    div_arrays_reg()
    div_arrays_np()
    sort_arrays()
    data_frames()

if __name__ == '__main__':
    main()
