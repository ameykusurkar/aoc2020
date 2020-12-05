import sys

def binary_parse(string, zero):
    """
    Interprets `string` as a binary number, where the char `zero`
    represents 0, anything else being a 1.

    >>> binary_parse("BBFFBBF", zero="F")
    102
    """
    return sum(
        (1 << i) * (not c == zero)
        for i, c in enumerate(reversed(string))
    )

def seat_id(string):
    """
    >>> seat_id("BBFFBBFRLL")
    820
    """
    row = binary_parse(string[:7], zero="F")
    col = binary_parse(string[-3:], zero="L")
    return row * 8 + col

def find_gap(ints):
    """
    Given a sorted list, finds the first missing number in the sequence.

    >>> find_gap([1, 2, 3, 5])
    4
    """
    # Compare adjacent ints: if the difference is more than 1,
    # then a number is missing.
    return next(l + 1 for l, r in zip(ints, ints[1:]) if r - l > 1)

lines = sys.stdin.readlines()
seat_ids = list(seat_id(s.strip()) for s in lines)

print(max(seat_ids))

print(find_gap(sorted(seat_ids)))
