import concurrent.futures
import re

from functions import read_lines_from_file

PART = 2

MAPS = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
]


def merge_ranges(ranges):
    ranges.sort()  # Sort the ranges based on the start value
    merged_ranges = [ranges[0]]

    for start, end in ranges[1:]:
        last_start, last_end = merged_ranges[-1]

        if (
            start <= last_end or last_end + 1 == start
        ):  # Check for overlap/consecutive numbers
            merged_ranges[-1] = (last_start, max(end, last_end))
        else:
            merged_ranges.append((start, end))

    return merged_ranges


def process_seed(seed, map_dic):
    for mp in MAPS:
        for mp_tmp in map_dic[mp]:
            if mp_tmp[0] <= seed <= mp_tmp[1]:
                seed += mp_tmp[2]
                break
    return seed


def process_seed_ranges(seed_ranges, map_dic):
    for mp in MAPS:
        new_seed_ranges = []

        map_ranges_iterator = iter(map_dic[mp])
        current_map_range = next(map_ranges_iterator)
        mp_a, mp_b, offset = (
            current_map_range[0],
            current_map_range[1],
            current_map_range[2],
        )

        seed_range_iterator = iter(seed_ranges)
        current_seed_range = next(seed_range_iterator)
        seed_a, seed_b = current_seed_range[0], current_seed_range[1]

        stop_loop = False
        while True:
            # print(f"Seed A:{seed_a} | Seed B:{seed_b} | Map A:{mp_a} | Map B:{mp_b}")

            while seed_a > mp_b:  # 6
                try:
                    current_map_range = next(map_ranges_iterator)
                    mp_a, mp_b, offset = (
                        current_map_range[0],
                        current_map_range[1],
                        current_map_range[2],
                    )
                except:  # All maps passed
                    new_seed_ranges.extend([current_seed_range, *seed_range_iterator])
                    stop_loop = True
                    break

            while seed_b < mp_a:  # 1
                new_seed_ranges.extend([current_seed_range])
                try:
                    current_seed_range = next(seed_range_iterator)
                    seed_a, seed_b = current_seed_range[0], current_seed_range[1]
                except:  # All seeds passed
                    stop_loop = True
                    break

            if stop_loop:
                break

            if seed_a >= mp_a:
                if seed_b <= mp_b:
                    new_seed_ranges.extend([(seed_a + offset, seed_b + offset)])
                    try:
                        current_seed_range = next(seed_range_iterator)
                        seed_a, seed_b = current_seed_range[0], current_seed_range[1]
                    except:  # All seeds passed
                        break

                elif seed_b > mp_b:
                    new_seed_ranges.extend([(seed_a + offset, mp_b + offset)])
                    seed_a = mp_b + 1

            elif seed_a < mp_a:
                if mp_a <= seed_b <= mp_b:
                    new_seed_ranges.extend(
                        [(seed_a, mp_a - 1), (mp_a + offset, seed_b + offset)]
                    )
                    try:
                        current_seed_range = next(seed_range_iterator)
                        seed_a, seed_b = current_seed_range[0], current_seed_range[1]
                    except:  # All seeds passed
                        break

                elif seed_b > mp_b:
                    new_seed_ranges.extend(
                        [(seed_a, mp_a - 1), (mp_a + offset, mp_b + offset)]
                    )
                    seed_a = mp_b + 1

        seed_ranges = merge_ranges(new_seed_ranges)

    return seed_ranges


def get_lowest_location(lines, part=1):
    # Get seeds
    seeds = [int(s) for s in re.findall(r"\d+", lines[0])]

    if part == 2:
        seed_ranges = sorted(
            [(it1, it1 + it2 - 1) for it1, it2 in list(zip(seeds[::2], seeds[1::2]))],
            key=lambda x: x[0],
        )

    lines.pop(0)
    lines = [line.strip() for line in lines if line.strip()]

    index_dic = {}
    map_iter = iter(MAPS)
    current_map = next(map_iter)
    for idx, line in enumerate(lines):
        if current_map in line:
            index_dic[current_map] = idx
            try:
                current_map = next(map_iter)
            except:
                break  # All indices found

    map_dic = {mp: [] for mp in MAPS}

    index_iter = iter(index_dic.items())
    start_key, start_value = next(index_iter)
    futur_key, futur_value = start_key, start_value

    for idx, line in enumerate(lines, start=start_value):
        if idx == futur_value:
            current_key = futur_key
            try:
                futur_key, futur_value = next(index_iter)
            except:
                continue  # last map
            continue

        matches = re.search(r"(\d+) (\d+) (\d+)", line)
        dst, src, rng = (
            int(matches.group(1)),
            int(matches.group(2)),
            int(matches.group(3)),
        )
        # Start-source, end-source, offset-to-start-source
        map_dic[current_key].append([src, src + rng - 1, dst - src])

    # Sort map dic (important for PART 2)
    for mp in MAPS:
        map_dic[mp] = sorted(map_dic[mp], key=lambda x: x[0])

    seed_list = []

    if part == 1:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            seed_list = list(executor.map(process_seed, seeds, [map_dic] * len(seeds)))
            return min(seed_list)

    elif part == 2:
        seed_ranges = process_seed_ranges(seed_ranges, map_dic)
        return min(seed_ranges, key=lambda x: x[0])[0]


if __name__ == "__main__":
    file_path = "inputs/5_0.txt"
    lines_list = read_lines_from_file(file_path)

    min_loc = get_lowest_location(lines_list, part=PART)
    print(min_loc)
