import importlib
import typer
from typing_extensions import Annotated


def day_callback(value: int):
    if value < 1 or value > 25:
        raise typer.BadParameter("Day must be between 1 and 25")
    return value


def main(day: Annotated[int, typer.Argument(callback=day_callback)], example: bool = False):
    try:
        day_str = f"day_{day:02d}"
        day = importlib.import_module(f"{day_str}.{day_str}")

        try:
            if example:
                input_file = f"{day_str}/input_example_part_1.txt"
            else:
                input_file = f"{day_str}/input.txt"
            print(f"Part 1: {day.part_one(input_file)}")
        except (AttributeError, NotImplementedError):
            print(f"{day_str}: Part one not implemented")
        try:
            if example:
                input_file = f"{day_str}/input_example_part_2.txt"
            else:
                input_file = f"{day_str}/input.txt"
            print(f"Part 2: {day.part_two(input_file)}")
        except (AttributeError, NotImplementedError):
            print(f"{day_str}: Part two not implemented")
    except ImportError:
        print(f"Day {day:02d} is not available yet")


if __name__ == "__main__":
    typer.run(main)