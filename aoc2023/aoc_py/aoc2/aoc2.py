import os
import re
import time
from collections import defaultdict

bag = {"red": 12, "green": 13, "blue": 14}

if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
        sum = 0
        for line in f:
            strip_line = line.strip()
            game, cubes_list = strip_line.split(":")

            game_id_s = re.match(r"^Game (?P<game_id>[1-9][0-9]*)$", game)
            if game_id_s is None:
                raise ValueError(f"Cannot find game id in {game_id_s}.")

            game_id = int(game_id_s.groupdict()["game_id"])

            valid_game = True
            for cubes in cubes_list.strip().split(";"):
                elements = [x.strip() for x in cubes.strip().split(",")]
                revealed: dict[str, int] = defaultdict(int)
                for elem in elements:
                    elem_match = re.match(r"(?P<n>[1-9][0-9]*) (?P<color>[a-z]+)", elem)
                    if elem_match is None:
                        raise ValueError(f"Cannot find n and color in {elem}.")

                    elem_match_dict = elem_match.groupdict()
                    revealed[elem_match_dict["color"]] = revealed[elem_match_dict["color"]] + int(elem_match_dict["n"])

                    for color, n in revealed.items():
                        if color not in bag or n > bag[color]:
                            valid_game = False
                            break

            if valid_game:
                sum += game_id

        print(f"{sum=}")
        print(f"Took: {time.perf_counter() - t0:.5f} seconds")
