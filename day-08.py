#!/usr/bin/env python
from functools import reduce
from operator import add, and_
from dataclasses import dataclass
from typing import List
import re
from pprint import pprint

regex_content = re.compile(r"(\d+) ((\w+\s?)+) bag")
regex_bag = re.compile(r"(.*?) bags contain")


@dataclass
class Command:
    cmd: str
    arg: int
    count: int


def parse_command(line):
    """Parse a line an creates a command"""
    parts = line.split(" ")
    cmd = Command(parts[0], int(parts[1]), 0)
    return cmd


def load_program(filename):
    """Load the program and returns a list of instructions"""
    with open(filename) as f:
        program = [parse_command(line) for line in f.readlines()]
        return program

def run(program):
    """Runs the program and prints the accumulator if an error occurs"""
    accumulator = 0
    try:
        length = len(program)
        i = 0
        while i < length:
            cmd = program[i]
            assert cmd.count == 0, f"instruction {cmd} at line {i+1} already executed"
            if cmd.cmd == "acc":
                accumulator += cmd.arg
            cmd.count += 1
            if cmd.cmd == "jmp":
                i += cmd.arg
            else:
                i += 1
    except Exception as ex:
        print(ex)
        print(f"accumulator before error: {accumulator}")
    return accumulator


if __name__ == "__main__":
    print("Example")
    program = load_program("data/day-08-example1.txt")
    accumulator = run(program)
    assert accumulator == 5
    print("Reality")
    program = load_program("data/day-08.txt")
    accumulator = run(program)
    # assert accumulator == 5
