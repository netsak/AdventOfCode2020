#!/usr/bin/env python
from copy import deepcopy
from time import sleep


slopes = ( (-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1), (1, 1), (-1, -1) )


def load_seats(filename):
    with open(filename) as f:
        seats = ["."+line.strip()+"." for line in f.readlines()]
        seats.insert(0, "." * len(seats[0]))
        seats.append("." * len(seats[0]))
        seats = [list(row) for row in seats]
        return seats


def simple_print(seats):
    for row in seats:
        print("".join(row))
    print()


def direct_neighbors(seats, x, y):
    kernel = seats[y-1][x-1:x+2]+[seats[y][x-1]]+[seats[y][x+1]]+seats[y+1][x-1:x+2]
    count = sum(1 for k in kernel if k == "#")
    return count


def line(x0, y0, dx, dy, max_x, max_y):
    x = x0
    y = y0
    while x < max_x and y < max_y and x > 0 and y > 0:
        y += dy
        x += dx
        yield x, y


def line_of_sight(seats, sx, sy):
    max_y = len(seats) - 1
    max_x = len(seats[0]) - 1
    count = 0
    for dx, dy in slopes:
        for x, y in line(sx, sy, dx, dy, max_x, max_y):
            seat = seats[y][x]
            if seat == "#":
                count += 1
                break
            elif seat == "L":
                break
    return count


def evolve(seats, max_occupied, kernel):
    new_seats = deepcopy(seats)
    max_y = len(seats)
    max_x = len(seats[0])
    for y in range(1, max_y-1):
        for x in range(1, max_x-1):
            seat = seats[y][x]
            count = kernel(seats, x, y)
            if seat == "L" and count == 0:
                new_seats[y][x] = "#"
            elif seat == "#" and count >= max_occupied:
                new_seats[y][x] = "L"
    simple_print(new_seats)
    return new_seats


def find_stable_configuration(seats, max_occupied, kernel, delay=0):
    old_seats = None
    while seats != old_seats:
        old_seats = seats
        seats = evolve(seats, max_occupied, kernel)
        sleep(delay)
    occupied = sum(1 for row in seats for s in row if s == "#")
    print(f"{occupied} seats are occupied")
    return occupied


if __name__ == "__main__":
    print("Example")
    seats = load_seats("data/day-11-example1.txt")
    simple_print(seats)
    result = find_stable_configuration(seats, 4, direct_neighbors)
    assert result == 37
    result = find_stable_configuration(seats, 5, line_of_sight)
    assert result == 26
    print("Reality")
    seats = load_seats("data/day-11.txt")
    result = find_stable_configuration(seats, 4, direct_neighbors, 0.25)
    assert result == 2251
    result = find_stable_configuration(seats, 5, line_of_sight, 0.25)
    assert result == 2019
