import re
from functools import reduce
from itertools import cycle
from math import gcd


def part_one(input_file: str) -> int:
    instructions, nodes = parse_input(input_file)
    return get_steps_until_z(instructions, nodes, "AAA", r"^ZZZ$")


def part_two(input_file: str) -> int:
    instructions, nodes = parse_input(input_file)
    steps_until_z_list = []
    for node in nodes.keys():
        if node.endswith("A"):
            steps_until_z = get_steps_until_z(instructions, nodes, node, r"Z$")
            steps_until_z_list.append(steps_until_z)
    return lcm_of_list(steps_until_z_list)


def get_steps_until_z(instructions: str, nodes: dict, node: str, end_pattern: str) -> int:
    instructions = cycle(instructions)
    counter = 0
    while not re.search(end_pattern, node):
        current_instruction = next(instructions)
        if current_instruction == "L":
            node = nodes[node][0]
        else:
            node = nodes[node][1]
        counter += 1
    return counter


def lcm_of_list(numbers: list[int]) -> int:
    return reduce((lambda x, y: int(x * y / gcd(x, y))), numbers)


def parse_input(input_file: str) -> tuple[str, dict]:
    with open(input_file) as f:
        split_file = f.read().split("\n\n")
        instructions = split_file[0].strip()
        nodes = dict()
        for line in split_file[1].splitlines():
            key, connections = line.split(" = ")
            left, right = connections[1:-1].split(", ")
            nodes[key] = (left, right)
    return instructions, nodes
