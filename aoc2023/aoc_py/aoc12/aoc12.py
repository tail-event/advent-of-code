import os
import time
from typing import Optional, TypeVar

T = TypeVar("T")


def flatten(list_of_lists: list[list[T]]) -> list[T]:
    return [el for li in list_of_lists for el in li]


def are_compatible(record: list[str], damaged_group: list[int]) -> bool:
    return [len(g) for g in ("".join(record)).split(".") if len(g) > 0] == damaged_group


def get_mark_indices(record: list[str], pos: int) -> list[int]:
    sub_record = record[: pos + 1]
    return [i for i in range(len(sub_record)) if sub_record[i] == "?"]


def get_match_pos(record: list[str], damaged_group: list[int], pos: int) -> tuple[int, bool]:
    sub_record = record[: pos + 1]
    groups = [g for g in ("".join(sub_record)).split(".") if len(g) > 0]
    is_ok = True

    if not groups:
        return 0, True

    len_groups = [len(g) for g in groups if len(g) > 0]

    if len(len_groups) > len(damaged_group):
        is_ok = False

    match_pos = 0
    for group, dmg_group in zip(len_groups, damaged_group):
        if group == dmg_group:
            match_pos += 1
        else:
            return match_pos, False

    return match_pos, is_ok


def solve_record(
    record: list[str],
    damaged_group: list[int],
    pos: int,
    match_pos: int,
    cache: Optional[dict[tuple[int, int], int]] = None,
) -> int:
    if cache is None:
        cache = {}
    mark_indices = get_mark_indices(record, len(record))

    if not mark_indices:
        # Leaf
        return int(are_compatible(record, damaged_group))
    else:
        idx = mark_indices[0]

        total = 0
        for kind in [".", "#"]:
            kind_record = [el for el in record]
            kind_record[idx] = kind

            # Retrieve the updated number of matched damaged groups
            new_match_pos, is_ok = get_match_pos(kind_record, damaged_group, idx)

            if not is_ok and (kind_record[idx] == "."):
                # Avoid visiting this subtree, it's already not a valid one
                # E.g., if record = #.????????????? and damaged_groups=[2,3]
                total += 0
                continue

            if kind == ".":
                # If we reach a node in the tree with a starting . we can use cache
                # And avoid visiting the subtree already visited
                if (idx, match_pos) not in cache:
                    kind_count = solve_record(kind_record, damaged_group, idx, new_match_pos, cache)
                    cache[(idx, match_pos)] = kind_count
                else:
                    kind_count = cache[(idx, match_pos)]
                    # print(f"Using cached {kind_count=}.")
            else:
                kind_count = solve_record(kind_record, damaged_group, idx, new_match_pos, cache)

            total += kind_count

        return total


def solve(records: list[list[str]], damaged_groups: list[list[int]], verbose: bool = False) -> int:
    total = 0
    for i, (record, damaged_group) in enumerate(zip(records, damaged_groups)):
        t0 = time.perf_counter()
        cache: Optional[dict[tuple[int, int], int]] = {}
        if verbose:
            print(f"Solving {i=}.")
        res = solve_record(record, damaged_group, pos=0, match_pos=0, cache=cache)
        total += res
        if verbose:
            print(f"Solved {i=}. Took {time.perf_counter() - t0:.3f} seconds.")
            print()
    return total


if __name__ == "__main__":
    N = 5

    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
        records = []
        damaged_groups = []

        for line in f:
            new_record, new_group = line.strip().split(" ")
            records.append([ch for ch in new_record])
            damaged_groups.append([int(x) for x in new_group.split(",")])

        t0 = time.perf_counter()
        first_part_solution = solve(records, damaged_groups)
        print(f"First part solution = {first_part_solution}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds")

        records = [el[:-1] for el in [flatten([r + ["?"] for _ in range(N)]) for r in records]]
        damaged_groups = [flatten([g for _ in range(N)]) for g in damaged_groups]

        t0 = time.perf_counter()
        first_part_solution = solve(records, damaged_groups, verbose=True)
        print(f"Second part solution = {first_part_solution}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds")
