from queue import Queue

import math
import numpy as np
import re

from functions import read_lines_from_file

MAPPER = {
    "S": {
        (0, 1): ["-", "J", "7"],
        (0, -1): ["-", "L", "F"],
        (-1, 0): ["|", "7", "F"],
        (1, 0): ["|", "L", "J"],
    },
    "F": {(0, 1): ["-", "7", "J"], (1, 0): ["|", "L", "J"]},
    "7": {(0, -1): ["-", "F", "L"], (1, 0): ["|", "J", "L"]},
    "L": {(0, 1): ["-", "J", "7"], (-1, 0): ["|", "F", "7"]},
    "J": {(0, -1): ["-", "L", "F"], (-1, 0): ["|", "7", "F"]},
    "-": {(0, 1): ["-", "J", "7"], (0, -1): ["-", "L", "F"]},
    "|": {(-1, 0): ["|", "F", "7"], (1, 0): ["|", "L", "J"]},
}

PART = 1


def find_element_position_numpy(matrix, element):
    indices = np.where(matrix == element)
    if len(indices[0]) > 0:
        return np.array([indices[0][0], indices[1][0]])
    else:
        return None


global counter_list
counter_list = []


def get_distance(lines):
    line_num = len(lines)
    line_width = len(lines[0]) - 1  # "\n"
    arr = np.array([[char for char in line.strip()] for line in lines]).reshape(
        line_num, line_width
    )

    S_pos = find_element_position_numpy(arr, "S")
    queue = Queue()
    queue.put((S_pos, "S", 0, (0, 0)))

    while not queue.empty():
        pos, val, counter, old_dir = queue.get()
        for dr, allowed in MAPPER[val].items():
            if tuple(-val for val in dr) == old_dir:
                continue
            elif np.any((new_pos := pos + dr) < 0):
                continue
            elif (new_val := arr[tuple(new_pos)]) == "S":
                return math.ceil(counter / 2)
            elif new_val in allowed:
                queue.put((new_pos, new_val, counter + 1, dr))
                print(counter)
    return -1  # If no valid path is found


if __name__ == "__main__":
    file_path = "inputs/10_0.txt"
    lines_list = read_lines_from_file(file_path)

    if PART == 1:
        dist = get_distance(lines_list)
        print(dist)
    elif PART == 2:
        pass
