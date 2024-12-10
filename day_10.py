import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Grid:
    def __init__(self, input):
        self.map = input

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def inside_grid(self, x, y):
        return 0 <= x < len(self.map) and 0 <= y < len(self.map[x])

    def find_nines(self, start):
        queue = [(0, start[0], start[1])]
        nines = set()
        count = {}
        while len(queue) > 0:
            value, curr_x, curr_y = queue.pop(0)
            for direction in self.directions:
                x = curr_x + direction[0]
                y = curr_y + direction[1]
                if self.inside_grid(x, y) and self.map[x][y] == str(value + 1):
                    queue.append((value + 1, x, y))
            if value == 9:
                nines |= {(curr_x, curr_y)}
                if (curr_x, curr_y) not in count:
                    count[(curr_x, curr_y)] = 0
                count[(curr_x, curr_y)] += 1
        return nines, count

    def get_zero_positions(self):
        zeros = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == '0':
                    zeros.append((i, j))
        return zeros


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        89010123
        78121874
        87430965
        96549874
        45678903
        32019012
        01329801
        10456732
        """.strip()
    input = [a.strip() for a in raw_input.strip().split('\n')]

    # part 1
    grid = Grid(input)
    s = 0
    for zero in grid.get_zero_positions():
        nines, count = grid.find_nines(zero)
        s += len(nines)
    print(s)

    # part 2
    s = 0
    for zero in grid.get_zero_positions():
        nines, count = grid.find_nines(zero)
        s += sum(count.values())
    print(s)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
