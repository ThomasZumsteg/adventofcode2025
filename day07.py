"""Advent of Code Day 7 Solution."""

from get_input import get_input
from collections import defaultdict


def part1(field):
    queue = [p for p, c in field.items() if c == 'S']
    splits = set()
    beam = set()
    while queue:
        p = queue.pop(0)
        if p in beam or p not in field:
            continue
        if field[p] == '^':
            splits.add(p)
            queue.append(p+1j)
            queue.append(p-1j)
        else:
            assert field[p] == '.' or field[p] == 'S'
            beam.add(p)
            queue.append(p+1)
    return len(splits)


def part2(field):
    next_row = {p: 1 for p, c in field.items() if c == 'S'}
    while next_row != {}:
        row = next_row
        next_row = defaultdict(int)
        for p, v in row.items():
            if p not in field:
                continue
            if field[p] == '^':
                next_row[p+1+1j] += v
                next_row[p+1-1j] += v
            else:
                assert field[p] == '.' or field[p] == 'S'
                next_row[p+1] += v
    return sum(row.values())


def parse(text):
    field = {}
    for r, row in enumerate(text.strip().splitlines()):
        for c, char in enumerate(row):
            field[complex(r, c)] = char
    return field


TEST1 = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""


def test_part1():
    assert part1(parse(TEST1)) == 21


def test_part2():
    assert part2(parse(TEST1)) == 40


if __name__ == "__main__":
    LINES = parse(get_input(day=7, year=2025))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
