#!/usr/bin/env python
from copy import deepcopy
import re
from dataclasses import dataclass
from typing import Set
from collections import defaultdict


regex_ingredients = re.compile(r"(\w+)\s")
regex_allergens = re.compile(r"(\w+)[,)]")


@dataclass
class Food(object):
    ingredients: Set[str]
    allergens: Set[str]


def load_food(filename):
    ret = list()
    with open(filename) as f:
        for line in f.readlines():
            # print(line)
            # print(regex_ingredients.findall(line))
            # print(regex_allergens.findall(line))
            f = Food(set(regex_ingredients.findall(line)) - {"contains"}, set(regex_allergens.findall(line)))
            ret.append(f)
        return ret


def build_translation_table(food):
    allergens = dict()
    for f in food:
        # print(f)
        for allergen in f.allergens:
            if not allergens.get(allergen):
                # print("new allergen", allergen, f.ingredients)
                allergens[allergen] = set(f.ingredients)
            else:
                # print("existing allergen", allergen, f.ingredients, allergens[allergen])
                allergens[allergen] &= set(f.ingredients)
            # print(">>>", allergens)
    all_possible_allergens = set()
    for items in allergens.values():
        all_possible_allergens.update(set(items))
    return allergens, all_possible_allergens


def count_non_allergic_ingredients(food, allergens):
    ingredients = set()
    for f in food:
        ingredients.update(set(f.ingredients))
    non_allergens = ingredients - allergens
    # print("non_allergens", non_allergens)
    count = 0
    for f in food:
        count += len(set(f.ingredients) & non_allergens)
    print(f"Found {count} non-allergic ingredients")
    return count
    

if __name__ == "__main__":
    print("======================================= Part 1 - Example 1 =========================================")
    food = load_food("data/day-21-example1.txt")
    assert len(food) == 4
    allergens, all_possible_allergens = build_translation_table(food)
    result = count_non_allergic_ingredients(food, all_possible_allergens)
    assert result == 5
    # print("======================================= Part 2 - Example 1 =========================================")
    # print("======================================= Part 2 - Example 2 =========================================")
    print("======================================= Part 1 - Real Puzzle =======================================")
    food = load_food("data/day-21.txt")
    assert len(food) == 41
    allergens, all_possible_allergens = build_translation_table(food)
    result = count_non_allergic_ingredients(food, all_possible_allergens)
    assert result == 2423
    # print("======================================= Part 2 - Real Puzzle =======================================")    

