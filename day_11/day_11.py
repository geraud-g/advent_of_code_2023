from dataclasses import dataclass


@dataclass
class Point:
    y: int
    x: int


def part_one(input_file: str):
    galaxies_map = get_galaxies_map(input_file)
    expanded_map = expand_galaxies_map(galaxies_map)
    galaxies = get_galaxies(expanded_map)

    total = 0
    for idx, point_a in enumerate(galaxies[:-1]):
        for point_b in galaxies[idx + 1 :]:
            total += manhattan_distance(point_a, point_b)
    return total


def get_galaxies_map(input_file: str) -> list[list[bool]]:
    galaxies_map = []
    with open(input_file) as f:
        for line in f.readlines():
            new_line = [value == "#" for value in line.strip()]
            galaxies_map.append(new_line)
    return galaxies_map


def expand_galaxies_map(galaxies_map: list[list[bool]]) -> list[list[bool]]:
    half_expanded_map = expand_map_vertically(galaxies_map)
    # Rotate map 90 degrees clockwise
    half_expanded_map = list(zip(*half_expanded_map[::-1]))
    fully_expanded_map = expand_map_vertically(half_expanded_map)
    # Rotate 90 degrees counter-clockwise
    fully_expanded_map = list(reversed(list(zip(*fully_expanded_map))))
    return fully_expanded_map


def expand_map_vertically(galaxies_map: list[list[bool]]):
    expanded_map = []
    for line in galaxies_map:
        expanded_map.append(line)
        if all(not val for val in line):
            expanded_map.append(line)
    return expanded_map


def get_galaxies(galaxies_map: list[list[bool]]) -> list[Point]:
    galaxies = []
    for y, line in enumerate(galaxies_map):
        for x, val in enumerate(line):
            if val:
                galaxies.append(Point(y, x))
    return galaxies


def manhattan_distance(point_a: Point, point_b: Point):
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)


def part_two(input_file: str):
    raise NotImplementedError
