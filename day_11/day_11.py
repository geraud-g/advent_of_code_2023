from dataclasses import dataclass
from itertools import combinations


@dataclass
class Point:
    y: int
    x: int


def part_one(input_file: str) -> int:
    return get_galaxies_distances_sum(input_file, 1)


def get_galaxies_distances_sum(input_file: str, expansion_rate: int):
    galaxies, galaxies_map = get_galaxies_and_map(input_file)
    expanded_parts = get_expanded_parts(galaxies_map)

    total = 0
    for point_a, point_b in combinations(galaxies, 2):
        distance = manhattan_distance(point_a, point_b)
        distance += get_additional_expanded_distance(expanded_parts, point_a, point_b, expansion_rate)
        total += distance
    return total


def get_galaxies_and_map(input_file: str) -> [list[Point], list[list[bool]]]:
    galaxies = []
    galaxies_map = []
    with open(input_file) as f:
        lines = f.readlines()
    for y, line in enumerate(lines):
        new_line = []
        for x, value in enumerate(line):
            if value == "#":
                new_line.append(True)
                galaxies.append(Point(y, x))
            else:
                new_line.append(False)
        galaxies_map.append(new_line)
    return galaxies, galaxies_map


def get_expanded_parts(galaxies_map: list[list[bool]]) -> [set[int], set[int]]:
    empty_y_set = set()
    empty_y_s = set()

    for y, line in enumerate(galaxies_map):
        if all(not val for val in line):
            empty_y_set.add(y)

    # Rotate map 90 degrees clockwise
    # from https://stackoverflow.com/a/8421412
    rotated_map = list(zip(*galaxies_map[::-1]))
    for x, col in enumerate(rotated_map):
        if all(not val for val in col):
            empty_y_s.add(x)
    return empty_y_set, empty_y_s


def get_additional_expanded_distance(
    expanded_parts: [set[int], set[int]], point_a: Point, point_b: Point, distance_coef: int
) -> int:
    min_y, max_y = sorted([point_a.y, point_b.y])
    min_x, max_x = sorted([point_a.x, point_b.x])
    empty_y_set = set(range(min_y, max_y + 1)) & expanded_parts[0]
    empty_x_set = set(range(min_x, max_x + 1)) & expanded_parts[1]
    return (len(empty_y_set) + len(empty_x_set)) * distance_coef


def manhattan_distance(point_a: Point, point_b: Point):
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)


def part_two(input_file: str):
    return get_galaxies_distances_sum(input_file, 999999)
