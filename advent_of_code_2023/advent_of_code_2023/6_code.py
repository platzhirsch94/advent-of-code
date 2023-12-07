import math
import re

from functions import read_lines_from_file

 # dist = (total_time-push_time)*push_time

PART = 2

def get_races(lines, part=1):

    times = re.findall(r"\d{1,3}", lines[0].split(":",1)[1])
    distances = re.findall(r"\d{1,5}", lines[1].split(":",1)[1])

    if part == 1:
        times = [int(t) for t in times]
        distances = [int(d) for d in distances]
        time_dist_dic = dict(zip(times,distances))
    else:
        time_dist_dic = {int("".join(times)):int("".join(distances))}

    res_list = []
    for t,d in time_dist_dic.items():
        delta_sqrt = math.sqrt(t**2-4*d)
        tp1_tmp, tp2_tmp = (t-delta_sqrt)/2, (t+delta_sqrt)/2
        tp1 = tp1_ceil if abs(tp1_tmp-(tp1_ceil:=math.ceil(tp1_tmp))) > 1e-9 else tp1_ceil+1
        tp2 = tp2_floor if abs(tp2_tmp-(tp2_floor:=math.floor(tp2_tmp))) > 1e-9 else tp2_floor-1
        res_list.append(tp2-tp1+1)

    return res_list


if __name__ == "__main__":
    
    file_path = 'inputs/6_0.txt'
    lines_list = read_lines_from_file(file_path)

    if PART == 1:
        res_total = math.prod(get_races(lines_list))

    elif PART == 2:
        res_total = get_races(lines_list, part=2)[0]
    
    print(res_total)