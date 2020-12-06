#!/usr/bin/env python
from functools import reduce
from pprint import pprint


def get_group_questions(filename):
    """Load the questions for each group"""
    with open(filename) as f:
        content = f.read().split("\n\n")
        group_questions = [set(c for c in line if c != "\n") for line in content]
        return group_questions


def sum_questions(questions):
    count = len(tuple(y for q in questions for y in q))
    print(f"The sum of all answered questions is {count}")
    return count


if __name__ == "__main__":
    # example
    questions = get_group_questions("data/day-06-example1.txt")
    count = sum_questions(questions)
    assert count == 11
    # reality
    questions = get_group_questions("data/day-06.txt")
    count = sum_questions(questions)
    assert count == 6297
