import sys
from itertools import count

def parse(lines):
    start_time = int(lines[0])
    buses = [(i, int(bus_interval)) for i, bus_interval in enumerate(lines[1].strip().split(",")) if not bus_interval == "x"]
    return start_time, buses

def smallest_multiple(x, lower):
    """
    Finds the smallest multiple of `x` that is greater than `lower`.

    >>> smallest_multiple(7, 10)
    14
    """
    return x * ((lower + x) // x)

def smallest_multiple_offset(x, y, lower, offset):
    """
    Finds the smallest multiple of `x` that is `offset` larger than a multiple of `y`
    """
    return next(i for i in count(start=lower, step=y) if (i + offset) % x == 0)

def wait_for_bus(start_time, interval):
    departure_time = smallest_multiple(interval, lower=start_time)
    return departure_time - start_time

def earliest_bus(buses):
    combined_interval, t = 1, 0
    for offset, interval in buses:
        t = smallest_multiple_offset(interval, combined_interval, t, offset)
        combined_interval *= interval
    return t

start_time, buses = parse(list(sys.stdin))

waiting_times = { bus_interval: wait_for_bus(start_time, bus_interval) for _, bus_interval in buses }
bus_id = min(waiting_times, key=waiting_times.get)
print(bus_id * waiting_times[bus_id])

result = earliest_bus(buses)
print(result)
