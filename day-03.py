#!/usr/bin/env python
from itertools import cycle, tee
from more_itertools import nth
from functools import reduce

def multiply(iter):
    """Multiplies each element of an iterator"""
    product = reduce((lambda x, y: x * y), iter)
    print(f"The product of all encountered trees is {product}")
    return product

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

def count_trees_for_slopes(iter, slopes):
    """Count trees on all given slopes"""
    trees = []
    column_iterators = tee(iter, len(slopes))
    for i, (dx, dy) in enumerate(slopes):
        count = count_trees(column_iterators[i], dx, dy)
        trees.append(count)
    return trees

if __name__ == "__main__":
    slopes = [(1,1),(3,1),(5,1),(7,1),(1,2)]
    # example
    columns = get_columns("data/day-03-example.txt")
    trees = count_trees(columns, 3, 1)
    assert trees == 7
    columns = get_columns("data/day-03-example.txt")
    trees = count_trees_for_slopes(columns, slopes)
    assert trees == [2, 7, 3, 4, 2]
    product = multiply(trees)
    assert product == 336
    # reality
    columns = get_columns("data/day-03.txt")
    trees = count_trees(columns, 3, 1)
    assert trees == 200
    columns = get_columns("data/day-03.txt")
    trees = count_trees_for_slopes(columns, slopes)
    assert trees == [66, 200, 76, 81, 46]
    product = multiply(trees)
    assert product == 3737923200
