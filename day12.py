import sys

def parse(lines):
    return [(line[0], int(line[1:])) for line in lines]

class Ship:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.vec = direction_to_vec(direction)

    def move(self, vec, dist):
        vx, vy = vec
        self.x += dist * vx
        self.y += dist * vy

    def rotate(self, deg):
        vx, vy = self.vec
        vx1 = cos(deg) * vx - sin(deg) * vy
        vy1 = sin(deg) * vx + cos(deg) * vy
        self.vec = (vx1, vy1)

    def execute(self, instruction):
        op, arg = instruction
        if op in ["N", "S", "E", "W"]:
            self.move(direction_to_vec(op), arg)
        if op == "F":
            self.move(self.vec, arg)
        if op == "L":
            self.rotate(arg)
        if op == "R":
            self.rotate(-arg)

def direction_to_vec(direction):
    if direction == "N":
        return (0, 1)
    elif direction == "S":
        return (0, -1)
    elif direction == "E":
        return (1, 0)
    elif direction == "W":
        return (-1, 0)
    else:
        assert False

SIN = [0, 1, 0, -1]
def sin(deg):
    index = int((deg % 360) / 90)
    return SIN[index]

COS = [1, 0, -1, 0]
def cos(deg):
    index = int((deg % 360) / 90)
    return COS[index]

ship = Ship(0, 0, "E")

instructions = parse(sys.stdin)

for instr in instructions:
    ship.execute(instr)

print(abs(ship.x) + abs(ship.y))
