#!/usr/bin/env python
from itertools import combinations


def get_input(filename):
    with open(filename) as f:
        numbers = [int(line) for line in f.readlines()]
        return numbers


def find_error(numbers, preamble_length):
    for i in range(preamble_length, len(numbers)):
        number = numbers[i]
        preamble = numbers[i-preamble_length:i]
        if number not in (sum(c) for c in combinations(preamble, 2)):
            print(f"{number} at index {i} is not part of the sum of two preamble numbers")
            return (i, number)


def find_weakness(numbers, index, target):
    for i in range(0, index):
        for j in range(i+1, index):
            number_range = numbers[i:j]
            range_sum = sum(number_range)
            if range_sum == target:
                smallest = min(number_range)
                largest = max(number_range)
                weakness = smallest + largest
                print(f"Found {smallest} + {largest} == {weakness}")
                return smallest, largest, weakness
            elif range_sum > target:
                break


if __name__ == "__main__":
    print("Example")
    numbers = get_input("data/day-09-example1.txt")
    index, number = find_error(numbers, 5)
    assert number == 127
    result = find_weakness(numbers, index, number)
    assert result == (15, 47, 62)
    print("Reality")
    numbers = get_input("data/day-09.txt")
    index, number = find_error(numbers, 25)
    assert number == 41682220
    result = find_weakness(numbers, index, number)
    assert result == (1706712, 3682264, 5388976)
