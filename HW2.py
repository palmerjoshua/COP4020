import numpy as np
import pandas as pd
import pprint
from palmerjoshua2013_PyHomework1 import make_pretty  # will probably need to copy to this file before submission
pp = pprint.PrettyPrinter(indent=4)




states, shows, viewers = [], [], []

LABELS = ("STATES:", "SHOWS:", "VIEWERS:")

def _print_div_lists(pretty_list=False):
    fn = (lambda lst: pp.pprint(lst)) if pretty_list else (lambda lst: print(lst))
    for label, lst in zip(LABELS, (states, shows, viewers)):
        print(label, end=' ')
        fn(lst)


n_array = None

@make_pretty("CREATE N_ARRAY")
def create_numpy_array():
    global n_array
    contents = None
    try:
        with open('show_results.txt', 'r') as ifile:
            contents = [[item for item in line.split(",")] for line in ifile.read().split('\n')]
    except FileNotFoundError:
        print("Could not find input file.")
    else:
        n_array = np.array(contents) if contents else None
        if n_array is not None:
            pp.pprint(n_array)
        else:
            print("Could not read input file.")



@make_pretty("DIVIDE N_ARRAY")
def divide_numpy_array():
    global states, shows, viewers, n_array

    states = list(set([item[0] for item in n_array]))
    shows = list(set([item[1] for item in n_array]))
    viewers = [item[2] for item in n_array]
    _print_div_lists()

@make_pretty("DIV ARRAYS")
def div_arrays():
    global states, shows, viewers
    states = np.array(states)
    shows = np.array(shows)
    viewers = np.array(viewers)
    _print_div_lists(True)


@make_pretty("SORT ARRAYS")
def sort_arrays():
    global states, shows, viewers
    states.sort()
    shows.sort()
    viewers = np.array([int(i) for i in viewers])
    count = sum(i for i in viewers)
    _print_div_lists()
    print('Sum:', count)


def main():
    create_numpy_array()
    divide_numpy_array()
    div_arrays()
    sort_arrays()

if __name__ == '__main__':
    main()
