import heapq
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from enum import Enum


def part_one(input_file: str):
    graph = get_graph(input_file)
    start_node = Node(0, 0, 3, Direction.EAST)
    distances, came_from, end = dijkstra(graph, start_node.copy())

    return distances[end] - graph.crucibles[-1][-1] + 1


def part_two(input_file: str):
    raise NotImplementedError


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


@dataclass
class Node:
    y: int
    x: int
    remaining_steps: int
    direction: Direction

    # turned: bool = False

    def copy(self):
        return copy(self)

    def move(self):
        y_delta, x_delta = self.direction.value
        self.y += y_delta
        self.x += x_delta
        self.remaining_steps -= 1

    def turn_left(self):
        self.direction = {
            Direction.NORTH: Direction.WEST,
            Direction.EAST: Direction.NORTH,
            Direction.SOUTH: Direction.EAST,
            Direction.WEST: Direction.SOUTH,
        }[self.direction]
        self.remaining_steps = 3

    def turn_right(self):
        self.direction = {
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH,
        }[self.direction]
        self.remaining_steps = 3

    def __hash__(self):
        return hash((self.y, self.x, self.remaining_steps, self.direction))

    def __lt__(self, other):
        if self.remaining_steps == other.remaining_steps:
            return (self.y, self.x) < (other.y, other.x)
        return self.remaining_steps < other.remaining_steps


class Graph:
    def __init__(self, crucibles: list[list[int]]):
        self.crucibles: list[list[int]] = crucibles
        self.width = len(crucibles[0])
        self.height = len(crucibles)
        # self.size = self.width * self.height

    def get_neighbors(self, node: Node):
        yield from self.advance(node)

        left_node = node.copy()
        left_node.turn_left()
        yield from self.advance(left_node)

        right_node = node.copy()
        right_node.turn_right()
        yield from self.advance(right_node)

    def advance(self, node: Node):
        if node.remaining_steps <= 0:
            return

        tmp_node = node.copy()
        weight = 0
        while tmp_node.remaining_steps > 0:
            tmp_node = tmp_node.copy()
            tmp_node.move()
            if self.out_of_map(tmp_node):
                return
            weight += self.crucibles[tmp_node.y][tmp_node.x]
            yield tmp_node, weight

    def out_of_map(self, node: Node) -> bool:
        return node.y < 0 or node.x < 0 or node.y >= self.height or node.x >= self.width


def dijkstra(graph: Graph, start: Node):
    distances = defaultdict(lambda: float("inf"))
    predecessors = {}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph.get_neighbors(current_vertex):
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

            if (neighbor.x == graph.width - 1) and (neighbor.y == graph.height - 1):
                return distances, predecessors, neighbor

    raise ValueError("No solution found for the given graph")


def get_path(predecessors, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = predecessors[current]
    path.append(start)
    path.reverse()
    return path


def get_graph(input_file: str) -> Graph:
    crucibles = []
    with open(input_file) as f:
        for y, line in enumerate(f.readlines()):
            crucible_row = []
            for x, value in enumerate(line.strip()):
                crucible_row.append(int(value))
            crucibles.append(crucible_row)
    return Graph(crucibles)
