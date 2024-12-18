import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def shortest_path(points, dim):
    start = (0, 0)
    queue = [(0, start)]
    seen = {start: 0}
    while len(queue) > 0:
        distance, curr_pos = queue.pop(0)
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
            if new_pos == (dim - 1, dim - 1):
                return distance + 1
            if new_pos not in seen and 0 <= new_pos[0] < dim and 0 <= new_pos[1] < dim and new_pos not in points:
                queue.append((distance + 1, new_pos))
                seen[new_pos] = distance + 1



def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
        dim = 71
        steps = 1024
    else:
        raw_input: str = """
        5,4
        4,2
        4,5
        3,0
        2,1
        6,3
        2,4
        1,5
        0,6
        3,3
        2,6
        5,1
        1,2
        5,5
        2,5
        6,5
        1,4
        0,4
        6,4
        1,1
        6,1
        1,0
        0,5
        1,6
        2,0
        """.strip()
        dim = 7
        steps = 12
    points = []
    for line in raw_input.strip().split('\n'):
        p1, p2 = line.strip().split(',')
        points.append((int(p2), int(p1)))

    # part 1
    print(shortest_path(points[:steps], dim))

    # part 2
    min_steps = steps
    max_steps = len(points)
    new_steps = (max_steps + min_steps) // 2
    while max_steps - min_steps > 1:
        sp = shortest_path(points[:new_steps], dim)
        if sp is None:
            max_steps = new_steps
        else:
            min_steps = new_steps
        new_steps = (max_steps + min_steps) // 2
    p = points[min_steps]
    print(f'{p[1]},{p[0]}')

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
