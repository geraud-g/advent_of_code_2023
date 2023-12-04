from collections import defaultdict
from typing import Set, List, Tuple

Scratchcard = Tuple[Set[int], Set[int]]


def part_one(input_file: str) -> int:
    scratchcards = get_scratchcards(input_file)
    total = 0
    for winning_numbers, numbers in scratchcards:
        points = len(winning_numbers & numbers)
        if points > 0:
            total += 2 ** (points - 1)
    return total


def part_two(input_file: str) -> int:
    scratchcards = get_scratchcards(input_file)
    scratchcards_count = defaultdict(lambda: 1)
    for idx, (winning_numbers, numbers) in enumerate(scratchcards):
        points = len(winning_numbers & numbers)
        current_ticket_nbr = scratchcards_count[idx]
        for point in range(1, points + 1):
            scratchcards_count[idx + point] += current_ticket_nbr
    return sum(scratchcards_count.values())


def get_scratchcards(input_file: str) -> List[Scratchcard]:
    scratchcards = []
    with open(input_file) as f:
        for line in f.readlines():
            left, right = line.split(":")[1].split("|")
            scratchcard = set(map(int, left.split())), set(map(int, right.split()))
            scratchcards.append(scratchcard)
    return scratchcards
