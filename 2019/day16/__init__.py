import common

def pt1(signal, target_phase=100):
    phase = 0
    pattern = [0, 1, 0, -1]

    while phase < target_phase:
        step = 0
        output = ''
        while step < len(signal):
            full_pattern = []
            for p in pattern:
                full_pattern.extend([p]*(step+1))

            total = 0
            i = 0
            # print(full_pattern)
            while i < len(signal):
                pattern_idx = (i + 1) % len(full_pattern)
                val = int(signal[i]) * full_pattern[pattern_idx]
                print(f"{int(signal[i])} * {full_pattern[pattern_idx]}", end='   +   ')
                total += val
                i += 1

            output += str(total)[-1:]
            print(' = total', output)
            step += 1

        print(output)
        signal = output
        phase += 1

    return output

def main(session=None):

    raw = common.load_input(16, session).strip()
    # raw = '03036732577212944063491565474664'
    phase = 0
    target_phase = 100 

    offset = int(raw[0:7])
    signal = raw * 10000

    # signal = '12345678'
    # offset = 0
    # target_phase = 5

    signal = signal[offset:]

    if offset < (len(signal) / 2):
        print("Cannot use offset trick")
        return

    previous = 0

    while phase < target_phase:
        step = 0
        previous = 0
        output = ''
        while step < len(signal):
            previous = (previous + int(signal[-1*(step+1)])) % 10
            output += str(previous)
            step += 1

        signal = output[::-1]
        print(phase)
        phase += 1

    return signal[0:8]
