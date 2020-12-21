#!/usr/bin/env python
import re
from dataclasses import dataclass
from typing import Set


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
            f = Food(set(regex_ingredients.findall(line)) - {"contains"}, set(regex_allergens.findall(line)))
            ret.append(f)
        return ret


def build_translation_table(food):
    allergens = dict()
    for f in food:
        for allergen in f.allergens:
            if not allergens.get(allergen):
                allergens[allergen] = set(f.ingredients)
            else:
                allergens[allergen] &= set(f.ingredients)
    all_possible_allergens = set()
    for items in allergens.values():
        all_possible_allergens.update(set(items))
    return allergens, all_possible_allergens


def count_non_allergic_ingredients(food, allergens):
    ingredients = set()
    for f in food:
        ingredients.update(set(f.ingredients))
    non_allergens = ingredients - allergens
    count = sum(len(set(f.ingredients) & non_allergens) for f in food)
    print(f"Found {count} non-allergic ingredients")
    return count
    

def canonical_dangerous_ingredient_list(allergens):
    for _ in range(10):
        for ingredient in allergens.values():
            if len(ingredient) == 1:
                remove = set(ingredient)
                for allergen, ingredients in allergens.items():
                    if len(ingredients) > 1:
                        allergens[allergen] -= remove 
    dangerous_ingredients = ",".join([allergens[x].pop() for x in sorted(allergens) if allergens[x]])
    print(f"Found canonical dangerous ingredient list: {dangerous_ingredients}")
    return dangerous_ingredients


if __name__ == "__main__":
    print("======================================= Part 1 - Example 1 =========================================")
    food = load_food("data/day-21-example1.txt")
    assert len(food) == 4
    allergens, all_possible_allergens = build_translation_table(food)
    result = count_non_allergic_ingredients(food, all_possible_allergens)
    assert result == 5
    print("======================================= Part 2 - Example 1 =========================================")
    result = canonical_dangerous_ingredient_list(allergens)
    assert result == "mxmxvkd,sqjhc,fvjkl"
    print("======================================= Part 1 - Real Puzzle =======================================")
    food = load_food("data/day-21.txt")
    assert len(food) == 41
    allergens, all_possible_allergens = build_translation_table(food)
    result = count_non_allergic_ingredients(food, all_possible_allergens)
    assert result == 2423
    print("======================================= Part 2 - Real Puzzle =======================================")    
    result = canonical_dangerous_ingredient_list(allergens)
    assert result == "jzzjz,bxkrd,pllzxb,gjddl,xfqnss,dzkb,vspv,dxvsp"

