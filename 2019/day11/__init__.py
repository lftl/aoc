import common
import day5

def main(session=None):
    raw = common.load_input(11, session)
    cmd = day5.parse(raw)

    halt = False
    pointer = 0
    relative_base = 0
    outputs = []

    position = (0, 0)
    direction = (0, 1)
    colors = {(0,0): 1}

    while not halt:
        if colors.get(position, 0) == 1:
            inputs = [1]
        else:
            inputs = [0]

        try:
            (output, cmd, pointer, relative_base) = day5.run(cmd, inputs, pointer, relative_base)
            if output > 1:
                return
        except ValueError:
            return (colors, position, direction)

        outputs.append(output)

        if len(outputs) % 2 == 0:
            colors[position] = outputs[-2]
            if outputs[-1] == 1:
                direction = (direction[1], -1*direction[0])
            else:
                direction = (-1*direction[1], direction[0])

            position = (position[0] + direction[0], position[1] + direction[1])

    return (colors, position, direction)
