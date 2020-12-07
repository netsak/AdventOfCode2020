#!/usr/bin/env python
from dataclasses import dataclass
import re


regex_content = re.compile(r"(\d+) ((\w+\s?)+) bag")
regex_bag = re.compile(r"(.*?) bags contain")


@dataclass
class Bag:
    color: str
    count: int


def create_rule(line):
    """Parse a line an creates a rule"""
    m = regex_bag.match(line) 
    matches = regex_content.findall(line)
    color = m.group(1)
    bags = [Bag(color, int(count)) for count, color, _ in matches]
    return color, bags  


def get_rules(filename):
    """Load and parse all bag rules"""
    with open(filename) as f:
        rules = {k: v for (k,v) in (create_rule(line) for line in f.readlines())}
        return rules


def find_bag_colors(rules, color, level=0):
    """Find all colors which can contain a bag of the given color"""
    found = []
    def mapper(rule, bags):
        ret = set()
        for bag in bags:
            ret.add(bag.color)
            if bag.color in rules:
                ret |= mapper(bag.color, rules[bag.color])
        return ret
    resolved = {rule: mapper(rule, bags) for rule, bags in rules.items()}
    found = tuple(filter(lambda item: bool(color in item[1]), resolved.items()))
    print(f"{len(found)} bags can contain at least one {color} bag")
    return found


def find_total_bag_colors(rules, color, level=0):
    """Find all colors which can contain a bag of the given color"""
    found = []
    def mapper(rule, times):
        ret = []
        for bag in rules[rule]:
            for _ in range(bag.count):
                ret.append(bag)
        for bag in tuple(ret):
            ret.extend(mapper(bag.color, bag.count))
        return ret
    found = mapper(color, 1)
    print(f"{len(found)} bags needed within a {color} bag")
    return found


if __name__ == "__main__":
    print("Example")
    rules = get_rules("data/day-07-example1.txt")
    found = find_bag_colors(rules, "shiny gold")
    assert len(found) == 4
    found = find_total_bag_colors(rules, "shiny gold")
    assert len(found) == 32
    print("Reality")
    rules = get_rules("data/day-07.txt")
    found = find_bag_colors(rules, "shiny gold")
    assert len(found) == 192
    found = find_total_bag_colors(rules, "shiny gold")
    assert len(found) == 12128
