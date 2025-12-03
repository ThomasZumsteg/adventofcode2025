"""Advent of Code Day 2 Solution."""

from get_input import get_input, line_parser
from functools import cache


def part1(codes):
    total = 0
    for before, after in codes:
        for n in range(before, after + 1):
            s = str(n)
            # repeats doesn't cover 999 or 111
            if s[:len(s)//2] == s[len(s)//2:]:
                total += n
    return total


@cache
def repeats(string: str) -> bool:
    length = len(string)
    for size in range(1, length // 2 + 1):
        if length % size != 0:
            continue
        groups = {string[i:i+size] for i in range(0, length, size)}
        if len(groups) == 1:
            return True
    return False


def part2(codes):
    total = 0
    for before, after in codes:
        for num in range(before, after + 1):
            string = str(num)
            if repeats(string):
                total += num
    return total


def parse(line):
    before, after = line.split('-')
    return (int(before), int(after))


TEST1 = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"\
    "1698522-1698528,446443-446449,38593856-38593862,565653-565659," \
    "824824821-824824827,2121212118-2121212124"


def test_part1():
    assert part1(line_parser(TEST1, parse=parse, seperator=',')) == 1227775554


def test_part2():
    assert part2(line_parser(TEST1, parse=parse, seperator=',')) == 4174379265


if __name__ == "__main__":
    LINES = line_parser(get_input(day=2, year=2025),
                        parse=parse, seperator=',')
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
