from dataclasses import dataclass


@dataclass
class Point:
    y: int
    x: int

    def __hash__(self):
        return hash((self.y, self.x))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)


@dataclass
class Grid:
    square_rocks: list[list[bool]]

    def print_map(self, round_rocks):
        for y, line in enumerate(self.square_rocks):
            for x, val in enumerate(line):
                if Point(y, x) in round_rocks:
                    print("O", end="")
                elif val:
                    print("#", end="")
                else:
                    print(".", end="")
            print(f"  {len(self.square_rocks) - y}")
        print(sorted(round_rocks))


def part_one(input_file: str):
    grid, round_rocks = get_grid(input_file)
    moved = True

    while moved:
        moved = False
        for round_rock in sorted(round_rocks, key=lambda p: (p.y, p.x)):
            if round_rock.y < 1:
                continue
            new_y = round_rock.y - 1
            new_point = Point(new_y, round_rock.x)
            if not grid.square_rocks[new_y][round_rock.x] and new_point not in round_rocks:
                round_rocks.remove(round_rock)
                round_rocks.add(new_point)
                moved = True

    grid_h = len(grid.square_rocks)
    return sum(grid_h - round_rock.y for round_rock in round_rocks)


def part_two(input_file: str):
    raise NotImplementedError


def get_grid(input_file: str) -> tuple[Grid, set[Point]]:
    round_rocks = set()
    square_rocks = []
    with open(input_file) as f:
        for y, line in enumerate(f.readlines()):
            square_line = []
            for x, value in enumerate(line.strip()):
                if value == "O":
                    round_rocks.add(Point(y, x))
                    square_line.append(False)
                elif value == ".":
                    square_line.append(False)
                elif value == "#":
                    square_line.append(True)
                else:
                    raise ValueError(f"Invalid value {value}")
            square_rocks.append(square_line)
    return Grid(square_rocks), round_rocks
