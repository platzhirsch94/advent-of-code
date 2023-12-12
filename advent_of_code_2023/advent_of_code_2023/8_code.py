import re
import math

from functions import read_lines_from_file

PART = 2


def get_direction(order):
    index = 0
    length = len(order)

    while True:
        yield order[index]
        index = (index + 1) % length


def process_input(startnode, node, node_dic, direction, counter, counter_dic):
    val = node_dic[node][direction]
    if val.endswith("Z"):
        counter_dic[startnode].append(counter)
    return val


def get_steps(lines, part=1):
    order = [0 if c == "L" else 1 for c in lines[0]][:-1]

    lines.pop(0)
    lines = [line.strip() for line in lines if line.strip()]

    start_nodes = []
    node_dic = {}
    for line in lines:
        match = re.search(r"(\S{3}) = \((\S{3}), (\S{3})\)", line)
        node, l, r = match.group(1), match.group(2), match.group(3)
        node_dic[node] = (l, r)
        if part == 2:
            if node.endswith("A"):
                start_nodes.append(node)

    if part == 1:
        node = "AAA"

    direction_generator = get_direction(order)
    counter = 0

    if part == 1:
        while True:
            counter += 1
            direction = next(direction_generator)

            if (node := node_dic[node][direction]) == "ZZZ":
                break

        return counter

    elif part == 2:
        direction_generator = get_direction(order)
        counter = 0
        nodes = start_nodes
        counter_dic = {i: [] for i in range(len(start_nodes))}

        while True:
            counter += 1
            direction = next(direction_generator)

            for idx, node in enumerate(nodes.copy()):
                if (val := node_dic[node][direction]).endswith("Z"):
                    counter_dic[idx].append(counter)
                nodes[idx] = val

            if all(len(value) >= 2 for value in counter_dic.values()):
                break

        diffs = [val[1] - val[0] for val in counter_dic.values()]

        return math.lcm(*diffs)


if __name__ == "__main__":
    file_path = "inputs/8_0.txt"
    lines_list = read_lines_from_file(file_path)

    res = get_steps(lines_list, part=PART)
    print(res)
