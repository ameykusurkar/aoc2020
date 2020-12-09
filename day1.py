import sys

def findn(entries, target, n):
    """
    Finds `n` numbers in `entries` that sum to `target`
    """
    if n == 1:
        return (target,) if target in entries else None
    else:
        for e in entries:
            remaining = target - e
            remaining_entries = entries - {e}
            match = findn(remaining_entries, remaining, n - 1)
            if match:
                return (e, *match)

if __name__ == "__main__":
    entries = set(map(int, sys.stdin))

    a, b = findn(entries, 2020, 2)
    print(a * b)

    a, b, c = findn(entries, 2020, 3)
    print(a * b * c)
