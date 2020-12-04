import sys
import re

required = { 'byr', 'hcl', 'pid', 'eyr', 'hgt', 'ecl', 'iyr' }
ecls = { "amb", "blu", "brn", "gry", "grn", "hzl", "oth" }

def parse(lines):
    """
    Returns a list of dicts, each dict being a passport
    """
    for passport in lines.split("\n\n"):
        yield dict(item.split(":") for item in passport.split())

def is_present(passport):
    return required.issubset(passport.keys())

def is_valid(passport):
    return all([
        1920 <= int(passport["byr"]) <= 2002,
        2010 <= int(passport["iyr"]) <= 2020,
        2020 <= int(passport["eyr"]) <= 2030,
        is_valid_height(passport["hgt"]),
        re.match("^#[0-9a-f]{6}$", passport["hcl"]),
        passport["ecl"] in ecls,
        re.match("^[0-9]{9}$", passport["pid"]),
    ])

def is_valid_height(field):
    height, units = field[:-2], field[-2:]
    return any([
        units == "cm" and 150 <= int(height) <= 193,
        units == "in" and 59 <= int(height) <= 76,
    ])

lines = sys.stdin.read()
passports = list(parse(lines))

result = sum(is_present(p) for p in passports)
print(result)

result = sum(is_present(p) and is_valid(p) for p in passports)
print(result)
