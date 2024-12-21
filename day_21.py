import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

keypad = {
    'A': (3, 2),
    '0': (3, 1), '1': (2, 0), '2': (2, 1), '3': (2, 2), '4': (1, 0),
    '5': (1, 1), '6': (1, 2), '7': (0, 0), '8': (0, 1), '9': (0, 2)
}
invert_keypad = {
    (3, 2): 'A',
    (3, 1): '0', (2, 0): '1', (2, 1): '2', (2, 2): '3', (1, 0): '4',
    (1, 1): '5', (1, 2): '6', (0, 0): '7', (0, 1): '8', (0, 2): '9'
}
robot = {
    'A': (0, 2), '^': (0, 1), '<': (1, 0), 'v': (1, 1), '>': (1, 2)
}
invert_robot = {
    (0, 2): 'A', (0, 1): '^', (1, 0): '<', (1, 1): 'v', (1, 2): '>'
}
direction_to_symbol = {
    (0, 1): '>',
    (0, -1): '<',
    (1, 0): 'v',
    (-1, 0): '^'
}

def recurse_path(start, end, path, invert_keypad):
    if start == end:
        return [path + 'A']
    directions = []
    if start[0] < end[0]:
        directions.append((1, 0))
    if start[0] > end[0]:
        directions.append((-1, 0))
    if start[1] < end[1]:
        directions.append((0, 1))
    if start[1] > end[1]:
        directions.append((0, -1))
    possible_paths = []
    for direction in directions:
        new_pos = (start[0] + direction[0], start[1] + direction[1])
        if new_pos in invert_keypad:
            possible_paths += recurse_path(new_pos, end, path + direction_to_symbol[direction], invert_keypad)
    return possible_paths

memo = {}

def recursive_path(curr_bot, path, num_bots):
    if curr_bot > num_bots:
        return len(path)
    if (curr_bot, num_bots, path) in memo:
        return memo[(curr_bot, num_bots, path)]
    curr = 'A'
    total = 0
    for c in path:
        new_paths = recurse_path(robot[curr], robot[c], '', invert_robot)
        new_totals = []
        for new_path in new_paths:
            new_totals.append(recursive_path(curr_bot + 1, new_path, num_bots))
        total += min(new_totals)
        curr = c
    memo[(curr_bot, num_bots, path)] = total
    return total

def get_min_path(code, num_bots):
    curr_num = 'A'
    s = 0
    for other_num in code:
        paths = recurse_path(keypad[curr_num], keypad[other_num], '', invert_keypad)
        vals = []
        for path in paths:
            vals.append(recursive_path(1, path, num_bots))
        s += min(vals)
        curr_num = other_num
    return s

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        029A
        980A
        179A
        456A
        379A
        """.strip()
    codes = [b.strip() for b in raw_input.strip().split('\n')]

    # part 1
    p = 0
    for code in codes:
        number = int(re.findall(r'([0-9]*)A', code)[0])
        count = get_min_path(code, 2)
        p += number * count
    print(p)

    # part 2
    p = 0
    for code in codes:
        number = int(re.findall(r'([0-9]*)A', code)[0])
        count = get_min_path(code, 25)
        p += number * count
    print(p)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
