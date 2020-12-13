import sys
from day1 import findn

def not_sum_of_prev(nums, lookback):
    """
    Finds numbers in `nums` which are not a sum of two numbers from
    the previous `lookback` numbers before it. The first `lookback`
    numbers in the list are ignored for the check.
    """
    for i, n in enumerate(numbers[lookback:]):
        lookback_nums = numbers[i:i+lookback] 
        if not findn(set(lookback_nums), n, 2):
            yield n

def find_contiguous(nums, target, min_length=2):
    """
    Finds a set of contiguous numbers in `nums` that sum to `target`.
    Only works if `nums` only contains positive numbers.

    >>> find_contiguous([1, 2, 8, 2, 5, 1, 7], 8)
    [2, 5, 1]
    """
    start, end = 0, min_length
    total = sum(nums[start:end])

    while not total == target:
        if nums[end] > target - total:
            total -= nums[start]
            start += 1
            if end - start < min_length:
                total += nums[end]
                end += 1
        else:
            total += nums[end]
            end += 1
    return nums[start:end]

import doctest
doctest.testmod()

numbers = [int(line) for line in sys.stdin]

target = next(not_sum_of_prev(numbers, lookback=25))
print(f"{target = }")

weakness_range = find_contiguous(numbers, target)
encryption_weakness = min(weakness_range) + max(weakness_range)
print(f"{encryption_weakness = }")
