"""Advent of Code Day 8 Solution."""

from get_input import get_input, line_parser
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    z: int

    def distance(self, other: "Node") -> float:
        return (self.x - other.x)**2 + \
               (self.y - other.y)**2 + \
               (self.z - other.z)**2

    def from_line(line: str) -> "Node":
        return Node(*map(int, line.split(",")))


def part1(points, count=1000):
    circuits = {point: frozenset([point]) for point in points}
    pairs = list(combinations(points, 2))
    for a, b in sorted(pairs, key=lambda p: p[0].distance(p[1]))[:count]:
        if circuits[a] is circuits[b]:
            continue
        union = circuits[a] | circuits[b]
        for node in union:
            circuits[node] = union
    sets = set(frozenset(v) for v in circuits.values())
    sizes = sorted([len(s) for s in sets], reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def part2(points):
    points = frozenset(points)
    circuits = {point: frozenset([point]) for point in points}
    pairs = list(combinations(points, 2))
    for a, b in sorted(pairs, key=lambda pair: pair[0].distance(pair[1])):
        if circuits[a] is circuits[b]:
            continue
        union = circuits[a] | circuits[b]
        if union == points:
            return a.x * b.x
        for node in union:
            circuits[node] = union
    raise NotImplementedError


def parse(line):
    return Node.from_line(line)


TEST1 = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
818,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


def test_part1():
    assert part1(line_parser(TEST1, parse=parse), count=10) == 40


def test_part2():
    assert part2(line_parser(TEST1, parse=parse)) == 25272


if __name__ == "__main__":
    LINES = line_parser(get_input(day=8, year=2025), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
