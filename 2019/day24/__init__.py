import common
from copy import copy

def bug_counter(levels, depth, x, y):
    lines = levels[depth]
    bug_count = 0
    for adj in common.get_adjacents((x, y)):
        try:
            if adj[0] < 0:
                pt = levels[depth+1][2][1]
            elif adj[1] < 0:
                pt = levels[depth+1][1][2]
            elif adj[0] > 4:
                pt = levels[depth+1][2][3]
            elif adj[1] > 4:
                pt = levels[depth+1][3][2]
            elif adj == (2, 2):
                if y == 1 and x == 2:
                    pts = levels[depth-1][0]
                elif y == 2 and x == 1:
                    pts = [line[0] for line in levels[depth-1]]
                elif y == 2 and x == 3:
                    pts = [line[-1] for line in levels[depth-1]]
                elif y == 3 and x == 2:
                    pts = levels[depth-1][-1]

                bug_count += sum((1 for x in pts if x == '#'))

                continue
            else: 
                pt = lines[adj[1]][adj[0]]

            if pt == '#':
                bug_count += 1
        except IndexError:
            pass
    return bug_count

def next_minute(levels):
    levels = copy(levels)
    next_levels = []

    levels.insert(0, [['.'] * 5] * 5)
    levels.append([['.'] * 5] * 5)

    for depth, lines in enumerate(levels):
        out = []
        for y in range(5):
            new_line = []
            for x in range(5):
                cur_item = lines[y][x]
                bug_count = bug_counter(levels, depth, x, y)

                if y == 2 and x == 2:
                    new_line.append('?')
                elif cur_item == '#' and bug_count != 1:
                    new_line.append('.')
                elif cur_item == '.' and (bug_count == 1 or bug_count == 2):
                    new_line.append('#')
                else:
                    new_line.append(cur_item)

            out.append(new_line)

        next_levels.append(out)

    return next_levels

def next_minute_pt1(lines):
    out = []
    for y in range(5):
        new_line = []
        for x in range(5):
            bug_count = 0
            cur_item = lines[y][x]
            for adj in common.get_adjacents((x, y)):
                try:
                    if adj[1] < 0 or adj[0] < 0:
                        continue
                    if lines[adj[1]][adj[0]] == '#':
                        bug_count += 1
                except IndexError:
                    pass
            if cur_item == '#' and bug_count != 1:
                new_line.append('.')
            elif cur_item == '.' and (bug_count == 1 or bug_count == 2):
                new_line.append('#')
            else:
                new_line.append(cur_item)
        out.append(new_line)

    return out

def print_map(lines):
    for line in lines:
        print(''.join(line))

def lines_to_str(lines):
    return "\n".join(map(lambda x: ''.join(x), lines))


def parse(raw):
    lines = list(map(list, raw.splitlines()))
    return lines

def biodiversity(lines):
    val = 1
    out = 0
    for y in range(5):
        for x in range(5):
            if lines[y][x] == '#':
                out += val
            val = val * 2

    return out
            

def main(session=None):
    raw = common.load_input(24, session)
    lines = parse(raw)
    line_str = ''

    states = set()

    while line_str not in states:
        states.add(line_str)
        lines = next_minute(lines)
        line_str = lines_to_str(lines)

    return lines
