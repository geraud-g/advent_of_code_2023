def part_one(input_file: str) -> int:
    calibration_values_sum = 0

    with open(input_file) as f:
        for line in f.readlines():
            line_digits = [char for char in line if char.isdigit()]
            calibration_values_sum += int(line_digits[0] + line_digits[-1])
    return calibration_values_sum


def part_two(input_file: str) -> int:
    calibration_values_sum = 0

    with open(input_file) as f:
        for line in f.readlines():
            line = convert_letters_to_digits(line)
            line_digits = [char for char in line if char.isdigit()]
            calibration_values_sum += int(line_digits[0] + line_digits[-1])
    return calibration_values_sum


def convert_letters_to_digits(string: str) -> str:
    """Replace each spelled letter in the string with its digit equivalent.

    Example:
        >>> convert_letters_to_digits("one2nine")
        "129"
    """
    digits = {
        "twone": "21",
        "oneight": "18",
        "eightwo": "82",
        "eighthree": "83",
        "sevenine": "79",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "zero": "0",
    }
    for word, digit in digits.items():
        string = string.replace(word, digit)
    return string
