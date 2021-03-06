#!/usr/bin/env python
from collections import defaultdict


kernel = ( 
    (-1, -1, -1), (0, -1, -1), (1, -1, -1),    
    (-1,  0, -1), (0,  0, -1), (1,  0, -1),    
    (-1,  1, -1), (0,  1, -1), (1,  1, -1),    

    (-1, -1, 0),  (0, -1, 0),  (1, -1, 0),    
    (-1,  0, 0),               (1,  0, 0),    
    (-1,  1, 0),  (0,  1, 0),  (1,  1, 0),    

    (-1, -1, 1),  (0, -1, 1),  (1, -1, 1),    
    (-1,  0, 1),  (0,  0, 1),  (1,  0, 1),    
    (-1,  1, 1),  (0,  1, 1),  (1,  1, 1),    
)


def load_grid(filename):
    with open(filename) as f:
        grid = defaultdict(bool)
        xy_dim = 0
        for y, line in enumerate(f.readlines()):
            xy_dim = len(line)
            for x, c in enumerate(line.strip()):
                if c == "#":
                    grid[(x+1,y+1,0)] = True
        return grid, xy_dim


def print_grid(grid, xy_dim, z_dim):
    for z in range(-z_dim, z_dim+1):
        print(f"---------- z={z} ----------")
        for y in range(0, xy_dim+1):
            line = ["#" if grid[(x,y,z)] else "." for x in range(0, xy_dim)]
            print("".join(line))
    print()


def count_active(grid, xy_dim, z_dim):
    count = 0
    for z in range(-z_dim, z_dim+1):
        for y in range(0, xy_dim+1):
            line = [1 if grid[(x,y,z)] else 0 for x in range(0, xy_dim)]
            count += sum(line)
    return count


def cycle(grid, xy_dim, z_dim):
    new_grid = defaultdict(bool)
    for z in range(-z_dim, z_dim+1):
        for y in range(0, xy_dim+1):
            for x in range(0, xy_dim+1):
                neighbors = [1 if grid[(x+dx,y+dy,z+dz)] else 0 for dx, dy, dz in kernel]
                count = sum(neighbors)
                if grid[(x,y,z)]:
                    if 2 <= count <= 3:
                        new_grid[x+1,y+1,z] = True
                else:
                    if count == 3:
                        new_grid[x+1,y+1,z] = True
    return new_grid, xy_dim + 2, z_dim+1


def evolve(grid, xy_dim, cycles):
    z_dim = 1
    for i in range(cycles):
        print(f"cycle={i}")
        grid, xy_dim, z_dim = cycle(grid, xy_dim+1, z_dim)
        print_grid(grid, xy_dim, z_dim)
    count = count_active(grid, xy_dim, z_dim)
    print(f"{count} cubes are left in active state")
    return count


if __name__ == "__main__":
    print("======================================== Example ========================================")
    grid, xy_dim = load_grid("data/day-17-example1.txt")
    assert xy_dim == 3
    result = evolve(grid, xy_dim, 6)
    assert result == 112
    print("======================================== Reality ========================================")
    grid, xy_dim = load_grid("data/day-17.txt")
    assert xy_dim == 8
    result = evolve(grid, xy_dim, 6)
    assert result > 206
    assert result < 301
    assert result == 207
    
