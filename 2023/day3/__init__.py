"""
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

import common

def is_part_number(char):
    return char.isdigit()

def get_adjacent_chars(engine, row, col):
    adjacent_chars = []
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i < len(engine) and 0 <= j < len(engine[i]):
                adjacent_chars.append(engine[i][j])
    return adjacent_chars

def is_symbol(char):
    return not char.isdigit() and char != '.'

def calculate_part_number_sum(engine):
    part_number_sum = 0
    for row in range(len(engine)):
        col = 0
        while col < len(engine[row]):
            char = engine[row][col]
            found_adjacent_symbol = False
            if is_part_number(char):
                part_number = char
                found_adjacent_symbol = any(is_symbol(adj_char) for adj_char in get_adjacent_chars(engine, row, col))

                col += 1
                while col < len(engine[row]) and is_part_number(engine[row][col]):
                    part_number += engine[row][col]
                    if not found_adjacent_symbol:
                        found_adjacent_symbol = any(is_symbol(adj_char) for adj_char in get_adjacent_chars(engine, row, col))
                    col += 1

                if found_adjacent_symbol:
                    part_number_sum += int(part_number)
            else:
                col += 1
    return part_number_sum

engine_schematic = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598.."
]

def solve(data=None):
    if not data:
        data = common.load_input(3)
        data = data.split("\n")

    return calculate_part_number_sum(data)

"""
--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""

def find_adjacent_part_numbers(engine, row, col):
    adjacent_part_numbers = []
    already_visited = set()
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if (i, j) in already_visited:
                continue
            already_visited.add((i, j))
            if 0 <= i < len(engine) and 0 <= j < len(engine[i]):
                if engine[i][j].isdigit():
                    # Scan backwards and then forward until the char is not a digit
                    part_number = engine[i][j]
                    k = j - 1
                    while k >= 0 and engine[i][k].isdigit():
                        part_number = engine[i][k] + part_number
                        already_visited.add((i, k))
                        k -= 1

                    k = j + 1
                    while k < len(engine[i]) and engine[i][k].isdigit():
                        part_number += engine[i][k]
                        already_visited.add((i, k))
                        k += 1

                    adjacent_part_numbers.append(part_number)

    return adjacent_part_numbers

def calculate_gear_ratio_sum(engine):
    gear_ratio_sum = 0
    for row in range(len(engine)):
        col = 0
        while col < len(engine[row]):
            char = engine[row][col]
            if char == '*':
                ratios = find_adjacent_part_numbers(engine, row, col)
                if len(ratios) == 2:
                    gear_ratio_sum += int(ratios[0]) * int(ratios[1])
                col += 1
            else:
                col += 1
    return gear_ratio_sum


def solve2(data=None):
    if not data:
        data = common.load_input(3)
        data = data.split("\n")

    return calculate_gear_ratio_sum(data)
