from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class Point:
    y: int
    x: int

    def get_neighbours(self) -> Iterable["Point"]:
        yield Point(self.y - 1, self.x)
        yield Point(self.y, self.x + 1)
        yield Point(self.y + 1, self.x)
        yield Point(self.y, self.x - 1)

    def __hash__(self):
        return hash((self.y, self.x))


def part_one(input_file: str):
    start, rock_map = get_input(input_file)
    max_distance = 64
    distances = bfs(rock_map, start, max_distance)
    return sum(1 for v in distances.values() if v % 2 == 0 and v <= max_distance)


def part_two(input_file: str):
    raise NotImplementedError


def get_input(input_file: str) -> tuple[Point, list[list[bool]]]:
    start = None
    rock_map = []
    with open(input_file) as f:
        for y, line in enumerate(f.readlines()):
            map_line = []
            for x, val in enumerate(line.strip()):
                if val == "S":
                    start = Point(y, x)
                    map_line.append(False)
                elif val == ".":
                    map_line.append(False)
                else:
                    map_line.append(True)
            rock_map.append(map_line)
    return start, rock_map


def bfs(graph: list[list[bool]], start: Point, max_distance: int) -> dict[Point:int]:
    visited = {start}
    queue = deque()
    queue.append((0, start))
    distances = {start: 0}
    height, width = len(graph), len(graph[0])

    while queue:
        distance, current_point = queue.popleft()

        for neighbor in current_point.get_neighbours():
            if (
                distance < max_distance
                and neighbor not in visited
                and not graph[neighbor.y % height][neighbor.x % width]
            ):
                visited.add(neighbor)
                queue.append((distance + 1, neighbor))
                distances[neighbor] = distance + 1

    return distances
