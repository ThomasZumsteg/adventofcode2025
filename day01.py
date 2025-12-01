"""Advent of Code Day 1 Solution."""

from get_input import get_input, line_parser


def dial(sequence: list[int], position=50, size=100):
    for value in sequence:
        position += value
        yield position
        position %= size


def part1(rows):
    return sum(1 if p % 100 == 0 else 0 for p in dial(rows))


def part2(rows):
    return sum(abs(p // 100) for p in dial(rows))


def parse(line):
    return int(line[1:]) * (1 if line[0] == 'R' else -1)


TEST1 = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def test_part1():
    assert part1(line_parser(TEST1, parse=parse)) == 3


def test_part2():
    assert part2(line_parser(TEST1, parse=parse)) == 6


if __name__ == "__main__":
    LINES = line_parser(get_input(day=1, year=2025), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
