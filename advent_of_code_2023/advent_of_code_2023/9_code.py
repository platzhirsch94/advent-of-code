import numpy as np
import re

from functions import read_lines_from_file

PART = 2


def find_history_1(matches):
    if all(val == 0 for val in matches):
        matches = np.append(matches, 0)
        return matches
    else:
        matches = np.append(matches, matches[-1] + find_history_1(np.diff(matches))[-1])
        return matches


def find_history_2(matches):
    if all(val == 0 for val in matches):
        matches = np.insert(matches, 0, 0)
        return matches
    else:
        matches = np.insert(
            matches, 0, matches[0] - find_history_2(np.diff(matches))[0]
        )
        return matches


if __name__ == "__main__":
    file_path = "inputs/9_0.txt"
    lines_list = read_lines_from_file(file_path)

    futures = []
    for line in lines_list:
        matches = np.array([int(i) for i in re.findall(r"(-?\d+)", line)])
        if PART == 1:
            futures.append(find_history_1(matches)[-1])
        else:
            futures.append(find_history_2(matches)[0])

    res = sum(futures)
    print(res)
