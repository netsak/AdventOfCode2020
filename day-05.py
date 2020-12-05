#!/usr/bin/env python
from functools import reduce

def get_boarding_passes(filename):
    """Load the passport file and returns all passports as objects"""
    with open(filename) as f:
        boarding_passes = [parse_boarding_pass(line.strip()) for line in f.readlines()]
        return boarding_passes

def decode(data, true_char):
    """Decode a binary string with special true char to decimal"""
    encode = lambda x: "1" if x == true_char else "0"
    binary = "".join(encode(x) for x in data)
    return int(binary, 2)

def parse_boarding_pass(boarding_pass):
    """Parses the boarding pass into (row, column, seat ID)"""
    row = decode(boarding_pass[:-3], "B")
    col = decode(boarding_pass[7:], "R")
    seat = row * 8 + col
    return (row, col, seat)

def find_max_boarding_pass(boarding_passes):
    """Find the maximum seat ID"""
    max_seat_id = max([b[2] for b in boarding_passes])
    print(f"Highest seat ID is {max_seat_id}")
    return max_seat_id

def find_missing_seats(boarding_passes):
    """Find empty seat in the middle of taken seats"""
    all_seats = {x for x in range(0, 128*8)}
    taken_seats = {b[2] for b in boarding_passes}
    free_seats = all_seats - taken_seats
    for seat in free_seats:
        if seat-1 in taken_seats and seat+1 in taken_seats:
            print(f"The ID of my seat is {seat}")
            return seat
    return None


if __name__ == "__main__":
    # example
    boarding_pass = parse_boarding_pass("FBFBBFFRLR")
    assert boarding_pass == (44, 5, 357)
    boarding_pass = parse_boarding_pass("BFFFBBFRRR")
    assert boarding_pass == (70, 7, 567)
    boarding_pass = parse_boarding_pass("FFFBBBFRRR")
    assert boarding_pass == (14, 7, 119)
    boarding_pass = parse_boarding_pass("BBFFBBFRLL")
    assert boarding_pass == (102, 4, 820)
    boarding_passes = get_boarding_passes("data/day-05-example1.txt")
    max_seat_id = find_max_boarding_pass(boarding_passes)
    assert max_seat_id == 820
    # # reality
    boarding_passes = get_boarding_passes("data/day-05.txt")
    max_seat_id = find_max_boarding_pass(boarding_passes)
    assert max_seat_id == 980
    my_seat = find_missing_seats(boarding_passes)
    assert my_seat == 607
