import os
import re
import time
from collections import defaultdict
from functools import reduce

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

            min_power: dict[str, int] = defaultdict(int)
            for cubes in cubes_list.strip().split(";"):
                elements = [x.strip() for x in cubes.strip().split(",")]
                for elem in elements:
                    elem_match = re.match(r"(?P<n>[1-9][0-9]*) (?P<color>[a-z]+)", elem)
                    if elem_match is None:
                        raise ValueError(f"Cannot find n and color in {elem}.")

                    elem_match_dict = elem_match.groupdict()
                    min_power[elem_match_dict["color"]] = max(
                        min_power[elem_match_dict["color"]], int(elem_match_dict["n"])
                    )

            power = reduce(lambda acc, v: acc * v, min_power.values())
            sum += power

        print(f"{sum=}")
        print(f"Took: {time.perf_counter() - t0:.5f} seconds")
