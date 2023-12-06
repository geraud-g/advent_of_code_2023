import math


def part_one(input_file: str) -> int:
    races = get_races(input_file)
    total = 1
    for race_time, race_distance in races:
        winning_possibilities_count = get_race_win_possibilities_count(race_time, race_distance)
        total *= winning_possibilities_count
    return total


def part_two(input_file: str):
    race_time, race_distance = get_race(input_file)
    winning_possibilities_count = get_race_win_possibilities_count(race_time, race_distance)
    return winning_possibilities_count


def get_race_win_possibilities_count(race_time: int, race_distance: int) -> int:
    winning_possibilities_count = 0
    for holding_time in range(math.ceil(race_time / 2), race_time):
        if holding_time * (race_time - holding_time) > race_distance:
            winning_possibilities_count += 1
        else:
            break
    winning_possibilities_count *= 2
    if race_time % 2 == 0:
        winning_possibilities_count -= 1
    return winning_possibilities_count


def get_races(input_file: str) -> list[tuple[int, int]]:
    with open(input_file) as f:
        lines = f.readlines()
        times = [int(x) for x in lines[0].split() if x.isdigit()]
        distances = [int(x) for x in lines[1].split() if x.isdigit()]
        return list(zip(times, distances))


def get_race(input_file: str) -> tuple[int, int]:
    with open(input_file) as f:
        lines = f.readlines()
        time = int(lines[0].replace(" ", "").split(":")[1])
        distance = int(lines[1].replace(" ", "").split(":")[1])
        return time, distance
