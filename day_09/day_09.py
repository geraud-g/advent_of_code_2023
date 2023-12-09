from itertools import tee


def part_one(input_file: str) -> int:
    sequences = get_sequences(input_file)
    return sum(map(get_last_sequence_number, sequences))


def part_two(input_file: str):
    sequences = get_sequences(input_file)
    return sum(map(get_first_sequence_number, sequences))


def get_sequences(input_file: str) -> list[list[int]]:
    sequences = []
    with open(input_file) as f:
        for line in f.readlines():
            sequences.append([int(n) for n in line.split()])
    return sequences


def get_last_sequence_number(sequence: list[int]) -> int:
    sequences = get_sequence_differences_list(sequence)

    # Step 2: Find next number from last to first
    for idx in reversed(range(0, len(sequences) - 1)):
        left_nbr = sequences[idx][-1]
        prev_nbr = sequences[idx + 1][-1]
        sequences[idx].append(left_nbr + prev_nbr)

    return sequences[0][-1]


def get_sequence_differences_list(sequence: list[int]) -> list[list[int]]:
    """Generates a list of difference sequences from an input sequence
        until a sequence of all zeros is reached.

    Example:
        >>> get_sequence_differences_list([1, 3, 6, 10, 15, 21])
        [[1, 3, 6, 10, 15, 21], [2, 3, 4, 5, 6], [1, 1, 1, 1], [0, 0, 0]]
    """
    sequences = [sequence]
    current_sequence = sequence

    while not all(n == 0 for n in current_sequence):
        current_sequence = [y - x for (x, y) in pairwise(current_sequence)]
        sequences.append(current_sequence)
    return sequences


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def get_first_sequence_number(sequence: list[int]) -> int:
    sequences = get_sequence_differences_list(sequence)

    for idx in reversed(range(0, len(sequences) - 1)):
        right_nbr = sequences[idx][0]
        prev_nbr = sequences[idx + 1][0]
        sequences[idx].insert(0, right_nbr - prev_nbr)

    return sequences[0][0]
