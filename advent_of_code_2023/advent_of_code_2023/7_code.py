from collections import Counter

import re

from functions import read_lines_from_file

TYPE_VALS = [
    "five",
    "four",
    "fh",
    "three",
    "two-pair",
    "pair",
    "hc"
]

CARD_LIST = [
    "A", "K", "Q", "J", "T", *[str(i) for i in range(9, 1, -1)]
]

PART = 2

def get_type(cc):
    
    if cc.get(5,0) == 1:
        return "five"
    elif cc.get(4,0) == 1:
        return "four"
    elif cc.get(3,0) == 1 and cc.get(2,0) == 1:
        return "fh"
    elif cc.get(3,0) == 1:
        return "three"
    elif cc.get(2,0) == 2:
        return "two-pair"
    elif cc.get(2,0) == 1:
        return "pair"
    else:
        return "hc"

def get_cards(lines, part=1):

    if part == 2:
        CARD_LIST.pop(CARD_LIST.index("J"))
        CARD_LIST.append("J")

    card_mapper = {char:format(idx, 'x') 
        for idx, char in enumerate(reversed(CARD_LIST))}
    
    cards_dic = {typ:[] for typ in TYPE_VALS} # is ordered

    for line in lines:
        match = re.search(r"(\S{5}) (\d{1,4})", line)
        hand, bid = match.group(1), match.group(2)
        counter = Counter(hand)
        counter_counter = Counter(counter.values())
        typ = get_type(counter_counter)
        if part == 2:
            if jnum:=counter.get("J",0):
                if typ == "four":
                    typ = "five" #XXXXJ XJJJJ
                elif typ == "fh": #XXXJJ XXJJJ
                    typ = "five"
                elif typ == "three": # XXXYJ XYJJJ
                    typ = "four"
                elif typ == "two-pair": 
                    if jnum == 1: #XXYYJ
                        typ = "fh"
                    elif jnum == 2: #XXYJJ
                        typ = "four"
                elif typ == "pair": #XXYZJ XYZJJ
                    typ = "three"
                elif typ == "hc": #XYZWJ
                    typ = "pair"

        cards_dic[typ].append([''.join([card_mapper[char] 
            for char in hand]), bid])

    res_ordered_bids = []
    for lst in cards_dic.values():
        res_ordered_bids.extend([*sorted(lst, key=lambda x: int(x[0], 16), 
                                            reverse=True)])

    weighted_factors = [idx*int(tpl[1]) 
        for idx, tpl in enumerate(reversed(res_ordered_bids), start=1)]

    return sum(weighted_factors)

if __name__ == "__main__":
    
    file_path = 'inputs/7_0.txt'
    lines_list = read_lines_from_file(file_path)

    res = get_cards(lines_list, part=PART)

    print(res)