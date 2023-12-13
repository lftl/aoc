"""
With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789

In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7

This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?
"""

import common

spec = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

def split_row(row, y):
    left = row[:y]
    right = row[y:]

    print(left, right)
    if len(left) > len(right):
        left = left[-1*len(right):]
    elif len(right) > len(left):
        right = right[:len(left)]

    return left, right

def check_row_reflection(row, y):
    left, right = split_row(row, y)
    if left == right[::-1]:
        return True

    return False

def count_mismatches(row, y):
    left, right = split_row(row, y)
    mismatches = 0
    for idx, char in enumerate(left):
        if char != right[::-1][idx]:
            mismatches += 1

    return mismatches

def parse (data):
    patterns = []
    current_pattern = []
    for row in data:
        if row == '':
            patterns.append(current_pattern)
            current_pattern = []
        else:
            current_pattern.append(row)

    if current_pattern:
        patterns.append(current_pattern)

    return patterns

def solve(data=None):
    if data is None:
        data = common.load_input(13)
    data = data.splitlines()

    patterns = parse(data)

    total = 0
    for data in patterns:
        for y in range(1, len(data[0])):
            reflects = True
            for row in data:
                if not check_row_reflection(row, y):
                    reflects = False
                    break

            if reflects:
                print(y)
                total += y


        transposed_data = []
        for idx in range(len(data[0])):
            new_row = [row[idx] for row in data]
            transposed_data.append(''.join(new_row))

        
        for y in range(1, len(transposed_data[0])):
            reflects = True
            for row in transposed_data:
                if not check_row_reflection(row, y):
                    reflects = False
                    break

            if reflects:
                print(y)
                total += (100 * y)

    return total

def solve2(data=None):
    if data is None:
        data = common.load_input(13)
    data = data.splitlines()

    patterns = parse(data)

    total = 0
    for data in patterns:
        for y in range(1, len(data[0])):
            mismatches = 0
            for row in data:
                mismatches += count_mismatches(row, y)
                if mismatches > 1:
                    break

            if mismatches == 1:
                print(y)
                total += y


        transposed_data = []
        for idx in range(len(data[0])):
            new_row = [row[idx] for row in data]
            transposed_data.append(''.join(new_row))

        
        for y in range(1, len(transposed_data[0])):
            mismatches = 0
            for row in transposed_data:
                mismatches += count_mismatches(row, y)
                if mismatches > 1:
                    break

            if mismatches == 1:
                print(y)
                total += (100 * y)

    return total