import common
from collections import defaultdict
from math import inf, atan2, pi

def parse(raw):
    asteroids = []
    lines = raw.splitlines()
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            if col == '#':
                asteroids.append((x, y))

    return asteroids


def slope(one, two):

    try:
        return (one[0] - two[0]) / (one[1] - two[1])
    except ZeroDivisionError:
        if one[0] > two[0]:
            return inf
        else:
            return -inf

def direction(one, two):
    return (one[0] >= two[0], one[1] >= two[1])
        

def count_detectable(asteroid, asteroids):
    return len(calc_detectable(asteroid, asteroids))

def distance(one, two):
    return abs(one[0] - two[0]) + abs(one[1] - two[1])


def calc_detectable(asteroid, asteroids):
    viewed = []
    for viewable in asteroids:
        if viewable == asteroid:
            continue

        blocked = False
        for already_viewed in viewed:
            if (
                    slope(asteroid, viewable) == slope(asteroid, already_viewed)
                    and
                    direction(asteroid, viewable) == direction(asteroid, already_viewed)
                ):
                blocked = True
                break

        if not blocked:
            viewed.append(viewable)

    return viewed


"""           s = 0
              d = T, T
              |    
   d = T, T   |           d = F, T
   s = +1     |           s = -1
              |
s = Inf   ------------------------  s = -Inf
d = T, T      |                     d = F, T
              |
   d = T, F   |          d = F, F
   s = -1     |          s = + 1
              s = 0
              d = T, F
"""


def find_next_target(cur_slope, cur_quadrant, slope_map):

    """
    if cur_quadrant == (True, True):
        sort_func = max
        val_func = lambda x: x < cur_slope
    if cur_quadrant == (False, True):
        sort_func = min
        val_func = lambda x: x < cur_slope
    if cur_quadrant == (False, False):
        sort_func = max
        val_func = lambda x: x < cur_slope
    if cur_quadrant == (True, False):
        sort_func = max
        val_func = lambda x: x < cur_slope
    """

    try:
        next_slope = max([s for s in slope_map[cur_quadrant] if s < cur_slope])
        return (next_slope, cur_quadrant)
    except ValueError:
        if cur_quadrant == (True, True):
            return find_next_target(1, (False, True), slope_map)
        if cur_quadrant == (False, True):
            return find_next_target(inf, (False, False), slope_map)
        if cur_quadrant == (False, False):
            return find_next_target(1, (True, False), slope_map)
        if cur_quadrant == (True, False):
            if len(slope_map[(True, True)][inf]) > 0:
                print('ok1')
                return (inf, (True, True))
            else:
                print(slope_map[(True, True)])
                print('nok1')
                return find_next_target(inf, (True, True), slope_map)


def vaporize(origin, asteroids):
    vaporized = []
    slope_map = {}

    slope_map[(True, True)] = defaultdict(list, {})
    slope_map[(True, False)] = defaultdict(list, {})
    slope_map[(False, True)] = defaultdict(list, {})
    slope_map[(False, False)] = defaultdict(list, {})

    for asteroid in asteroids:
        if asteroid == origin:
            continue
        ast_slope = slope(origin, asteroid)
        quadrant = direction(origin, asteroid)
        slope_map[quadrant][ast_slope].append(asteroid)

    for quadrant in slope_map:
        for ast_slope in slope_map[quadrant]:
            slope_map[quadrant][ast_slope] = sorted(
                slope_map[quadrant][ast_slope],
                key=lambda x: distance(origin, x)
            )

    cur_slope = 0
    cur_quadrant = (True, True)

    if len(slope_map[cur_quadrant][cur_slope]) == 0:
        (cur_slope, cur_quadrant) = find_next_target(cur_slope, cur_quadrant, slope_map)

    while len(vaporized) < 201:
        try:
            asteroid = slope_map[cur_quadrant][cur_slope].pop(0)
        except IndexError:
            return (slope_map, cur_quadrant, cur_slope)
        vaporized.append(asteroid)

        if len(slope_map[cur_quadrant][cur_slope]) == 0:
            del slope_map[cur_quadrant][cur_slope]

        (cur_slope, cur_quadrant) = find_next_target(cur_slope, cur_quadrant, slope_map)

    return vaporized

def angle(origin, asteroid):
    return atan2(
        origin[1] - asteroid[1], 
        asteroid[0] - origin[0]
    ) / pi * 180

def calc_angle(v1, v2):
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    print(dot)
    det = v1[0]*v2[0] - v1[1]*v2[1]
    print(det)
    return atan2(det, dot)

def vaporize2(origin, asteroids):

    angle_map = defaultdict(list, {})
    vaporized = []

    for asteroid in asteroids:

        if asteroid == origin:
            continue

        angle_map[angle(origin, asteroid)].append(asteroid)


    for ang in angle_map:
        angle_map[ang] = sorted(
            angle_map[ang],
            key=lambda x: distance(origin, x)
        )

    angles = sorted(angle_map.keys())
    start = angles.index(90)

    while len(vaporized) < 201:

        cur_angle = angles[start]
        if len(angle_map[cur_angle]) > 0:
            vaporized.append(angle_map[cur_angle].pop(0))

        start -= 1
        if start < 0:
            start = len(angles) - 1

    return vaporized

def main(session=None):
    raw = common.load_input(10, session)

    asteroids = parse(raw)
    counts = {}

    for asteroid in asteroids:
        counts[asteroid] = calc_detectable(asteroid, asteroids)

    return counts
