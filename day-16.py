#!/usr/bin/env python
from re import compile
from collections import defaultdict
from operator import mul
from functools import reduce
from more_itertools import chunked
from itertools import combinations


regex_rule = compile(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)")


def load_data(filename):
    rules = dict()
    my_ticket = list()
    nearby_tickets = list()
    with open(filename) as f:
        line = f.readline().strip() # rules
        while line != "":
            m = regex_rule.match(line)
            rules[m.group(1)] = list(chunked((int(g) for g in m.groups()[1:]), 2))
            line = f.readline().strip()
        line = f.readline().strip() # your ticket
        line = f.readline().strip()
        my_ticket = [int(x) for x in line.split(",")]
        line = f.readline().strip() # nearby tickets
        line = f.readline().strip()
        line = f.readline().strip()
        while line != "":
            ticket = [int(x) for x in line.split(",")]
            nearby_tickets.append(ticket)
            line = f.readline().strip()
    return rules, my_ticket, nearby_tickets


def find_invalid_numbers(rules, ticket):
    invalid = list()
    for number in ticket:
        valid_number = [(min_value <= number <= max_value) for rule in rules.values() for min_value, max_value in rule ]
        if not any(valid_number):
            invalid.append(number)
    return invalid


def find_valid_tickets(rules, tickets):
    invalid = list()
    valid_tickets = list()
    for ticket in tickets:
        invalid_ticket_numbers = find_invalid_numbers(rules, ticket)
        invalid.extend(invalid_ticket_numbers)
        if len(invalid_ticket_numbers) == 0:
            valid_tickets.append(ticket)
    invalid_sum = sum(invalid)
    print(f"The sum of all invalid numbers is {invalid_sum}")
    return invalid_sum, valid_tickets


def find_valid_fields(rules, ticket):
    valid_fields = defaultdict(set)
    invalid_fields = defaultdict(set)
    for i, number in enumerate(ticket):
        for name, values in rules.items():
            valid_numbers = [(min_value <= number <= max_value) for min_value, max_value in values]
            if any(valid_numbers):
                valid_fields[name] |= {i}
            else:
                invalid_fields[name] |= {i}
    ret = defaultdict(set)
    for name, values in valid_fields.items():
        ret[name] = values - invalid_fields[name]
    return ret


def match_fields(rules, tickets, prefix=""):
    fields = dict()
    for ticket in tickets:
        valid_fields = find_valid_fields(rules, ticket)
        for name, values in valid_fields.items():
            if fields.get(name) is None:
                fields[name] = values
            else:
                fields[name] &= values
    for _ in fields:
        ones = [(name, values) for name, values in fields.items() if len(fields[name]) == 1]
        for v in ones:
            for n in fields:
                if n != v[0]:
                    fields[n] -= v[1]
    result = [values.pop() for name, values in fields.items() if name.startswith(prefix)]
    return result


def multiply(ticket, mapping):
    values = [ticket[i] for i in mapping]
    product = reduce(mul, values)
    print(f"The product of {values} is {product}")
    return product


if __name__ == "__main__":
    print("======================================== Example ========================================")
    rules, my_ticket, nearby_tickets = load_data("data/day-16-example1.txt")
    invalid_sum, valid_tickets = find_valid_tickets(rules, nearby_tickets)
    assert invalid_sum == 71
    assert valid_tickets == [[7, 3, 47]]
    rules, my_ticket, nearby_tickets = load_data("data/day-16-example2.txt")
    invalid_sum, valid_tickets = find_valid_tickets(rules, nearby_tickets)
    assert invalid_sum == 0
    assert valid_tickets == nearby_tickets
    indices = match_fields(rules, valid_tickets)
    assert indices == [0, 2, 1]
    result = multiply(my_ticket, indices)
    assert result == 1716
    print("======================================== Reality ========================================")
    rules, my_ticket, nearby_tickets = load_data("data/day-16.txt")
    invalid_sum, valid_tickets = find_valid_tickets(rules, nearby_tickets)
    assert invalid_sum == 29759
    indices = match_fields(rules, valid_tickets, "departure")
    assert indices == [2, 14, 16, 1, 17, 6]
    result = multiply(my_ticket, indices)
    assert result > 866802964589
    assert result == 1307550234719
