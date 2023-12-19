from dataclasses import dataclass
from itertools import tee


@dataclass
class Point:
    y: int
    x: int


def part_one(input_file: str) -> int:
    points = get_points(input_file)
    return get_lava_cubic_meters(points)


def part_two(input_file: str):
    points = get_points(input_file, part=2)
    return get_lava_cubic_meters(points)


def get_lava_cubic_meters(points: list[Point]) -> int:
    boundary_len = 0
    shoelace_area = 0

    for point_a, point_b in pairwise(points):
        shoelace_area += (point_a.x * point_b.y - point_b.x * point_a.y) / 2.0
        boundary_len += manhattan_distance(point_a, point_b)
    pick_area = shoelace_area - boundary_len / 2 + 1
    return int(boundary_len + pick_area)


def manhattan_distance(point_a: Point, point_b: Point):
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)


def get_points(input_file: str, part: int = 1) -> list[Point]:
    points = [Point(0, 0)]
    y, x = 0, 0
    with open(input_file) as f:
        for line in f.readlines():
            if part == 1:
                direction, steps, _colors = line.split()
            else:
                _direction, _steps, colors = line.split()
                steps = int(colors[2:7], 16)
                direction = "RDLU"[int(colors[7])]

            if direction == "U":
                y -= int(steps)
            elif direction == "R":
                x += int(steps)
            elif direction == "D":
                y += int(steps)
            elif direction == "L":
                x -= int(steps)
            else:
                raise ValueError
            points.append(Point(y, x))

    return points


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
