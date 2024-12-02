import argparse
from get_input import get_input
import re
from typing import List

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def safe(a: int, b: int) -> bool:
    return 0 < b - a <= 3

def check_safe(l: List) -> bool:
    modification = -1 if l[1] < l[0] else 1
    for i in range(1, len(l)):
        if not safe(modification * l[i - 1], modification * l[i]):
            return False
    return True

def check_safe_dampened(l: List) -> bool:
    if not check_safe(l):
        for i in range(len(l)):
            if check_safe(l[:i] + l[i+1:]):
                return True
    else:
        return True
    return False

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
        """.strip()
    input = [list(map(int, a.split(' '))) for a in raw_input.split('\n')]

    # part 1
    num_safe = 0
    for line in input:
        num_safe += check_safe(line)
    print(num_safe)

    # part 2
    num_safe = 0
    for line in input:
        num_safe += check_safe_dampened(line)
    print(num_safe)


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
