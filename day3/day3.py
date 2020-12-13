import sys
from functools import reduce
from operator import mul

def build_grid(lines):
    return [
        list(c == "#" for c in line.strip())
        for line in lines
    ]

def traverse(grid, move):
    move_x, move_y = move
    x = 0
    trees = 0
    width = len(grid[0])

    for y in range(0, len(grid), move_y):
        if grid[y][x]:
            trees += 1
        x = (x + move_x) % width
    return trees

product = lambda xs: reduce(mul, xs)

grid = build_grid(sys.stdin)

# problem 1
moves = [(3, 1)]
result = product(traverse(grid, move) for move in moves)
print(result)

# problem 2
moves = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
result = product(traverse(grid, move) for move in moves)
print(result)
