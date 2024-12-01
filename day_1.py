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
        3   4
        4   3
        2   5
        1   3
        3   9
        3   3
        """.strip()
    input = [tuple(map(int, a.strip().split('   '))) for a in raw_input.strip().split('\n')]
    list_1 = sorted([line[0] for line in input])
    list_2 = sorted([line[1] for line in input])

    # part 1
    print(sum([abs(r - l) for r, l in zip(list_1, list_2)]))

    # part 2
    count = {}
    for entry in list_2:
        if entry not in count:
            count[entry] = 0
        count[entry] += 1

    similarity = 0
    for entry in list_1:
        similarity += entry * count.get(entry, 0)
    print(similarity)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
