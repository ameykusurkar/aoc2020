import sys
from itertools import product, count
import numpy as np

class Seats:
    def __init__(self, grid):
        self.seats = grid

    @classmethod
    def from_lines(cls, lines):
        seats = []
        for line in lines:
            seats.append(list(line.strip()))
        return cls(np.array(seats))

    def stabilize(self, occupied_counter, crowded_count):
        while True:
            new_seats = step(self.seats, occupied_counter, crowded_count)
            if np.all(new_seats == self.seats):
                break
            self.seats = new_seats

    def occupied_count(self):
        return np.sum(self.seats == "#")

def step(seats, occupied_counter, crowded_count):
    new_seats = np.full_like(seats, None)
    for (j, i), seat in points(seats):
        occupied_count = occupied_counter(seats, (i, j))
        if seat == "L" and occupied_count == 0:
            new_seats[j, i] = "#"
        elif seat == "#" and occupied_count >= crowded_count:
            new_seats[j, i] = "L"
        else:
            new_seats[j, i] = seat
    return new_seats

def points(grid):
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            yield (j, i), grid[j, i]

def directions():
    return (
        (i, j)
        for i, j in product([-1, 0, 1], [-1, 0, 1])
        if not (i, j) == (0, 0)
    )

DIRECTIONS = list(directions())

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

lines = sys.stdin.readlines()

seats = Seats.from_lines(lines)
seats.stabilize(occupied_counter=count_adjacent_occupied, crowded_count=4)
print(seats.occupied_count())

seats = Seats.from_lines(lines)
seats.stabilize(occupied_counter=count_visible_occupied, crowded_count=5)
print(seats.occupied_count())
