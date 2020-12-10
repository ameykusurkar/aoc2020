import sys
import re
from collections import Counter
from functools import reduce
from operator import mul

product = lambda xs: reduce(mul, xs)

def combinations(diffs):
    """
    Finds the number of valid adapter combinations.

    `diffs` is a list of differences between the value of adjacent adapters,
    where the diff can either be 1 or 3. Since the difference between adjacent
    adapters can be at most 3, we only really have a choice when there are a series
    of consecutive 1s, where some can be omitted to still form a valid sequence.
    """
    return product(
        consecutive_ones_count(len(ones))
        for ones in re.compile("3+").split("".join(str(i) for i in diffs))
        if not ones == ""
    )

def consecutive_ones_count(num_ones):
    """
    Given we have a sub-sequence of `num_ones` 1s in a list of adjacent adapter diffs,
    finds the number of valid combinations for that sub-sequence.
    """
    return sum(
        not (bin(n).endswith("0") or "000" in bin(n)[2:].rjust(num_ones, "0"))
        for n in range(2**num_ones)
    )

adapters = sorted(int(line) for line in sys.stdin)
chain = [0] + adapters + [adapters[-1] + 3]

diffs = [r - l for l, r in zip(chain, chain[1:])]
diff_counts = Counter(diffs)

print(diff_counts[1] * diff_counts[3])
print(combinations(diffs))
