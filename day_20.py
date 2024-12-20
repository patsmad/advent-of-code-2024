import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def get_path(grid, start, end):
    queue = [(0, start)]
    seen = {start: 0}
    while len(queue) > 0:
        distance, curr_pos = queue.pop(0)
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
            if new_pos == end:
                seen[new_pos] = distance + 1
                return seen
            if new_pos not in seen and grid[new_pos[0]][new_pos[1]] != '#':
                queue.append((distance + 1, new_pos))
                seen[new_pos] = distance + 1
    return seen

def get_shortcuts(seen, shortcut_cutoff, shortcut_length):
    shortcuts = 0
    for pos in seen:
        for i in range(-shortcut_length, shortcut_length + 1):
            for j in range(-shortcut_length + abs(i), shortcut_length - abs(i) + 1):
                new_pos = (pos[0] + i, pos[1] + j)
                if new_pos in seen:
                    manhattan_distance = abs(new_pos[0] - pos[0]) + abs(new_pos[1] - pos[1])
                    shortcut = seen[new_pos] - seen[pos] - manhattan_distance
                    if shortcut >= shortcut_cutoff:
                        shortcuts += 1
    return shortcuts

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
        shortcut_cutoff_1 = 100
        shortcut_cutoff_2 = 100
    else:
        raw_input: str = """
        ###############
        #...#...#.....#
        #.#.#.#.#.###.#
        #S#...#.#.#...#
        #######.#.#.###
        #######.#.#...#
        #######.#.###.#
        ###..E#...#...#
        ###.#######.###
        #...###...#...#
        #.#####.#.###.#
        #.#...#.#.#...#
        #.#.#.#.#.#.###
        #...#...#...###
        ###############
        """.strip()
        shortcut_cutoff_1 = 1
        shortcut_cutoff_2 = 50
    grid = [[c for c in line.strip()] for line in raw_input.strip().split('\n')]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                start = (i, j)
                grid[i][j] = '.'
            if grid[i][j] == 'E':
                end = (i, j)
                grid[i][j] = '.'

    # part 1
    path = get_path(grid, start, end)
    print(get_shortcuts(path, shortcut_cutoff_1, 2))

    # part 2
    print(get_shortcuts(path, shortcut_cutoff_2, 20))


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
