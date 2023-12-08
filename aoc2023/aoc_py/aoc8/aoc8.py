import math
import os
import time
from dataclasses import dataclass, field
from typing import Callable, Optional, Self


@dataclass(slots=True)
class NetworkNode:
    name: str
    left: Optional[Self] = field(repr=False, default=None)
    right: Optional[Self] = field(repr=False, default=None)
    cache: dict = field(default_factory=dict)

    def __str__(self) -> str:
        assert self.left is not None and self.right is not None
        return f"NetworkNode(name={self.name},left={self.left.name},right={self.right.name})"


def solve(start_node: NetworkNode, instructions: str, fn_is_target: Callable[[NetworkNode], bool]) -> int:
    ins_idx = 0
    steps = 0
    curr = start_node

    while True:
        steps += 1
        instruction = instructions[ins_idx]

        assert curr.left is not None and curr.right is not None
        curr = curr.left if instruction == "L" else curr.right

        ins_idx = (ins_idx + 1) % len(instructions)

        if fn_is_target(curr):
            break

    return steps


if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
        instructions, network = f.read().split("\n\n")

        nodes_id_to_members = {}
        for line in network.split("\n"):
            node, members = line.split(" = ")
            network_node = NetworkNode(name=node)
            left_right_split = members.split(", ")
            nodes_id_to_members[node] = (network_node, (left_right_split[0][1:], left_right_split[1][:-1]))

        network_nodes = []
        start_node = None
        start_nodes = []
        for name, (network_node, (left, right)) in nodes_id_to_members.items():
            network_node.left = nodes_id_to_members[left][0]
            network_node.right = nodes_id_to_members[right][0]
            network_nodes.append(network_node)
            if name == "AAA":
                start_node = network_node
            if name[-1] == "A":
                start_nodes.append(network_node)

        # First part
        assert start_node is not None
        first_part_res = solve(start_node, instructions, fn_is_target=lambda node: node.name == "ZZZ")
        print(f"First part solution = {first_part_res}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")

        # Second part
        # Intution:
        # Assume we have three different starting point (S1, S2, S3) leading to three different destinations (D1, D2, D3).
        # If following S1 we reach D1 in 2 steps
        # If following S2 we reach D2 in 3 steps
        # If following S3 we reach D3 in 7 steps
        # We can reach all of three at the same time after 2*3*7 steps
        # Therefore we need to find the least common multiple of the three
        steps_list = []
        for start_node in start_nodes:
            steps_list.append(solve(start_node, instructions, fn_is_target=lambda node: node.name[-1] == "Z"))

        print(f"Second part solution = {math.lcm(*steps_list)}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")
