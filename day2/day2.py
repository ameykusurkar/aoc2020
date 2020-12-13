import sys

def parse(lines):
    for line in lines:
        rules, password = line.split(":")
        rnge, letter = rules.split()
        low, high = map(int, rnge.split("-"))
        yield (low, high, letter, password.strip())

# List because we will need to iterate over the data twice
parsed = list(parse(map(str.strip, sys.stdin)))

def part1(parsed):
    for low, high, letter, password in parsed:
        yield low <= password.count(letter) <= high

print(sum(part1(parsed)))

def part2(parsed):
    for low, high, letter, password in parsed:
        yield (password[low-1] == letter) ^ (password[high-1] == letter)

print(sum(part2(parsed)))
