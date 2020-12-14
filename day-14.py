#!/usr/bin/env python
from dataclasses import dataclass
from re import compile
from collections import defaultdict


regex_mask = compile(r"mask = ([X01]+)")
regex_memory = compile(r"mem\[(\d+)\] = (\d+)")


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
            program.append(prg)
        return program


def apply_mask_to_value(program):
    memory = defaultdict(int)
    for prg in program:
        bin_str = format(prg.value, "#038b")[2:]
        new_str = "".join(b if b != "X" else a for a, b in zip(bin_str, prg.mask))
        value = int(new_str, 2)
        memory[prg.addr] = value
    return memory


def generate_address(address):
    i = address.find("X")
    if i < 0:
        yield int(address, 2)
    else:
        yield from generate_address(address[:i] + "0" + address[i+1:])
        yield from generate_address(address[:i] + "1" + address[i+1:])


def apply_mask_to_address(program):
    memory = defaultdict(int)
    for prg in program:
        bin_str = format(prg.addr, "#038b")[2:]
        new_str = "".join(b if b in "1X" else a for a, b in zip(bin_str, prg.mask))
        for a in generate_address(new_str):
            memory[a] = prg.value
    return memory


def sum_memory(memory):
    value = sum(memory.values())
    print(f"sum of all memory values is {value}")
    return value



if __name__ == "__main__":
    print("======================================== Example ========================================")
    program = load_program("data/day-14-example1.txt")
    assert program == [Program(mask="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", addr=8, value=11), Program(mask="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", addr=7, value=101), Program(mask="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",addr=8, value=0), Program(mask="000XXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",addr=10, value=0)]
    memory = apply_mask_to_value(program)
    assert memory == {8: 64, 7: 101, 10: 64}
    result = sum_memory(memory)
    assert result == 165 + 64
    assert list(generate_address("101")) == [0b101]
    assert list(generate_address("1X1")) == [0b101, 0b111]
    program = load_program("data/day-14-example2.txt")
    memory = apply_mask_to_address(program)
    assert memory[58] == memory[59] == 100
    assert memory[16] == memory[17] == memory[18] == memory[19] == memory[24] == memory[25] == memory[26]  == memory[27] == 1
    result = sum_memory(memory)
    assert result == 208
    print("========================================  Reality ========================================")
    program = load_program("data/day-14.txt")
    memory = apply_mask_to_value(program)
    result = sum_memory(memory)
    assert result == 7477696999511
    memory = apply_mask_to_address(program)
    result = sum_memory(memory)
    assert result == 3687727854171
