import os
import time
from collections import defaultdict

if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as f:
        card_to_num: dict[int, int] = defaultdict(int)
        first_part_sum = 0

        for line in f:
            card_and_nums_s, winning_nums_s = line.split(" | ")
            card_s, nums_s = card_and_nums_s.split(": ")

            card_num = int(card_s.split()[1])
            nums = set(int(x) for x in nums_s.strip().split())
            winning_nums = set(int(x) for x in winning_nums_s.strip().split())

            card_to_num[card_num] += 1
            n_winning = len(nums & winning_nums)
            if n_winning:
                # First part solution
                first_part_sum += 1 * 2 ** (n_winning - 1)

                # Second part solution
                for i in range(n_winning):
                    card_to_num[card_num + i + 1] += card_to_num[card_num]

        print(f"First part solution={first_part_sum}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")

        print(f"Second part solution={sum(card_to_num.values())}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")
