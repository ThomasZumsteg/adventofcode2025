"""Advent of Code Day 12 Solution."""

from get_input import get_input
from dataclasses import dataclass, field
from functools import cache
from typing import Iterator
import sys
import re


class State:
    def __init__(self, cells: dict[int: chr], shapes: dict["Shape", int]):
        self.shapes = shapes
        self.cells = cells

    @classmethod
    def from_line(cls, rows: int, cols: int, shapes: dict[int, "Shape"], counts: list[int]) -> "State":
        cells = {
            complex(r, c): '.'
            for r in range(int(rows))
            for c in range(int(cols))
        }
        shape_counts = {shapes[sid]: count for sid, count in enumerate(counts) if count > 0}
        return cls(cells=cells, shapes=shape_counts)

    def __str__(self):
        max_row = int(max(cell.real for cell in self.cells))
        max_col = int(max(cell.imag for cell in self.cells))
        rows = []
        for r in range(max_row + 1):
            row = []
            for c in range(max_col + 1):
                row.append(self.cells.get(complex(r, c), '#'))
            rows.append("".join(row))
        return "\n".join(rows)

    def fits(self, shape) -> bool:
        return all(self.cells.get(point, '#') == '.' for point in shape.cells)

    def __iter__(self) -> Iterator["State"]:
        for shape_template, counts in self.shapes.items():
            for offset in self.cells:
                for shape in shape_template.transformations():
                    shape = shape.shift(offset)
                    if not self.fits(shape):
                        continue
                    new_cells = self.cells.copy()
                    for cell in shape.cells:
                        new_cells[cell] = '#'
                    new_shapes = self.shapes.copy()
                    new_shapes[shape_template] -= 1
                    if new_shapes[shape_template] == 0:
                        del new_shapes[shape_template]
                    yield State(cells=new_cells, shapes=new_shapes)


@dataclass(frozen=True)
class Shape:
    cells: frozenset[complex]

    def flip(self) -> "Shape":
        return Shape(frozenset(complex(cell.imag, cell.real) for cell in self.cells))

    def rotate(self) -> "Shape":
        """Rotate 90 degrees clockwise."""
        max_row = int(max(cell.real for cell in self.cells))
        return Shape(frozenset(complex(cell.imag, max_row - cell.real) for cell in self.cells))

    def shift(self, offset: complex) -> "Shape":
        return Shape(frozenset(cell + offset for cell in self.cells))

    @cache
    def transformations(self) -> set["Shape"]:
        shapes = set()
        current_shape = self
        for _ in range(4):
            shapes.add(current_shape)
            shapes.add(current_shape.flip())
            current_shape = current_shape.rotate()
        return shapes

    def __str__(self):
        max_row = int(max(cell.real for cell in self.cells))
        max_col = int(max(cell.imag for cell in self.cells))
        rows = []
        for r in range(max_row + 1):
            row = []
            for c in range(max_col + 1):
                row.append("#" if complex(r, c) in self.cells else ".")
            rows.append("".join(row))
        return "\n".join(rows)

    def shape_iterator(self, shapes: list["Shape"], positions: set[complex]) -> Iterator[dict["Shape", int]]:
        for shape_template in shapes:
            for offset in positions:
                for shape in shape_template.transformations():
                    yield shape_template, shape.shift(offset)


def part1(data):
    shapes, states = data
    for shape in shapes.values():
        assert len(str(shape).split("\n")) == 3, str(shape)
        assert all(len(row) == 3 for row in str(shape).split("\n")), str(shape)
    total = 0
    for rows, cols, counts in states:
        if (rows // 3) * (cols // 3) >= sum(counts):
            total += 1
            continue
        grid_area = rows * cols
        shape_area = sum(len(shapes[shape_id].cells) * count for shape_id, count in enumerate(counts))
        if grid_area < shape_area:
            continue
        print(f"PANIC!: {grid_area:5d} - {shape_area:5d} = {grid_area - shape_area:5d}", file=sys.stderr)
        queue = [iter(State.from_line(rows, cols, shapes, counts))]
        while queue:
            if next_state := next(queue[-1], None):
                if not next_state.shapes:
                    total += 1
                    break
                queue.append(iter(next_state))
            else:
                queue.pop()
        total += 1
    return total


def part2(rows):
    raise NotImplementedError


def parse(lines):
    lines = iter(lines.strip().split("\n"))
    shapes = {}
    states = []
    while True:
        if (line := next(lines, None)) is None:
            break
        if m := re.match(r"(\d+):", line):
            shape_id = int(m.group(1))
            shape = set()
            row = 0
            while line := next(lines).strip():
                for col, ch in enumerate(line):
                    if ch == "#":
                        shape.add(complex(row, col))
                row += 1
            shapes[shape_id] = Shape(frozenset(shape))
        elif m := re.match(r"(\d+)x(\d+): (.+)", line):
            states.append((
                int(m.group(1)),  # rows
                int(m.group(2)),  # cols
                [int(s) for s in m.group(3).split()]  # shape counts
            ))
    return shapes, states


TEST1 = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""


def test_part1():
    assert part1(parse(TEST1)) == 2


def test_part2():
    assert part2(parse(TEST1)) == 0


if __name__ == "__main__":
    LINES = parse(get_input(day=12, year=2025))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
