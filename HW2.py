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
from palmerjoshua2013_PyHomework1 import make_pretty  # will probably need to copy to this file before submission
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
        return self.__set_filter__(other)

    def __set_filter__(self, other):
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
RAW_DICT = MyDict({label: [] for label in LABELS.ordered()})
RAW_DATA = []
data = MyDict()
n_array = None
# endregion


# region HELPER FUNCTIONS
def _save_data(lines):
    global RAW_DATA, RAW_DICT, data
    RAW_DATA = [[item for item in line.split(",")] for line in lines]
    RAW_DICT = MyDict({label: [line[i] for line in RAW_DATA]
                       for i, label in enumerate(LABELS.ordered())})
    data = MyDict({label: list(set(lst)) for label, lst in RAW_DICT.items()})


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
    viewers = {outer: {inner: 0 for inner in data[inner_label]} for outer in data[outer_label]}
    if include_total:
        viewers[LABELS.total] = {inner: 0 for inner in data[inner_label]}
    for line in RAW_DATA:
        state, show, view = line[0], line[1], int(line[2])
        (inner, outer) = (state, show) if inner_label == LABELS.states else (show, state)
        viewers[outer][inner] += view
        if include_total:
            viewers[LABELS.total][inner] += view
    return viewers


def _get_show_stats(current_viewer_dict=None):
    pass


def load():
    with open('show_results.txt', 'r') as ifile:
        try:
            lines = [line.rstrip() for line in ifile.readlines()]
        except FileNotFoundError:
            print("Could not find input file.")
        else:
            _save_data(lines)
# endregion


# region NUMPY ARRAYS
@make_pretty("NUMPY ARRAY (whole)")
def create_numpy_array():
    global n_array, RAW_DATA
    if RAW_DATA:
        n_array = np.array(RAW_DATA)
        pp.pprint(n_array)


@make_pretty("NUMPY ARRAYS (separate)")
def div_arrays():
    global data
    n_arrays = {label: np.array(lst) for label, lst in data.items()}
    _print_dict(n_arrays)


@make_pretty("SORT ARRAYS")
def sort_arrays():
    global data
    viewers = LABELS.viewers
    data = MyDict({label: sorted(lst) if label != viewers else [int(i) for i in lst]
                   for label, lst in data.items()})
    count = sum(i for i in data[viewers])
    _print_dict(data - viewers)
    print(LABELS.sum_ + ":", count)
# endregion


# region DATA FRAMES
@make_pretty("DATA FRAME")
def make_data_frames():
    viewers = _get_viewers_by_state()
    df = pd.DataFrame.from_dict(viewers)
    print(df)
    print(df.describe())
# endregion


def main():
    load()
    div_arrays()
    sort_arrays()
    make_data_frames()

if __name__ == '__main__':
    main()
