#!/usr/bin/env python
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from io import BytesIO
from operator import add, mul
import re


operators = {"*": mul, "+": add}
regex_parenthesis = re.compile(r"\(([^()]+)\)")
regex_add = re.compile(r"\s*(\d+)\s*\+\s*(\d+)\s*")
regex_mul = re.compile(r"\s*(\d+)\s*\*\s*(\d+)\s*")


def evaluate_basic(line):
    result = 0
    tmp = None
    op = add
    for toknum, tokval, _, _, _ in tokenize(BytesIO(line.encode("utf-8")).readline):
        if toknum == NUMBER:
            tmp = int(tokval)
        elif toknum == OP:
            op = operators[tokval]
        if op is not None and tmp is not None:
            result = op(result, tmp)
            tmp = None
            op = None
    return result


def evaluate(line, evaluator=evaluate_basic):
    original_line = line
    while True:
        m = regex_parenthesis.search(line)
        if m is None:
            break
        part_result = evaluator(m.group(1))
        line = regex_parenthesis.sub(str(part_result), line, count=1)
    result = evaluator(line)
    print(f"{original_line} = {result}")
    return result


def evaluate_advanced(line):
    while True:
        m = regex_add.search(line)
        if m is None:
            break
        part_result = add(int(m.group(1)), int(m.group(2)))
        line = regex_add.sub(str(part_result), line, count=1)
    result = eval(line)
    return result


def sum_all(filename, evaluator=evaluate_basic):
    with open(filename) as f:
        result = 0
        for line in f:
            result += evaluate(line.strip(), evaluator)
    print(f"The sum of all equations is {result}")
    return result


if __name__ == "__main__":
    print("======================================== Example ========================================")
    result = evaluate("1 + 2 * 3 + 4 * 5 + 6")
    assert result == 71
    result = evaluate("1 + (2 * 3) + (4 * (5 + 6))")
    assert result == 51
    result = sum_all("data/day-18-example1.txt")
    assert result == 26 + 437 + 12240 + 13632
    result = evaluate("1 + 2 * 3 + 4 * 5 + 6", evaluate_advanced)
    assert result == 231
    result = evaluate("1 + (2 * 3) + (4 * (5 + 6))", evaluate_advanced)
    assert result == 51
    result = sum_all("data/day-18-example1.txt", evaluate_advanced)
    assert result == 46 + 1445 + 669060 + 23340
    print("======================================== Reality ========================================")
    result = sum_all("data/day-18.txt")
    assert result == 11076907812171
    result = sum_all("data/day-18.txt", evaluate_advanced)
    assert result == 283729053022731
    
