#!/usr/bin/env python
import re

regex = re.compile(r"(?P<min>\d+)-(?P<max>\d+) (?P<char>\w): (?P<password>.+)")

def is_valid(args):
    """Checks if the password contains the char within the limits of min and max"""
    (min, max, char, password) = args
    return min <= password.count(char) <= max

def parse_line(line):
    """Prase the line for processing"""
    m = regex.match(line)
    min = int(m.group("min"))
    max = int(m.group("max"))
    char = m.group("char")
    password = m.group("password")
    return (min, max, char, password)

def count_valid_passwords():
    """Count the number of valid passwords in a list according to rules specified on the same line"""
    with open("data/day-02.txt") as f:
        rows = map(parse_line, f.readlines())
        valid = filter(is_valid, rows)
        count = len(tuple(valid))
        print(f"{count} passwords are valid")
        return count


if __name__ == "__main__":
    result = count_valid_passwords()
    assert result == 383
