from itertools import chain

import re

from functions import read_lines_from_file

WORD_TO_DIGIT = {
    # 'zero': 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

PART = 1


def get_digits(row, verbose=False, part=1, version=1):
    if part == 1:
        occurences = {d: row.find(str(d)) for d in [str(i) for i in range(1, 10)]}
    elif part == 2:
        occurences = {
            d: row.find(str(d))
            for d in chain(*zip(WORD_TO_DIGIT, [str(i) for i in range(1, 10)]))
        }

    valid_occurences = {key: value for key, value in occurences.items() if value >= 0}

    min_dig = min(valid_occurences, key=lambda k: valid_occurences[k], default=None)
    if min_dig is None:
        return 0
    if min_dig in WORD_TO_DIGIT:
        min_dig = WORD_TO_DIGIT[min_dig]

    if version == 1:  # Code for 'oneeight' -> 18
        last_occurences = {key: row.rfind(key) for key in valid_occurences}
        max_dig = max(last_occurences, key=lambda k: last_occurences[k])

    elif version == 2:  # Code for 'oneeight' -> 11
        match_spans = list(
            chain(
                *[
                    [
                        (key, match.start(), match.end())
                        for match in re.finditer(key, row)
                    ]
                    for key in valid_occurences
                ]
            )
        )
        sorted_match_spans = iter(
            sorted(match_spans, key=lambda x: x[-1], reverse=True)
        )

        tmp_key_lo, tmp_min_lo, _ = next(sorted_match_spans)
        while True:
            try:
                key_lo, min_lo, max_lo = next(sorted_match_spans)

                if tmp_min_lo >= max_lo:
                    max_dig = tmp_key_lo
                    break
                else:
                    tmp_key_lo, tmp_min_lo = key_lo, min_lo

            except StopIteration:  # is raised when there are no more keys
                max_dig = tmp_key_lo
                break

    if max_dig in WORD_TO_DIGIT:
        max_dig = WORD_TO_DIGIT[max_dig]

    res = int(f"{min_dig}{max_dig}")

    if verbose:
        print(f"{row} -> {res}")

    return res


if __name__ == "__main__":
    file_path = "inputs/1_0.txt"
    lines_list = read_lines_from_file(file_path)

    total_sum = sum(
        get_digits(row, verbose=False, part=PART, version=1) for row in lines_list
    )

    print(f"The sum is {total_sum} .")
