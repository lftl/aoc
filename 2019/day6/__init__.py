import common
from collections import defaultdict

class Node(object):
    parent = None
    children = None

    def orbit(node):
        self.parent = node
        node.children.append(self)

def walk(nodes, start, depth):

    if start not in nodes:
        print(f"{start} {depth}")
        return depth

    total = depth
    for node in nodes[start]:
        total += walk(nodes, node, depth+1)

    print(f"{start} {depth} {total}")
    return total


def parse(raw):
    nodes = defaultdict(list, {})

    for line in raw.splitlines():
        vals = line.split(')')
        nodes[vals[0]].append(vals[1])

    return nodes


def main(session=None):
    raw = common.load_input(6, session)
    nodes = parse(raw)

    return walk(nodes, 'COM', 0)

def parse2(raw):
    nodes = {}

    for line in raw.splitlines():
        vals = line.split(')')
        nodes[vals[1]] = vals[0]

    return nodes

class FoundException(Exception):
    pass

def search(orbit_map, orbiter_map, start, end, visited):

    next_targets = orbiter_map[start]

    if start != 'COM':
        next_targets.append(orbit_map[start])

    next_targets = [t for t in next_targets if t not in visited]

    new_paths = {}
    if end in next_targets:
        e = FoundException()
        e.path = [end]
        raise e

    for t in next_targets:
        visited.append(t)

    for target in next_targets:
        visited.append(target)
        try:
            search(orbit_map, orbiter_map, target, end, visited)
        except FoundException as p:
            e = FoundException()
            e.path = p.path + [target]
            raise e

def pt2(session=None, start='YOU'):
    raw = common.load_input(6, session)
    orbiter_map = parse(raw)
    orbit_map = parse2(raw)

    try:
        search(orbit_map, orbiter_map, 'YOU', 'SAN', ['YOU'])
    except FoundException as e:
        return e.path

