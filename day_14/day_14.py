class Grid:
    def __init__(self, square_rocks: list[list[bool]], round_rocks: list[list[bool]], width: int, height: int):
        self.square_rocks: list[list[bool]] = square_rocks
        self.round_rocks: list[list[bool]] = round_rocks
        self.width: int = width
        self.height: int = height

    def tilt_up(self):
        moved = False
        for y in range(1, self.height):
            for x in range(self.width):
                if self.round_rocks[y][x] and not self.round_rocks[y - 1][x] and not self.square_rocks[y - 1][x]:
                    self.round_rocks[y][x] = False
                    self.round_rocks[y - 1][x] = True
                    moved = True
        return moved

    def tilt_down(self):
        moved = False
        for y in reversed(range(self.height - 1)):
            for x in range(self.width):
                if self.round_rocks[y][x] and not self.round_rocks[y + 1][x] and not self.square_rocks[y + 1][x]:
                    self.round_rocks[y][x] = False
                    self.round_rocks[y + 1][x] = True
                    moved = True
        return moved

    def tilt_right(self):
        moved = False
        for y in range(self.height):
            for x in reversed(range(self.width - 1)):
                if self.round_rocks[y][x] and not self.round_rocks[y][x + 1] and not self.square_rocks[y][x + 1]:
                    self.round_rocks[y][x] = False
                    self.round_rocks[y][x + 1] = True
                    moved = True
        return moved

    def tilt_left(self):
        moved = False
        for y in range(self.height):
            for x in range(1, self.width):
                if self.round_rocks[y][x] and not self.round_rocks[y][x - 1] and not self.square_rocks[y][x - 1]:
                    self.round_rocks[y][x] = False
                    self.round_rocks[y][x - 1] = True
                    moved = True
        return moved

    def print_map(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.round_rocks[y][x]:
                    print("O", end="")
                elif self.square_rocks[y][x]:
                    print("#", end="")
                else:
                    print(".", end="")
            print()


def part_one(input_file: str):
    grid = get_grid(input_file)

    while grid.tilt_up():
        pass

    total = 0
    for y, row in enumerate(grid.round_rocks):
        total += (grid.height - y) * sum(1 if val else 0 for val in row)
    return total


def part_two(input_file: str):
    # grid = get_grid(input_file)
    # cycles = 1000000000
    # remaining_cycles = cycles
    # history = set()
    raise NotImplementedError


def perform_cycle(grid: Grid):
    while grid.tilt_up():
        pass
    while grid.tilt_left():
        pass
    while grid.tilt_down():
        pass
    while grid.tilt_right():
        pass


def get_grid(input_file: str) -> Grid:
    round_rocks = []
    square_rocks = []
    with open(input_file) as f:
        for y, line in enumerate(f.readlines()):
            square_line = []
            round_line = []
            for x, value in enumerate(line.strip()):
                if value == "O":
                    round_line.append(True)
                    square_line.append(False)
                elif value == ".":
                    round_line.append(False)
                    square_line.append(False)
                elif value == "#":
                    round_line.append(False)
                    square_line.append(True)
                else:
                    raise ValueError(f"Invalid value {value}")
            square_rocks.append(square_line)
            round_rocks.append(round_line)
    width = len(square_rocks[0])
    height = len(square_rocks)
    return Grid(square_rocks, round_rocks, width, height)
