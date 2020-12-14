#!/usr/bin/env python
from dataclasses import dataclass
import math
import numpy as np
from typing import List
from itertools import count
import re
from copy import deepcopy
from collections import defaultdict


regex_mask = re.compile(r"mask = ([X01]+)")
regex_memory = re.compile(r"mem\[(\d+)\] = (\d+)")


@dataclass
class Program(object):
    mask: str
    addr: int
    value: int


def load_program(filename):
    program = list()
    with open(filename) as f:
        mask = ""
        for line in f.readlines():
            m = regex_mask.match(line)
            if m:
                mask = m.group(1)
                continue
            m = regex_memory.match(line)
            prg = Program(mask, int(m.group(1)), int(m.group(2)))
            print(prg)
            program.append(prg)
        return program


def apply_mask(program):
    memory = defaultdict(int)
    for prg in program:
        # print("mask   ", mask)
        bin_str = format(prg.value, "#038b")[2:]
        # print("bin_str", bin_str)
        new_str = "".join(b if b != "X" else a for a, b in zip(bin_str, prg.mask))
        # print("new_str", new_str)
        value = int(new_str, 2)
        memory[prg.addr] = value
    return memory


def sum_memory(memory):
    value = sum(memory.values())
    print(f"sum of all memory values is {value}")
    return value


if __name__ == "__main__":
    print("========== Example ========== ")
    program = load_program("data/day-14-example1.txt")
    print(program)
    assert program == [Program(mask="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", addr=8, value=11), Program(mask="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", addr=7, value=101), Program(mask="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",addr=8, value=0), Program(mask="000XXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",addr=10, value=0)]
    memory = apply_mask(program)
    print(memory)
    assert memory == {8: 64, 7: 101, 10: 64}
    result = sum_memory(memory)
    assert result == 165 + 64
    print("==========  Reality ========== ")
    program = load_program("data/day-14.txt")
    # print(program)
    memory = apply_mask(program)
    # print(memory)
    result = sum_memory(memory)
    assert result == 7477696999511
