#!/usr/bin/env python
from functools import reduce
from operator import add, and_


def get_group_questions(filename):
    """Load all answered questions for each group"""
    with open(filename) as f:
        content = f.read().split("\n\n")
        group_questions = [set(c for c in line if c != "\n") for line in content]
        return group_questions


def sum_answers(questions):
    count = reduce(add, (len(answer) for question in questions for answer in question))
    print(f"The sum of all answered questions is {count}")
    return count


def get_common_group_questions(filename):
    """Load all answered questions for each group answered by each group member"""
    with open(filename) as f:
        groups = f.read().split("\n\n")
        split_set = lambda group: (set(group) for group in group.split("\n"))
        group_sets = (map(split_set, groups))
        group_questions = (reduce(and_, group) for group in group_sets)
        return group_questions


if __name__ == "__main__":
    print("Example")
    questions = get_group_questions("data/day-06-example1.txt")
    count = sum_answers(questions)
    assert count == 11
    questions = get_common_group_questions("data/day-06-example1.txt")
    count = sum_answers(questions)
    assert count == 6
    print("Reality")
    questions = get_group_questions("data/day-06.txt")
    count = sum_answers(questions)
    assert count == 6297
    questions = get_common_group_questions("data/day-06.txt")
    count = sum_answers(questions)
    assert count == 3158