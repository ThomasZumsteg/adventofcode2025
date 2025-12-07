"""Advent of Code Day 6 Solution."""

from get_input import get_input
from functools import reduce


def solve(oper, nums):
    if oper == '+':
        return sum(int(n) for n in nums)
    elif oper == '*':
        return reduce(lambda x, y:  x * int(y), nums, 1)
    raise ValueError(f"Unknown operator: {oper}")


def part1(lines):
    # Pivot on columns
    pivot = zip(*[lines.split() for lines in lines])
    return sum(solve(line[-1], line[:-1]) for line in pivot)


def part2(lines):
    # Pivot on characters
    pivot = list(reversed(list(zip(*lines))))
    pivot.append([' ']*len(pivot[0]))
    total = 0
    queue = []
    for line in pivot:
        if any(c != ' ' for c in line):
            queue.append(line)
            continue
        problem = ''.join(c for row in queue for c in row).strip()
        total += solve(problem[-1], problem[:-1].split())
        queue.clear()
    return total


def parse(text):
    return tuple(text.strip('\n').splitlines())


TEST1 = (
    "123 328  51 64 \n"
    " 45 64  387 23 \n"
    "  6 98  215 314\n"
    "*   +   *   +  \n"
)


def test_part1():
    assert part1(parse(TEST1)) == 4277556


def test_part2():
    assert part2(parse(TEST1)) == 3263827


if __name__ == "__main__":
    LINES = parse(get_input(day=6, year=2025))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
