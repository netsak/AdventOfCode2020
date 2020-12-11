#!/usr/bin/env python
from collections import defaultdict
from itertools import accumulate
from functools import reduce, partial
import timeit

def load_adapters(filename):
    with open(filename) as f:
        adapters = [int(line) for line in f.readlines()]
        return adapters


def find_differences_and_product(adapters,  max_diff=3, build_in_joltage=3):
    adapters = sorted([0] + adapters)
    adapters.append(adapters[-1] + build_in_joltage)
    differences = tuple((b - a for a,b in zip(adapters,adapters[1:])))
    assert not any(d for d in differences if d > max_diff), f"difference must not be greater than {max_diff}"
    diff_1 = sum(1 for d in differences if d == 1)
    diff_3 = sum(1 for d in differences if d == 3)
    product = diff_1 * diff_3
    print(f"There are {diff_1} differences of 1 jolt and {diff_3} differences of 3 jolt.", end=" ")
    print(f"The product joltage is {product}.")
    return diff_1,diff_3, product


def find_differences_and_product2(adapters, build_in_joltage=3):
    differences = defaultdict(int)
    differences[build_in_joltage] = 1
    adapters = sorted(adapters)
    last = 0
    for adapter in adapters:
        differences[adapter-last] += 1
        last = adapter
    joltage_product = differences[1] * differences[3]
    print(f"There are {differences[1]} differences of 1 jolt and {differences[3]} differences of 3 jolt.", end=" ")
    print(f"The product joltage is {joltage_product}.")
    return differences[1], differences[3], joltage_product
                

def find_combinations(adapters, max_diff=3):
    paths = defaultdict(int)
    paths[0] = 1
    adapters = sorted(adapters)
    for joltage in adapters:
        paths[joltage] = sum(paths[j] for j in range(joltage-max_diff, joltage))
    combinations = paths[adapters[-1]]
    print(f"Found {combinations} disctinct arrangements.")
    return combinations


if __name__ == "__main__":
    print("Example")
    adapters = load_adapters("data/day-10-example1.txt")
    result = find_differences_and_product(adapters)
    assert result == (7, 5, 35)
    # print("timeit 1", timeit.repeat(partial(find_differences_and_product, adapters)))
    result = find_differences_and_product2(adapters)
    assert result == (7, 5, 35)
    # print("timeit 2", timeit.repeat(partial(find_differences_and_product2, adapters)))
    result = find_combinations(adapters)
    assert result == 8
    adapters = load_adapters("data/day-10-example2.txt")
    result = find_differences_and_product(adapters)
    assert result == (22, 10, 220)
    result = find_differences_and_product2(adapters)
    assert result == (22, 10, 220)
    result = find_combinations(adapters)
    assert result == 19208
    print("Reality")
    adapters = load_adapters("data/day-10.txt")
    result = find_differences_and_product(adapters)
    assert result == (69, 33, 2277)
    # print("timeit 1", timeit.repeat(partial(find_differences_and_product, adapters)))
    result = find_differences_and_product2(adapters)
    assert result == (69, 33, 2277)
    # print("timeit 2", timeit.repeat(partial(find_differences_and_product2, adapters)))
    result = find_combinations(adapters)
    assert result == 37024595836928
    
