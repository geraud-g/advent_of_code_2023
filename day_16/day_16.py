from collections import deque
from copy import copy
from dataclasses import dataclass

EMPTY = "."
SLASH = "/"
BSLASH = "\\"
VERTICAL = "|"
HORIZONTAL = "-"

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


@dataclass
class Beam:
    y: int
    x: int
    direction: int

    def advance(self):
        y_delta, x_delta = DIRECTIONS[self.direction]
        self.y += y_delta
        self.x += x_delta

    def rotate_slash(self):
        self.direction = {
            NORTH: EAST,
            EAST: NORTH,
            SOUTH: WEST,
            WEST: SOUTH,
        }[self.direction]

    def rotate_bslash(self):
        self.direction = {
            NORTH: WEST,
            EAST: SOUTH,
            SOUTH: EAST,
            WEST: NORTH,
        }[self.direction]

    def __hash__(self):
        return hash((self.y, self.x, self.direction))


class MirrorMap:
    def __init__(self, mirrors: list[list[str]]):
        self.beams = deque([Beam(0, 0, EAST)])
        self.mirrors = mirrors
        self.history = set()

    def clear(self):
        """Reset the MirrorMap instance to a new state, by cleaning the history and beams"""
        self.beams = deque()
        self.history = set()

    def process(self):
        while self.beams:
            current_beam = self.beams.pop()
            self.process_beam(current_beam)

    def process_beam(self, beam: Beam):
        while True:
            if beam in self.history or self.out_of_map(beam):
                return

            self.history.add(copy(beam))
            tile = self.mirrors[beam.y][beam.x]

            if tile == SLASH:
                beam.rotate_slash()
            elif tile == BSLASH:
                beam.rotate_bslash()
            elif tile == VERTICAL and beam.direction in (EAST, WEST):
                up_beam = Beam(beam.y - 1, beam.x, NORTH)
                down_beam = Beam(beam.y + 1, beam.x, SOUTH)
                self.beams.append(up_beam)
                self.beams.append(down_beam)
                return

            elif tile == HORIZONTAL and beam.direction in (NORTH, SOUTH):
                left_beam = Beam(beam.y, beam.x - 1, WEST)
                right_beam = Beam(beam.y, beam.x + 1, EAST)
                self.beams.append(left_beam)
                self.beams.append(right_beam)
                return
            beam.advance()

    def out_of_map(self, beam: Beam) -> bool:
        return beam.y < 0 or beam.x < 0 or beam.y >= len(self.mirrors) or beam.x >= len(self.mirrors[0])

    def get_energized_tiles(self) -> int:
        return len({(t.y, t.x) for t in self.history})


def part_one(input_file: str):
    mirror_map = get_mirrors_map(input_file)
    mirror_map.process()
    return mirror_map.get_energized_tiles()


def part_two(input_file: str):
    mirror_map = get_mirrors_map(input_file)
    max_energized_tiles_nbr = 0
    height = len(mirror_map.mirrors)
    width = len(mirror_map.mirrors[0])

    # Top -> South
    for x in range(width):
        mirror_map.clear()
        mirror_map.beams.append(Beam(0, x, SOUTH))
        mirror_map.process()
        max_energized_tiles_nbr = max(max_energized_tiles_nbr, mirror_map.get_energized_tiles())

    # Bottom -> North
    for x in range(width):
        mirror_map.clear()
        mirror_map.beams.append(Beam(height - 1, x, NORTH))
        mirror_map.process()
        max_energized_tiles_nbr = max(max_energized_tiles_nbr, mirror_map.get_energized_tiles())

    # Left -> East
    for y in range(height):
        mirror_map.clear()
        mirror_map.beams.append(Beam(y, 0, EAST))
        mirror_map.process()
        max_energized_tiles_nbr = max(max_energized_tiles_nbr, mirror_map.get_energized_tiles())

    # Right -> West
    for y in range(height):
        mirror_map.clear()
        mirror_map.beams.append(Beam(y, width - 1, WEST))
        mirror_map.process()
        max_energized_tiles_nbr = max(max_energized_tiles_nbr, mirror_map.get_energized_tiles())

    return max_energized_tiles_nbr


def get_mirrors_map(input_file: str) -> MirrorMap:
    mirrors = []
    with open(input_file) as f:
        for line in f.readlines():
            mirrors.append(list(line.strip()))
    return MirrorMap(mirrors)
