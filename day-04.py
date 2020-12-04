#!/usr/bin/env python
from re import compile

token_regex = compile(r"(\w+):(\S+)")
color_regex = compile(r"^#[0-9a-fA-F]{6}$")
height_regex = compile(r"(?P<value>\d+)(?P<unit>cm|in)")
pid_regex = compile(r"^\d{9}$")

def get_passports(filename):
    """Load the passport file and returns all passports as objects"""
    with open(filename) as f:
        content = f.read().split("\n\n")
        passports = [dict(token_regex.findall(line)) for line in content]
        return passports

def simple_validator(passport):
    """Checks if a passport is valid (quick and dirty and wrong)"""
    if len(passport) == 8:
        return True
    if len(passport) == 7 and "cid" not in passport:
        return True
    return False

def complex_validator(passport):
    """Checks if a passport is valid according to a rule set"""
    if not 1920 <= int(passport.get("byr", 0)) <= 2002:
        return False
    if not 2010 <= int(passport.get("iyr", 0)) <= 2020:
        return False
    if not 2020 <= int(passport.get("eyr", 0)) <= 2030:
        return False
    if color_regex.fullmatch(passport.get("hcl", "")) is None:
        return False
    if not passport.get("ecl", "") in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False 
    m = height_regex.match(passport.get("hgt", ""))
    if m is None:
        return False 
    if m.group("unit") == "cm" and not 150 <= int(m.group("value")) <= 193:
        return False 
    if m.group("unit") == "in" and not 59 <= int(m.group("value")) <= 76:
        return False 
    if pid_regex.fullmatch(passport.get("pid", "")) is None:
        return False
    return True

def count_valid_passwords(passwords, validator):
    """Count all valid passwords"""
    count = len(list(filter(validator, passports)))
    print(f"Found {count} valid passwords")
    return count


if __name__ == "__main__":
    # example
    passports = get_passports("data/day-04-example.txt")
    assert len(passports) == 4
    valid_passports = count_valid_passwords(passports, simple_validator)
    assert valid_passports == 2
    passports = get_passports("data/day-04-example2.txt")
    valid_passports = count_valid_passwords(passports, complex_validator)
    assert valid_passports == 4
    # reality
    passports = get_passports("data/day-04.txt")
    assert len(passports) == 299
    valid_passports = count_valid_passwords(passports, simple_validator)
    assert valid_passports == 247
    valid_passports = count_valid_passwords(passports, complex_validator)
    assert valid_passports == 145
