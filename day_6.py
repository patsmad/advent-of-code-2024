import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()


carat_to_direction = {'^': 'N', '>': 'E', 'v': 'S', '<': 'W'}
direction_to_xy = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
turn = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}

class Grid:
    def __init__(self, map_input, initial_guard, initial_direction):
        self.map = [[a for a in b] for b in map_input]
        self.guard = initial_guard
        self.direction = initial_direction
        self.marked = [[set() for _ in range(len(self.map[0]))] for _ in range(len(self.map))]

    def out(self, guard):
        return not (0 <= guard[0] < len(self.map) and 0 <= guard[1] < len(self.map[0]))

    def move(self):
        if self.direction in self.marked[self.guard[0]][self.guard[1]]:
            return True
        self.marked[self.guard[0]][self.guard[1]] |= {self.direction}
        xy = direction_to_xy[self.direction]
        new_guard = (self.guard[0] + xy[0], self.guard[1] + xy[1])
        new_direction = self.direction
        if not self.out(new_guard):
            if self.map[new_guard[0]][new_guard[1]] == '#':
                new_direction = turn[self.direction]
                new_guard = self.guard
        self.direction = new_direction
        self.guard = new_guard
        return False

    def run(self):
        while not self.out(self.guard):
            in_loop = self.move()
            if in_loop:
                return False
        return True

    def count(self):
        return sum([len(place) > 0 for line in self.marked for place in line])

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        ....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
        """.strip()

    # part 1
    map_input = [[b for b in a.strip()] for a in raw_input.strip().split('\n')]
    for i in range(len(map_input)):
        for j in range(len(map_input[0])):
            if map_input[i][j] not in ['.', '#']:
                initial_direction = carat_to_direction[map_input[i][j]]
                initial_guard = (i, j)
                map_input[i][j] = '.'

    grid = Grid(map_input, initial_guard, initial_direction)
    grid.run()
    print(grid.count())

    possible_obstruction_locations = [(i, j) for i in range(len(grid.marked)) for j in range(len(grid.marked[i])) if len(grid.marked[i][j]) > 0 and (i, j) != initial_guard]
    # part 2
    count = 0
    for obstruction_location in possible_obstruction_locations:
        new_map_input = [[a for a in b] for b in map_input]
        new_map_input[obstruction_location[0]][obstruction_location[1]] = '#'
        obstruction_grid = Grid(new_map_input, initial_guard, initial_direction)
        if not obstruction_grid.run():
            count += 1
    print(count)


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
