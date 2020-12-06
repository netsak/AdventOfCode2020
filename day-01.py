#!/usr/bin/env python
from itertools import combinations
from functools import reduce
from operator import mul


def find_sum_and_multiply_items(target, times):
    """Find n elements in an array with a given sum and returns the product of these elements"""
    with open("data/day-01.txt") as f:
        numbers = [int(x) for x in f.readlines()]
    for items in combinations(numbers, times):
        items_sum = sum(items)
        if items_sum == target:
            items_product = reduce(mul, items)
            print(f"items={items} sum={items_sum} product={items_product}")
            return items_product


def find_sum_and_multiply_items2(target, times):
    """Find n elements in an array with a given sum and returns the product of these elements"""
    with open("data/day-01.txt") as f:
        numbers = [int(x) for x in f.readlines()]
    items = next(filter(lambda items: sum(items) == target, combinations(numbers, times)))
    items_sum = sum(items)
    items_product = reduce(mul, items)
    print(f"items={items} sum={items_sum} product={items_product}")
    return items_product


if __name__ == "__main__":
    result = find_sum_and_multiply_items(2020, 2)
    assert result == 539851
    result = find_sum_and_multiply_items(2020, 3)
    assert result == 212481360
    # alternative solution
    result = find_sum_and_multiply_items2(2020, 2)
    assert result == 539851
    result = find_sum_and_multiply_items2(2020, 3)
    assert result == 212481360
