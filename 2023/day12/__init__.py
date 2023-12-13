"""
--- Day 12: Hot Springs ---

You finally reach the hot springs! You can see steam rising from secluded areas attached to the primary, ornate building.

As you turn to enter, the researcher stops you. "Wait - I thought you were looking for the hot springs, weren't you?" You indicate that this definitely looks like hot springs to you.

"Oh, sorry, common mistake! This is actually the onsen! The hot springs are next door."

You look in the direction the researcher is pointing and suddenly notice the massive metal helixes towering overhead. "This way!"

It only takes you a few more steps to reach the main gate of the massive fenced-off area containing the springs. You go through the gate and into a small administrative building.

"Hello! What brings you to the hot springs today? Sorry they're not very hot right now; we're having a lava shortage at the moment." You ask about the missing machine parts for Desert Island.

"Oh, all of Gear Island is currently offline! Nothing is being manufactured at the moment, not until we get more lava to heat our forges. And our springs. The springs aren't very springy unless they're hot!"

"Say, could you go up and see why the lava stopped flowing? The springs are too cold for normal operation, but we should be able to find one springy enough to launch you up there!"

There's just one problem - many of the springs have fallen into disrepair, so they're not actually sure which springs would even be safe to use! Worse yet, their condition records of which springs are damaged (your puzzle input) are also damaged! You'll need to help them repair the damaged records.

In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.

However, the engineer that produced the condition records also duplicated some of this information in a different format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in the order those groups appear in the row. This list always accounts for every damaged spring, and each number is the entire size of its contiguous group (that is, groups are always separated by at least one operational spring: #### would always be 4, never 2,2).

So, condition records with no unknown spring conditions might look like this:

#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1

However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?). For example:

???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1

Equipped with this information, it is your job to figure out how many different arrangements of operational and broken springs fit the given criteria in each row.

In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three broken springs (in that order) can appear in that row: the first three unknown springs must be broken, then operational, then broken (#.#), making the whole row #.#.###.

The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different arrangements. The last ? must always be broken (to satisfy the final contiguous group of three broken springs), and each ?? must hide exactly one of the two broken springs. (Neither ?? could be both broken springs or they would form a single contiguous group of two; if that were true, the numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are four possible arrangements of springs.

The last line is actually consistent with ten different arrangements! Because the first number is 3, the first and second ? must both be . (if either were #, the first number would have to be 4 or higher). However, the remaining run of unknown spring conditions have many different ways they could hold groups of two and one broken springs:

?###???????? 3,2,1
.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#

In this example, the number of possible arrangements for each row is:

    ???.### 1,1,3 - 1 arrangement
    .??..??...?##. 1,1,3 - 4 arrangements
    ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
    ????.#...#... 4,1,1 - 1 arrangement
    ????.######..#####. 1,6,5 - 4 arrangements
    ?###???????? 3,2,1 - 10 arrangements

Adding all of the possible arrangement counts together produces a total of 21 arrangements.

For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?
"""

from collections import defaultdict
import time
import common


spec = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def count_arrangements(row):
    # Split the row into springs and groups of damaged springs
    springs, groups = row.split()
    groups = list(map(int, groups.split(',')))

    possibilities = expand_springs([], '', springs, groups)

    count = 0
    for possibility in possibilities:
        if count_contiguous_groups(possibility) == groups:
            count += 1

    return count

def count_contiguous_groups(springs):
    groups = []
    count = 0
    for i, spring in enumerate(springs):
        if spring == '#':
            count += 1
        
        if count > 0:
            if i+1 >= len(springs):
                groups.append(count)
            elif springs[i + 1] == '.':
                groups.append(count)
                count = 0
    return groups


def expand_springs(possibilities, current_possibility, springs, groups, cull=True):
    if len(springs) == 0:
        possibilities.append(current_possibility)
        return possibilities

    char = springs[0]

    if cull:
        count = ''
        if char != '?':
            count = count_contiguous_groups(current_possibility + char)

        if char == '.':
            if count != groups[:len(count)]:
                return possibilities
        elif char == '#':
            if len(count) > len(groups):
                return possibilities
            if len(count) > 1:

                if count[:-1] != groups[:len(count)-1]:
                    return possibilities

                offset = 0
                while offset+1 < len(springs) and springs[offset+1] == '#':
                    offset += 1

                current_count = count[-1]

                if current_count + offset > groups[len(count)-1]:
                    return possibilities

        # print(current_possibility, springs, groups, count)

    if char == '?':
        possibilities = expand_springs(possibilities, current_possibility + '.', springs[1:], groups, cull)
        possibilities = expand_springs(possibilities, current_possibility + '#', springs[1:], groups, cull)
        return possibilities
    else:
        return expand_springs(possibilities, current_possibility + char, springs[1:], groups, cull)

def solve(data=None):
    if data is None:
        data = common.load_input(12)
    data = data.splitlines()

    total_arrangements = sum(count_arrangements(row) for row in data)
    return total_arrangements

def expand_group(group, singles, init_groups):
    expanded = defaultdict(int)
    for count, last_char_hash in group:
        num_in_group = group[(count, last_char_hash)]
        for count2 in singles:
            for single2 in singles[count2]:
                if not last_char_hash or single2[0] == '.' or len(count) == 0 or len(count2) == 0:
                    new_count = count + count2
                else:
                    new_count = count[:-1] + (count[-1] + count2[0],) + count2[1:]

                if single2[-1] == '#' and list(new_count[:-1]) == init_groups[0:len(new_count)-1]:
                    expanded[(tuple(new_count), single2[-1] == '#')] += num_in_group
                elif list(new_count) == init_groups[0:len(new_count)]:
                    expanded[(tuple(new_count), single2[-1] == '#')] += num_in_group

    return expanded


def solve2(data=None):
    if data is None:
        data = common.load_input(12)
    data = data.splitlines()

    total = 0
    i = 0
    for row in data:
        init_springs, init_groups = row.split()
        init_groups = list(map(int, init_groups.split(',')))
        full_groups = init_groups * 5
        terminators = defaultdict(list)
        springs = expand_springs([], '', init_springs, full_groups, cull=False)
        for spring in springs:
            count = tuple(count_contiguous_groups(spring))

            if len(count) > 0 and max(count) > max(full_groups):
                continue

            terminators[count].append(spring)

        singles = defaultdict(list)
        init = defaultdict(int)
        for count in terminators:
            for terminator in terminators[count]:
                single = terminator + '#'
                count2 = count_contiguous_groups(single)

                if len(count2) == 0 or max(count2) <= max(init_groups):
                    singles[tuple(count2)].append(single)

                if count2[:-1] == full_groups[0:len(count2)-1]:
                    init[(tuple(count2), True)] += 1

                single = terminator + '.'
                count2 = count_contiguous_groups(single)

                if len(count2) == 0 or max(count) <= max(init_groups):
                    singles[tuple(count2)].append(single)

                if count2 == full_groups[0:len(count2)]:
                    init[(tuple(count2), False)] += 1

        # return (terminators, singles, init)
        # 2x
        init = expand_group(init, singles, full_groups)
        # 3x
        init = expand_group(init, singles, full_groups)
        # 4x
        init = expand_group(init, singles, full_groups)

        for count in terminators:
            for terminator in terminators[count]:
                for count2, last_char_hash in init:
                    if not last_char_hash or terminator[0] == '.' or len(count) == 0 or len(count2) == 0:
                        new_count = count2 + count
                    else:
                        new_count = count2[:-1] + (count2[-1] + count[0],) + count[1:]

                    if list(new_count) == full_groups:
                        total += init[(count2, last_char_hash)]

        print(i, total)
        i += 1

    return total