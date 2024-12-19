import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def possible(available, pattern):
    if len(pattern) == 0:
        return True
    for stripe in available:
        if pattern[:len(stripe)] == stripe:
            if possible(available, pattern[len(stripe):]):
                return True
    return False

memo = {}
def get_arrangements(available, pattern):
    if len(pattern) == 0:
        return 1
    if pattern in memo:
        return memo[pattern]
    arrangements = 0
    for stripe in available:
        if pattern[:len(stripe)] == stripe:
            arrangements += get_arrangements(available, pattern[len(stripe):])
    memo[pattern] = arrangements
    return arrangements

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        r, wr, b, g, bwu, rb, gb, br

        brwrr
        bggr
        gbbr
        rrbgbr
        ubwu
        bwurrg
        brgr
        bbrgwb
        """.strip()
    input = [a.strip() for a in raw_input.strip().split('\n')]
    available = input[0].split(', ')
    patterns = input[2:]

    # part 1
    possible_patterns = 0
    for pattern in patterns:
        possible_patterns += possible(available, pattern)
    print(possible_patterns)

    # part 2
    possible_patterns = 0
    for pattern in patterns:
        possible_patterns += get_arrangements(available, pattern)
    print(possible_patterns)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
