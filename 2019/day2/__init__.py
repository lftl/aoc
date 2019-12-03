import common
from copy import copy

def parse(inp):
    return list(map(int, inp.strip().split(',')))

def run(cmd):
    lines = copy(cmd)
    pointer = 0
    while True:
        if lines[pointer] == 1:
            print(f"Add at {pointer}")
            lines[lines[pointer+3]] = lines[lines[pointer+1]] + lines[lines[pointer+2]]
        elif lines[pointer] == 2:
            print(f"Mult at {pointer}")
            lines[lines[pointer+3]] = lines[lines[pointer+1]] * lines[lines[pointer+2]]
        elif lines[pointer] == 99:
            print(f"Halt at {pointer}")
            return lines
        else:
            print(f"Error: {lines[pointer]} at {pointer}")
            return lines

        pointer += 4

def main(session, noun=10, verb=2):
    raw = common.load_input(2, session)
    lines = parse(raw)

    lines[1] = noun
    lines[2] = verb

    return run(lines)
