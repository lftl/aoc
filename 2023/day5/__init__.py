"""
--- Day 5: If You Give A Seed A Fertilizer ---

You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed number:

    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
"""

spec = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

import common


def parse_map(lines):
    mapping = {}

    line = lines.pop(0)
    while line.strip():

        if ':' in line:
            line = lines.pop(0)
            continue

        dest_start, src_start, length = [int(x) for x in line.split()]
        map_range = range(src_start, src_start + length)
        mapping[map_range] = dest_start

        try:
            line = lines.pop(0)
        except IndexError:
            line = ''

    return mapping, lines

def find_intersection(test_range, mapping):
    matching = []
    for k, v in mapping.items():
        if test_range.start in k or test_range.stop in k or k.start in test_range:
            matching.append(k)
    matching.sort(key=lambda x: x.start)
    return matching

def combine_maps(mapping1, mapping2, collapse_unmapped=True):
    combined = {}
    for src_range, dest_start in mapping1.items():
        print(f"Mapping {src_range} to {dest_start}")
        mapped_range = range(dest_start, dest_start + len(src_range))
        breakpoints = find_intersection(mapped_range, mapping2)

        while len(mapped_range) > 0:
            new_end = find_next_end(breakpoints, mapped_range)
            new_value = find_value(mapping2, mapped_range.start)
            print(f"""
                Mapped Range: {mapped_range}
                Combined: {combined}
                Intersection: {breakpoints}
                M1: {mapping1} 
                M2: {mapping2}
                New End: {new_end}
                Source Range: {src_range}
                """)

            if len(breakpoints) > 0 and new_end == breakpoints[0].stop:
                print("pop", breakpoints.pop(0))

            comb_start = src_range.start + (mapped_range.start - dest_start)
            comb_end = comb_start + new_end - mapped_range.start
            if(comb_start > comb_end):
                print(f"""
                      Error bad range
                      Source Range: {src_range}
                      Mapped Range: {mapped_range}
                      New End: {new_end}
                      Dest Start: {dest_start}
                      Comb Start: {comb_start}
                      Comb End: {comb_end}
                      """)
                break
            combined[range(comb_start, comb_end)] = new_value
            mapped_range = range(new_end, mapped_range.stop)

    if collapse_unmapped:
        for k, v in mapping2.items():
            breakpoints = find_intersection(k, combined)
            print(k, breakpoints)

            range_to_map = k

            while len(range_to_map) > 0:
                if len(breakpoints) == 0:
                    combined[range_to_map] = v
                    range_to_map = range(0)
                elif range_to_map.start in breakpoints[0]:
                    range_to_map = range(breakpoints[0].stop, range_to_map.stop)
                    breakpoints.pop(0)
                else:
                    new_end = min(range_to_map.stop, breakpoints[0].start)
                    print("Combining: ",range_to_map, new_end, breakpoints[0])
                    if range_to_map.start > new_end:
                        print("Error")
                        break
                    combined[range(range_to_map.start, new_end)] = v
                    range_to_map = range(new_end, range_to_map.stop)

        """
        while len(dest_range) > 0:
            print(f""
                  Range to map: {map1_range}
                  Combined: {combined}
                  Intersection: {dest_ranges}
                  M1: {mapping1} 
                  M2: {mapping2}
                "")
            new_dest_range, dest_ranges = map_range(mapping2, combined, dest_ranges, dest_range, map1_range.start)
            if new_dest_range == dest_range:
                print("Error")
                break
            dest_range = new_dest_range
        """

    return combined

def find_next_end(breakpoints, dest_range):
    if len(breakpoints) == 0:
        return dest_range.stop
    if dest_range.start not in breakpoints[0]:
        return min(dest_range.stop, breakpoints[0].start)
    else:
        return min(dest_range.stop, breakpoints[0].stop)

def map_range(mapping2, combined, dest_ranges, dest_range, offset):
    new_range = None
    new_start = dest_range.start
    if len(dest_ranges) == 0:
        combined[range(dest_range.start+offset, dest_range.stop+offset)] = new_start
        new_range = range(0)
    elif dest_range.start not in dest_ranges[0]:
        new_end = min(dest_range.stop, dest_ranges[0].start)
        combined[range(new_start+offset, new_end+offset)] = new_start
        new_range = range(new_end, dest_range.stop)
    else:
        new_end = min(dest_range.stop, dest_ranges[0].stop)
        combined[range(new_start+offset, new_end+offset)] = mapping2[dest_ranges[0]]
        new_range = range(new_end, dest_range.stop)
        if new_end == dest_ranges[0].stop:
            dest_ranges.pop(0)

    return new_range, dest_ranges

def find_value(mapping, key):
    for k, v in mapping.items():
        if key in k:
            return v + (key - k.start)
    return key

def build_map(lines):
    out = []
    lines = lines[2:]
    while len(lines) > 0:
        mapping, lines = parse_map(lines)
        out.append(mapping)

    return out

def find_seed_location(seed, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location):
    soil = find_value(seed_to_soil, seed)
    fertilizer = find_value(soil_to_fertilizer, soil)
    water = find_value(fertilizer_to_water, fertilizer)
    light = find_value(water_to_light, water)
    temperature = find_value(light_to_temperature, light)
    humidity = find_value(temperature_to_humidity, temperature)
    location = find_value(humidity_to_location, humidity)
    return location

def solve(inp=None):

    if inp is None:
        inp = common.load_input(5)
    inp = inp.splitlines()

    # Parse the input
    seeds = [int(x) for x in inp[0].split()[1:]]

    maps = build_map(inp)
    combined_map = maps.pop(0)

    while len(maps) > 0:
        combined_map = combine_maps(combined_map, maps.pop(0))

    # Find the lowest location number that corresponds to any of the initial seed numbers
    lowest_location = None
    for seed in seeds:
        location = find_value(combined_map, seed)
        if lowest_location is None or location < lowest_location:
            lowest_location = location

    return lowest_location

"""
--- Part Two ---

Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""

def solve2(inp=None):

    if inp is None:
        inp = common.load_input(5)
    inp = inp.splitlines()

    seeds = [int(x) for x in inp[0].split()[1:]]
    # Group the seeds into pairs of start, length
    seeds = list(zip(seeds[::2], seeds[1::2]))
    # Map each list to a range
    seeds = {range(x[0], x[0] + x[1]): x[0] for x in seeds}

    maps = build_map(inp)
    combined_map = seeds

    while len(maps) > 0:
        combined_map = combine_maps(combined_map, maps.pop(0), False)

    return min(combined_map.values())  