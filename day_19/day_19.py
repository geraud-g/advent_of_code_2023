import operator
import re
from collections import namedtuple
from dataclasses import dataclass

Rule = namedtuple("Rule", ["var", "op", "value", "dest"])


@dataclass
class Part:
    values: dict[str:int]

    def get_rating(self):
        return self.values["x"] + self.values["m"] + self.values["a"] + self.values["s"]


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    default: str

    def process(self, part: Part) -> str:
        for rule in self.rules:
            if rule.op(part.values[rule.var], rule.value):
                return rule.dest
        return self.default


def part_one(input_file: str) -> int:
    workflows, parts = parse_file(input_file)
    total_rating_score = 0
    for part in parts:
        if is_accepted(workflows, part):
            total_rating_score += part.get_rating()
    return total_rating_score


def is_accepted(workflows: dict[str:Workflow], part: Part) -> bool:
    current_workflow = "in"
    while current_workflow not in ("A", "R"):
        current_workflow = workflows[current_workflow].process(part)
    return current_workflow == "A"


def part_two(input_file: str) -> int:
    raise NotImplementedError


def parse_file(input_file: str) -> tuple[dict[str:Workflow], list[Part]]:
    with open(input_file) as f:
        raw_workflows, raw_parts = f.read().split("\n\n")
        workflows = get_workflows(raw_workflows)
        parts = get_parts(raw_parts)
    return workflows, parts


def get_workflows(raw_workflows: str) -> dict[str:Workflow]:
    workflows = dict()
    pattern = re.compile(r"^([a-zA-Z]+)([<>])(\d+):([a-zA-Z]+)")

    for line in raw_workflows.split("\n"):
        name, remainder = line.split("{")
        *raw_rules, default = remainder[:-1].split(",")
        rules = []
        for raw_rule in raw_rules:
            match = pattern.match(raw_rule)
            if match:
                op = operator.lt if match.group(2) == "<" else operator.gt
                rules.append(Rule(match.group(1), op, int(match.group(3)), match.group(4)))
        workflow = Workflow(name, rules, default)
        workflows[name] = workflow
    return workflows


def get_parts(raw_parts: str) -> list[Part]:
    parts = []
    for line in raw_parts.strip().split("\n"):
        raw_values = line[1:-1].split(",")
        values = dict()
        for val in raw_values:
            split_val = val.split("=")
            values[split_val[0]] = int(split_val[1])
        parts.append(Part(values))
    return parts
