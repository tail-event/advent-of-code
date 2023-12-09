import os


def find_diff_sequence(sequence: list[int]) -> list[int]:
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]


def solve(sequences: list[list[int]]) -> tuple[int, int]:
    first_part_res, second_part_res = 0, 0
    for sequence in sequences:
        curr = sequence
        last_values, reduced = [curr[-1]], [curr]
        while not all(x == 0 for x in curr):
            curr = find_diff_sequence(curr)
            last_values.append(curr[-1])
            reduced.append(curr)
        first_part_res += sum(last_values)

        backward_preds = [0]
        for red in reversed(reduced):
            first_value = red[0]
            backward_preds.append(first_value - backward_preds[-1])

        second_part_res += backward_preds[-1]

    return first_part_res, second_part_res


if __name__ == "__main__":
    import time

    t0 = time.perf_counter()
    with open(os.path.join(os.path.dirname(__file__), "in.txt")) as f:
        sequences = []
        for line in f:
            sequences.append([int(x) for x in line.split()])

        first_part_res, second_part_res = solve(sequences)
        print(f"First part solution = {first_part_res}")
        print(f"Second part solution = {second_part_res}")
        print(f"Took {time.perf_counter() - t0:.5f} seconds.")
