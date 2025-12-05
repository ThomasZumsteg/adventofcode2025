"""Advent of Code Day 4 Solution."""

from get_input import get_input


def find(rolls):
    directions = (
       1+-1j,  1+0j,  1+1j,
       0+-1j,         0+1j,
      -1+-1j, -1+0j, -1+1j
    )

    remove = set()
    for p in rolls:
        if sum(1 for d in directions if p+d in rolls) < 4:
            remove.add(p)
    return remove


def part1(rolls):
    return len(find(rolls))


def part2(rolls):
    start = len(rolls)
    while len(to_remove := find(rolls)) > 0:
        rolls -= to_remove
    return start - len(rolls)


def parse(diagram):
    grid = set()
    for r, row in enumerate(diagram.strip().splitlines()):
        for c, char in enumerate(row):
            if char != '@':
                continue
            grid.add(complex(r, c))
    return grid


TEST1 = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


def test_part1():
    assert part1(parse(TEST1)) == 13


def test_part2():
    assert part2(parse(TEST1)) == 43


if __name__ == "__main__":
    LINES = parse(get_input(day=4, year=2025))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
