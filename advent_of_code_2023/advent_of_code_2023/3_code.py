import math
import numpy as np
import re
import sys

from functions import read_lines_from_file

PART = 2

neighbors_positions = np.array([
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ])

right_shift = np.array([0,1])

test_string = """467..114..\n...*......\n..35..633.\n......#...\n617*......\n.....+.58.\n..592.....\n......755.\n...$.*....\n.664.598.."""
np.set_printoptions(threshold=sys.maxsize)
    
def get_part_numbers(filepath, part=1):

    lines = [line.replace("\n","") for line in read_lines_from_file(filepath)]
    # lines = [line.replace("\n","") for line in test_string.splitlines()]
    line_num = len(lines)
    line_width = len(lines[0])

    matches = []
    for idx, line in enumerate(lines):
        # Fill up empty spaces
        if (line_tmp:=len(line)) != line_width:
            line += (line_width-line_tmp)*"."
            lines[idx] = line

        # Get number indices considering the padding which will follow
        matches.extend([(tmp:=match.group(), [idx+1, match.start()+1]+neighbors_positions, len(tmp)) 
                    for match in re.finditer(r"\d{1,4}", line)])

    content = "".join(lines)

    # Get different symbols
    symbols = set([char for char in content if not(char.isdigit() or char == ".")])
    
    # Convert the string to a flattened NumPy array
    arr_1d = np.array(list(content))

    # Reshape the 1D array into a 2D array
    arr_2d = arr_1d.reshape((line_num, line_width))

    # Pad the 2D array with "." 
    padded_array = np.pad(arr_2d, ((1, 1), (1, 1)), constant_values=".")

    valid_vals = []

    if part == 1:

        for match in matches:
            neighbors = match[1]
            for _ in range(match[2]):
                if any([padded_array[tuple(item)] in symbols for item in neighbors]):
                    valid_vals.append(int(match[0]))
                    break
                else:
                    neighbors += right_shift
    
    elif part == 2:

        star_dic = {}
        for match in matches:
            neighbors = match[1]
            for _ in range(match[2]):
                if star_indices := [item for item in neighbors if padded_array[tuple(item)] == "*"]:
                    for star_pos in star_indices:
                        try:
                            star_dic[str(star_pos)].append(int(match[0]))
                        except:
                            star_dic[str(star_pos)] = [int(match[0])]
                    break
                else:
                    neighbors += right_shift

        for star_pos, vals in star_dic.items():
            if len(vals) == 2:
                valid_vals.append(math.prod(vals))
        
    return sum(valid_vals)
        

if __name__ == "__main__":
    
    file_path = 'inputs/3_0.txt'
    res = get_part_numbers(file_path, part=PART)

    print(res)