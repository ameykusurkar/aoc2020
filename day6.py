import sys
from functools import reduce

def parse(string):
    """
    Parses a string representing a group response.

    >>> parse("ab\\nac\\na\\n")
    [{'a', 'b'}, {'a', 'c'}, {'a'}]
    """
    return list(set(s) for s in string.strip().split())

def any_has_answered(group):
    return set.union(*group)

def all_have_answered(group):
    return set.intersection(*group)
    
raw = sys.stdin.read()
groups = [parse(g) for g in raw.split("\n\n")]

result = sum(len(any_has_answered(g)) for g in groups)
print(result)

result = sum(len(all_have_answered(g)) for g in groups)
print(result)
