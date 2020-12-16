import sys
from itertools import count

def play(numbers):
    turns = count(1)
    seen = {}
    last = None
    for n in numbers:
        t = next(turns)
        last = n
        record(seen, last, t)
        yield t, last

    for t in turns:
        if len(seen[last]) == 1:
            last = 0
        else:
            prev2, prev = seen[last][-2:]
            last = prev - prev2
        record(seen, last, t)
        yield t, last

def record(seen, n, t):
    if not n in seen:
        seen[n] = [t]
    else:
        seen[n].append(t)

numbers = [int(x) for x in sys.stdin.read().split(",")]


t, result = next((t, n) for t, n in play(numbers) if t == 2020)
print(result)

# TODO: Try to make this more efficient
t, result = next((t, n) for t, n in play(numbers) if t == 30000000)
print(result)
