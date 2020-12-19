#!/usr/bin/env python
from copy import deepcopy
import re


def load_data(filename):
    with open(filename) as f:
        rules = dict()
        while True:
            line = f.readline().strip()
            if line == "":
                break
            parts = line.split(":")
            idx = int(parts[0])
            rules[idx] = parts[1].strip(' "')
        messages = list()
        for line in f.readlines():
            messages.append(line.strip())
        return rules, messages


def resolve_rules(rules):
    ret = deepcopy(rules)
    for _ in range(7):
        for idx, rule in ret.items():
            parts = rule.split(" ")
            new_rule = ""
            for part in parts:
                if part.isnumeric():
                    sub_rule = ret[int(part)]
                    if "|" in sub_rule:
                        new_rule += f"( {sub_rule} )"
                    else:
                        new_rule += f" {sub_rule} "
                else:
                    new_rule += part
            ret[idx] = new_rule
    return ret


def filter_matching_rule(messages, rule):
    rule_regex = re.compile(rule)
    valid = [msg for msg in messages if rule_regex.fullmatch(msg)]
    count = len(valid)
    print(f"Found {count} valid messages")
    return valid, count


def fix_it(rules):
    rules[8] = "42 | 42 8"
    rules[11] = "42 31 | 42 11 31"
    return rules
    

if __name__ == "__main__":
    print("======================================= Part 1 - Example 1 =========================================")
    rules, messages = load_data("data/day-19-example1.txt")
    assert rules == {0: '4 1 5', 1: '2 3 | 3 2', 2: '4 4 | 5 5', 3: '4 5 | 5 4', 4: 'a', 5: 'b'}
    assert messages == ["ababbb", "bababa", "abbbab", "aaabbb", "aaaabbb"]
    resolved = resolve_rules(rules)
    valid, count = filter_matching_rule(messages, resolved[0])
    assert count == 2
    assert valid == ["ababbb", "abbbab"]
    print("======================================= Part 2 - Example 1 =========================================")
    rules, messages = load_data("data/day-19-example2.txt")
    resolved = resolve_rules(rules)
    valid, count = filter_matching_rule(messages, resolved[0])
    assert count == 3
    assert valid == ["bbabbbbaabaabba", "ababaaaaaabaaab", "ababaaaaabbbaba"]
    print("======================================= Part 2 - Example 2 =========================================")
    rules = fix_it(rules)
    resolved = resolve_rules(rules)
    valid, count = filter_matching_rule(messages, resolved[0])
    assert count == 12
    assert valid == ["bbabbbbaabaabba", "babbbbaabbbbbabbbbbbaabaaabaaa" , "aaabbbbbbaaaabaababaabababbabaaabbababababaaa" , "bbbbbbbaaaabbbbaaabbabaaa" , "bbbababbbbaaaaaaaabbababaaababaabab" , "ababaaaaaabaaab" , "ababaaaaabbbaba" , "baabbaaaabbaaaababbaababb" , "abbbbabbbbaaaababbbbbbaaaababb" , "aaaaabbaabaaaaababaa" , "aaaabbaabbaaaaaaabbbabbbaaabbaabaaa", "aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"]
    print("======================================= Part 1 - Real Puzzle =======================================")
    rules, messages = load_data("data/day-19.txt")
    resolved = resolve_rules(rules)
    valid, count = filter_matching_rule(messages, resolved[0])
    assert count == 195
    print("======================================= Part 2 - Real Puzzle =======================================")    
    rules = fix_it(rules)
    resolved = resolve_rules(rules)
    valid, count = filter_matching_rule(messages, resolved[0])
    assert count == 309

