#!/usr/bin/env python
from dataclasses import dataclass
import math
import numpy as np


@dataclass
class Instruction(object):
    direction: str
    value: int


def load_navigation_data(filename):
    with open(filename) as f:
        data = [Instruction(line[0], int(line[1:])) for line in f.readlines()]
        return data


@dataclass
class Nav(object):
    east: int
    north: int

    def move(self, direction, value):
        self.north += round(value * np.cos(np.deg2rad(direction)))
        self.east += round(value * np.sin(np.deg2rad(direction)))

    def move_waypoint(self, waypoint, value):
        self.north += waypoint.north * value
        self.east += waypoint.east * value


NORTH = 0
EAST = 90
SOUTH = 180
WEST = 270


def navigate(data):
    position = Nav(0, 0)
    orientation = EAST
    for d in data:
        if d.direction == "F":
            position.move(orientation, d.value)
        elif d.direction == "R":
            orientation += d.value
        elif d.direction == "L":
            orientation -= d.value
        elif d.direction == "N":
            position.move(NORTH, d.value)
        elif d.direction == "S":
            position.move(SOUTH, d.value)
        elif d.direction == "E":
            position.move(EAST, d.value)
        elif d.direction == "W":
            position.move(WEST, d.value)
    return position


def cart2pol(east, north):
    rho = np.sqrt(north**2 + east**2)
    phi = np.arctan2(east, north)
    return (rho, phi)


def pol2cart(rho, phi):
    north = rho * np.cos(phi)
    east = rho * np.sin(phi)
    return east, north


@dataclass
class Waypoint(object):
    east: int
    north: int

    def move(self, direction, value):
        east, north = pol2cart(value, np.deg2rad(direction))
        self.east += east
        self.north += north
    
    def rotate(self, direction):
        rho, phi = cart2pol(self.east, self.north)
        self.east, self.north = pol2cart(rho, np.deg2rad(direction) + phi)

    def rotate_without_numpy(self, direction):
        x, y = self.east, self.north
        radians = direction * math.pi / 180
        self.east = x * math.cos(radians) + y * math.sin(radians)
        self.north = -x * math.sin(radians) + y * math.cos(radians)

    def rotate_matrix(self, direction):
        radians = np.deg2rad(direction)
        c, s = np.cos(radians), np.sin(radians)
        j = np.matrix([[c, s], [-s, c]])
        m = np.dot(j, [self.east, self.north])
        self.east = float(m.T[0])
        self.north = float(m.T[1])
        

def navigate_waypoint(data):
    position = Nav(0, 0)
    waypoint = Waypoint(10, 1)
    for d in data:
        if d.direction == "F":
            position.move_waypoint(waypoint, d.value)
        elif d.direction == "R":
            waypoint.rotate(d.value)
        elif d.direction == "L":
            waypoint.rotate(-d.value)
        elif d.direction == "N":
            waypoint.move(NORTH, d.value)
        elif d.direction == "S":
            waypoint.move(SOUTH, d.value)
        elif d.direction == "E":
            waypoint.move(EAST, d.value)
        elif d.direction == "W":
            waypoint.move(WEST, d.value)
    return position


def manhattan_distance(nav):
    distance = round(abs(nav.north) + abs(nav.east))
    print(f"The distance is {distance}")
    return distance


if __name__ == "__main__":
    print("========== Example ========== ")
    data = load_navigation_data("data/day-12-example1.txt")
    result = navigate(data)
    assert result == Nav(17, -8)
    distance = manhattan_distance(result)
    assert distance == 25
    result = navigate_waypoint(data)
    distance = manhattan_distance(result)
    assert distance == 286
    print("==========  Reality ========== ")
    data = load_navigation_data("data/day-12.txt")
    result = navigate(data)
    distance = manhattan_distance(result)
    assert distance == 2847
    result = navigate_waypoint(data)
    distance = manhattan_distance(result)
    assert distance < 56587 # this was too high :-(
    assert distance == 29839
