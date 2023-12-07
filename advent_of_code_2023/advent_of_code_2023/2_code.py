import math
import re

from functions import read_lines_from_file

PART = 2


def analyze_game(game, part=1, red=None, green=None, blue=None):
    def get_balls(subgame, color):
        try:
            return int(re.search(rf" (\d{{1,3}}) {color}", subgame).group(1))
        except:
            return 0

    subgames = game.split(";")

    if part == 1:
        game_id = int(re.match(r"Game (\d{1,3})", game).group(1))

        valid_game = True
        for sg in subgames:
            r = get_balls(sg, "red")
            b = get_balls(sg, "blue")
            g = get_balls(sg, "green")

            if any([r > red, b > blue, g > green]):
                valid_game = False
                break

        return valid_game, game_id

    elif part == 2:
        color_dic = {"red": 0, "green": 0, "blue": 0}
        for sg in subgames:
            for c in color_dic:
                color_dic[c] = max(color_dic[c], get_balls(sg, c))
        return math.prod(color_dic.values())


if __name__ == "__main__":
    file_path = "inputs/2_0.txt"
    lines_list = read_lines_from_file(file_path)

    if PART == 1:
        res = sum(
            [
                value[1]
                for item in lines_list
                if (value := analyze_game(item, red=12, green=13, blue=14))[0] is True
            ]
        )

        print(f"Sum of valid Game-IDs: {res}")

    elif PART == 2:
        res = sum([analyze_game(item, part=2) for item in lines_list])

        print(f"Sum of Game-powers: {res}")
