import itertools

RECORD_OPERATIONAL: str = "."
RECORD_DAMAGED: str = "#"
RECORD_UNKNOWN: str = "?"

STATUS_INVALID = -1
STATUS_NO_FINISHED = 0
STATUS_VALID = 1


class Spring:
    def __init__(self, record: list[str], checksum: list[int]):
        self.record_idx: int = 0
        self.remaining_unknown = len([r == RECORD_UNKNOWN for r in record])
        self.record: list[str] = record
        self.checksum: list[int] = checksum
        self.checksum_idx: int = 0
        self.end_of_last_damaged_group_idx: int = 0


def part_one(input_file: str) -> int:
    springs = get_springs(input_file)
    total_valid_combinations = 0
    for spring in springs:
        total_valid_combinations += count_valid_combinations(spring)
    return total_valid_combinations


def get_springs(input_file: str) -> list[Spring]:
    springs = []
    with open(input_file) as f:
        for line in f.readlines():
            left, right = line.split()
            checksum = list(map(int, right.split(",")))
            springs.append(Spring(list(left), checksum))
    return springs


def count_valid_combinations(spring: Spring) -> int:
    while spring.record_idx < len(spring.record) and spring.record[spring.record_idx] != RECORD_UNKNOWN:
        spring.record_idx += 1

    if spring.record_idx == len(spring.record):
        return 1 if is_valid(spring) else 0

    initial_record_idx = spring.record_idx
    initial_checksum_idx = spring.checksum_idx
    initial_end_of_last_damaged_group_idx = spring.end_of_last_damaged_group_idx
    valid_combinations = 0

    spring.record[initial_record_idx] = RECORD_OPERATIONAL
    if not is_invalid(spring):
        valid_combinations += count_valid_combinations(spring)
        spring.record_idx = initial_record_idx
        spring.checksum_idx = initial_checksum_idx
        spring.end_of_last_damaged_group_idx = initial_end_of_last_damaged_group_idx

    spring.record[initial_record_idx] = RECORD_DAMAGED
    if not is_invalid(spring):
        valid_combinations += count_valid_combinations(spring)
        spring.record_idx = initial_record_idx
        spring.checksum_idx = initial_checksum_idx
        spring.end_of_last_damaged_group_idx = initial_end_of_last_damaged_group_idx

    # We reset the tile we changed
    # This way we reset the record between 2 branches
    spring.record[initial_record_idx] = RECORD_UNKNOWN

    return valid_combinations


def is_invalid(spring: Spring) -> bool:
    # import itertools
    # damages = [len(list(g)) for k, g in itertools.groupby(spring.record) if k == RECORD_DAMAGED]
    #
    #
    # broken_group_open = False
    # broken_group_min_size = 0
    # broken_group_max_size = 0
    # checksum_idx = 0
    #
    # for idx, value in enumerate(spring.record):
    #     # #
    #     # ?
    #     # .
    #     pass
    #
    # # checksum is not finished
    # # checksum is finished and there is more `broken` parts
    # # group the broken bits

    # group DAMAGED
    # if DAMAGED

    # TODO -> V2
    # broken_group_open = False
    # broken_group_size = 0
    # checksum_idx = 0
    # for idx in range(0, spring.record_idx + 1):
    #     if spring.record[idx] == "#":
    #         broken_group_size += 1
    #         broken_group_open = True
    #     elif spring.record[idx] == ".":
    #         if broken_group_open:
    #             if checksum_idx >= len(spring.checksum) or spring.checksum[checksum_idx] != broken_group_size:
    #                 return False
    #             else:
    #                 broken_group_size = 0
    #                 broken_group_open = False
    #                 checksum_idx += 1
    #
    #     else:
    #         raise ValueError("? found in substring")

    # TODO : V3
    # now from end_last_damaged_group to idx
    broken_group_open = False
    broken_group_size = 0
    # checksum_idx = 0
    for idx in range(spring.end_of_last_damaged_group_idx, spring.record_idx + 1):
        if spring.record[idx] == "#":
            broken_group_size += 1
            broken_group_open = True
        elif spring.record[idx] == ".":
            if broken_group_open:
                if (
                    spring.checksum_idx >= len(spring.checksum)
                    or spring.checksum[spring.checksum_idx] != broken_group_size
                ):
                    return False
                else:
                    broken_group_size = 0
                    broken_group_open = False
                    spring.checksum_idx += 1
                    spring.end_of_last_damaged_group_idx = idx

        else:
            raise ValueError("? found in substring")
    return False


def is_valid(spring: Spring) -> bool:
    damages = [len(list(g)) for k, g in itertools.groupby(spring.record) if k == RECORD_DAMAGED]
    return damages == spring.checksum


def part_two(input_file: str):
    raise NotImplementedError
