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
    start, grid = get_input(input_file)
    _, right_node = grid[start.y][start.x]
    paths = bfs(grid, start)
    return (len(get_path(paths, right_node)) + 1) // 2


def get_input(input_file: str) -> (Point, list[list[list[Point]]]):
    with open(input_file) as f:
        raw_grid = f.read().split("\n")
    grid = []
    start_point = None
    for y, line in enumerate(raw_grid):
        grid_line = []
        for x, value in enumerate(line):
            if value == "S":
                start_point = Point(y, x)
                grid_line.append([])
            else:
                grid_line.append(get_connections(value, y, x))
        grid.append(grid_line)

    for neighbour in start_point.get_neighbours():
        if start_point in grid[neighbour.y][neighbour.x]:
            grid[start_point.y][start_point.x].append(neighbour)
    return start_point, grid


def get_connections(value: str, y: int, x: int) -> list[Point]:
    """Return the connections for a given value according to the following descriptions:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.

    Returns an empty array if the value is not part of these values.
    """
    # Each value is the delta in form [(y, x), (y, x)]
    connections_delta = {
        "|": [(-1, 0), (1, 0)],
        "-": [(0, -1), (0, 1)],
        "L": [(-1, 0), (0, 1)],
        "J": [(-1, 0), (0, -1)],
        "7": [(1, 0), (0, -1)],
        "F": [(1, 0), (0, 1)],
    }
    if value not in connections_delta:
        return []
    left_delta, right_delta = connections_delta[value]
    left_point = Point(y + left_delta[0], x + left_delta[1])
    right_point = Point(y + right_delta[0], x + right_delta[1])
    return [left_point, right_point]


def bfs(graph: list[list[list[Point]]], s_point: Point) -> dict[Point:Point]:
    starting_point_paths = graph[s_point.y][s_point.x]
    # We are looking to go from one side to the other side of the loop
    left_side, right_side = starting_point_paths[0], starting_point_paths[1]
    # We add `s_point` to `visited` as well,
    # to break the link between `left_side` and `right_side`
    visited = {s_point, left_side}
    queue = deque()
    queue.append(left_side)
    came_from = {left_side: None}

    while queue:
        current_point = queue.popleft()
        if current_point == right_side:
            return came_from

        for neighbor in graph[current_point.y][current_point.x]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current_point
    raise ValueError(f"Path from {left_side} to {right_side} not found")


def get_path(came_from: dict[Point:Point], start: Point) -> list[Point]:
    path = []
    current = start
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def part_two(input_file: str):
    raise NotImplementedError
