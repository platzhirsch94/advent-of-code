import numpy as np
import re

from functions import read_lines_from_file

PART = 2

def get_points(row, part=1):

    card, win_res= row.split(":", 1)
    win, res = win_res.split("|")
    win_digs = re.findall(r"\d{1,2}", win)
    win_res = re.findall(r"\d{1,2}", res)

    intersection_length=len(np.intersect1d(win_digs, win_res))

    if part == 1:

        if intersection_length>1:
            return np.power(2,intersection_length-1)
        else:
            return 0
        
    elif part == 2:

        cardid = int(re.search(r"\d{1,3}", card).group())
        offset = cardid+1
        global cardid_dic

        for match in range(offset,offset+intersection_length):
            cardid_dic[match] += cardid_dic[cardid]

if __name__ == "__main__":
    
    file_path = 'inputs/4_0.txt'
    lines_list = read_lines_from_file(file_path)

    if PART == 1:

        total_sum = sum([get_points(line, part=PART) for line in lines_list])

    elif PART == 2:

        lines_num = len(lines_list)
        global cardid_dic
        cardid_dic = {i:1 for i in range(1,lines_num+1)}

        for line in lines_list:
            get_points(line, part=PART)

        total_sum = sum(cardid_dic.values())

    print(total_sum)


