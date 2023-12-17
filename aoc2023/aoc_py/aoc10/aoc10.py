import heapq
import os
import time
from dataclasses import dataclass, field
from typing import Optional, Self


@dataclass(frozen=True, slots=True, order=True)
class Node:
    symbol: str = field(compare=False)
    row_idx: int = field(compare=False)
    col_idx: int = field(compare=False)
    cost: int
    father: Optional[Self] = field(compare=False, default=None, repr=False)

    @classmethod
    def new(cls, row_idx: int, col_idx: int, cost: int, father: Optional[Self], tiles: list[list[str]]) -> Self:
        return cls(
            symbol=tiles[row_idx][col_idx],
            row_idx=row_idx,
            col_idx=col_idx,
            father=father,
            cost=cost,
        )


def is_valid_tile(row_idx: int, col_idx: int, tiles: list[list[str]]) -> bool:
    return 0 <= row_idx < len(tiles) and 0 <= col_idx < len(tiles[0])


def expand_node(node: Node, tiles: list[list[str]], visited: list[list[bool]]) -> list[Node]:
    expanded = []
    for d_row, d_col in [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)]:
        if (
            is_valid_tile(node.row_idx + d_row, node.col_idx + d_col, tiles)
            and not visited[node.row_idx + d_row][node.col_idx + d_col]
        ):
            target_symbol = tiles[node.row_idx + d_row][node.col_idx + d_col]
            if target_symbol == "." or target_symbol == "S":
                continue

            if (
                target_symbol == "|"
                and (d_row, d_col) in {(-1, 0), (1, 0)}
                or target_symbol == "-"
                and (d_row, d_col) in {(0, 1), (0, -1)}
                or target_symbol == "L"
                and (d_row, d_col) in {(1, 0), (0, -1)}
                or target_symbol == "J"
                and (d_row, d_col) in {(1, 0), (0, 1)}
                or target_symbol == "7"
                and (d_row, d_col) in {(-1, 0), (0, 1)}
                or target_symbol == "F"
                and (d_row, d_col) in {(-1, 0), (0, -1)}
            ):
                expanded_node = Node.new(
                    row_idx=node.row_idx + d_row,
                    col_idx=node.col_idx + d_col,
                    cost=node.cost + 1,
                    father=node,
                    tiles=tiles,
                )
                expanded.append(expanded_node)

    return expanded


def count_internal(loop: list[list[bool]], tiles: list[list[str]]) -> int:
    """
    Solved noticing the following property:
        If we start at a enclosed tile and move right we encounter an odd number of | tiles (called fulls below).
        We may also encounter border tiles (e.g., F and 7) which we don't have to count.

    The property above must be satisfied when moving from left to right, from right to left, from bottom to top
    and from top to bottom starting from each enclosed tile. (for bottom-top and top-bottom movements full tiles are -)

    Code below assumes the S tile has been replaced properly.
    """
    count = 0
    for row_idx in range(len(tiles)):
        for col_idx in range(len(tiles[0])):
            if not loop[row_idx][col_idx]:
                r_border, r_full = 0, 0
                l_border, l_full = 0, 0
                t_border, t_full = 0, 0
                b_border, b_full = 0, 0

                # Right
                for i in range(col_idx, len(tiles[0])):
                    if loop[row_idx][i] and tiles[row_idx][i] in {"F", "7"}:
                        r_border += 1
                    elif loop[row_idx][i] and tiles[row_idx][i] in {"|", "J", "L"}:
                        r_full += 1

                # Left
                for i in range(col_idx, -1, -1):
                    if loop[row_idx][i] and tiles[row_idx][i] in {"F", "7"}:
                        l_border += 1
                    elif loop[row_idx][i] and tiles[row_idx][i] in {
                        "|",
                        "J",
                        "L",
                    }:
                        l_full += 1

                # Bottom
                for i in range(row_idx, len(tiles)):
                    if loop[i][col_idx] and tiles[i][col_idx] in {"L", "F"}:
                        b_border += 1
                    elif loop[i][col_idx] and tiles[i][col_idx] in {"-", "7", "J"}:
                        b_full += 1

                # Top
                for i in range(row_idx, -1, -1):
                    if loop[i][col_idx] and tiles[i][col_idx] in {"L", "F"}:
                        t_border += 1
                    elif loop[i][col_idx] and tiles[i][col_idx] in {"-", "7", "J"}:
                        t_full += 1

                check_r = r_full > 0 and r_full % 2 != 0
                check_l = l_full > 0 and l_full % 2 != 0
                check_b = b_full > 0 and b_full % 2 != 0
                check_t = t_full > 0 and t_full % 2 != 0

                if check_r and check_l and check_b and check_t:
                    # Tile enclosed in the loop
                    count += 1
    return count


def solve(start: tuple[int, int], tiles: list[list[str]]) -> tuple[int, int]:
    visited = [[False for _ in range(len(tiles[0]))] for _ in range(len(tiles))]

    curr = Node.new(row_idx=start[0], col_idx=start[1], cost=0, father=None, tiles=tiles)
    prio_queue = [curr]
    prev_curr = None
    max_cost = -1

    while prio_queue:
        curr = heapq.heappop(prio_queue)
        max_cost = max(max_cost, curr.cost)
        visited[curr.row_idx][curr.col_idx] = True

        expanded_nodes = expand_node(curr, tiles, visited)
        for node in expanded_nodes:
            heapq.heappush(prio_queue, node)

        if prio_queue:
            prev_curr = curr

    # Identify loop
    loop = [[False for _ in range(len(tiles[0]))] for _ in range(len(tiles))]
    assert curr is not None and prev_curr is not None, "Type guard"
    for node in [curr, prev_curr]:
        n: Optional[Node] = node
        while n is not None:
            loop[n.row_idx][n.col_idx] = True
            n = n.father

    # All the lines below just to identify the S tile
    # with its corresponding standard tile
    nodes_after_start_point = []
    for node in [curr, prev_curr]:
        n = node
        while n.father is not None:
            n = n.father
            assert n.father is not None, "Type guard"
            if n.father.symbol == "S":
                nodes_after_start_point.append(n)
                break

    diffs_to_target_symbol: dict[tuple[tuple[int, int], ...], str] = {
        ((-1, 0), (1, 0)): "|",
        ((0, 1), (0, -1)): "-",
        ((1, 0), (0, -1)): "L",
        ((1, 0), (0, 1)): "J",
        ((-1, 0), (0, 1)): "7",
        ((-1, 0), (0, -1)): "F",
    }
    diffs_to_target_symbol = {tuple(sorted(k)): v for k, v in diffs_to_target_symbol.items()}
    diffs: list[tuple[int, int]] = []
    for node in nodes_after_start_point:
        diffs.append((start[0] - node.row_idx, start[1] - node.col_idx))

    s_replace_symbol = diffs_to_target_symbol[tuple(sorted(diffs))]
    print(f"Replacing starting symbol S with {s_replace_symbol} for second part.")
    tiles[start[0]][start[1]] = s_replace_symbol

    # Having replaced S with a normal tile, we can now solve part2
    count = count_internal(loop, tiles)

    return max_cost, count


if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
        tiles = []
        start = (0, 0)
        for line in f:
            tiles.append([ch for ch in line.strip()])
            if (col_idx := line.find("S")) != -1:
                start = (len(tiles) - 1, col_idx)

        first_res, second_res = solve(start, tiles)
        print(f"First part solution = {first_res}")
        print(f"Secoond part solution = {second_res}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds")
