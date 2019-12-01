import common
import math

def fuel(x):
    return math.floor(int(x)/3) - 2

def total_fuel(x):
    sum = -1 * x 
    while x > 0:
        sum += x
        x = fuel(x)

    return sum


def main(session):
    raw = common.load_input(1, session)
    lines = map(int, raw.splitlines())

    part1 = 0
    part2 = 0
    for line in lines:
        part1 += fuel(line)
        part2 += total_fuel(line)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
