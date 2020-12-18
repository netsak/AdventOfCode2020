#!/usr/bin/env python
import re


regex_number = re.compile(r"(\d+)")


class Basic(object):
    """Basic calculation is like normal math but with same precedence for + and * operators"""

    def __init__(self, number):
        if isinstance(number, int):
            self.number = number
        else:
            self.number == int(number)
    
    def __add__(self, other):
        if isinstance(other, Basic):
            other = other.number
        return Basic(self.number + other)

    def __sub__(self, other):
        if isinstance(other, Basic):
            other = other.number
        return Basic(self.number * other)

    @staticmethod
    def transform(line):
        return regex_number.sub(r"Basic(\1)", line).replace("*","-")


class Advanced(object):
    """Basic calculation is like normal math but with swapped precedence for + and * operators"""

    def __init__(self, number):
        if isinstance(number, int):
            self.number = number
        else:
            self.number == int(number)
    
    def __add__(self, other):
        if isinstance(other, Advanced):
            other = other.number
        return Advanced(self.number * other)

    def __mul__(self, other):
        if isinstance(other, Advanced):
            other = other.number
        return Advanced(self.number + other)

    @staticmethod
    def transform(line):
        return regex_number.sub(r"Advanced(\1)", line).replace("*","-").replace("+","*").replace("-","+")


def evaluate(line, transformer=Basic):
    original_line = line
    line = transformer.transform(line)
    result = eval(line)
    print(f"{original_line} = {result.number}")
    return result.number


def sum_all(filename, transformer=Basic):
    with open(filename) as f:
        result = 0
        for line in f:
            result += evaluate(line.strip(), transformer)
    print(f"The sum of all equations is {result}")
    return result


if __name__ == "__main__":
    print("======================================== Example ========================================")
    result = evaluate("1 + 2 + 3")
    assert result == 6
    result = evaluate("1 + 2 * 3 + 4 * 5 + 6")
    assert result == 71
    result = evaluate("1 + (2 * 3) + (4 * (5 + 6))")
    assert result == 51
    result = sum_all("data/day-18-example1.txt")
    assert result == 26 + 437 + 12240 + 13632
    result = evaluate("1 + 2 * 3 + 4 * 5 + 6", Advanced)
    assert result == 231
    result = evaluate("1 + (2 * 3) + (4 * (5 + 6))", Advanced)
    assert result == 51
    result = sum_all("data/day-18-example1.txt", Advanced)
    assert result == 46 + 1445 + 669060 + 23340
    # print("======================================== Reality ========================================")
    result = sum_all("data/day-18.txt")
    assert result == 11076907812171
    result = sum_all("data/day-18.txt", Advanced)
    assert result == 283729053022731
    
