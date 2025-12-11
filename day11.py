"""Advent of Code Day 10 Solution."""

from dataclasses import dataclass
from get_input import get_input, line_parser
from functools import cache


@dataclass
class Graph:
    graph: dict[str, tuple[str]]

    @cache
    def paths(self, src, dst: str) -> int:
        if src == dst:
            return 1
        return sum(self.paths(next_node, dst=dst)
                   for next_node in self.graph.get(src, []))

    def __hash__(self):
        """
        Custom hash to allow caching methods.
        DO NOT MODIFY THE graph AFTER CREATING IT.
        """
        return hash(id(self))


def part1(machines):
    graph = Graph({name: nodes for name, nodes in machines})
    return graph.paths('you', 'out')


def part2(machines):
    graph = Graph({name: nodes for name, nodes in machines})

    # Directed acyclic graph. Only one of these will be non-zero
    if (ways := graph.paths('fft', 'dac')) != 0:
        second, third = 'fft', 'dac'
    elif (ways := graph.paths('dac', 'fft')) != 0:
        second, third = 'dac', 'fft'
    else:
        raise ValueError("No path between fft and dac found")
    return graph.paths('svr', second) * ways * graph.paths(third, 'out')


def parse(line: str) -> dict[str, tuple[str]]:
    name, outs = line.split(":")
    return name.strip(), tuple(outs.strip().split())


TEST1 = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""


TEST2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""


def test_part1():
    assert part1(line_parser(TEST1, parse=parse)) == 5


def test_part2():
    assert part2(line_parser(TEST2, parse=parse)) == 2


if __name__ == "__main__":
    LINES = line_parser(get_input(day=11, year=2025), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
