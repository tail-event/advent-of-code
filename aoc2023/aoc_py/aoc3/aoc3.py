import itertools
import os
import string
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, Sequence


@dataclass(slots=True)
class GridNumber:
    digits: str
    near_symbols: set[tuple[int, int]] = field(default_factory=set)

    def add_digit(self, digit: str) -> None:
        self.digits += digit

    def add_near_symbol(self, i: int, j: int) -> None:
        self.near_symbols.add((i, j))

    def is_engine_number(self) -> bool:
        return len(self.near_symbols) > 0

    @property
    def num(self) -> int:
        return int(self.digits)


@dataclass(frozen=True)
class Grid:
    mat: list[list[str]]

    def __str__(self) -> str:
        out = ""
        for row in self.mat:
            for col in row:
                out += col
            out += "\n"
        return out[:-1]

    def is_cell_digit(self, cell: str) -> int:
        return cell in string.digits

    def is_cell_dot(self, cell: str) -> int:
        return cell == "."

    def is_cell_symbol(self, cell: str) -> int:
        return not self.is_cell_dot(cell) and not self.is_cell_digit(cell)

    def near_symbol(self, i: int, j: int) -> Optional[tuple[int, int]]:
        indices_to_check = list(itertools.product([0, 1, -1], [0, 1, -1]))
        for delta_i, delta_j in indices_to_check:
            if 0 <= i + delta_i < len(self.mat) and 0 <= j + delta_j < len(self.mat[0]):
                if self.is_cell_symbol(self.mat[i + delta_i][j + delta_j]):
                    return (i + delta_i, j + delta_j)
        return None

    def find_engine_numbers(self) -> list[GridNumber]:
        scanning_number: Optional[GridNumber] = None
        grid_numbers: list[GridNumber] = []
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                if self.is_cell_digit(self.mat[i][j]):
                    if scanning_number is None:
                        # Start a new scan
                        scanning_number = GridNumber(digits="")
                        grid_numbers.append(scanning_number)
                    # Add digit and check for neighbor symbols
                    scanning_number.add_digit(self.mat[i][j])
                    if near := self.near_symbol(i, j):
                        scanning_number.add_near_symbol(near[0], near[1])

                elif self.is_cell_dot(self.mat[i][j]) or self.is_cell_symbol(self.mat[i][j]):
                    if scanning_number is not None:
                        # Stop active scan
                        scanning_number = None

                if j == len(self.mat[0]) - 1 and scanning_number is not None:
                    scanning_number = None

        return grid_numbers


def compute_first_part_solution(grid_numbers: Sequence[GridNumber]) -> int:
    sum = 0
    for grid_number in grid_numbers:
        if grid_number.is_engine_number():
            sum += grid_number.num
    return sum


def compute_second_part_solution(grid: Grid, grid_numbers: Sequence[GridNumber]) -> int:
    potential_gears = defaultdict(list)
    for grid_number in grid_numbers:
        if grid_number.is_engine_number():
            for i, j in grid_number.near_symbols:
                if grid.mat[i][j] == "*":
                    potential_gears[(i, j)].append(grid_number.num)

    gears = {k: v[0] * v[1] for (k, v) in potential_gears.items() if len(v) == 2}
    return sum(gears.values())


if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
        grid_mat = []

        for line in f:
            grid_mat.append([ch for ch in line.strip()])

        grid = Grid(mat=grid_mat)
        grid_numbers = grid.find_engine_numbers()

        first_solution = compute_first_part_solution(grid_numbers)
        print("First part")
        print(f"sum={first_solution}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")

        second_solution = compute_second_part_solution(grid, grid_numbers)
        print("Second part")
        print(f"sum={second_solution}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")
