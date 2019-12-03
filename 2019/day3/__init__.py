import common
import shapely.geometry as geom

def move(point):
    if point[0] == 'R':
        return (int(point[1:]), 0)
    if point[0] == 'L':
        return (-1*int(point[1:]), 0)
    if point[0] == 'U':
        return (0, int(point[1:]))
    if point[0] == 'D':
        return (0, -1*int(point[1:]))

    print(f"Bad point: {point}")


def wire2multiline(wire):
    out = []
    cur = (0, 0)
    for pt in wire:
        movement = move(pt)
        nextPt = (cur[0]+movement[0], cur[1]+movement[1])
        out.append((cur, nextPt))
        cur = nextPt

    return geom.MultiLineString(out)

def wireLengthToPoint(wire, point):
    if point == geom.Point(0, 0):
        return 0

    length = 0
    for line in wire:
        if line.contains(point):
            subLine = geom.LineString((line.coords[0], point))
            length += subLine.length
            return length
        length += line.length

    print(f"Point not found {point.x} {point.y}")


def manhattan_distance(pt):
    return abs(pt.x) + abs(pt.y)


def wire_length_gen(wires):
    def combined_wire_length(pt):
        return sum([wireLengthToPoint(wire, pt) for wire in wires])
    return combined_wire_length

def main(session=None):
    raw = common.load_input(3, session)
    lines = raw.splitlines()
    wires = list(map(wire2multiline, [line.split(',') for line in lines]))

    intersections = wires[0].intersection(wires[1])
    distances = list(map(manhattan_distance, intersections))
    distances.sort()

    print (f"Part 1: {distances[1]}")

    distances2 = list(map(wire_length_gen(wires), intersections[1:]))
    distances2.sort()
    print (f"Part 2: {distances2[1]}")
