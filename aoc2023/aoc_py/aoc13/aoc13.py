import os
import time
from dataclasses import dataclass
from typing import Literal, Optional

import numpy as np


@dataclass(frozen=True, slots=True)
class Solution:
    kind: Literal["row", "col"]
    start_idx: int
    end_idx: int
    value: int


def solve_pattern(pattern: np.ndarray, original_solution: Optional[Solution] = None) -> Solution:
    solution = None
    original_pattern = pattern.copy()

    # Row-wise code is similar to column-wise code and could be refactored...

    # Search for a solution row-wise
    for i in range(pattern.shape[0]):
        j = i + 1
        if j >= pattern.shape[0]:
            continue
        row_start = pattern[i, :].reshape(-1, pattern.shape[1])
        row_end = pattern[j, :].reshape(-1, pattern.shape[1])
        max_reflection = min(i, pattern.shape[0] - j - 1)

        if original_solution is not None and (
            original_solution.kind != "row" or (i != original_solution.start_idx and j != original_solution.end_idx)
        ):
            # Try to find an alternative solution (second part)
            diff = row_start != row_end
            if np.sum(diff) > 1:
                continue

            if np.sum(diff) == 1:
                diff_idx = np.argwhere(diff)[0][1]
                curr_symbol = pattern[i, diff_idx]
                changed_symbol = "#" if curr_symbol == "." else "."
                pattern[i, diff_idx] = changed_symbol
                pattern[j, diff_idx] = changed_symbol
            else:
                # They are equal but maybe we can change something externally
                external_diff = (
                    pattern[i - max_reflection : i, :][::-1, :] != pattern[j + 1 : j + 1 + max_reflection, :]
                )
                if np.sum(external_diff) == 1:
                    diff_idx = np.argwhere(external_diff)[0]
                    curr_symbol = pattern[j + 1 + diff_idx[0], diff_idx[1]]
                    changed_symbol = "#" if curr_symbol == "." else "."
                    pattern[j + 1 + diff_idx[0], diff_idx[1]] = changed_symbol

            row_start = pattern[i, :].reshape(-1, pattern.shape[1])
            row_end = pattern[j, :].reshape(-1, pattern.shape[1])
            max_reflection = min(i, pattern.shape[0] - j - 1)
            if (
                (row_start == row_end).all()
                and (pattern[i : j + 1, :] == row_start).all()
                and (pattern[i - max_reflection : i, :][::-1, :] == pattern[j + 1 : j + 1 + max_reflection, :]).all()
            ):
                solution = Solution(kind="row", start_idx=i, end_idx=j, value=(i + 1) * 100)
                if solution != original_solution:
                    # print(f"Found alternative solution = {solution}. Original was {original_solution}.")
                    return solution

            # Alternative solution not found, reset to original pattern
            pattern = original_pattern

        else:
            # Find original solution (first part)
            if (
                (row_start == row_end).all()
                and (pattern[i : j + 1, :] == row_start).all()
                and (pattern[i - max_reflection : i, :][::-1, :] == pattern[j + 1 : j + 1 + max_reflection, :]).all()
            ):
                solution = Solution(kind="row", start_idx=i, end_idx=j, value=(i + 1) * 100)
                if original_solution is None:
                    return solution

    # Search for a solution column-wise
    for i in range(pattern.shape[1]):
        # Try to find an alternative solution (second part)
        j = i + 1
        if j >= pattern.shape[1]:
            continue

        col_start = pattern[:, i].reshape(pattern.shape[0], -1)
        col_end = pattern[:, j].reshape(pattern.shape[0], -1)
        max_reflection = min(i, pattern.shape[1] - j - 1)

        if original_solution is not None and (
            original_solution != "col" or (i != original_solution.start_idx and j != original_solution.end_idx)
        ):
            diff = col_start != col_end
            if np.sum(diff) > 1:
                continue

            if np.sum(diff) == 1:
                diff_idx = np.argwhere(diff)[0][0]
                curr_symbol = pattern[diff_idx, i]
                changed_symbol = "#" if curr_symbol == "." else "."
                pattern[diff_idx, i] = changed_symbol
                pattern[diff_idx, j] = changed_symbol
            else:
                # They are equal but maybe we can change something externally
                external_diff = (
                    pattern[:, i - max_reflection : i][:, ::-1] != pattern[:, j + 1 : j + 1 + max_reflection]
                )
                if np.sum(external_diff) == 1:
                    diff_idx = np.argwhere(external_diff)[0]
                    curr_symbol = pattern[diff_idx[0], j + 1 + diff_idx[1]]
                    changed_symbol = "#" if curr_symbol == "." else "."
                    pattern[diff_idx[0], j + 1 + diff_idx[1]] = changed_symbol

            col_start = pattern[:, i].reshape(pattern.shape[0], -1)
            col_end = pattern[:, j].reshape(pattern.shape[0], -1)
            max_reflection = min(i, pattern.shape[1] - j - 1)

            if (
                (col_start == col_end).all()
                and (pattern[:, i : j + 1] == col_start).all()
                and (pattern[:, i - max_reflection : i][:, ::-1] == pattern[:, j + 1 : j + 1 + max_reflection]).all()
            ):
                solution = Solution(kind="col", start_idx=i, end_idx=j, value=(i + 1))
                if solution != original_solution:
                    # print(f"Found alternative solution = {solution}. Original was {original_solution}.")
                    return solution

            # Alternative solution not found, reset to original pattern
            pattern = original_pattern
        else:
            # Find original solution (first part)
            if (
                (col_start == col_end).all()
                and (pattern[:, i : j + 1] == col_start).all()
                and (pattern[:, i - max_reflection : i][:, ::-1] == pattern[:, j + 1 : j + 1 + max_reflection]).all()
            ):
                solution = Solution(kind="col", start_idx=i, end_idx=j, value=(i + 1))
                if original_solution is None:
                    return solution

    assert solution is not None

    return solution


def first_part_solution(patterns: list[np.ndarray]) -> tuple[int, list[Solution]]:
    total, solutions = 0, []
    for i, pattern in enumerate(patterns):
        solution = solve_pattern(pattern)
        total += solution.value
        solutions.append(solution)

    return total, solutions


def second_part_solution(patterns: list[np.ndarray], original_solutions: list[Solution]) -> tuple[int, list[Solution]]:
    total, solutions = 0, []
    for i, pattern in enumerate(patterns):
        solution = solve_pattern(pattern, original_solutions[i])
        total += solution.value
        solutions.append(solution)

    return total, solutions


with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
    t0 = time.perf_counter()
    patterns = [np.array([[ch for ch in line] for line in pattern.split("\n")]) for pattern in f.read().split("\n\n")]

    first_part_res, solutions = first_part_solution(patterns)
    print(f"First part solution = {first_part_res}.")
    print(f"Took {time.perf_counter() - t0:.5f} seconds.")

    assert len(patterns) == len(solutions)

    second_part_res, _ = second_part_solution(patterns, solutions)
    print(f"Second part solution = {second_part_res}.")
    print(f"Took {time.perf_counter() - t0:.5f} seconds.")
