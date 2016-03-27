#region HEADER
"""
Joshua Palmer
COP 4020
Python Homework 2
April 5, 2016
"""
#endregion


#region IMPORTS
import numpy as np
import pandas as pd
import pprint
from collections import Counter
from palmerjoshua2013_PyHomework1 import make_pretty  # will probably need to copy to this file before submission
#endregion


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
    states = "STATES"
    shows = "SHOWS"
    viewers = "VIEWERS"
    sum = "SUM"
    total = "Total"

    @staticmethod
    def ordered():
        yield LABELS.states
        yield LABELS.shows
        yield LABELS.viewers
#endregion


#region GLOBAL VARIABLES
pp = pprint.PrettyPrinter(indent=4)
RAW_DICT = MyDict({label: [] for label in LABELS.ordered()})
RAW_DATA = []
data = MyDict()
n_array = None
#endregion


#region HELPER FUNCTIONS
def _save_data(lines):
    global RAW_DATA, RAW_DICT, data
    RAW_DATA = [[item for item in line.split(",")] for line in lines]
    RAW_DICT = MyDict({label: [line[i] for line in RAW_DATA]
                       for i, label in enumerate(LABELS.ordered())})
    data = MyDict({label: list(set(lst)) for label, lst in RAW_DICT.items()})


def _print_dict(particular_dict=None, pretty=True):
    fn = (lambda lst: pp.pprint(lst)) if pretty else (lambda lst: print(lst))
    to_print = particular_dict or data
    for label, lst in to_print.items():
        print(label, end=' ')
        fn(lst)


def _get_viewers_by_state():
    viewers = {state: {show: 0 for show in data[LABELS.shows]} for state in data[LABELS.states]}
    viewers[LABELS.total] = {show: 0 for show in data[LABELS.shows]}
    for line in RAW_DATA:
        state, show, view = line[0], line[1], int(line[2])
        viewers[state][show] += view
        viewers[LABELS.total][show] += view
    return viewers



def load():
    with open('show_results.txt', 'r') as ifile:
        try:
            lines = [line.rstrip() for line in ifile.readlines()]
        except FileNotFoundError:
            print("Could not find input file.")
        else:
            _save_data(lines)
#endregion


#region NUMPY ARRAYS
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
    print(LABELS.sum, count)
#endregion


#region DATA FRAMES
@make_pretty("DATA FRAME")
def make_data_frames():
    viewers = _get_viewers_by_state()
    df = pd.DataFrame.from_dict(viewers)
    cols = df.columns.tolist()
    cols[-1], cols[-2] = cols[-2], cols[-1]  # move 'Total' column to end of the DataFrame
    df = df[cols]
    df.sort_values(by=LABELS.total, ascending=False, inplace=True)
    print(df)
#endregion


def main():
    load()
    #div_arrays()
    #sort_arrays()
    make_data_frames()

if __name__ == '__main__':
    main()
