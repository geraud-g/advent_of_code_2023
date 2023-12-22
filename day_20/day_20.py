from collections import deque
from dataclasses import dataclass, field
from typing import NamedTuple


class Pulse(NamedTuple):
    src: str
    type: bool
    dst: str


LOW: bool = False
HIGH: bool = True
OFF: bool = False
ON: bool = True


@dataclass
class Module:
    name: str
    destinations: list[str] = field(default_factory=list)

    def receive(self, pulse: bool, _source: "Module", _pulses: deque):
        raise NotImplementedError

    def send_pulse(self, pulse: bool, pulses: deque):
        for dst in self.destinations:
            pulses.append(Pulse(self.name, pulse, dst))


@dataclass
class Rx(Module):
    last_signal: bool = None

    def receive(self, pulse: bool, _source: Module, _pulses: deque):
        self.last_signal = pulse


@dataclass
class Broadcaster(Module):
    def receive(self, pulse: bool, _source: Module, pulses: deque):
        self.send_pulse(pulse, pulses)


@dataclass
class FlipFlop(Module):
    state: bool = OFF

    def receive(self, pulse: bool, _source: Module, pulses: deque):
        if pulse == LOW:
            if self.state == OFF:
                self.state = ON
                self.send_pulse(HIGH, pulses)
            else:
                self.state = OFF
                self.send_pulse(LOW, pulses)


@dataclass
class Conjunction(Module):
    name: str
    state: bool = OFF
    inputs: dict[str:bool] = field(default_factory=dict)

    def receive(self, pulse: bool, source: Module, pulses: deque):
        self.inputs[source.name] = pulse
        if all(val == HIGH for val in self.inputs.values()):
            self.send_pulse(LOW, pulses)
        else:
            self.send_pulse(HIGH, pulses)


def part_one(input_file: str):
    modules = get_modules(input_file)
    pulses = deque()
    low_nbr = 0
    high_nbr = 0

    for i in range(1000):
        pulses.append(Pulse("button", LOW, "broadcaster"))
        while pulses:
            pulse = pulses.popleft()
            if pulse.type == HIGH:
                high_nbr += 1
            else:
                low_nbr += 1
            module = modules[pulse.dst]
            module.receive(pulse.type, modules.get(pulse.src), pulses)

    return low_nbr * high_nbr


def part_two(input_file: str):
    raise NotImplementedError


def get_modules(input_file: str) -> dict[str:Module]:
    modules = dict()
    with open(input_file) as f:
        lines = [line.strip().split(" -> ") for line in f.readlines()]

    for module_name, dst in lines:
        destinations = dst.split(", ")
        if module_name.startswith("%"):
            modules[module_name[1:]] = FlipFlop(module_name[1:], destinations=destinations)
        elif module_name.startswith("&"):
            modules[module_name[1:]] = Conjunction(module_name[1:], destinations=destinations)
        elif module_name == "broadcaster":
            modules[module_name] = Broadcaster(module_name, destinations=destinations)

    for module_name, dst in lines:
        destinations = dst.split(", ")
        for dest in destinations:
            if dest not in modules:
                modules[dest] = Rx(dest)
            if type(modules[dest]) is Conjunction:
                if module_name[1:] not in modules[dest].inputs:
                    modules[dest].inputs[module_name[1:]] = LOW

    return modules
