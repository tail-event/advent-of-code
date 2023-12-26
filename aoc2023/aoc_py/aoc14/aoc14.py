import copy
import os
import time

# The tilt functions below could be optimized


def tilt_east(platform: list[list[str]]) -> list[list[str]]:
    moved = True

    while moved:
        moved = False
        for j in range(len(platform) - 1):
            for i in range(len(platform)):
                if platform[i][j] == "O" and platform[i][j + 1] not in {"#", "O"}:
                    platform[i][j] = "."
                    platform[i][j + 1] = "O"
                    moved = True

    return platform


def tilt_west(platform: list[list[str]]) -> list[list[str]]:
    moved = True

    while moved:
        moved = False
        for j in range(len(platform[0]) - 1, 0, -1):
            for i in range(len(platform)):
                if platform[i][j] == "O" and platform[i][j - 1] not in {"#", "O"}:
                    platform[i][j] = "."
                    platform[i][j - 1] = "O"
                    moved = True

    return platform


def tilt_south(platform: list[list[str]]) -> list[list[str]]:
    moved = True

    while moved:
        moved = False
        for i in range(len(platform) - 1):
            for j in range(len(platform)):
                if platform[i][j] == "O" and platform[i + 1][j] not in {"#", "O"}:
                    platform[i][j] = "."
                    platform[i + 1][j] = "O"
                    moved = True

    return platform


def tilt_north(platform: list[list[str]]) -> list[list[str]]:
    moved = True

    while moved:
        moved = False
        for i in range(len(platform) - 1, 0, -1):
            for j in range(len(platform[0])):
                if platform[i][j] == "O" and platform[i - 1][j] not in {"#", "O"}:
                    platform[i][j] = "."
                    platform[i - 1][j] = "O"
                    moved = True

    return platform


def tilt_cycle(platform: list[list[str]]) -> list[list[str]]:
    copy_platform = copy.deepcopy(platform)
    return tilt_east(tilt_south(tilt_west(tilt_north(copy_platform))))


def compute_load(platform: list[list[str]]) -> int:
    total = 0
    for i in range(len(platform)):
        for j in range(len(platform[0])):
            if platform[i][j] == "O":
                total += len(platform) - i
    return total


def first_part_solution(platform: list[list[str]]) -> int:
    tilted_platform = tilt_north(platform)
    return compute_load(tilted_platform)


def get_previously_visited_idx(platform: list[list[str]], previously_visited_platforms: list[list[list[str]]]) -> int:
    for i, visited_platform in enumerate(previously_visited_platforms):
        if visited_platform == platform:
            return i
    return 0


def second_part_solution(platform: list[list[str]]) -> int:
    N = 1000000000
    platforms_found: list[list[list[str]]] = [platform]
    results: dict[int, list[int]] = {}
    cycle_len = 0

    for n_cycle in range(N):
        tilted_platform = tilt_cycle(platform)
        if duplicate_idx := get_previously_visited_idx(tilted_platform, platforms_found):
            # We don't have to iter up to N but just compute the solution
            # the first time we find a previosly visited platform
            cycle_len = n_cycle - duplicate_idx + 1
            for total, values in results.items():
                for v in values:
                    if v > duplicate_idx and ((N - 1) - v) % (cycle_len) == 0:
                        return total
        else:
            platforms_found.append(tilted_platform)

        load = compute_load(tilted_platform)
        results.setdefault(load, []).append(n_cycle)
        platform = tilted_platform

    raise RuntimeError("A solution should have already been found.")


if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt")) as f:
        platform = [[ch for ch in line.strip()] for line in f]

        first_part_res = first_part_solution(platform)
        print(f"First part solution = {first_part_res}.")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")

        second_part_res = second_part_solution(platform)
        print(f"Second part solution = {second_part_res}.")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")
