import common


moons = [
    [ -2, 9, -5 ],
    [ 16, 19, 9 ],
    [ 0, 3, 6 ],
    [ 11, 0, 11 ],
]

velocities = [
    [ 0, 0, 0 ],
    [ 0, 0, 0 ],
    [ 0, 0, 0 ],
    [ 0, 0, 0 ]
]

def comp(a, b):
    if a < b:
        return -1
    if a > b:
        return 1

    return 0


def total_energy(moon, velocity):
    pe = sum((abs(x) for x in moon))
    ke = sum((abs(x) for x in velocity))
    return  pe * ke

def step(moons, velocities):

    for k, moon in enumerate(moons):
        dx = sum((comp(m[0], moon[0]) for m in moons))
        dy = sum((comp(m[1], moon[1]) for m in moons))
        dz = sum((comp(m[2], moon[2]) for m in moons))

        velocities[k][0] += dx
        velocities[k][1] += dy
        velocities[k][2] += dz

    for k, moon in enumerate(moons):
        moon[0] += velocities[k][0]
        moon[1] += velocities[k][1]
        moon[2] += velocities[k][2]

    return (moons, velocities)

def main(session=None):
    cur_step = 0
    states = set()
    while True:
        step(moons, velocities)
        state = (
            moons[0][2],
            moons[1][2],
            moons[2][2],
            moons[3][2],
            velocities[0][2],
            velocities[1][2],
            velocities[2][2],
            velocities[3][2]
        )

        if state in states:
            return print(cur_step, state)

        cur_step += 1
        states.add(state)
        if cur_step % 10000 == 0:
            print(cur_step)

    return raw
