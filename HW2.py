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
n_array = None
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


def _get_show_stats(current_viewer_dict=None):
    stats = {label: {show: 0 for show in data[LABELS.shows]} for label in LABELS.ordered_stats()}
    by_show = _get_viewers_by_show()
    total_viewers = sum(int(i) for i in data[LABELS.viewers])
    for show in by_show:
        stats[LABELS.maximum][show] = max(by_show[show].values())
        stats[LABELS.minimum][show] = min(by_show[show].values())
        stats[LABELS.total][show] = sum(val for val in by_show[show].values())
        stats[LABELS.percent][show] = "{:2.2f}".format((stats[LABELS.total][show] / total_viewers) * 100)
    return stats
# endregion


# region NUMPY ARRAYS
@make_pretty("NUMPY ARRAY (whole)")
def create_numpy_array():  # questions 3-4
    global n_array, RAW_DATA
    if RAW_DATA:
        n_array = np.array(RAW_DATA)
        pp.pprint(n_array)


@make_pretty("SEPARATED REGULAR ARRAYS")
def div_arrays_reg():  # questions 5-6
    _print_dict(data, False)


@make_pretty("SEPARATED NUMPY ARRAYS")
def div_arrays_np():  # questions 7-8
    global data
    n_arrays = {label: np.array(lst) for label, lst in data.items()}
    _print_dict(n_arrays)


@make_pretty("SORTED ARRAYS")
def sort_arrays():  # questions 9-12
    global data
    viewers = LABELS.viewers
    data = MyDict({label: sorted(lst) if label != viewers else [int(i) for i in lst]
                   for label, lst in data.items()})
    count = sum(i for i in data[viewers])
    _print_dict(data - viewers)
    print(LABELS.sum_ + ":", count)
# endregion


# region DATA FRAMES
@make_pretty("DATA FRAMES")
def data_frames():  # questions 13-17
    viewer_frame = pd.DataFrame.from_dict(_get_viewers_by_state())
    stats_frame = pd.DataFrame.from_dict(_get_show_stats())[[lb for lb in LABELS.ordered_stats()]]

    print(viewer_frame, end="\n\n")
    print(stats_frame, end="\n\n")

    gen = lambda: (float(i) for i in stats_frame[LABELS.percent].values)
    max_percent = max(gen())
    min_percent = min(gen())

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
