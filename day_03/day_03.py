from collections.abc import Iterable
from itertools import product
from typing import Optional

Schematic = list[list[str]]


def part_one(input_file: str) -> int:
    schematic = get_schematic(input_file)
    part_numbers = []
    for (y, x), value in iterate_on_schematic(schematic):
        if x > 0 and schematic[y][x - 1].isdigit():
            continue  # this part number already has been evaluated
        if is_part_number(schematic, y, x):
            part_numbers.append(get_part_number(schematic, y, x))
    return sum(part_numbers)


def is_part_number(schematic: Schematic, y: int, x: int) -> bool:
    while x < len(schematic[y]) and schematic[y][x].isdigit():
        if touch_symbol(schematic, y, x):
            return True
        x += 1
    return False


def touch_symbol(schematic: Schematic, y: int, x: int) -> bool:
    for tmp_y, tmp_x in get_tile_neighbours(y, x):
        if 0 <= tmp_y < len(schematic) and 0 <= tmp_x < len(schematic[tmp_y]):
            value = schematic[tmp_y][tmp_x]
            if value != "." and not value.isdigit():
                return True
    return False


def get_part_number(schematic: Schematic, y: int, x: int, delete=False) -> Optional[None]:
    """Returns the complete number from this tile as an `int`, or `None`.

    A complete number is the concatenation of the digits linked to the initial tile on the x-axis.
    If the tile is not a digit, this function will return `None`
    If `delete` is set to `True`, each digit from the number will be replaced by `.` once read.
    """
    nbr = ""
    if not schematic[y][x].isdigit():
        return None
    while x >= 0 and schematic[y][x].isdigit():
        x -= 1
    x += 1
    while x < len(schematic[y]) and schematic[y][x].isdigit():
        nbr += schematic[y][x]
        if delete:
            schematic[y][x] = "."
        x += 1
    if not nbr:
        return None
    else:
        return int(nbr)


def part_two(input_file: str):
    schematic = get_schematic(input_file)
    total = 0
    for (y, x), value in iterate_on_schematic(schematic):
        if value == "*":
            numbers = get_surrounding_numbers(schematic, y, x)
            if len(numbers) == 2:
                total += numbers[0] * numbers[1]
    return total


def get_surrounding_numbers(schematic, y: int, x: int) -> list[int]:
    numbers = []
    for tmp_y, tmp_x in get_tile_neighbours(y, x):
        value = get_part_number(schematic, tmp_y, tmp_x, delete=True)
        if value:
            numbers.append(value)
    return numbers


def get_schematic(input_file: str) -> Schematic:
    schematic = []
    with open(input_file) as f:
        for line in f.readlines():
            schematic.append(list(line.strip()))
    return schematic


def iterate_on_schematic(
    schematic: Schematic,
) -> Iterable[tuple[tuple[int, int], str]]:
    for y, line in enumerate(schematic):
        for x, value in enumerate(line):
            yield (y, x), value


def get_tile_neighbours(y: int, x: int) -> Iterable[tuple[int, int]]:
    delta = [-1, 0, 1]
    for y_delta, x_delta in product(delta, delta):
        yield y + y_delta, x + x_delta
