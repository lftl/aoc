import common
import day5
from collections import defaultdict


def print_output(output):

    for code in output:
        print(chr(code), end='')


def output_to_map(output):
    scaffold_map = {}
    x = 0
    y = 0
    robot_pos = None
    for code in output:
        ascii_char = chr(code)
        if code == 10:
            y += 1
            x = 0
        elif ascii_char == '^':
            robot_pos = (x, y)
            scaffold_map[(x, y)] = '#'
            x += 1
        else:
            scaffold_map[(x, y)] = ascii_char
            x += 1

    return (scaffold_map, robot_pos)

def stepstr_to_ascii(stepstr):
    output = list(map(ord, stepstr))
    output.append(10)
    return output


def walk_scaffold(smap, pos, cur_dir=(0, -1), steps=None):
    if steps is None:
        steps = []

    next_pt = common.vector_add(pos, cur_dir)
    prev_pt = None
    while smap.get(next_pt, False) == '#':
        steps[-1] += 1
        prev_pt = pos
        pos = next_pt
        next_pt = common.vector_add(pos, cur_dir)

    adjacents = common.get_adjacents(pos)
    try:
        next_pt = next((pt for pt in adjacents if smap.get(pt, False) == '#' and pt != prev_pt))
    except StopIteration:
        return (steps, pos)
    next_dir = common.vector_sub(next_pt, pos)

    if next_dir == (cur_dir[1] * -1, cur_dir[0]):
        steps.append('R')
    else:
        steps.append('L')

    steps.append(0)

    return walk_scaffold(smap, pos, next_dir, steps)

def calculate_substrings(steps):
    subcount = defaultdict(int, {})

    for x in range(len(steps)):
        if x % 2 == 1:
            continue
        for y in range(len(steps)-x):
            if y % 2 == 0:
                continue
            substr = ','.join(map(str, steps[x:(len(steps)-y-1)]))
            subcount[substr] += 1

    trimmed_count = {}
    for k in subcount:
        if len(k) <= 20:
            trimmed_count[k] = subcount[k]

    return trimmed_count


def main(session=None):
    raw = common.load_input(17, session)
    cmd = day5.parse(raw)

    result = day5.run(cmd)
    (smap, robot_pos) = output_to_map(result[0])

    total_alignment = 0
    for pt in smap:
        if smap[pt] != '#':
            continue

        adjacents = common.get_adjacents(pt)
        adj_scaffold_count = sum((1 for adj in adjacents if smap.get(adj, False) == '#'))
        if adj_scaffold_count == 4:
            total_alignment += pt[0] * pt[1]

    return total_alignment
