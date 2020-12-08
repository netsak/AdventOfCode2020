#!/usr/bin/env python
from dataclasses import dataclass
from copy import deepcopy


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
    program = deepcopy(program)
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
        print(f"ERROR: {ex}: accumulator before error: {accumulator}")
        return accumulator, False
    return accumulator, True


def fix_it(program):
    """Tries to fix the program by changing switching nop and jmp statements"""
    for i, cmd in enumerate(program):
        current_program = deepcopy(program)
        if cmd.cmd == "jmp":
            current_program[i].cmd = "nop"
        elif cmd.cmd == "nop":
            current_program[i].cmd = "jmp"
        else:
            continue
        accumulator, success = run(current_program)
        if success:
            print(f"accumulator after successful run: {accumulator}")
            return accumulator


if __name__ == "__main__":
    print("Example")
    program = load_program("data/day-08-example1.txt")
    result = run(program)
    assert result == (5, False)
    accumulator = fix_it(program)
    assert accumulator == 8
    print("Reality")
    program = load_program("data/day-08.txt")
    result = run(program)
    assert result == (1675, False)
    accumulator = fix_it(program)
    assert accumulator == 1532

