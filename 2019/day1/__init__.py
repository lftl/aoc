import common
import math

def fuel(x):
    return math.floor(int(x)/3) - 2

def total_fuel(x):
    total = -1 * x 
    while x > 0:
        total += x
        x = fuel(x)

    return total

def total_fuel_recursive(x, total=0):
    additional = fuel(x)
    if additional > 0:
        return total_fuel_recursive(additional, additional+total)

    return total


def main(session):
    raw = common.load_input(1, session)
    lines = list(map(int, raw.splitlines()))

    part1 = sum(map(fuel, lines))
    part2 = sum(map(total_fuel_recursive, lines))

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
