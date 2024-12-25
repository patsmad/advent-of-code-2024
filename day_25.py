import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def get_count(new_item):
    counts = [0] * len(new_item[0])
    for i in range(len(new_item)):
        for j in range(len(new_item[0])):
            if new_item[i][j] == '#':
                counts[j] += 1
    return counts

def process(locks_and_keys):
    locks = []
    keys = []
    height = 0
    while 0 in [len(a) for a in locks_and_keys]:
        idx = [len(a) for a in locks_and_keys].index(0)
        new_item = locks_and_keys[:idx]
        height = len(new_item)
        locks_and_keys = locks_and_keys[idx + 1:]
        if new_item[0][0] == '#':
            locks.append(get_count(new_item))
        else:
            keys.append(get_count(new_item))
    new_item = locks_and_keys
    if new_item[0][0] == '#':
        locks.append(get_count(new_item))
    else:
        keys.append(get_count(new_item))
    return locks, keys, height


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        #####
        .####
        .####
        .####
        .#.#.
        .#...
        .....
        
        #####
        ##.##
        .#.##
        ...##
        ...#.
        ...#.
        .....
        
        .....
        #....
        #....
        #...#
        #.#.#
        #.###
        #####
        
        .....
        .....
        #.#..
        ###..
        ###.#
        ###.#
        #####
        
        .....
        .....
        .....
        #....
        #.#..
        #.#.#
        #####
        """.strip()
    locks_and_keys = [line.strip() for line in raw_input.strip().split('\n')]
    locks, keys, height = process(locks_and_keys)

    # part 1
    count = 0
    for lock in locks:
        for key in keys:
            if all([lock[i] + key[i] <= height for i in range(len(lock))]):
                count += 1
    print(count)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
