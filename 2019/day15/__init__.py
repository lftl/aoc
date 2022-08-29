import common
import readchar
import day5
import os
from copy import copy

def get_adjacents(pt):
    return (
        (pt[0]+1, pt[1]),
        (pt[0]-1, pt[1]),
        (pt[0], pt[1]+1),
        (pt[0], pt[1]-1)
    )


def count_open(pt, space_map):
    num_open = 0
    for adj in get_adjacents(pt):
        if space_map.get(adj, False) == '.':
            num_open += 1

    return num_open


def print_map(space_map, bounds, cur_pos, last_output):
    os.system('clear') 
    for y in reversed(range(bounds[1]-1, bounds[3]+1)):
        print("")
        for x in range(bounds[0]-1, bounds[2]+1):
            if (x, y) == (0, 0):
                print('X', end='')
            elif (x, y) == cur_pos:
                print('\u001B[31mD\u001B[37m', end='')
            elif (x, y) in space_map:
                if space_map[(x,y)] == '.' and count_open((x,y), space_map) > 2:
                    print("\u001B[32m" + space_map[(x,y)] + "\u001B[37m", end='')
                else:
                    print(space_map[(x,y)], end='')
            else:
                print('?', end='')

    print('')
    print(cur_pos, bounds, last_output)

def main(session=None, space_map=None):
    raw = common.load_input(15, session)
    cmds = day5.parse(raw)

    if space_map is None:
        space_map = {}
    cur_pos = (0,0)
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    pointer = 0
    relative_base = 0

    while True:
        key = readchar.readkey()
        if key == '\x1b[A': # up inp = 1
            inp = 1
            next_pos = (cur_pos[0], cur_pos[1]+1)
        elif key == '\x1b[D': # left
            inp = 3
            next_pos = (cur_pos[0]-1, cur_pos[1])
        elif key == '\x1b[B': # down
            inp = 2
            next_pos = (cur_pos[0], cur_pos[1]-1)
        elif key == '\x1b[C': #right
            inp = 4
            next_pos = (cur_pos[0]+1, cur_pos[1])
        elif key == 'X':
            return (space_map, cur_pos)

        if next_pos[0] > max_x:
            max_x = next_pos[0]
        if next_pos[1] > max_y:
            max_y = next_pos[1]
        if next_pos[0] < min_x:
            min_x = next_pos[0]
        if next_pos[1] < min_y:
            min_y = next_pos[1]
        (outputs, cmds, pointer, relative_base) = day5.run(cmds, [inp], pointer, relative_base)

        if outputs[0] == 0:
            space_map[next_pos] = '#'
        if outputs[0] == 1:
            space_map[next_pos] = '.'
            cur_pos = next_pos
        if outputs[0] == 2:
            space_map[next_pos] = 'o'
            cur_pos = next_pos

        print_map(space_map, (min_x, min_y, max_x, max_y), cur_pos, outputs[0])

    return raw


def expand(source_map):
    t = 0
    out_map = copy(source_map)
    open_spots = 0

    for k in source_map.keys():
        if source_map[k] == 'o':
            origin = k
        if source_map[k] == '.':
            open_spots += 1

    air_spots = set([origin])
    while len(air_spots) < open_spots:
        new_airspots = set() 
        for pt in air_spots:
            for adj in get_adjacents(pt):
                if out_map.get(adj, False) == '.':
                    out_map[adj] = 'O'
                    new_airspots.add(adj)

        air_spots = air_spots.union(new_airspots)
        t += 1
        print_map(out_map, (-21, -19, 19, 21), (0, 0), [t, len(air_spots)])

    return (t, out_map)
