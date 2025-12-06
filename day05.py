"""Advent of Code Day 5 Solution."""
from get_input import get_input


def part1(recipes):
    ranges, ingredients = recipes
    total = 0
    for ingredient in ingredients:
        for start, end in ranges:
            if start <= ingredient <= end:
                total += 1
                break
    return total


def part2(recipes):
    ranges, _ = recipes
    total = 0
    last = 0
    for start, end in sorted(ranges):
        total += max(0, end - max(last, start - 1))
        last = max(last, end)
    return total


def parse(text):
    lines = iter(text.strip().splitlines())
    ranges = []
    for line in lines:
        if line == "":
            break
        start, end = map(int, line.split("-"))
        ranges.append((start, end))
    ingredients = [int(line) for line in lines]
    return (ranges, ingredients)


TEST1 = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


def test_part1():
    assert part1(parse(TEST1)) == 3


def test_part2():
    assert part2(parse(TEST1)) == 14


if __name__ == "__main__":
    LINES = parse(get_input(day=5, year=2025))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
