#!/usr/bin/env python
from functools import reduce
from operator import mul

def multiply(iter):
    """Multiplies each element of an iterator"""
    product = reduce(mul, iter)
    print(f"The product of all encountered trees is {product}")
    return product

def get_map(filename):
    """Load the map as line array"""
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def count_trees(area, dx, dy):
    """Count the trees along a given slope"""
    trees = 0
    y = 0
    x = 0
    max_x = len(area[0])
    max_y = len(area)
    while y < max_y-dy:
        y += dy
        x += dx
        pos = area[y][x % max_x]
        if pos == "#":
            trees += 1
    print(f"Encountered {trees} trees using this slope")
    return trees

def count_trees_for_slopes(area, slopes):
    """Count trees on all given slopes"""
    trees = []
    for (dx, dy) in slopes:
        count = count_trees(area, dx, dy)
        trees.append(count)
    return trees

if __name__ == "__main__":
    slopes = [(1,1),(3,1),(5,1),(7,1),(1,2)]
    # example
    area = get_map("data/day-03-example.txt")
    trees = count_trees(area, 3, 1)
    assert trees == 7
    area = get_map("data/day-03-example.txt")
    trees = count_trees_for_slopes(area, slopes)
    assert trees == [2, 7, 3, 4, 2]
    product = multiply(trees)
    assert product == 336
    # # reality
    area = get_map("data/day-03.txt")
    trees = count_trees(area, 3, 1)
    assert trees == 200
    area = get_map("data/day-03.txt")
    trees = count_trees_for_slopes(area, slopes)
    assert trees == [66, 200, 76, 81, 46]
    product = multiply(trees)
    assert product == 3737923200
