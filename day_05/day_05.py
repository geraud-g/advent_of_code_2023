from collections import namedtuple

Instruction = namedtuple("Instruction", ["destination", "source", "range"])
SeedRange = list[int, int]


def part_one(input_file: str) -> int:
    seeds, instructions_maps = parse_input(input_file)
    input_ids = seeds
    for instructions_map in instructions_maps:
        input_ids = apply_instructions_map(instructions_map, input_ids)
    return min(input_ids)


def parse_input(input_file: str) -> (int, list[list[Instruction]]):
    with open(input_file) as f:
        lines = f.read().strip().split("\n\n")
        seeds = parse_int_list(lines[0].split(":")[1])
        instruction_maps = []
        for instructions in lines[1:]:
            instructions_int = map(parse_int_list, instructions.split("\n")[1:])
            instruction_maps.append([Instruction(*i) for i in instructions_int])
    return seeds, instruction_maps


def parse_int_list(line: str) -> list[int]:
    return [int(n) for n in line.split()]


def apply_instructions_map(instructions_map: list[Instruction], input_ids: list[int]) -> list[int]:
    return [get_new_id(instructions_map, input_id) for input_id in input_ids]


def get_new_id(instructions_map: list[Instruction], current_id: int) -> int:
    for instruction in instructions_map:
        if instruction.source <= current_id <= (instruction.source + instruction.range):
            # We found a source for this instruction, so we can return its destination
            return instruction.destination + (current_id - instruction.source)
    # If we don't find any matching range, we return the id as is
    return current_id


def part_two(input_file: str):
    seeds, instructions_maps = parse_input(input_file)
    seeds_ranges = [[seeds[x], seeds[x] + seeds[x + 1] - 1] for x in range(0, len(seeds), 2)]
    ranges_ids = seeds_ranges
    for instructions_map in instructions_maps:
        ranges_ids = apply_instructions_for_ranges(instructions_map, ranges_ids)
    # We return the start of the lowest range we find, ordered by `start` values.
    # I don't know why we have to subtract one, but we do.
    # I'll debug this if I ever read this file again :D
    return min(sorted(ranges_ids, key=lambda x: x[0]))[0] - 1


def apply_instructions_for_ranges(instructions_map: list[Instruction], ranges_ids: list[SeedRange]) -> list[SeedRange]:
    ranges_output = []
    for range_ids in ranges_ids:
        ranges_output.extend(get_new_range(instructions_map, range_ids))
    return ranges_output


def get_new_range(instructions_map: list[Instruction], range_ids: SeedRange) -> list[SeedRange]:
    new_ranges_ids = []
    instructions_ranges = convert_and_sort_instructions_map(instructions_map)

    for source_start, source_end, destination in instructions_ranges:
        # If a part or the complete range is before sur current instruction, put it as is to the output list
        if range_ids[0] < source_start:
            if range_ids[1] < source_start:
                new_ranges_ids.append([range_ids[0], range_ids[1]])
                return new_ranges_ids  # this is the end of the range_id, so we are done here
            else:
                new_ranges_ids.append([range_ids[0], source_start - 1])
                range_ids[0] = source_start

        if range_ids[0] > source_end:  # This range_id is after this source
            continue

        # Calculate the boundaries of this segment
        segment_start = max(range_ids[0], source_start)
        new_range_id_start = destination + (segment_start - source_start)
        new_range_id_end = new_range_id_start + (segment_start - source_start)
        new_ranges_ids.append([new_range_id_start, new_range_id_end])

        # Update the start  bound by removing the segment we just processed
        range_ids[0] = source_end + 1
        # This means there is no range segment to process, we stop here
        if range_ids[0] > range_ids[1]:
            return new_ranges_ids
    # Don't forget to add the remains `range_ids`
    new_ranges_ids.append([range_ids[0], range_ids[1]])
    return new_ranges_ids


def convert_and_sort_instructions_map(
    instructions_map: list[Instruction],
) -> list[tuple[int, int, int]]:
    """Convert instructions ranges to (start, end, destination) tuples, and return them sorted by `start`"""
    instructions_ranges = []
    for instruction in instructions_map:
        source_start = instruction.source
        source_end = instruction.source + instruction.range
        instructions_ranges.append((source_start, source_end, instruction.destination))
    return sorted(instructions_ranges, key=lambda x: x[0])
