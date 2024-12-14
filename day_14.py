import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Robot:
    def __init__(self, grid_x, grid_y, raw_line):
        self.grid_x = grid_x
        self.grid_y = grid_y
        ps, vs = raw_line.split(' ')
        self.x, self.y = map(int, ps.split('=')[-1].split(','))
        self.vx, self.vy = map(int, vs.split('=')[-1].split(','))

    def get_pos(self, seconds):
        return (self.x + self.vx * seconds) % self.grid_x, (self.y + self.vy * seconds) % self.grid_y


def print_robots(seconds, grid_x, grid_y, robots):
    positions = [robot.get_pos(seconds) for robot in robots]
    for j in range(grid_y):
        line = []
        for i in range(grid_x):
            s = sum([p == (i, j) for p in positions])
            line.append('.' if s == 0 else str(s))
        print(''.join(line))

def get_quadrant_counts(seconds, grid_x, grid_y, robots):
    positions = [robot.get_pos(seconds) for robot in robots]
    middle_x = grid_x // 2
    middle_y = grid_y // 2
    quadrant_counts = [
        sum([1 for p in positions if p[0] < middle_x and p[1] < middle_y]),
        sum([1 for p in positions if p[0] > middle_x and p[1] < middle_y]),
        sum([1 for p in positions if p[0] < middle_x and p[1] > middle_y]),
        sum([1 for p in positions if p[0] > middle_x and p[1] > middle_y])
    ]
    return quadrant_counts

def get_stats(seconds, robots):
    positions = [robot.get_pos(seconds) for robot in robots]
    n = len(positions)
    mx = sum([pos[0] for pos in positions]) / n
    my = sum([pos[1] for pos in positions]) / n
    sx = (sum([(pos[0] - mx)**2 for pos in positions]) / n)**0.5
    sy = (sum([(pos[1] - my) ** 2 for pos in positions]) / n) ** 0.5
    return mx, my, sx, sy


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
        grid_x, grid_y = 101, 103
    else:
        raw_input: str = """
        p=0,4 v=3,-3
        p=6,3 v=-1,-3
        p=10,3 v=-1,2
        p=2,0 v=2,-1
        p=0,0 v=1,3
        p=3,0 v=-2,-2
        p=7,6 v=-1,-3
        p=3,0 v=-1,-2
        p=9,3 v=2,3
        p=7,3 v=-1,2
        p=2,4 v=2,-3
        p=9,5 v=-3,-3
        """.strip()
        grid_x, grid_y = 11, 7
    robots = [Robot(grid_x, grid_y, line.strip()) for line in raw_input.strip().split('\n')]

    # part 1
    quandrant_counts = get_quadrant_counts(100, grid_x, grid_y, robots)
    p = 1
    for quandrant_count in quandrant_counts:
        p *= quandrant_count
    print(p)

    # part 2
    for seconds in range(1000000000):
        mx, my, sx, sy = get_stats(seconds, robots)
        # A little post hoc here, I do know the variance is likely to be small if it is forming a picture in the grid
        # But the numbers are chosen as small enough to get the answer for my question, but possibly not all solutions
        if sx < 20 and sy < 20:
            print(seconds)
            break

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
