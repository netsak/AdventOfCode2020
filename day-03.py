#!/usr/bin/env python
import re
from itertools import cycle
from more_itertools import nth

def get_columns(filename):
    """Load the map and returns an iterator of endless columns"""
    with open(filename) as f:
        line_arrays = [list(line.strip()) for line in f.readlines()]
        columns = list(zip(*line_arrays))
        return cycle(columns)

def count_trees(iter, dx, dy):
    """Count the trees along a given slope"""
    trees = 0
    y = 0
    start = next(iter)
    max_y = len(start)
    while y < max_y-dy:
        y += dy
        col = nth(iter, dx-1)
        if col[y] == "#":
            trees += 1
    print(f"Encountered {trees} trees using this slope")
    return trees

if __name__ == "__main__":
    columns = get_columns("data/day-03-example.txt")
    trees = count_trees(columns, 3, 1)
    assert trees == 7
    columns = get_columns("data/day-03.txt")
    trees = count_trees(columns, 3, 1)
    assert trees == 200
