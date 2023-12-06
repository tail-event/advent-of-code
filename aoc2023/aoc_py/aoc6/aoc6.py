import math
import operator
import os
import time
from functools import reduce


def compute_n_holding_ways(time: int, distance: int) -> int:
    """
    Find winning holding milliseconds
    by solving (time - x) * x > distance
    where x is the holding time
    """
    b = -time
    c = distance
    a = 1

    lower = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    upper = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)

    lower_int = int(lower + 1) if int(lower) == lower else math.ceil(lower)
    upper_int = int(upper - 1) if int(upper) == upper else math.floor(upper)
    return upper_int - lower_int + 1


def first_part_solution(times: list[int], distances: list[int]) -> int:
    possibilities = [compute_n_holding_ways(time, distance) for time, distance in zip(times, distances)]
    return reduce(operator.mul, possibilities, 1)


def second_part_solution(times: list[int], distances: list[int]) -> int:
    time = int("".join(str(x) for x in times))
    distance = int("".join(str(x) for x in distances))
    return compute_n_holding_ways(time, distance)


if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
        times = [int(x) for x in f.readline().split(": ")[1].strip().split()]
        distances = [int(x) for x in f.readline().split(": ")[1].strip().split()]

        print(f"First part solution={first_part_solution(times, distances)}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds")

        print(f"Second part solution={second_part_solution(times, distances)}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds")
