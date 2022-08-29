import common
from copy import copy
from defaultlist import defaultlist

def parse(inp):
    return list(map(int, inp.strip().split(',')))


def find_type(output, code):
    types = [x for k, x in enumerate(output) if (k+1) % 3 == 0]
    try:
        idx = types.index(code)
    except ValueError:
        return False
    full_idx = ((idx+1)*3)-1
    return output[full_idx-2:full_idx]


def run(cmd, inputs=None, pointer=0, relative_base=0):

    last_paddle = False
    last_ball = [0, 0]

    if inputs is None:
        inputs = []
    else:
        inputs = copy(inputs)

    outputs = []

    lines = defaultlist(lambda: 0)
    lines.extend(copy(cmd))
    p1 = 0
    p2 = 0
    p3 = 0

    while True:
        opcode = str(lines[pointer]).zfill(5)
        try:
            if opcode[2] == '0':
                p1 = lines[lines[pointer+1]]
            elif opcode[2] == '1':
                p1 = lines[pointer+1]
            else:
                p1 = lines[lines[pointer+1]+relative_base]
        except IndexError:
            pass
        try:
            if opcode[1] == '0':
                p2 = lines[lines[pointer+2]]
            elif opcode[1] == '1':
                p2 = lines[pointer+2]
            else:
                p2 = lines[lines[pointer+2]+relative_base]
        except IndexError:
            pass
        try:
            if opcode[0] == '2':
                p3 = lines[pointer+3]+relative_base
            else:
                p3 = lines[pointer+3]

        except IndexError:
            pass

        # print(opcode, lines[pointer+1], lines[pointer+2], lines[pointer+3])
        # max_len = max(p1,p2,p3)
        # if len(lines) < max_len:
        #     additional = (max_len - len(lines)) * [0]
        #    lines.extend(additional)


        cmd = opcode[3:]

        if cmd == '01':
            lines[p3] = p1 + p2
            pointer += 4
        elif cmd == '02':
            lines[p3] = p1 * p2
            pointer += 4
        elif cmd == '03':
            # print(f"Input at {pointer} {opcode}")
            # ball = find_type(outputs, 4)
            # paddle = find_type(outputs, 3)
            # if paddle is False:
            #     paddle = last_paddle
            # else:
            #     last_paddle = paddle
            # print(f"Ball {ball} {ball[0]-last_ball[0]}")
            # print(f"Paddle {paddle}")
            # ball_next_x = ball[0] + (ball[0]-last_ball[0])
            # ball_next_y = ball[1] + (ball[1]-last_ball[1])
            # last_ball = ball
            # outputs = []
            # if paddle[0] == ball[0]:
            #     move = 0
            # elif ball_next_x > paddle[0] and paddle[0] < 40:
            #     move = 1
            # elif ball_next_x < paddle[0] or paddle[0] > 0:
            #     move = -1
            # else:
            #    move = 0

            # inputs = [move]
            if len(inputs) == 0:
                # return (outputs, lines, pointer, relative_base)
                val = int(input("Please input a value: "))
            else:
                val = int(inputs.pop(0))
            if opcode[2] == '2':
                lines[lines[pointer+1]+relative_base] = val
            else:
                lines[lines[pointer+1]] = val
            print(val)
            pointer += 2
        elif cmd == '04':
            if opcode[2] == '0':
                val = lines[lines[pointer+1]]
            elif opcode[2] == '1':
                val = lines[pointer+1]
            else:
                val = lines[lines[pointer+1]+relative_base]
            # print(f"Output at {pointer} {opcode} {val}")
            pointer += 2
            outputs.append(val)
            # return (val, lines, pointer, relative_base)
        elif cmd == '05':
            if p1 != 0:
                pointer = p2
            else:
                pointer += 3
        elif cmd == '06':
            if p1 == 0:
                pointer = p2
            else:
                pointer += 3
        elif cmd == '07':
            if p1 < p2:
                lines[p3] = 1
            else:
                lines[p3] = 0
            pointer += 4
        elif cmd == '08':
            if p1 == p2:
                lines[p3] = 1
            else:
                lines[p3] = 0
            pointer += 4
        elif cmd == '09':
            relative_base += p1
            pointer += 2
        elif cmd == '99':
            print(f"Halt at {pointer} {opcode}")
            return (outputs, lines, pointer, relative_base)
        else:
            print(f"Error: {lines[pointer]} at {pointer}")
            return lines


def main(session, noun=10, verb=2):
    raw = common.load_input(5, session)
    lines = parse(raw)

    lines[1] = noun
    lines[2] = verb

    return run(lines)
