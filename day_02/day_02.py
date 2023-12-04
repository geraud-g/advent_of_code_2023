from dataclasses import dataclass


@dataclass
class Cubes:
    red: int
    green: int
    blue: int


@dataclass
class Game:
    id: int
    max_colors_nbr: Cubes


def part_one(input_file: str) -> int:
    games = get_input(input_file)
    max_cubes = Cubes(red=12, green=13, blue=14)
    possible_games_ids = [game.id for game in games if has_game_enough_cubes(game, max_cubes)]
    return sum(possible_games_ids)


def part_two(input_file: str) -> int:
    games = get_input(input_file)
    return sum(get_game_power(game) for game in games)


def parse_handful(handful_str: str) -> Cubes:
    color_counts = {"red": 0, "blue": 0, "green": 0}
    for part in handful_str.split(", "):
        count, color = part.strip().split(" ")
        color_counts[color] = int(count)
    return Cubes(**color_counts)


def get_input(input_file: str) -> list[Game]:
    games = []
    with open(input_file) as f:
        for line in f.readlines():
            left, right = line.split(":")
            game_id = int(left.split(" ")[-1])
            handfuls = [parse_handful(handful) for handful in right.split(";")]
            red = max(handful.red for handful in handfuls)
            blue = max(handful.blue for handful in handfuls)
            green = max(handful.green for handful in handfuls)
            games.append(Game(id=game_id, max_colors_nbr=Cubes(red=red, blue=blue, green=green)))
    return games


def has_game_enough_cubes(game: Game, handful: Cubes) -> bool:
    return (
        game.max_colors_nbr.red <= handful.red
        and game.max_colors_nbr.green <= handful.green
        and game.max_colors_nbr.blue <= handful.blue
    )


def get_game_power(game: Game) -> int:
    return game.max_colors_nbr.red * game.max_colors_nbr.green * game.max_colors_nbr.blue
