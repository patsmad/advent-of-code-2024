import argparse
from get_input import get_input
import re
from typing import List

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()


class WordSearch:
    def __init__(self, input: List) -> None:
        self.input = input

    directions = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]

    def check_xmas(self, i: int, j: int, direction: (int, int)) -> bool:
        target = 'XMAS'
        for k in range(4):
            if self.input[i + k * direction[0]][j + k * direction[1]] != target[k]:
                return False
        return True

    def check_masses(self, i: int, j: int) -> bool:
        return self.input[i][j] == 'A' and \
                        {self.input[i - 1][j - 1], self.input[i + 1][j + 1]} == {'S', 'M'} and \
                        {self.input[i - 1][j + 1], self.input[i + 1][j - 1]} == {'S', 'M'}

    def xmas_count(self) -> int:
        count = 0
        for i in range(len(self.input)):
            for j in range(len(self.input[0])):
                for direction in self.directions:
                    if 0 <= i + 3 * direction[0] < len(self.input) and 0 <= j + 3 * direction[1] < len(self.input[0]):
                        count += self.check_xmas(i, j, direction)
        return count

    def masses_count(self) -> int:
        count = 0
        for i in range(1, len(self.input) - 1):
            for j in range(1, len(self.input[0]) - 1):
                count += self.check_masses(i, j)
        return count

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
        """.strip()

    input = [a.strip() for a in raw_input.strip().split('\n')]

    # part 1
    grid = WordSearch(input)
    print(grid.xmas_count())

    # part 2
    print(grid.masses_count())

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
