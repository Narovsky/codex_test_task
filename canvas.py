#!/usr/bin/env python
import math
import sys
from dataclasses import dataclass
from typing import List


class CanvasNotCreated(Exception):
    ...


class Canvas:
    """docstring for Canvas"""

    dot: str = 'X'
    space: str = ' '

    def __init__(self, width: int = 10, height: int = 10):
        self.width: int = width
        self.height: int = height
        self.matrix: list = [
            [0 for x in range(self.width)] for y in range(self.height)
        ]

    def draw(self, actions: list):
        for action in actions:
            action.draw(self.matrix)

    def __str__(self):
        output: str = ''
        for row in self.matrix:
            for e in row:
                if e == 1:
                    output += self.dot
                elif e == 0:
                    output += self.space
                else:
                    output += e
            output += '\n'
        return output


@dataclass
class Line:
    """docstring for Line"""

    x1: int
    y1: int
    x2: int
    y2: int

    def draw(self, matrix: List[list]) -> List[list]:
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        for x in range(self.x1, self.x2):
            y = math.ceil(self.y1 + dy * (x - self.x1) / dx)
            matrix[y][x] = 1
        return matrix


@dataclass
class Rectangle:
    """docstring for Rectangle"""

    x1: int
    y1: int
    x2: int
    y2: int

    def draw(self, matrix: List[list]) -> List[list]:
        for y in range(self.y1, self.y2 + 1):
            matrix[y][self.x1] = matrix[y][self.x2] = 1
        for x in range(self.x1, self.x2 + 1):
            matrix[self.y1][x] = matrix[self.y2][x] = 1
        return matrix


@dataclass
class BucketFill:
    """
    class BucketFill
    recursion traversal around the point
    """

    x: int
    y: int
    char: str

    def draw(self, matrix: List[list]) -> List[list]:
        self.matrix = matrix
        self._fill_around(self.x, self.y)
        return matrix

    def _fill_around(self, x: int, y: int):
        self.matrix[y][x] = self.char

        try:
            for y_ in range(y - 1, y + 2):
                if self.matrix[y_][x] == 0:
                    self._fill_around(x, y_)
            for x_ in range(x - 1, x + 2):
                if self.matrix[y][x_] == 0:
                    self._fill_around(x_, y)
        except IndexError:
            pass


if __name__ == '__main__':
    commands: list = []

    try:
        with open(sys.argv[1]) as h:
            for one in h.readlines():
                cmd, *params = one.strip().split(' ')
                commands.append((cmd, params))

            if 'C' not in [c[0] for c in commands]:
                raise CanvasNotCreated

    except IndexError:
        print('No arguments passed!')
    except FileNotFoundError:
        print(f'File {sys.argv[1]} not found!')
    except CanvasNotCreated:
        print('Canvas not created!')
    else:
        actions: list = []
        canvas: Canvas
        for cmd, params in commands:
            if cmd == 'C':
                canvas = Canvas(*[int(p) for p in params])
            elif cmd == 'L':
                actions.append(Line(*[int(p) for p in params]))
            elif cmd == 'R':
                actions.append(Rectangle(*[int(p) for p in params]))
            elif cmd == 'B':
                actions.append(
                    BucketFill(*([int(p) for p in params[:-1]]) + [params[-1]])
                )

        canvas.draw(actions)
        print(canvas)
