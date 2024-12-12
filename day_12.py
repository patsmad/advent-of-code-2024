import argparse
from get_input import get_input
import re
from typing import List, Set

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def get_region(x: int, y: int, grid: List[str]) -> Set:
    value = grid[x][y]
    queue = [(x, y)]
    region = {(x, y)}
    while len(queue) > 0:
        curr_x, curr_y = queue.pop(0)
        for di, dj in directions:
            i = di + curr_x
            j = dj + curr_y
            if (i, j) not in region and 0 <= i < len(grid) and 0 <= j < len(grid[i]) and grid[i][j] == value:
                region |= {(i, j)}
                queue.append((i, j))
    return region

def get_perim_area(value: str, region: Set, grid: List[str]) -> (int, int):
    perim = 0
    area = 0
    for x, y in region:
        for di, dj in directions:
            i = di + x
            j = dj + y
            if 0 <= i < len(grid) and 0 <= j < len(grid[i]) and grid[i][j] == value:
                perim -= 1
            perim += 1
        area += 1
    return perim, area


add_comp = {
    'top': lambda value, x, y, grid: x == 0 or grid[x - 1][y] != value,
    'left': lambda value, x, y, grid: y == 0 or grid[x][y - 1] != value,
    'bottom': lambda value, x, y, grid: x == len(grid) - 1 or grid[x + 1][y] != value,
    'right': lambda value, x, y, grid: y == len(grid[x]) - 1 or grid[x][y + 1] != value
}
sort_method = {
    'top': lambda t: (t[0], t[1]),
    'left': lambda t: (t[1], t[0]),
    'bottom': lambda t: (t[0], t[1]),
    'right': lambda t: (t[1], t[0]),
}
check_method = {
    'top': lambda i, fences: i == 0 or fences[i][0] != fences[i - 1][0] or fences[i][1] != fences[i - 1][1] + 1,
    'left': lambda i, fences: i == 0 or fences[i][1] != fences[i - 1][1] or fences[i][0] != fences[i - 1][0] + 1,
    'bottom': lambda i, fences: i == 0 or fences[i][0] != fences[i - 1][0] or fences[i][1] != fences[i - 1][1] + 1,
    'right': lambda i, fences: i == 0 or fences[i][1] != fences[i - 1][1] or fences[i][0] != fences[i - 1][0] + 1
}

def get_sides(value: str, region: Set, grid: List[str]) -> int:
    sides = 0
    for side_type in ['left', 'right', 'top', 'bottom']:
        fences = set()
        for x, y in region:
            if add_comp[side_type](value, x, y, grid):
                fences |= {(x, y)}
        fences = sorted(list(fences), key=sort_method[side_type])
        for i in range(len(fences)):
            if check_method[side_type](i, fences):
                sides += 1
    return sides


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        RRRRIICCFF
        RRRRIICCCF
        VVRRRCCFFF
        VVRCCCJFFF
        VVVVCJJCFE
        VVIVCCJJEE
        VVIIICJJEE
        MIIIIIJJEE
        MIIISIJEEE
        MMMISSJEEE
        """.strip()
    grid = [a.strip() for a in raw_input.strip().split('\n')]

    # part 1
    potential_sites = {(i, j) for i in range(len(grid)) for j in range(len(grid[i]))}
    regions = []
    while len(potential_sites) > 0:
        x, y = potential_sites.pop()
        region = get_region(x, y, grid)
        regions.append((grid[x][y], region))
        potential_sites -= region
    s = 0
    for value, region in regions:
        perim, area = get_perim_area(value, region, grid)
        s += perim * area
    print(s)

    # part 2
    s = 0
    for value, region in regions:
        perim, area = get_perim_area(value, region, grid)
        sides = get_sides(value, region, grid)
        s += area * sides
    print(s)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
