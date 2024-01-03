import os
import time
from dataclasses import dataclass, field
from typing import Optional


def hash_algo(s: str) -> int:
    curr = 0
    for ch in s:
        curr += ord(ch)
        curr *= 17
        curr = curr % 256
    return curr


@dataclass(slots=True)
class Lens:
    label: str
    focal_length: int


@dataclass(slots=True)
class Box:
    idx: int
    lens_map: dict[str, int] = field(default_factory=dict)
    lens: list[Optional[Lens]] = field(default_factory=list)

    def add_lens(self, lens: str, focal_length: int) -> None:
        if lens not in self.lens_map:
            self.lens.append(Lens(label=lens, focal_length=focal_length))
            self.lens_map[lens] = len(self.lens) - 1
        else:
            curr_idx = self.lens_map[lens]
            lens_to_update = self.lens[curr_idx]
            assert lens_to_update is not None
            lens_to_update.label = lens
            lens_to_update.focal_length = focal_length

    def remove_lens(self, lens: str) -> None:
        if lens not in self.lens_map:
            return

        self.lens[self.lens_map[lens]] = None
        del self.lens_map[lens]

    def get_value(self) -> int:
        total = 0
        final_lens = [lens for lens in self.lens if lens is not None]
        for i, lens in enumerate(final_lens):
            total += (1 + self.idx) * (i + 1) * lens.focal_length
        return total


def second_part_solution(data: str) -> int:
    boxes: list[Box] = [Box(idx=i) for i in range(256)]
    for s in data.split(","):
        if "=" in s:
            lens, focal_length_s = s.split("=")
            focal_length = int(focal_length_s)
            boxes[hash_algo(lens)].add_lens(lens, focal_length)
        elif "-" in s:
            lens = s.split("-")[0]
            boxes[hash_algo(lens)].remove_lens(lens)
        else:
            raise RuntimeError()

    return sum(box.get_value() for box in boxes)


if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), "r", encoding="utf-8") as f:
        data: str = f.read()
        first_part_res = sum(hash_algo(s) for s in data.split(","))
        print(f"First part solution = {first_part_res}.")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")

        second_part_res = second_part_solution(data)
        print(f"First part solution = {second_part_res}.")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")
