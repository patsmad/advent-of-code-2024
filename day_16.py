import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Grid:
    def __init__(self, raw_input):
        self.grid = [line.strip() for line in raw_input.strip().split('\n')]
        self.start = None
        self.end = None
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == 'S':
                    self.start = (i, j)
                if self.grid[i][j] == 'E':
                    self.end = (i, j)

    direction_to_move = {
        'E': (0, 1),
        'S': (1, 0),
        'W': (0, -1),
        'N': (-1, 0)
    }

    turns = {
        'E': ['S', 'N'],
        'S': ['E', 'W'],
        'W': ['S', 'N'],
        'N': ['E', 'W']
    }

    def get_min_end_score_key(self, scores):
        end_scores = [(direction, self.end, scores[(direction, self.end)]) for direction in self.direction_to_move if (direction, self.end) in scores]
        if len(end_scores) > 0:
            return sorted(end_scores, key=lambda x: x[2])[0]

    def scores(self):
        queue = [(0, 'E', self.start)]
        scores = {}
        while len(queue) > 0:
            curr_score, direction, curr_pos = queue.pop(0)
            if (direction, curr_pos) not in scores or curr_score < scores[(direction, curr_pos)]:
                scores[(direction, curr_pos)] = curr_score
            move = self.direction_to_move[direction]
            new_pos = (curr_pos[0] + move[0], curr_pos[1] + move[1])
            if (self.grid[new_pos[0]][new_pos[1]] != '#' and ((direction, new_pos) not in scores or curr_score + 1 < scores[(direction, new_pos)])):
                queue.append((curr_score + 1, direction, new_pos))
            for new_direction in self.turns[direction]:
                if (new_direction, curr_pos) not in scores or curr_score + 1000 < scores[(new_direction, curr_pos)]:
                    queue.append((curr_score + 1000, new_direction, curr_pos))
        return scores

    def path(self, scores):
        queue = [self.get_min_end_score_key(scores)]
        path = {queue[0][1]}
        while len(queue) > 0:
            direction, curr_pos, curr_score = queue.pop(0)
            move = self.direction_to_move[direction]
            new_pos = (curr_pos[0] - move[0], curr_pos[1] - move[1])
            if (direction, new_pos) in scores and scores[(direction, new_pos)] == curr_score - 1:
                queue.append((direction, new_pos, curr_score - 1))
                path |= {new_pos}
            for new_direction in self.turns[direction]:
                if (new_direction, curr_pos) in scores and scores[(new_direction, curr_pos)] == curr_score - 1000:
                    queue.append((new_direction, curr_pos, curr_score - 1000))
        return len(path)


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        ###############
        #.......#....E#
        #.#.###.#.###.#
        #.....#.#...#.#
        #.###.#####.#.#
        #.#.#.......#.#
        #.#.#####.###.#
        #...........#.#
        ###.#.#####.#.#
        #...#.....#.#.#
        #.#.#.###.#.#.#
        #.....#...#.#.#
        #.###.#.#.#.#.#
        #S..#.....#...#
        ###############
        """.strip()

        raw_input: str = """
        #################
        #...#...#...#..E#
        #.#.#.#.#.#.#.#.#
        #.#.#.#...#...#.#
        #.#.#.#.###.#.#.#
        #...#.#.#.....#.#
        #.#.#.#.#.#####.#
        #.#...#.#.#.....#
        #.#.#####.#.###.#
        #.#.#.......#...#
        #.#.###.#####.###
        #.#.#...#.....#.#
        #.#.#.#####.###.#
        #.#.#.........#.#
        #.#.#.#########.#
        #S#.............#
        #################
        """.strip()


    # part 1
    grid = Grid(raw_input)
    scores = grid.scores()
    key = grid.get_min_end_score_key(scores)
    print(scores[(key[0], key[1])])

    # part 2
    print(grid.path(scores))

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
