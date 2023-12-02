import os
import string
import time

if __name__ == "__main__":
    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt"), mode="r", encoding="utf-8") as file:
        sum = 0
        for line in file:
            line = line.strip()
            first, second = None, None

            # Find first digit
            for i in range(len(line)):
                if line[i] in string.digits:
                    first = int(line[i])
                    break

            # Find last digit
            for i in range(len(line) - 1, -1, -1):
                if line[i] in string.digits:
                    second = int(line[i])
                    break

            # print(f"Found digits: {first}{second}")
            sum += int(f"{first}{second}")

        print(f"{sum=}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds")
