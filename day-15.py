#!/usr/bin/env python
from collections import defaultdict


def play(starting_numbers, stop=10):
    numbers = [-1] + starting_numbers
    spoken = defaultdict(list)
    number = starting_numbers[-1]
    for i, n in enumerate(starting_numbers):
        spoken[n].append(i+1)
    for turn in range(len(numbers), stop+1):
        last = numbers[-1]
        count = len(spoken[last])
        if count <= 1:
            number = 0
        else:
            number = spoken[last][-1] - spoken[last][-2]
        numbers.append(number)
        spoken[number].append(turn)
    result = numbers[-1]
    print(f"The last number spoken was {result}")
    return result



if __name__ == "__main__":
    print("======================================== Example ========================================")
    numbers = [0,3,6]
    result = play(numbers)
    assert result == 0
    result = play(numbers, 2020)
    assert result == 436
    print("========================================  Reality ========================================")
    numbers = [15,5,1,4,7,0]
    result = play(numbers, 2020)
    assert result == 1259
    result = play(numbers, 30000000)
    assert result == 689
