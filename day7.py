import sys
import re

def parse_line(line):
    """
    >>> parse_line('dotted black bags contain no other bags.')
    ('dotted black', {})
    >>> parse_line('bright white bags contain 1 shiny gold bag.')
    ('bright white', {'shiny gold': 1})
    >>> parse_line('muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.')
    ('muted yellow', {'shiny gold': 2, 'faded blue': 9})
    """
    key_string, val_string = line.split(" contain ")
    bag_color = key_string.removesuffix(" bags")

    if val_string.strip() == "no other bags.":
        return (bag_color, {})

    inner_matcher = re.compile("(?P<qty>\d+) (?P<color>[a-z]+ [a-z]+) bags?\.?")

    inner_bags = {}
    for s in val_string.split(","):
        group = inner_matcher.match(s.strip()).groupdict()
        inner_bags[group["color"]] = int(group["qty"])

    return (bag_color, inner_bags)

def can_hold(rules, bag_color, target_color):
    if bag_color not in rules.keys():
        return False
    if target_color in rules[bag_color].keys():
        return True
    return any(can_hold(rules, bc, target_color) for bc in rules[bag_color].keys())

def inner_bag_count(rules, bag_color):
    if not rules[bag_color]:
        return 0
    else:
        return sum(
            count * (1 + inner_bag_count(rules, bc))
            for bc, count in rules[bag_color].items()
        )


import doctest
doctest.testmod()

rules = dict(parse_line(line) for line in sys.stdin)

import time

start = time.time()
result = sum(can_hold(rules, bc, "shiny gold") for bc in rules.keys())
duration = time.time() - start
print(f"{result = }, {duration = }")

start = time.time()
result = inner_bag_count(rules, "shiny gold")
duration = time.time() - start
print(f"{result = }, {duration = }")
