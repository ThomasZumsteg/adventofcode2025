"""Advent of Code Day 10 Solution."""

from dataclasses import dataclass
from get_input import get_input, line_parser
from scipy.optimize import linprog
import numpy as np


@dataclass
class Machine:
    lights: tuple[bool]
    buttons: list[tuple[int, ...]]
    joltage: tuple[int]

    def solve(self) -> int:
        previous = {tuple([False] * len(self.lights))}

        count = 0
        seen = set()
        while True:
            current = set()
            for state in previous:
                if state in seen:
                    continue
                if state == self.lights:
                    return count
                for button in self.buttons:
                    new_state = list(state)
                    for idx in button:
                        new_state[idx] = not new_state[idx]
                    current.add(tuple(new_state))
            previous = current
            count += 1

    def solve_joltage(self) -> int:
        buttons = np.array([
            [int(i in button) for i in range(len(self.joltage))]
            for button in self.buttons
        ]).T
        objective = [1] * len(self.buttons)
        result = linprog(c=objective, A_eq=buttons, b_eq=self.joltage, integrality=1)
        return round(result.fun)


def part1(machines):
    return sum(machine.solve() for machine in machines)


def part2(machines):
    return sum(machine.solve_joltage() for machine in machines)


def parse(line):
    lights, *buttons, joltage = list(line.split(' '))
    return Machine(
        lights=tuple([c == '#' for c in lights.strip('[]')]),
        buttons=[tuple(map(int, b.strip('()').split(','))) for b in buttons],
        joltage=tuple(map(int, joltage.strip('{}').split(','))),
    )


TEST1 = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


def test_part1():
    assert part1(line_parser(TEST1, parse=parse)) == 7


def test_part2():
    assert part2(line_parser(TEST1, parse=parse)) == 33


if __name__ == "__main__":
    LINES = line_parser(get_input(day=10, year=2025), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
