import sys
from itertools import product, count
import numpy as np

def build_seats(lines):
    seats = []
    for line in lines:
        seats.append(list(line.strip()))
    return np.array(seats)

def directions():
    return (
        (i, j)
        for i, j in product([-1, 0, 1], [-1, 0, 1])
        if not (i, j) == (0, 0)
    )

DIRECTIONS = list(directions())

def adjacents(grid, x, y):
    """
    >>> adjacents(np.arange(12).reshape(3, 4), 0, 0)
    [1, 4, 5]
    >>> adjacents(np.arange(12).reshape(3, 4), 2, 0)
    [1, 3, 5, 6, 7]
    >>> adjacents(np.arange(12).reshape(3, 4), 1, 1)
    [0, 1, 2, 4, 6, 8, 9, 10]
    """
    max_x, max_y = len(grid[0]), len(grid)
    indexes = sorted(
        [y + dy, x + dx]
        for dx, dy in DIRECTIONS
        if 0 <= y + dy < max_y and 0 <= x + dx < max_x
    )
    return [grid[j, i] for j, i in indexes]

def step(seats, occupied_counter, crowded_count):
    new_seats = np.full_like(seats, None)
    for j in range(len(seats)):
        for i in range(len(seats[0])):
            occupied_count = occupied_counter(seats, (i, j))
            if seats[j, i] == "L" and occupied_count == 0:
                new_seats[j, i] = "#"
            elif seats[j, i] == "#" and occupied_count >= crowded_count:
                new_seats[j, i] = "L"
            else:
                new_seats[j, i] = seats[j, i]
    return new_seats

def count_adjacent_occupied(seats, point):
    return [visible_seat(seats, point, d, depth=1) for d in DIRECTIONS].count("#")

def count_visible_occupied(seats, point):
    return [visible_seat(seats, point, d) for d in DIRECTIONS].count("#")

def visible_seat(seats, point, direction, depth=None):
    max_x, max_y = len(seats[0]), len(seats)
    x, y = point
    dx, dy = direction
    for i in count(1):
        if depth is not None and i > depth:
            return "."
        curr_y, curr_x = (i * dy) + y, (i * dx) + x
        if not (0 <= curr_y < max_y and 0 <= curr_x < max_x):
            return "."
        elif seats[curr_y, curr_x] != ".":
            return seats[curr_y, curr_x]

def stabilize(seats, occupied_counter, crowded_count):
    while True:
        new_seats = step(seats, occupied_counter, crowded_count)
        if np.all(new_seats == seats):
            break
        seats = new_seats
    return np.sum(seats == "#")

import doctest
doctest.testmod()

seats = build_seats(sys.stdin.readlines())

result = stabilize(seats, occupied_counter=count_adjacent_occupied, crowded_count=4)
print(result)

result = stabilize(seats, occupied_counter=count_visible_occupied, crowded_count=5)
print(result)
