import os
import string
import time
from typing import Optional

num_mapping = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

num_reverse_mapping = {"".join(reversed(k)): v for k, v in num_mapping.items()}


def find_matching_digits(s: str, i: int, reverse: bool) -> Optional[int]:
    """Find first matching digit in string.

    Find first matching digit in string starting from a given index.
    This function can identify digits that are spelled out with letters.

    Examples:
        >>> find_matching_digits("xtwone3four", 0, reverse=False)
        None
        >>> find_matching_digits("xtwone3four", 1, reverse=False)
        2
        >>> find_matching_digits("xtwone3four", 10, reverse=True)
        4

    Args:
        s (str): the string.
        i (int): the starting index.
        reverse (bool): whether to find a match from right to left.

    Returns:
        Optional[int]: matching digit, if found.
    """
    if s[i] in string.digits:
        return int(s[i])

    mapping = num_reverse_mapping if reverse else num_mapping
    matching = list(mapping.keys())
    matching_idx = 0
    while True:
        new_matching = []
        for num_s in matching:
            if matching_idx < len(num_s):
                if num_s[matching_idx] == s[i + matching_idx * (-1 if reverse else 1)]:
                    if len(num_s) - 1 == matching_idx:
                        return mapping[num_s]
                    new_matching.append(num_s)

        matching = new_matching
        matching_idx += 1
        if not matching:
            return None


if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as file:
        sum = 0
        for line in file:
            line = line.strip()
            first, second = None, None

            # Find first digit
            for i in range(len(line)):
                match = find_matching_digits(line, i, reverse=False)
                if match is not None:
                    first = match
                    break

            # Find last digit
            for i in range(len(line) - 1, -1, -1):
                match = find_matching_digits(line, i, reverse=True)
                if match is not None:
                    second = match
                    break

            sum += int(f"{first}{second}")

        print(f"{sum=}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds")
