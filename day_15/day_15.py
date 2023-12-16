from dataclasses import dataclass


@dataclass
class Lens:
    label: str
    focal: int


def part_one(input_file: str):
    steps = get_steps(input_file)
    return sum(get_string_hash(step) for step in steps)


def part_two(input_file: str):
    steps = get_steps(input_file)
    boxes: list[list[Lens]] = [[] for _ in range(256)]

    for step in steps:
        if step.endswith("-"):
            remove_lens(boxes, step[:-1])
        else:
            label, focal_length = step.split("=")
            update_or_create_lens(boxes, label, int(focal_length))

    total = 0
    for box_nbr, box in enumerate(boxes):
        for idx, lens in enumerate(box):
            total += (box_nbr + 1) * (idx + 1) * lens.focal
    return total


def remove_lens(boxes: list[list[Lens]], label: str):
    box_idx = get_string_hash(label)
    boxes[box_idx] = [lens for lens in boxes[box_idx] if lens.label != label]


def update_or_create_lens(boxes: list[list[Lens]], label: str, focal_length: int):
    box_idx = get_string_hash(label)
    for lens in boxes[box_idx]:
        if lens.label == label:
            lens.focal = focal_length
            return

    boxes[box_idx].append(Lens(label, focal_length))


def get_steps(input_file: str) -> list[str]:
    with open(input_file) as f:
        return f.read().strip().split(",")


def get_string_hash(step: str) -> int:
    current_value = 0
    for c in step:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value
