import os
import time


def solve(
    *, galaxies: list[tuple[int, int]], expansion_multiplier: int, row_expansions: set[int], col_expansions: set[int]
) -> int:
    sum = 0
    for galaxy_idx, galaxy in enumerate(galaxies):
        for other_galaxy in galaxies[galaxy_idx + 1 :]:
            pos_row = galaxy[0]
            pos_col = galaxy[1]
            delta_row = other_galaxy[0] - galaxy[0]
            delta_col = other_galaxy[1] - galaxy[1]
            n_steps = 0

            i = 1
            while delta_row and i <= abs(delta_row):
                check_row = pos_row + i * (-1 if delta_row < 0 else +1)
                n_steps += 1 * (expansion_multiplier if check_row in row_expansions else 1)
                i += 1

            j = 1
            while delta_col and j <= abs(delta_col):
                check_col = pos_col + j * (-1 if delta_col < 0 else +1)
                n_steps += 1 * (expansion_multiplier if check_col in col_expansions else 1)
                j += 1

            sum += n_steps
    return sum


if __name__ == "__main__":
    t0 = time.perf_counter()

    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
        universe = []
        galaxies = []
        row_expansions = set()
        col_expansions = set()

        for line in f:
            line = line.strip()
            universe.append([ch for ch in line])

        for i in range(len(universe)):
            found_galaxy = False
            for j in range(len(universe[0])):
                if universe[i][j] == "#":
                    found_galaxy = True
                    break

            if not found_galaxy:
                row_expansions.add(i)

        for j in range(len(universe[0])):
            found_galaxy = False
            for i in range(len(universe)):
                if universe[i][j] == "#":
                    found_galaxy = True
                    break

            if not found_galaxy:
                col_expansions.add(j)

        for i in range(len(universe)):
            for j in range(len(universe[0])):
                if universe[i][j] == "#":
                    galaxies.append((i, j))

        first_part_solution = solve(
            galaxies=galaxies, expansion_multiplier=2, row_expansions=row_expansions, col_expansions=col_expansions
        )
        print(f"Part one solution = {first_part_solution}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds")

        second_part_solution = solve(
            galaxies=galaxies,
            expansion_multiplier=int(1e6),
            row_expansions=row_expansions,
            col_expansions=col_expansions,
        )
        print(f"Part two solution = {second_part_solution}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds")
