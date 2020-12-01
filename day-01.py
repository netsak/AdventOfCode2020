#!/usr/bin/env python
from itertools import combinations
from functools import reduce

def find_sum_and_multiply_items(target, times):
    """Find n elements in an array with a given sum and returns the product of these elements"""
    with open("data/day-01.txt") as f:
        numbers = [int(x) for x in f.readlines()]
    for items in combinations(numbers, times):
        items_sum = sum(items)
        if items_sum == target:
            items_product = reduce((lambda x, y: x * y), items)
            print(f"items={items} sum={items_sum} product={items_product}")
            return


if __name__ == "__main__":
    find_sum_and_multiply_items(2020, 2)
    find_sum_and_multiply_items(2020, 3)
