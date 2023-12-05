import os
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True, slots=True)
class Interval:
    source: int
    dest: int
    range_: int

    def contains(self, x: int) -> bool:
        return self.source <= x < self.source + self.range_

    def get_target(self, x: int) -> Optional[int]:
        if self.contains(x):
            diff = x - self.source
            return self.dest + diff
        return None


@dataclass(slots=True)
class Match:
    num: int
    targets: list[int] = field(default_factory=list)
    matched_intervals: list[Interval] = field(default_factory=list)


@dataclass(slots=True)
class Mapping:
    intervals: list[Interval] = field(default_factory=list)

    def get_target(self, x: Match) -> Match:
        for interval in self.intervals:
            target = interval.get_target(x.targets[-1] if x.targets else x.num)
            if target is not None:
                x.targets.append(target)
                x.matched_intervals.append(interval)
                return x

        raise RuntimeError("Should never arrive here")

    def add_dummy_intervals(self) -> None:
        self.intervals = sorted(self.intervals, key=lambda i: i.source)
        dummy_intervals = []

        if self.intervals[0].source > 0:
            dummy_start = Interval(0, 0, self.intervals[0].source)
            dummy_intervals.append(dummy_start)

        for i in range(len(self.intervals) - 1):
            prev, next = self.intervals[i], self.intervals[i + 1]
            if next.source > prev.source + prev.range_:
                dummy_intervals.append(
                    Interval(
                        prev.source + prev.range_, prev.source + prev.range_, next.source - prev.source - prev.range_
                    )
                )

        self.intervals.extend(dummy_intervals)
        self.intervals = sorted(self.intervals, key=lambda i: i.source)

        last_interval = self.intervals[-1]
        self.intervals.append(Interval(last_interval.source, last_interval.source, int(1e20)))


def first_solution(cascade_maps: list[Mapping]) -> int:
    lowest_location: Optional[int] = None
    for seed in seeds:
        curr = Match(num=seed)
        for mapping in cascade_maps:
            curr = mapping.get_target(curr)
        lowest_location = curr.targets[-1] if lowest_location is None else min(lowest_location, curr.targets[-1])

    assert lowest_location is not None
    return lowest_location


def second_solution(cascade_maps: list[Mapping], seeds: list[int], ranges: list[int]) -> int:
    lowest: Optional[int] = None

    for seed, seed_range in zip(seeds, ranges):
        num = seed
        can_skip = 0
        while True:
            curr = Match(num=num)

            for map in cascade_maps:
                curr = map.get_target(curr)

            lowest = curr.targets[-1] if lowest is None else min(curr.targets[-1], lowest)
            can_skip = min(
                [
                    (curr.matched_intervals[i].dest + curr.matched_intervals[i].range_) - curr.targets[i] - 1
                    for i in range(len(curr.matched_intervals))
                ]
            )
            num += max(can_skip, 1)
            if num >= seed + seed_range:
                break

    assert lowest is not None
    return lowest


if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
        blocks = f.read().split("\n\n")

        seeds = [int(x) for x in blocks[0].split(": ")[1].split()]
        cascade_maps = []

        for mapping in blocks[1:]:
            new_map = Mapping()
            name, data_s = mapping.split(":\n")
            for line_data in data_s.split("\n"):
                dest, source, range_ = [int(x) for x in line_data.split()]
                new_map.intervals.append(Interval(source, dest, range_))

            cascade_maps.append(new_map)
            new_map.add_dummy_intervals()

        print("First part solution", first_solution(cascade_maps))
        print(f"Took {time.perf_counter() - t0:.5f} seconds")

        print("Second part solution", second_solution(cascade_maps, seeds[0::2], seeds[1::2]))
        print(f"Took {time.perf_counter() - t0:.5f} seconds")
