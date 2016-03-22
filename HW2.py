import numpy as np
import pandas as pd
import pprint
pp = pprint.PrettyPrinter(indent=4)


states, shows, viewers = [], [], []
n_array = None


def sort_arrays():
    global states, shows, viewers
    if not states or not shows or not viewers:
        div_arrays()
    states.sort()
    shows.sort()
    viewers = np.array([int(i) for i in viewers])
    count = sum(i for i in viewers)
    print('States:', states)
    print('Shows:', shows)
    print('Viewers:', viewers)
    print('Sum:', count)

def div_arrays():
    global states, shows, viewers
    if not states or not shows or not viewers:
        divide_numpy_array()
    states = np.array(states)
    shows = np.array(shows)
    viewers = np.array(viewers)
    for lst in (states, shows, viewers):
        pp.pprint(lst)


def divide_numpy_array():
    global states, shows, viewers, n_array
    if n_array is None:
        create_numpy_array()

    states = list(set([item[0] for item in n_array]))
    shows = [item[1] for item in n_array]
    viewers = [item[2] for item in n_array]

    data = {'states': states, 'shows': shows, 'viewers': viewers}  # not required; just convenient
    pp.pprint(data)


def create_numpy_array():
    global n_array
    contents = None
    with open('show_results.txt', 'r') as ifile:
        contents = [[item for item in line.split(",")] for line in ifile.read().split('\n')]
    n_array = np.array(contents) if contents else None
    if n_array is not None:
        pp.pprint(n_array)
    else:
        print("Could not read input file.")


def main():

    sort_arrays()

if __name__ == '__main__':
    main()
