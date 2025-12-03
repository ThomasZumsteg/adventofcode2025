"""Advent of Code Day 3 Solution."""

from get_input import get_input, line_parser


def joltage(row, size):
    joltage = 0
    for i in range(size, 0, -1):
        p, digit = max(
            enumerate(row if i == 0 else row[:len(row)+1-i]),
            key=lambda x: x[1]
        )
        joltage = joltage * 10 + digit
        row = row[p+1:]
    return joltage


def part1(rows):
    return sum(joltage(row, 2) for row in rows)


def part2(rows):
    return sum(joltage(row, 12) for row in rows)


def parse(line):
    return tuple(int(d) for d in line)


TEST1 = """
987654321111111
811111111111119
234234234234278
818181911112111
"""


def test_part1():
    assert part1(line_parser(TEST1, parse=parse)) == 357


def test_part2():
    assert part2(line_parser(TEST1, parse=parse)) == 3121910778619


if __name__ == "__main__":
    LINES = line_parser(get_input(day=3, year=2025), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
