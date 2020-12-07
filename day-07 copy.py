#!/usr/bin/env python
from functools import reduce
from operator import add, and_
from dataclasses import dataclass
from typing import List
import re
from pprint import pprint

regex_content = re.compile(r"(\d+) ((\w+\s?)+) bag")
regex_bag = re.compile(r"(.*?) bags contain")


# @dataclass
# class Bag:
#     color: str
#     count: int

#     def can_contain(self, color):
#         print("can contain", color, self)
#         return color == self.color

# @dataclass
# class Rule:
#     color: str
#     bags: List[Bag]

#     def can_contain(self, color):
#         ret = any(bag.can_contain(color) for bag in self.bags)
#         print("can contain", color, self, ret)
#         return 

# def create_rule(line):
#     """Parse a line an creates a rule"""
#     m = regex_bag.match(line) 
#     matches = regex_content.findall(line)
#     rule = Rule(m.group(1), None)
#     # if len(matches) > 0:
#     rule.bags = [Bag(color, count) for count, color, _ in matches]
#     return rule  


# def get_rules(filename):
#     """Load and parse all bag rules"""
#     with open(filename) as f:
#         rules = [create_rule(line) for line in f.readlines()]
#         return rules

# def find_bag_colors(rules, color):
#     """Find all colors which can contain a bag of the given color"""
#     bags = [rule.can_contain(color) for rule in rules]
#     pprint(bags)

def create_rule(line):
    """Parse a line an creates a rule"""
    m = regex_bag.match(line) 
    matches = regex_content.findall(line)
    color = m.group(1)
    # if len(matches) > 0:
    bags = [color for count, color, _ in matches]
    return color, bags

def get_rules(filename):
    """Load and parse all bag rules"""
    with open(filename) as f:
        rules = dict(create_rule(line) for line in f.readlines())
        return rules

def can_contain(rules, color):
    print("can", rules, "contain", color)
    # for bags in rules[rule]:
    #     if bags == color:
    #         print("found1", bag)
    #         return bag
    #     print("deeper", bags)
    #     for bag in bags:
    #         if can_contain(rules, rules[bag], color):
    #             print("found2", bag)
    #             return bag
    return False

def find_bag_colors(rules, color, level=0):
    """Find all colors which can contain a bag of the given color"""
    # found = [can_contain(rules, rule, color) for rule in rules]
    # print("\t"*level, "find", color, "in rules", rules.keys())
    found = []
    # for rule, bags in rules.items():
    #     print("\t"*level, "rule:", rule, "bags:", bags)
    #     if color in bags:
    #         found.append(rule)
    #         continue
    #     subset = {k: rules.get(k, None) for k in ('bright white', 'muted yellow')}
    #     print("\t"*level, "subset", subset)
    #     in_subset = find_bag_colors(subset, color, level + 1)
    #     print("\t"*level, "found in subset", in_subset)
    #     if len(in_subset) > 0:
    #         found.append(rule)
    def mapper(rule, bags):
        ret = set()
        print(">>> mapping rule", rule, bags)
        for bag in bags:
            ret.add(bag)
            # if bag in rules and bag != color:
            if bag in rules:
                print("submappper", bag, rules[bag])
                ret |= mapper(bag, rules[bag])
        return ret
    resolved = {rule: mapper(rule, bags) for rule, bags in rules.items()}
    print("resolved")
    pprint(resolved)
    print("found")
    found = tuple(filter(lambda item: bool(color in item[1]), resolved.items()))
    print(f"{len(found)} bags can contain at least one {color} bag")
    return found


if __name__ == "__main__":
    print("Example")
    rules = get_rules("data/day-07-example1.txt")
    pprint(rules)
    # assert rules[0] == Rule(color='light red', bags=[Bag(color='bright white', count='1'), Bag(color='muted yellow', count='2')])
    # assert rules[8] == Rule(color='dotted black', bags=[])
    found = find_bag_colors(rules, "shiny gold")
    pprint(found)
    print("Reality")
