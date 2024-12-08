import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        ............
        ........0...
        .....0......
        .......0....
        ....0.......
        ......A.....
        ............
        ............
        ........A...
        .........A..
        ............
        ............
        """.strip()
    input = [[place for place in line.strip()] for line in raw_input.strip().split('\n')]

    nodes = {}
    for i in range(len(input)):
        for j in range(len(input[i])):
            if input[i][j] != '.':
                if input[i][j] not in nodes:
                    nodes[input[i][j]] = []
                nodes[input[i][j]].append((i, j))

    # part 1
    antinodes = set()
    for node, points in nodes.items():
        for p1 in range(len(points)):
            for p2 in range(p1 + 1, len(points)):
                vec = (points[p2][0] - points[p1][0], points[p2][1] - points[p1][1])
                for direction in [2, -1]:
                    antinode = (points[p1][0] + vec[0] * direction, points[p1][1] + vec[1] * direction)
                    if 0 <= antinode[0] < len(input) and 0 <= antinode[1] < len(input[antinode[0]]):
                        antinodes |= {antinode}
    print(len(antinodes))

    # part 2
    antinodes = set()
    for node, points in nodes.items():
        for p1 in range(len(points)):
            for p2 in range(p1 + 1, len(points)):
                vec = (points[p2][0] - points[p1][0], points[p2][1] - points[p1][1])
                for direction in range(-1 - len(input), len(input) + 1):
                    antinode = (points[p1][0] + vec[0] * direction, points[p1][1] + vec[1] * direction)
                    if 0 <= antinode[0] < len(input) and 0 <= antinode[1] < len(input[antinode[0]]):
                        antinodes |= {antinode}
    print(len(antinodes))

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
