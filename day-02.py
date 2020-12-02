#!/usr/bin/env python
import re

regex = re.compile(r"(?P<n1>\d+)-(?P<n2>\d+) (?P<char>\w): (?P<password>.+)")

def is_valid_old(args):
    """Checks if the password contains the char n times within the limits of min and max.
    This is the old method used down the street.
    """
    (min, max, char, password) = args
    return min <= password.count(char) <= max

def is_valid_new(args):
    """Checks if the password contains the char at exactly one of the given positions.
    This is the official Toboggan Corporate Policy.
    """
    (pos1, pos2, char, password) = args
    positions = (pos1 -1, pos2 -1) # Toboggan Corporate Policies have no concept of "index zero"
    matches = [password[i] for i in positions if password[i] == char]
    return len(matches) == 1

def parse_line(line):
    """Prase the line for processing"""
    m = regex.match(line)
    n1 = int(m.group("n1"))
    n2 = int(m.group("n2"))
    char = m.group("char")
    password = m.group("password")
    return (n1, n2, char, password)

def count_valid_passwords(validator):
    """Count the number of valid passwords in a list according to rules specified on the same line"""
    with open("data/day-02.txt") as f:
        rows = map(parse_line, f.readlines())
        valid = filter(validator, rows)
        count = len(tuple(valid))
        print(f"{count} passwords are valid")
        return count


if __name__ == "__main__":
    result = count_valid_passwords(is_valid_old)
    assert result == 383
    result = count_valid_passwords(is_valid_new)
    assert result == 272
